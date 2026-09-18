import hashlib
import json
import logging
import re
import time
from typing import Any, Dict, List, Optional, Tuple

import httpx

from src import config
from src.guardrails import (
    GuardrailValidationError,
    normalize_raw_directive,
    validate_guardrails,
)
from src.models import (
    BatteryInput,
    DirectiveInterpretation,
    RawDirectiveItem,
    RawLLMOutput,
)
from src.prompts import FEW_SHOT_EXAMPLES, SYSTEM_PROMPT

logger = logging.getLogger("gridwise.llm")

# Global async client for connection reuse
_http_client: Optional[httpx.AsyncClient] = None

# In-memory LRU cache
_INTERPRETATION_CACHE: Dict[str, List[DirectiveInterpretation]] = {}
_CACHE_MAX_SIZE = 500


def get_http_client() -> httpx.AsyncClient:
    global _http_client
    if _http_client is None or _http_client.is_closed:
        _http_client = httpx.AsyncClient(
            timeout=httpx.Timeout(config.LLM_PER_CALL_TIMEOUT, connect=3.0),
            limits=httpx.Limits(max_keepalive_connections=20, max_connections=50),
        )
    return _http_client


def _compute_cache_key(notes: List[str], capacity_kwh: float) -> str:
    serialized = json.dumps({"notes": notes, "capacity_kwh": round(capacity_kwh, 4)}, sort_keys=True)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _build_user_prompt(notes: List[str], capacity_kwh: float, error_feedback: Optional[str] = None) -> str:
    notes_list_formatted = "\n".join([f"Note [{i}]: \"{note}\"" for i, note in enumerate(notes)])
    prompt = (
        f"OPERATOR NOTES TO INTERPRET:\n"
        f"{notes_list_formatted}\n\n"
        f"CAMPUS BATTERY CAPACITY: {capacity_kwh} kWh\n\n"
        f"Translate each of the {len(notes)} notes into the specified raw JSON format."
    )
    if error_feedback:
        prompt += (
            f"\n\nCRITICAL FIX REQUIRED: Your previous output failed validation with the following error:\n"
            f"{error_feedback}\n"
            f"Carefully correct the error and output valid JSON conforming strictly to the required schema."
        )
    return prompt


async def _call_gemini_native(
    client: httpx.AsyncClient,
    model: str,
    api_key: str,
    prompt: str,
) -> str:
    """Direct Google Generative Language API call with JSON schema enforcement."""
    base_url = config.LLM_BASE_URL or "https://generativelanguage.googleapis.com/v1beta"
    url = f"{base_url.rstrip('/')}/models/{model}:generateContent?key={api_key}"

    payload = {
        "systemInstruction": {
            "parts": [{"text": SYSTEM_PROMPT}]
        },
        "contents": [
            {"role": "user", "parts": [{"text": prompt}]}
        ],
        "generationConfig": {
            "temperature": 0.0,
            "responseMimeType": "application/json",
        },
    }

    resp = await client.post(url, json=payload, headers={"Content-Type": "application/json"})
    if resp.status_code != 200:
        logger.error(f"Gemini API returned status {resp.status_code}")
        raise RuntimeError(f"Gemini API returned status code {resp.status_code}")

    data = resp.json()
    try:
        candidate_text = data["candidates"][0]["content"]["parts"][0]["text"]
        return candidate_text
    except (KeyError, IndexError) as exc:
        raise RuntimeError("Invalid response structure from Gemini API") from exc


async def _call_openai_compat(
    client: httpx.AsyncClient,
    model: str,
    api_key: str,
    base_url: Optional[str],
    prompt: str,
) -> str:
    """OpenAI-compatible chat completions endpoint."""
    endpoint = f"{base_url.rstrip('/')}/chat/completions" if base_url else "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.0,
        "response_format": {"type": "json_object"},
    }

    resp = await client.post(endpoint, json=payload, headers=headers)
    if resp.status_code != 200:
        logger.error(f"OpenAI-compatible API returned status {resp.status_code}")
        raise RuntimeError(f"OpenAI-compatible API error {resp.status_code}")

    data = resp.json()
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as exc:
        raise RuntimeError("Invalid response structure from OpenAI-compatible provider") from exc


async def _execute_provider_call(model: str, prompt: str) -> str:
    client = get_http_client()
    api_key = config.LLM_API_KEY
    if not api_key:
        raise RuntimeError("No LLM_API_KEY configured")

    provider = config.LLM_PROVIDER
    if provider == "gemini":
        return await _call_gemini_native(client, model, api_key, prompt)
    else:
        return await _call_openai_compat(client, model, api_key, config.LLM_BASE_URL, prompt)


def _parse_raw_llm_json(text: str) -> RawLLMOutput:
    clean_text = text.strip()
    if clean_text.startswith("```"):
        lines = clean_text.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        clean_text = "\n".join(lines).strip()

    data = json.loads(clean_text)
    return RawLLMOutput.model_validate(data)


def heuristic_fallback_interpreter(notes: List[str], battery: BatteryInput) -> List[DirectiveInterpretation]:
    """
    Clearly-labelled degraded-mode heuristic parser used ONLY as a last resort
    when all LLM attempts, retries, and fallback models are unavailable (e.g. rate limits or offline).
    Documented transparently per competition specification.
    """
    logger.warning("ENGAGING DEGRADED-MODE HEURISTIC INTERPRETER FALLBACK")
    interpretations: List[DirectiveInterpretation] = []

    words_to_num = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
        "eleven": 11, "twelve": 12, "noon": 12, "midnight": 0,
    }

    def parse_time_expr(text: str) -> Optional[Tuple[int, int]]:
        t = text.lower()
        # 1. Check standard 24h format: "13:00 to 15:00", "between 13:00 and 15:00", "13:00 - 15:00"
        m24 = re.search(r"(\d{1,2}):00\s*(?:to|and|until|-|till)\s*(\d{1,2}):00", t)
        if m24:
            return int(m24.group(1)), int(m24.group(2))

        # 2. Check 12h format: e.g. "1-3 pm", "1 PM to 3 PM", "10 pm to 2 am", "6 PM till 10 PM", "8 AM to 11 AM"
        m12 = re.search(r"(\d{1,2})\s*(am|pm)?\s*(?:to|and|until|-|till)\s*(\d{1,2})\s*(am|pm)", t)
        if m12:
            s_val = int(m12.group(1))
            s_merid = m12.group(2)
            e_val = int(m12.group(3))
            e_merid = m12.group(4)

            # If start has no meridian, infer from end meridian unless midnight cross
            if not s_merid:
                s_merid = e_merid

            s_h = s_val % 12 + (12 if s_merid == "pm" else 0)
            e_h = e_val % 12 + (12 if e_merid == "pm" else 0)
            return s_h, e_h

        # 3. Check "noon until three PM", "one until three"
        m_words = re.search(r"(noon|midnight|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\s*(?:to|and|until|-|till)\s*(noon|midnight|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\s*(am|pm)?", t)
        if m_words:
            w1 = m_words.group(1)
            w2 = m_words.group(2)
            merid = m_words.group(3)
            v1 = words_to_num[w1]
            v2 = words_to_num[w2]
            if merid == "pm" or (not merid and v1 <= 6): # daytime afternoon
                if v1 < 12: v1 += 12
                if v2 < 12: v2 += 12
            return v1, v2

        return None

    for idx, note in enumerate(notes):
        n = note.lower()

        # Check for distractor / irrelevant note
        distractor_words = [
            "cafeteria", "biryani", "deadline", "seminar", "club", "contest",
            "menu", "auditorium", "water supply", "meeting", "air conditioning",
            "filter", "holiday", "registration",
        ]
        if any(dw in n for dw in distractor_words):
            interpretations.append(
                DirectiveInterpretation(
                    note_index=idx,
                    applies=False,
                    directive_type="no_op",
                    structured_adjustment=None,
                    explanation="Heuristic identified informational/distractor announcement.",
                )
            )
            continue

        time_window = parse_time_expr(n)
        start_h, end_h = time_window if time_window else (12, 14)

        # Check Solar Reduction
        if any(k in n for k in ["solar", "pv", "rooftop", "panel"]):
            # Extract factor
            factor = 0.2 # default
            # Check percentage
            m_pct = re.search(r"(\d+)\s*(?:%|percent)", n)
            if m_pct:
                pct = float(m_pct.group(1))
                if "curtailed to" in n or "curtail to" in n or "drops to" in n or "drop to" in n or "at " in n:
                    factor = pct / 100.0
                elif any(k in n for k in ["reduction", "reduced", "curtailment", "curtailed", "drop by", "drops by", "cut by", "reduce by", "reduce pv", "reduce"]):
                    factor = 1.0 - (pct / 100.0)
                else:
                    factor = pct / 100.0
            elif "one-fifth" in n:
                factor = 0.2
            elif "halved" in n or "half" in n:
                factor = 0.5
            elif "quarter" in n:
                if "loses a quarter" in n:
                    factor = 0.75
                else:
                    factor = 0.25

            raw_item = RawDirectiveItem(
                note_index=idx,
                relevant=True,
                directive_type="solar_reduction",
                start_hour=start_h,
                end_hour_exclusive=end_h,
                value=round(factor, 4),
                value_kind="fraction_remaining",
                explanation="Heuristic extracted solar reduction.",
            )
            item = normalize_raw_directive(raw_item, battery)

        # Check Minimum Battery Reserve
        elif any(k in n for k in ["reserve", "capacity", "hold", "remains above", "retain at least", "state-of-charge"]):
            m_pct = re.search(r"(\d+)\s*(?:%|percent)", n)
            if m_pct:
                pct = float(m_pct.group(1))
                raw_item = RawDirectiveItem(
                    note_index=idx,
                    relevant=True,
                    directive_type="minimum_battery_reserve",
                    start_hour=start_h,
                    end_hour_exclusive=end_h,
                    value=pct,
                    value_kind="percent_of_capacity",
                    explanation="Heuristic extracted battery reserve percentage.",
                )
            else:
                m_kwh = re.search(r"(\d+)\s*kwh", n)
                val_kwh = float(m_kwh.group(1)) if m_kwh else 80.0
                raw_item = RawDirectiveItem(
                    note_index=idx,
                    relevant=True,
                    directive_type="minimum_battery_reserve",
                    start_hour=start_h,
                    end_hour_exclusive=end_h,
                    value=val_kwh,
                    value_kind="kwh",
                    explanation="Heuristic extracted battery reserve in kWh.",
                )
            item = normalize_raw_directive(raw_item, battery)

        # Check No Discharge Window (must check before no charge to avoid conflict)
        elif any(k in n for k in ["no discharge", "no discharging", "prevent battery discharging", "prevent battery discharge", "discharging disabled", "not discharge"]):
            raw_item = RawDirectiveItem(
                note_index=idx,
                relevant=True,
                directive_type="no_discharge_window",
                start_hour=start_h,
                end_hour_exclusive=end_h,
                explanation="Heuristic extracted no discharge window.",
            )
            item = normalize_raw_directive(raw_item, battery)

        # Check No Charge Window
        elif any(k in n for k in ["no charge", "no charging", "charger isolated", "do not charge", "charging is prohibited", "not charge", "charging prohibited", "charging permitted"]):
            raw_item = RawDirectiveItem(
                note_index=idx,
                relevant=True,
                directive_type="no_charge_window",
                start_hour=start_h,
                end_hour_exclusive=end_h,
                explanation="Heuristic extracted no charge window.",
            )
            item = normalize_raw_directive(raw_item, battery)

        # Check Max Grid Window
        elif any(k in n for k in ["grid import", "grid intake", "must not exceed", "at or below", "grid electricity purchase", "grid purchase", "cap grid", "grid import limit", "grid import capped"]):
            m_cap = re.search(r"(\d+)\s*kwh", n)
            cap_val = float(m_cap.group(1)) if m_cap else 60.0
            raw_item = RawDirectiveItem(
                note_index=idx,
                relevant=True,
                directive_type="max_grid_window",
                start_hour=start_h,
                end_hour_exclusive=end_h,
                value=cap_val,
                value_kind="kwh",
                explanation="Heuristic extracted grid import limit.",
            )
            item = normalize_raw_directive(raw_item, battery)

        else:
            item = DirectiveInterpretation(
                note_index=idx,
                applies=False,
                directive_type="no_op",
                structured_adjustment=None,
                explanation="Unrecognized note classified as no_op by heuristic.",
            )

        interpretations.append(item)

    return validate_guardrails(interpretations, len(notes), battery)


async def interpret_operator_notes(
    operator_notes: List[str],
    battery: BatteryInput,
) -> List[DirectiveInterpretation]:
    """
    Main interpretation pipeline:
    1. Check LRU Cache
    2. Primary LLM call with structured output
    3. Deterministic normalization + guardrail validation
    4. Self-repair loop on error (retry with feedback)
    5. Fallback model retry
    6. Heuristic fallback (if enabled)
    """
    cache_key = _compute_cache_key(operator_notes, battery.capacity_kwh)
    if cache_key in _INTERPRETATION_CACHE:
        logger.info("Using cached directive interpretation")
        return _INTERPRETATION_CACHE[cache_key]

    start_time = time.monotonic()
    models_to_try = [config.LLM_MODEL]
    if config.LLM_FALLBACK_MODEL and config.LLM_FALLBACK_MODEL != config.LLM_MODEL:
        models_to_try.append(config.LLM_FALLBACK_MODEL)

    last_error: Optional[Exception] = None

    for model in models_to_try:
        # We allow up to 2 attempts per model (initial + 1 self-repair)
        error_feedback: Optional[str] = None
        for attempt in range(2):
            elapsed = time.monotonic() - start_time
            if elapsed > config.LLM_TOTAL_TIMEOUT_BUDGET:
                logger.warning("LLM total timeout budget exceeded")
                break

            prompt = _build_user_prompt(operator_notes, battery.capacity_kwh, error_feedback)
            try:
                raw_text = await _execute_provider_call(model, prompt)
                parsed_raw = _parse_raw_llm_json(raw_text)

                if len(parsed_raw.directives) != len(operator_notes):
                    raise GuardrailValidationError(
                        f"Expected {len(operator_notes)} directive items in JSON, got {len(parsed_raw.directives)}"
                    )

                normalized_items: List[DirectiveInterpretation] = []
                for raw_item in parsed_raw.directives:
                    norm = normalize_raw_directive(raw_item, battery)
                    normalized_items.append(norm)

                final_directives = validate_guardrails(normalized_items, len(operator_notes), battery)

                # Cache and return
                if len(_INTERPRETATION_CACHE) >= _CACHE_MAX_SIZE:
                    _INTERPRETATION_CACHE.pop(next(iter(_INTERPRETATION_CACHE)))
                _INTERPRETATION_CACHE[cache_key] = final_directives
                return final_directives

            except Exception as exc:
                last_error = exc
                error_feedback = str(exc)
                logger.warning(
                    f"Model {model} attempt {attempt + 1} failed: {exc}. "
                    f"{'Retrying with self-repair feedback...' if attempt == 0 else 'Switching models or fallback.'}"
                )

    # If all LLM calls failed, check heuristic fallback flag
    if config.ENABLE_HEURISTIC_FALLBACK:
        try:
            fallback_res = heuristic_fallback_interpreter(operator_notes, battery)
            _INTERPRETATION_CACHE[cache_key] = fallback_res
            return fallback_res
        except Exception as h_exc:
            logger.error(f"Heuristic fallback failed: {h_exc}")

    raise RuntimeError(
        f"Unable to interpret operator notes using LLM or fallbacks. Detail: {last_error}"
    )
