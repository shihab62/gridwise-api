import numpy as np
from typing import List, Tuple, Optional
from scipy.optimize import linprog

from src.models import (
    BatteryAction,
    BatteryInput,
    DirectiveInterpretation,
    HourInput,
    HourlyPlanItem,
    MaxGridAdjustment,
    MinimumBatteryReserveAdjustment,
    SolarReductionAdjustment,
    WindowHoursAdjustment,
)


class InfeasiblePlanError(Exception):
    """Raised when the optimization problem is infeasible under the given constraints."""
    pass


def compute_effective_solar(hours: List[HourInput], directives: List[DirectiveInterpretation]) -> List[float]:
    """Compute effective solar generation for each hour after applying solar reduction directives."""
    effective_solar = [h.solar_kwh for h in hours]
    for d in directives:
        if d.applies and d.directive_type == "solar_reduction" and d.structured_adjustment:
            adj = d.structured_adjustment
            if isinstance(adj, SolarReductionAdjustment):
                factor = adj.factor
                for h_idx in adj.hours:
                    if 0 <= h_idx < 24:
                        effective_solar[h_idx] *= factor
            elif isinstance(adj, dict):
                factor = float(adj.get("factor", 1.0))
                for h_idx in adj.get("hours", []):
                    if 0 <= h_idx < 24:
                        effective_solar[h_idx] *= factor
    return [max(0.0, float(s)) for s in effective_solar]


def optimize_energy_schedule(
    hours: List[HourInput],
    battery: BatteryInput,
    directives: List[DirectiveInterpretation],
) -> Tuple[List[HourlyPlanItem], float, float, float]:
    """
    Solves the linear program using SciPy HiGHS:
      Minimize total grid electricity cost over 24 hours.

    Variables for h in 0..23 (total 96 vars):
      g[h] (0..23): grid purchase in kWh
      s[h] (24..47): solar used in kWh
      b[h] (48..71): net battery flow in kWh (+charge, -discharge)
      E[h] (72..95): battery energy state of charge at end of hour h
    """
    N = 24
    effective_solar = compute_effective_solar(hours, directives)

    # Determine window constraints per hour
    no_charge_hours = set()
    no_discharge_hours = set()
    min_reserve_per_hour = [battery.minimum_energy_kwh] * N
    max_grid_per_hour: List[Optional[float]] = [None] * N

    for d in directives:
        if not d.applies or not d.structured_adjustment:
            continue
        adj = d.structured_adjustment
        d_type = d.directive_type

        # Handle pydantic models or dicts
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

    # Cost vector c
    c = np.zeros(4 * N)
    for h in range(N):
        c[h] = hours[h].tariff_bdt_per_kwh

    # Variable bounds
    bounds = []
    # g[h] bounds
    for h in range(N):
        upper_g = max_grid_per_hour[h]
        bounds.append((0.0, upper_g))

    # s[h] bounds
    for h in range(N):
        bounds.append((0.0, effective_solar[h]))

    # b[h] bounds: signed battery flow (+charge, -discharge)
    for h in range(N):
        lower_b = 0.0 if h in no_discharge_hours else -battery.max_discharge_kwh_per_hour
        upper_b = 0.0 if h in no_charge_hours else battery.max_charge_kwh_per_hour
        bounds.append((lower_b, upper_b))

    # E[h] bounds: battery energy
    for h in range(N):
        lower_e = min_reserve_per_hour[h]
        upper_e = battery.capacity_kwh
        if lower_e > upper_e + 1e-9:
            raise InfeasiblePlanError(
                f"Hour {h}: minimum reserve ({lower_e} kWh) exceeds battery capacity ({upper_e} kWh)"
            )
        bounds.append((lower_e, upper_e))

    # Equality constraints:
    # 1) Energy balance: g[h] + s[h] - b[h] = demand[h]  (24 rows)
    # 2) Battery transitions: E[0] - b[0] = initial_energy_kwh
    #    E[h] - E[h-1] - b[h] = 0 for h in 1..23 (24 rows)
    # 3) End of day neutrality: E[23] = initial_energy_kwh (1 row)
    num_eq = N + N + 1
    A_eq = np.zeros((num_eq, 4 * N))
    b_eq = np.zeros(num_eq)

    row = 0
    # 1) Energy balance
    for h in range(N):
        A_eq[row, h] = 1.0  # g[h]
        A_eq[row, N + h] = 1.0  # s[h]
        A_eq[row, 2 * N + h] = -1.0  # -b[h]
        b_eq[row] = hours[h].demand_kwh
        row += 1

    # 2) Battery transitions
    # h = 0
    A_eq[row, 3 * N + 0] = 1.0  # E[0]
    A_eq[row, 2 * N + 0] = -1.0  # -b[0]
    b_eq[row] = battery.initial_energy_kwh
    row += 1

    for h in range(1, N):
        A_eq[row, 3 * N + h] = 1.0  # E[h]
        A_eq[row, 3 * N + h - 1] = -1.0  # -E[h-1]
        A_eq[row, 2 * N + h] = -1.0  # -b[h]
        b_eq[row] = 0.0
        row += 1

    # 3) End of day neutrality: E[23] = initial_energy_kwh
    A_eq[row, 3 * N + 23] = 1.0
    b_eq[row] = battery.initial_energy_kwh

    res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")
    if not res.success:
        raise InfeasiblePlanError(f"Linear program infeasible or unbounded: {res.message}")

    x = res.x
    g_sol = x[0:N]
    s_sol = x[N : 2 * N]
    b_sol = x[2 * N : 3 * N]

    hourly_plan: List[HourlyPlanItem] = []
    current_energy = battery.initial_energy_kwh

    for h in range(N):
        b_val = float(b_sol[h])
        if abs(b_val) < 1e-7:
            action: BatteryAction = "idle"
            bat_kwh = 0.0
            signed_flow = 0.0
        elif b_val > 0.0:
            action = "charge"
            bat_kwh = round(b_val, 6)
            signed_flow = bat_kwh
        else:
            action = "discharge"
            bat_kwh = round(-b_val, 6)
            signed_flow = -bat_kwh

        s_val = round(float(s_sol[h]), 6)
        s_val = min(s_val, effective_solar[h])
        s_val = max(0.0, s_val)

        # Enforce exact hourly balance: grid = demand - solar + charge - discharge
        # i.e. grid + solar - signed_flow = demand => grid = demand - solar + signed_flow
        g_val = max(0.0, round(hours[h].demand_kwh - s_val + signed_flow, 6))

        current_energy = round(current_energy + signed_flow, 6)
        if h == N - 1:
            current_energy = round(battery.initial_energy_kwh, 6)

        hourly_plan.append(
            HourlyPlanItem(
                hour=h,
                grid_kwh=g_val,
                solar_used_kwh=s_val,
                battery_action=action,
                battery_kwh=bat_kwh,
                battery_energy_after_kwh=current_energy,
            )
        )

    total_grid_kwh = round(sum(item.grid_kwh for item in hourly_plan), 4)
    total_cost_bdt = round(
        sum(item.grid_kwh * hours[i].tariff_bdt_per_kwh for i, item in enumerate(hourly_plan)),
        2,
    )
    peak_grid_kwh = round(max(item.grid_kwh for item in hourly_plan), 4)

    return hourly_plan, total_grid_kwh, total_cost_bdt, peak_grid_kwh
