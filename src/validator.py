import math
from typing import List, Optional

from src.models import (
    BatteryInput,
    DirectiveInterpretation,
    HourInput,
    HourlyPlanItem,
)
from src.optimizer import compute_effective_solar


class PlanValidationError(Exception):
    """Raised when the plan fails deterministic validation checks."""
    pass


def validate_plan(
    hours: List[HourInput],
    battery: BatteryInput,
    directives: List[DirectiveInterpretation],
    hourly_plan: List[HourlyPlanItem],
    total_grid_kwh: float,
    total_cost_bdt: float,
    peak_grid_kwh: float,
    tolerance: float = 0.01,
) -> None:
    """
    Independently replays and verifies the 24-hour schedule against all physical
    and operational constraints with a specified numerical tolerance.
    """
    # 1. Structural check: exactly 24 entries, hours 0..23 in order
    if len(hourly_plan) != 24:
        raise PlanValidationError(f"hourly_plan must have exactly 24 entries, got {len(hourly_plan)}")

    for idx, item in enumerate(hourly_plan):
        if item.hour != idx:
            raise PlanValidationError(f"hourly_plan[{idx}] has hour={item.hour}, expected {idx}")

    # 2. Extract directive constraints per hour
    N = 24
    effective_solar = compute_effective_solar(hours, directives)
    no_charge_hours = set()
    no_discharge_hours = set()
    min_reserve_per_hour = [battery.minimum_energy_kwh] * N
    max_grid_per_hour: List[Optional[float]] = [None] * N

    for d in directives:
        if not d.applies or not d.structured_adjustment:
            continue
        adj = d.structured_adjustment
        d_type = d.directive_type
        hours_list = adj.hours if hasattr(adj, "hours") else adj.get("hours", [])

        if d_type == "no_charge_window":
            for h in hours_list:
                if 0 <= h < N:
                    no_charge_hours.add(h)
        elif d_type == "no_discharge_window":
            for h in hours_list:
                if 0 <= h < N:
                    no_discharge_hours.add(h)
        elif d_type == "minimum_battery_reserve":
            reserve_val = (
                adj.minimum_energy_kwh
                if hasattr(adj, "minimum_energy_kwh")
                else float(adj.get("minimum_energy_kwh", battery.minimum_energy_kwh))
            )
            for h in hours_list:
                if 0 <= h < N:
                    min_reserve_per_hour[h] = max(min_reserve_per_hour[h], reserve_val)
        elif d_type == "max_grid_window":
            grid_cap = (
                adj.max_grid_kwh
                if hasattr(adj, "max_grid_kwh")
                else float(adj.get("max_grid_kwh", float("inf")))
            )
            for h in hours_list:
                if 0 <= h < N:
                    if max_grid_per_hour[h] is None:
                        max_grid_per_hour[h] = grid_cap
                    else:
                        max_grid_per_hour[h] = min(max_grid_per_hour[h], grid_cap)

    # Replay simulation hour-by-hour
    current_energy = battery.initial_energy_kwh
    sum_grid = 0.0
    sum_cost = 0.0
    max_grid_observed = 0.0

    for h, item in enumerate(hourly_plan):
        # Non-negative & finite checks
        for name, val in [
            ("grid_kwh", item.grid_kwh),
            ("solar_used_kwh", item.solar_used_kwh),
            ("battery_kwh", item.battery_kwh),
            ("battery_energy_after_kwh", item.battery_energy_after_kwh),
        ]:
            if not math.isfinite(val):
                raise PlanValidationError(f"Hour {h}: {name} is not finite ({val})")
            if val < -tolerance:
                raise PlanValidationError(f"Hour {h}: {name} is negative ({val})")

        # Battery action consistency
        if item.battery_action == "idle" and item.battery_kwh > tolerance:
            raise PlanValidationError(
                f"Hour {h}: battery_action is idle but battery_kwh={item.battery_kwh} > 0"
            )

        if item.battery_action == "charge":
            signed_flow = item.battery_kwh
            if item.battery_kwh > battery.max_charge_kwh_per_hour + tolerance:
                raise PlanValidationError(
                    f"Hour {h}: charge amount {item.battery_kwh} exceeds max_charge {battery.max_charge_kwh_per_hour}"
                )
            if h in no_charge_hours:
                raise PlanValidationError(f"Hour {h}: battery charged during no_charge_window")
        elif item.battery_action == "discharge":
            signed_flow = -item.battery_kwh
            if item.battery_kwh > battery.max_discharge_kwh_per_hour + tolerance:
                raise PlanValidationError(
                    f"Hour {h}: discharge amount {item.battery_kwh} exceeds max_discharge {battery.max_discharge_kwh_per_hour}"
                )
            if h in no_discharge_hours:
                raise PlanValidationError(f"Hour {h}: battery discharged during no_discharge_window")
        else:
            signed_flow = 0.0

        # Solar constraint
        if item.solar_used_kwh > effective_solar[h] + tolerance:
            raise PlanValidationError(
                f"Hour {h}: solar_used {item.solar_used_kwh} exceeds effective solar {effective_solar[h]}"
            )

        # Max grid cap constraint
        if max_grid_per_hour[h] is not None:
            if item.grid_kwh > max_grid_per_hour[h] + tolerance:
                raise PlanValidationError(
                    f"Hour {h}: grid_kwh {item.grid_kwh} exceeds max_grid_window cap {max_grid_per_hour[h]}"
                )

        # Energy balance constraint: grid + solar - signed_flow = demand
        balance_diff = abs(item.grid_kwh + item.solar_used_kwh - signed_flow - hours[h].demand_kwh)
        if balance_diff > tolerance:
            raise PlanValidationError(
                f"Hour {h}: energy balance violated by {balance_diff:.4f} kWh (grid={item.grid_kwh}, solar={item.solar_used_kwh}, flow={signed_flow}, demand={hours[h].demand_kwh})"
            )

        # Battery energy transition check
        expected_energy = current_energy + signed_flow
        if abs(item.battery_energy_after_kwh - expected_energy) > tolerance:
            raise PlanValidationError(
                f"Hour {h}: battery transition error. Expected {expected_energy:.4f}, got {item.battery_energy_after_kwh}"
            )
        current_energy = item.battery_energy_after_kwh

        # Battery capacity & minimum reserve check
        min_reserve = min_reserve_per_hour[h]
        if current_energy < min_reserve - tolerance:
            raise PlanValidationError(
                f"Hour {h}: battery energy {current_energy} fell below required minimum {min_reserve}"
            )
        if current_energy > battery.capacity_kwh + tolerance:
            raise PlanValidationError(
                f"Hour {h}: battery energy {current_energy} exceeded capacity {battery.capacity_kwh}"
            )

        sum_grid += item.grid_kwh
        sum_cost += item.grid_kwh * hours[h].tariff_bdt_per_kwh
        if item.grid_kwh > max_grid_observed:
            max_grid_observed = item.grid_kwh

    # End-of-day neutrality check
    if abs(current_energy - battery.initial_energy_kwh) > tolerance:
        raise PlanValidationError(
            f"End of day neutrality violated. Battery energy at h=23 is {current_energy:.4f}, initial was {battery.initial_energy_kwh}"
        )

    # Totals check
    if abs(total_grid_kwh - sum_grid) > tolerance:
        raise PlanValidationError(
            f"total_grid_kwh mismatch: reported {total_grid_kwh}, calculated {sum_grid:.4f}"
        )
    if abs(total_cost_bdt - sum_cost) > tolerance:
        raise PlanValidationError(
            f"total_cost_bdt mismatch: reported {total_cost_bdt}, calculated {sum_cost:.4f}"
        )
    if abs(peak_grid_kwh - max_grid_observed) > tolerance:
        raise PlanValidationError(
            f"peak_grid_kwh mismatch: reported {peak_grid_kwh}, calculated {max_grid_observed:.4f}"
        )
