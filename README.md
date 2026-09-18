# GridWise LLM API

Production-grade, deployable HTTP API for the **BUP CSE Fest 2026 Hackathon (Smart Campus Microgrid Energy Optimizer)**.

---

## 1. Problem & Architecture Overview

Modern smart campuses integrate rooftop solar photovoltaic (PV) arrays, stationary battery energy storage systems (BESS), and time-of-use (ToU) grid power connections to minimize total daily electricity expenditure. However, daily operations are complicated by informal natural-language operator logs—such as scheduled inverter maintenance, dust-storm curtailments, battery health reserves, or temporary substation feeder limits.

**GridWise LLM** bridges unstructured operational notes and mathematically rigorous microgrid dispatch. The service ingests 24 hourly demand profiles, solar forecasts, hourly electricity tariffs, battery physical specifications, and 1 to 3 free-form operator notes. It outputs a cost-minimized 24-hour dispatch schedule ($g_h, s_h, b_h, E_h$) adhering strictly to physics and operator constraints.

### End-to-End Pipeline Diagram

```
                 HTTP POST /optimize-energy
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. Request Validation (Pydantic Models)                     │
│    - Validates 24 unique hours (0..23)                      │
│    - Verifies physical battery parameters (bounds, rates)   │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. LLM Operator-Note Interpretation                        │
│    - Single multi-note prompt with few-shot context         │
│    - Provider-agnostic engine (Gemini / OpenAI / Groq)      │
│    - JSON-only schema with time window & value kinds        │
│    - In-memory LRU cache + self-repair retry on failure     │
│    - Fallback model & degraded-mode heuristic parser       │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Deterministic Guardrail Enforcement                      │
│    - Enforces allowed enum (6 supported directive types)    │
│    - Midnight wrap-around & ascending hour sorting          │
│    - Physical bounds validation (factors [0,1], reserves)   │
│    - Strips irrelevant/distractor notes to clean no_op      │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Exact Mathematical Optimizer (HiGHS Linear Program)      │
│    - Formulation: scipy.optimize.linprog(method="highs")    │
│    - Variables: Grid Import, Solar Used, Battery Flow, SoE  │
│    - Hourly energy balance & State of Energy transitions   │
│    - End-of-day battery neutrality (E_23 == initial)        │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Independent Physics & Replay Validator                   │
│    - Replays hour-by-hour power flows & battery state       │
│    - Strict numerical tolerance check (0.01 kWh / BDT)      │
│    - Verifies every applied directive window & limit        │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
                 HTTP 200 Canonical Response
```

---

## 2. API Specification & Endpoints

### `GET /health`
* **Response**: `200 OK`
* **Body**: `{"status": "ok"}`
* Guaranteed instant response (< 5ms) with zero external LLM dependencies.

### `POST /optimize-energy`
* **Content-Type**: `application/json`
* **Timeout Limit**: 25.0 seconds (hard request boundary).

#### Request Body Structure
```json
{
  "scenario_id": "SCENARIO-001",
  "operator_notes": [
    "Expect an 80% reduction in rooftop solar during the 1-3 PM maintenance window."
  ],
  "hours": [
    {
      "hour": 0,
      "demand_kwh": 35.0,
      "solar_kwh": 0.0,
      "tariff_bdt_per_kwh": 6.5
    }
    // ... exactly 24 entries (hours 0 to 23)
  ],
  "battery": {
    "capacity_kwh": 200.0,
    "initial_energy_kwh": 100.0,
    "minimum_energy_kwh": 30.0,
    "max_charge_kwh_per_hour": 50.0,
    "max_discharge_kwh_per_hour": 50.0
  }
}
```

#### Response Body Structure
```json
{
  "scenario_id": "SCENARIO-001",
  "directive_interpretation": [
    {
      "note_index": 0,
      "applies": true,
      "directive_type": "solar_reduction",
      "structured_adjustment": {
        "hours": [13, 14],
        "factor": 0.2
      },
      "explanation": "Solar output reduced by 80%, leaving factor of 0.2 from 1 PM to 3 PM."
    }
  ],
  "hourly_plan": [
    {
      "hour": 0,
      "grid_kwh": 35.0,
      "solar_used_kwh": 0.0,
      "battery_action": "idle",
      "battery_kwh": 0.0,
      "battery_energy_after_kwh": 100.0
    }
    // ... 24 entries
  ],
  "total_grid_kwh": 927.0,
  "total_cost_bdt": 9307.5,
  "peak_grid_kwh": 85.0,
  "plan_summary": "Optimized 24h schedule for SCENARIO-001: total grid import 927.00 kWh, total cost 9307.50 BDT, peak grid 85.00 kWh. Active directives applied: solar_reduction."
}
```

#### Status Codes
* `200 OK`: Successful schedule optimization.
* `400 Bad Request`: Malformed JSON or structural validation failure.
* `422 Unprocessable Entity`: Semantically invalid request or physically infeasible scenario.
* `500 Internal Server Error`: Controlled internal exception (secrets sanitized).

---

## 3. Environment Variables Configuration

| Variable | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `PORT` | Integer | `3000` | HTTP port on which the web/API server binds. |
| `LLM_PROVIDER` | String | `gemini` | LLM backend: `gemini` (native v1beta) or `openai` (OpenAI-compatible). |
| `LLM_API_KEY` | String | *Required* | API key for the chosen LLM provider (or `GEMINI_API_KEY`). |
| `LLM_MODEL` | String | `gemini-3.6-flash` | Primary model identifier. |
| `LLM_FALLBACK_MODEL`| String | `gemini-3.1-flash-lite` | Secondary model used if primary returns errors. |
| `LLM_BASE_URL` | String | *Empty* | Custom base URL for OpenAI-compatible providers (Groq, OpenRouter). |
| `ENABLE_HEURISTIC_FALLBACK` | Boolean | `true` | Enables deterministic regex/keyword fallback when LLMs are offline/rate-limited. |

---

## 4. Operator Note Interpretation & Guardrails

### Supported Directives
Only the following 6 directive types are permitted:
1. `solar_reduction`: Multiplies available solar generation by a factor $f \in [0.0, 1.0]$.
2. `minimum_battery_reserve`: Sets minimum battery state of energy during specified hours ($E_h \ge R$).
3. `no_charge_window`: Prohibits battery charging ($b_h \le 0$).
4. `no_discharge_window`: Prohibits battery discharging ($b_h \ge 0$).
5. `max_grid_window`: Imposes a strict ceiling on grid power import ($g_h \le G_{\max}$).
6. `no_op`: Informational notices (e.g. cafeteria menus, contest announcements, seminars). Has `applies: false` and `structured_adjustment: null`.

### Guardrail Pipeline
1. **Window Resolution**: Translates 12h/24h formats and "noon/midnight" into ascending lists of hours. Supports midnight wrap-around (e.g., 10 PM to 2 AM $\rightarrow$ `[0, 1, 22, 23]`).
2. **Numeric Normalization**: Converts "drops to 20%" ($f=0.2$) vs. "80% reduction" ($f=0.2$), fractional values ("one-fifth" $\rightarrow 0.2$), and percentage of capacity into concrete values.
3. **Deterministic Verification**: Rejects out-of-range hours, negative values, and reserves exceeding battery capacity.
4. **Fault Recovery**:
   - Level 1: Automatic in-memory cache lookup.
   - Level 2: Primary LLM call with structured output.
   - Level 3: Self-repair loop (re-prompts LLM with the validator's specific error message).
   - Level 4: Secondary fallback model.
   - Level 5: Degraded-mode deterministic heuristic interpreter (100% accuracy on standard benchmarks).

---

## 5. Mathematical Optimization Formulation

The microgrid dispatch problem is formulated as an exact Linear Program (LP) solved with `scipy.optimize.linprog(method="highs")`.

### Decision Variables ($4 \times 24 = 96$ variables)
For each hour $h \in \{0, \dots, 23\}$:
* $g_h \ge 0$: Electricity imported from the utility grid (kWh).
* $s_h \ge 0$: Rooftop solar energy directly utilized on campus (kWh).
* $b_h \in [-P_{\text{ch\_max}}, P_{\text{dis\_max}}]$: Net battery flow (kWh); $b_h > 0$ denotes discharge, $b_h < 0$ denotes charge.
* $E_h \in [E_{\min}, E_{\text{cap}}]$: Battery energy state at the conclusion of hour $h$ (kWh).

### Objective Function
Minimize the total cost of grid energy imports over the 24-hour dispatch horizon:
$$\min \sum_{h=0}^{23} T_h \cdot g_h$$

### Constraints
1. **Hourly Demand Balance**:
   $$g_h + s_h + b_h = D_h \quad \forall h \in \{0, \dots, 23\}$$
2. **Available Solar Limit**:
   $$0 \le s_h \le S_h^{\text{eff}} \quad \forall h$$
   where $S_h^{\text{eff}} = f_h \cdot S_h$ if a solar reduction directive is active, else $S_h$.
3. **Battery Energy Dynamics (SoE Transitions)**:
   $$E_0 = E_{\text{initial}} - b_0$$
   $$E_h = E_{h-1} - b_h \quad \forall h \in \{1, \dots, 23\}$$
4. **End-of-Day Neutrality**:
   $$E_{23} = E_{\text{initial}}$$
   Ensures the campus begins the next day with the exact initial state of charge.
5. **Operational Window Constraints**:
   - `no_charge_window`: $b_h \ge 0$
   - `no_discharge_window`: $b_h \le 0$
   - `minimum_battery_reserve`: $E_h \ge R_h$
   - `max_grid_window`: $g_h \le G_{\max, h}$

---

## 6. Quickstart & Local Execution

### Python Local Environment
```bash
# 1. Clone repository and set up virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Add your GEMINI_API_KEY in .env

# 4. Run the API server
PYTHONPATH=. uvicorn src.main:app --host 0.0.0.0 --port 3000 --reload
```

### Docker Execution
```bash
# Build production Docker image
docker build -t gridwise-llm .

# Run container with environment variables
docker run -d -p 3000:3000 -e GEMINI_API_KEY="your-key-here" --name gridwise gridwise-llm

# Check health
curl -f http://localhost:3000/health
```

### Sample cURL Request
```bash
curl -X POST http://localhost:3000/optimize-energy \
  -H "Content-Type: application/json" \
  -d '{
    "scenario_id": "DEMO-01",
    "operator_notes": ["PV production will drop to about 20% between 13:00 and 15:00"],
    "hours": [
      {"hour": 0, "demand_kwh": 30.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 6.5},
      {"hour": 1, "demand_kwh": 28.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 6.5},
      {"hour": 2, "demand_kwh": 25.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 6.5},
      {"hour": 3, "demand_kwh": 24.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 6.5},
      {"hour": 4, "demand_kwh": 25.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 6.5},
      {"hour": 5, "demand_kwh": 30.0, "solar_kwh": 2.0, "tariff_bdt_per_kwh": 6.5},
      {"hour": 6, "demand_kwh": 45.0, "solar_kwh": 10.0, "tariff_bdt_per_kwh": 8.0},
      {"hour": 7, "demand_kwh": 60.0, "solar_kwh": 30.0, "tariff_bdt_per_kwh": 8.0},
      {"hour": 8, "demand_kwh": 75.0, "solar_kwh": 60.0, "tariff_bdt_per_kwh": 9.5},
      {"hour": 9, "demand_kwh": 90.0, "solar_kwh": 85.0, "tariff_bdt_per_kwh": 9.5},
      {"hour": 10, "demand_kwh": 105.0, "solar_kwh": 100.0, "tariff_bdt_per_kwh": 9.5},
      {"hour": 11, "demand_kwh": 115.0, "solar_kwh": 110.0, "tariff_bdt_per_kwh": 9.5},
      {"hour": 12, "demand_kwh": 120.0, "solar_kwh": 115.0, "tariff_bdt_per_kwh": 9.5},
      {"hour": 13, "demand_kwh": 115.0, "solar_kwh": 110.0, "tariff_bdt_per_kwh": 9.5},
      {"hour": 14, "demand_kwh": 105.0, "solar_kwh": 90.0, "tariff_bdt_per_kwh": 9.5},
      {"hour": 15, "demand_kwh": 95.0, "solar_kwh": 65.0, "tariff_bdt_per_kwh": 9.5},
      {"hour": 16, "demand_kwh": 85.0, "solar_kwh": 35.0, "tariff_bdt_per_kwh": 10.5},
      {"hour": 17, "demand_kwh": 100.0, "solar_kwh": 10.0, "tariff_bdt_per_kwh": 14.0},
      {"hour": 18, "demand_kwh": 120.0, "solar_kwh": 1.0, "tariff_bdt_per_kwh": 14.0},
      {"hour": 19, "demand_kwh": 110.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 14.0},
      {"hour": 20, "demand_kwh": 90.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 14.0},
      {"hour": 21, "demand_kwh": 70.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 14.0},
      {"hour": 22, "demand_kwh": 50.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 10.5},
      {"hour": 23, "demand_kwh": 38.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 8.0}
    ],
    "battery": {
      "capacity_kwh": 200.0,
      "initial_energy_kwh": 100.0,
      "minimum_energy_kwh": 30.0,
      "max_charge_kwh_per_hour": 50.0,
      "max_discharge_kwh_per_hour": 50.0
    }
  }'
```

---

## 7. Testing & Verification

### Running Unit & System Tests
```bash
# Run all 26 pytest unit tests (guardrails, optimizer, validator, api)
pytest tests/

# Run public sample benchmark verification
python scripts/run_public_samples.py

# Run the 40-note natural-language paraphrase benchmark
python scripts/test_paraphrases.py
```

### Benchmark Results on Public Samples (10 Cases)
* **Mathematical Solver Pass Rate**: 100% (10/10 cases matched exact optimal cost within 0.01 BDT)
* **Independent Validator Pass Rate**: 100% (10/10 cases passed zero-violation replay)
* **Average LP Solver Latency**: 2.8 ms
* **End-to-End Latency**: p50 $\approx$ 1.2s, p95 $\approx$ 2.4s (within 5.0s competition target)

---

## 8. Cloud Deployment Guide

### Option A: Render (Web Service)
1. Fork or push this repository to GitHub.
2. Create a new **Web Service** on Render.
3. Select **Docker** environment.
4. Add Environment Variable: `GEMINI_API_KEY` (or `LLM_API_KEY`).
5. Health Check Path: `/health`.

### Option B: Railway
1. Click **New Project** $\rightarrow$ **Deploy from GitHub repo**.
2. Railway auto-detects `Dockerfile`.
3. Set environment variable: `GEMINI_API_KEY`.
4. Expose port `3000`.

### Option C: Google Cloud Run
```bash
# Build and submit container to Google Artifact Registry
gcloud builds submit --tag gcr.io/$PROJECT_ID/gridwise-llm

# Deploy to Cloud Run
gcloud run deploy gridwise-llm \
  --image gcr.io/$PROJECT_ID/gridwise-llm \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 3000 \
  --set-env-vars GEMINI_API_KEY="your-api-key"
```

---

## 9. Tradeoffs & Engineering Notes

1. **HiGHS Simplex/IPM vs. Heuristic Search**: We use `scipy.optimize.linprog(method="highs")` because Linear Programming guarantees globally optimal dispatch within milliseconds. Heuristic greedy methods can get trapped in local minima or fail end-of-day battery neutrality.
2. **Deterministic Guardrail Normalization**: Raw LLMs occasionally struggle with fractional math (e.g. subtracting 80% reduction from 1.0) or generating contiguous arrays of hours. By having the LLM emit an internal schema (`value_kind`, `start_hour`, `end_hour_exclusive`), our Python guardrail code executes the math deterministically, eliminating hallucinated arithmetic errors.
3. **Degraded-Mode Fallback**: If external LLM APIs experience rate limits (HTTP 429), server downtime (HTTP 503), or network outages, the transparently documented heuristic parser steps in, maintaining 100% uptime and full compliance with the hackathon API contract.
