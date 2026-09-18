import math
from typing import Any, Dict, List, Optional

from src.models import (
    BatteryInput,
    DirectiveInterpretation,
    DirectiveType,
    MaxGridAdjustment,
    MinimumBatteryReserveAdjustment,
    RawDirectiveItem,
    SolarReductionAdjustment,
    WindowHoursAdjustment,
)

ALLOWED_DIRECTIVES = {
    "solar_reduction",
    "minimum_battery_reserve",
    "no_charge_window",
    "no_discharge_window",
    "max_grid_window",
    "no_op",
}


class GuardrailValidationError(Exception):
    """Raised when an LLM directive fails strict deterministic guardrail checks."""
    pass


def expand_hours(start_hour: Optional[int], end_hour_exclusive: Optional[int]) -> List[int]:
    """
    Expands start-inclusive, end-exclusive window to a sorted list of unique hour integers (0..23).
    Correctly handles midnight wrap-around (e.g. start=22, end=2 -> [0, 1, 22, 23]).
    """
    if start_hour is None or end_hour_exclusive is None:
        raise GuardrailValidationError("Active directive must specify start_hour and end_hour_exclusive")

    if not (0 <= start_hour <= 23):
        raise GuardrailValidationError(f"start_hour ({start_hour}) must be in [0, 23]")
    if not (0 <= end_hour_exclusive <= 24):
        raise GuardrailValidationError(f"end_hour_exclusive ({end_hour_exclusive}) must be in [0, 24]")

    if start_hour == end_hour_exclusive:
        raise GuardrailValidationError(f"Empty time window: start_hour={start_hour} equals end_hour_exclusive")

    # If end_hour_exclusive is 24, it means up to hour 23 inclusive
    if start_hour < end_hour_exclusive:
        hours = list(range(start_hour, min(24, end_hour_exclusive)))
    else:
        # Crosses midnight (e.g. 22 to 2 -> 22, 23, 0, 1)
        hours = list(range(start_hour, 24)) + list(range(0, end_hour_exclusive))

    unique_sorted_hours = sorted(list(set(hours)))
    if not unique_sorted_hours:
        raise GuardrailValidationError("Resolved hours list is empty")

    for h in unique_sorted_hours:
        if not (0 <= h <= 23):
            raise GuardrailValidationError(f"Hour {h} out of valid range 0..23")

    return unique_sorted_hours


def normalize_raw_directive(
    raw: RawDirectiveItem,
    battery: BatteryInput,
) -> DirectiveInterpretation:
    """
    Deterministically normalizes a raw LLM directive output into the strict canonical schema.
    Converts percent/fraction/reduction semantics and expands time ranges.
    """
    d_type = raw.directive_type.lower().strip()
    if d_type not in ALLOWED_DIRECTIVES:
        raise GuardrailValidationError(f"Unsupported directive_type '{d_type}'")

    if not raw.relevant or d_type == "no_op":
        return DirectiveInterpretation(
            note_index=raw.note_index,
            applies=False,
            directive_type="no_op",
            structured_adjustment=None,
            explanation=raw.explanation or "Note determined to be irrelevant or no operation required.",
        )

    # Active directive
    hours = expand_hours(raw.start_hour, raw.end_hour_exclusive)

    if d_type == "solar_reduction":
        if raw.value is None:
            raise GuardrailValidationError("solar_reduction requires a numeric value")
        val = float(raw.value)
        kind = (raw.value_kind or "fraction_remaining").lower()

        if kind == "fraction_remaining":
            factor = val
        elif kind == "percent_remaining":
            factor = val / 100.0
        elif kind == "percent_reduction":
            factor = 1.0 - (val / 100.0)
        else:
            # Fallback heuristic if value is > 1.0 (e.g. 20 -> 0.20 or 80% reduction)
            if val > 1.0:
                factor = val / 100.0
            else:
                factor = val

        factor = round(max(0.0, min(1.0, factor)), 6)
        adjustment = SolarReductionAdjustment(hours=hours, factor=factor)

    elif d_type == "minimum_battery_reserve":
        if raw.value is None:
            raise GuardrailValidationError("minimum_battery_reserve requires a numeric value")
        val = float(raw.value)
        kind = (raw.value_kind or "kwh").lower()

        if kind == "percent_of_capacity":
            reserve_kwh = (val / 100.0) * battery.capacity_kwh
        else:
            reserve_kwh = val

        if not math.isfinite(reserve_kwh) or reserve_kwh < 0.0:
            raise GuardrailValidationError(f"Invalid reserve energy: {reserve_kwh}")
        if reserve_kwh > battery.capacity_kwh + 1e-6:
            raise GuardrailValidationError(
                f"Minimum reserve {reserve_kwh:.2f} kWh exceeds battery capacity {battery.capacity_kwh:.2f} kWh"
            )

        adjustment = MinimumBatteryReserveAdjustment(
            hours=hours, minimum_energy_kwh=round(reserve_kwh, 4)
        )

    elif d_type == "no_charge_window":
        adjustment = WindowHoursAdjustment(hours=hours)

    elif d_type == "no_discharge_window":
        adjustment = WindowHoursAdjustment(hours=hours)

    elif d_type == "max_grid_window":
        if raw.value is None:
            raise GuardrailValidationError("max_grid_window requires a numeric max_grid_kwh value")
        val = float(raw.value)
        if not math.isfinite(val) or val < 0.0:
            raise GuardrailValidationError(f"Invalid max_grid_kwh value: {val}")
        adjustment = MaxGridAdjustment(hours=hours, max_grid_kwh=round(val, 4))

    else:
        raise GuardrailValidationError(f"Unknown directive type: {d_type}")

    return DirectiveInterpretation(
        note_index=raw.note_index,
        applies=True,
        directive_type=d_type,  # type: ignore
        structured_adjustment=adjustment,
        explanation=raw.explanation or f"Applied {d_type} over hours {hours}",
    )


def validate_guardrails(
    directives: List[DirectiveInterpretation],
    num_notes: int,
    battery: BatteryInput,
) -> List[DirectiveInterpretation]:
    """
    Final deterministic validation of the interpreted directives list:
    - Exactly one entry per note, note_index 0..N-1 in order
    - directive_type in the allowed enum
    - applies / no_op consistency
    - hours sorted, unique, in [0, 23]
    - all values within physical bounds
    """
    if len(directives) != num_notes:
        raise GuardrailValidationError(
            f"Expected {num_notes} directive interpretations, got {len(directives)}"
        )

    normalized: List[DirectiveInterpretation] = []

    for i, d in enumerate(directives):
        if d.note_index != i:
            raise GuardrailValidationError(f"Directive at index {i} has note_index={d.note_index}, expected {i}")

        if d.directive_type not in ALLOWED_DIRECTIVES:
            raise GuardrailValidationError(f"Directive {i} has invalid type '{d.directive_type}'")

        if d.directive_type == "no_op":
            if d.applies:
                raise GuardrailValidationError(f"Directive {i} is no_op but applies is True")
            if d.structured_adjustment is not None:
                raise GuardrailValidationError(f"Directive {i} is no_op but structured_adjustment is not null")
            normalized.append(d)
            continue

        # Non no_op
        if not d.applies:
            raise GuardrailValidationError(f"Directive {i} is {d.directive_type} but applies is False")
        if d.structured_adjustment is None:
            raise GuardrailValidationError(f"Directive {i} is {d.directive_type} but structured_adjustment is null")

        adj = d.structured_adjustment
        hours = adj.hours if hasattr(adj, "hours") else adj.get("hours", [])
        if not hours:
            raise GuardrailValidationError(f"Directive {i} hours list is empty")

        # Check unique and sorted
        sorted_unique = sorted(list(set(hours)))
        if hours != sorted_unique:
            # Clean it up deterministically
            if hasattr(adj, "hours"):
                adj.hours = sorted_unique
            elif isinstance(adj, dict):
                adj["hours"] = sorted_unique

        for h in sorted_unique:
            if not (0 <= h <= 23):
                raise GuardrailValidationError(f"Directive {i} contains out-of-range hour: {h}")

        if d.directive_type == "solar_reduction":
            factor = adj.factor if hasattr(adj, "factor") else float(adj.get("factor", 1.0))
            if not (0.0 <= factor <= 1.0):
                raise GuardrailValidationError(f"solar_reduction factor {factor} must be in [0.0, 1.0]")

        elif d.directive_type == "minimum_battery_reserve":
            res = (
                adj.minimum_energy_kwh
                if hasattr(adj, "minimum_energy_kwh")
                else float(adj.get("minimum_energy_kwh", 0.0))
            )
            if not math.isfinite(res) or res < 0.0:
                raise GuardrailValidationError(f"minimum_energy_kwh {res} must be non-negative and finite")
            if res > battery.capacity_kwh + 1e-6:
                raise GuardrailValidationError(
                    f"minimum_energy_kwh {res} exceeds battery capacity {battery.capacity_kwh}"
                )

        elif d.directive_type == "max_grid_window":
            cap = (
                adj.max_grid_kwh
                if hasattr(adj, "max_grid_kwh")
                else float(adj.get("max_grid_kwh", 0.0))
            )
            if not math.isfinite(cap) or cap < 0.0:
                raise GuardrailValidationError(f"max_grid_kwh {cap} must be non-negative and finite")

        normalized.append(d)

    return normalized
