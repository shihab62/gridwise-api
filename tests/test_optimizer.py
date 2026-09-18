import pytest
from src.models import (
    BatteryInput,
    DirectiveInterpretation,
    HourInput,
    MaxGridAdjustment,
    MinimumBatteryReserveAdjustment,
    SolarReductionAdjustment,
    WindowHoursAdjustment,
)
from src.optimizer import InfeasiblePlanError, optimize_energy_schedule
from src.validator import validate_plan


@pytest.fixture
def standard_setup():
    hours = []
    base_demand = [30, 28, 25, 24, 25, 30, 45, 60, 75, 90, 105, 115, 120, 115, 105, 95, 85, 100, 120, 110, 90, 70, 50, 38]
    base_solar = [0, 0, 0, 0, 0, 2, 10, 30, 60, 85, 100, 110, 115, 110, 90, 65, 35, 10, 1, 0, 0, 0, 0, 0]
    base_tariff = [6.5]*6 + [8.0]*2 + [9.5]*8 + [10.5]*1 + [14.0]*5 + [10.5]*1 + [8.0]*1

    for h in range(24):
        hours.append(HourInput(hour=h, demand_kwh=base_demand[h], solar_kwh=base_solar[h], tariff_bdt_per_kwh=base_tariff[h]))

    battery = BatteryInput(
        capacity_kwh=200.0,
        initial_energy_kwh=100.0,
        minimum_energy_kwh=30.0,
        max_charge_kwh_per_hour=50.0,
        max_discharge_kwh_per_hour=50.0,
    )
    return hours, battery


def test_baseline_optimization(standard_setup):
    hours, battery = standard_setup
    plan, tg, tc, pg = optimize_energy_schedule(hours, battery, [])
    assert len(plan) == 24
    assert tc > 0
    # End-of-day battery energy neutrality
    assert plan[-1].battery_energy_after_kwh == pytest.approx(battery.initial_energy_kwh, abs=1e-4)
    # Replay validator
    validate_plan(hours, battery, [], plan, tg, tc, pg)


def test_solar_reduction_impact(standard_setup):
    hours, battery = standard_setup
    plan_base, _, tc_base, _ = optimize_energy_schedule(hours, battery, [])

    # Curtail solar from 11 to 14 by 90% (factor 0.1)
    d = DirectiveInterpretation(
        note_index=0,
        applies=True,
        directive_type="solar_reduction",
        structured_adjustment=SolarReductionAdjustment(hours=[11, 12, 13], factor=0.1),
        explanation="",
    )
    plan_curtailed, tg_curt, tc_curt, pg_curt = optimize_energy_schedule(hours, battery, [d])
    # Total cost should increase since solar is lost
    assert tc_curt > tc_base
    validate_plan(hours, battery, [d], plan_curtailed, tg_curt, tc_curt, pg_curt)


def test_no_charge_window_enforcement(standard_setup):
    hours, battery = standard_setup
    d = DirectiveInterpretation(
        note_index=0,
        applies=True,
        directive_type="no_charge_window",
        structured_adjustment=WindowHoursAdjustment(hours=[11, 12, 13]),
        explanation="",
    )
    plan, tg, tc, pg = optimize_energy_schedule(hours, battery, [d])
    for h in [11, 12, 13]:
        assert plan[h].battery_action != "charge"
    validate_plan(hours, battery, [d], plan, tg, tc, pg)


def test_no_discharge_window_enforcement(standard_setup):
    hours, battery = standard_setup
    d = DirectiveInterpretation(
        note_index=0,
        applies=True,
        directive_type="no_discharge_window",
        structured_adjustment=WindowHoursAdjustment(hours=[18, 19, 20]),
        explanation="",
    )
    plan, tg, tc, pg = optimize_energy_schedule(hours, battery, [d])
    for h in [18, 19, 20]:
        assert plan[h].battery_action != "discharge"
    validate_plan(hours, battery, [d], plan, tg, tc, pg)


def test_minimum_reserve_enforcement(standard_setup):
    hours, battery = standard_setup
    d = DirectiveInterpretation(
        note_index=0,
        applies=True,
        directive_type="minimum_battery_reserve",
        structured_adjustment=MinimumBatteryReserveAdjustment(hours=[18, 19, 20], minimum_energy_kwh=120.0),
        explanation="",
    )
    plan, tg, tc, pg = optimize_energy_schedule(hours, battery, [d])
    for h in [18, 19, 20]:
        assert plan[h].battery_energy_after_kwh >= 120.0 - 1e-4
    validate_plan(hours, battery, [d], plan, tg, tc, pg)


def test_infeasible_grid_cap(standard_setup):
    hours, battery = standard_setup
    # Demand at hour 19 is 120 kWh, solar is 0. If max grid is capped at 20 kWh and max discharge is 50 kWh:
    # 20 + 50 = 70 < 120 => physically infeasible
    d = DirectiveInterpretation(
        note_index=0,
        applies=True,
        directive_type="max_grid_window",
        structured_adjustment=MaxGridAdjustment(hours=[19], max_grid_kwh=20.0),
        explanation="",
    )
    with pytest.raises(InfeasiblePlanError):
        optimize_energy_schedule(hours, battery, [d])
