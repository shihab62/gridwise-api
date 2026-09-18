import copy
import pytest

from src.models import (
    BatteryInput,
    DirectiveInterpretation,
    HourInput,
    WindowHoursAdjustment,
)
from src.optimizer import optimize_energy_schedule
from src.validator import PlanValidationError, validate_plan


@pytest.fixture
def valid_run():
    base_demand = [30, 28, 25, 24, 25, 30, 45, 60, 75, 90, 105, 115, 120, 115, 105, 95, 85, 100, 120, 110, 90, 70, 50, 38]
    base_solar = [0, 0, 0, 0, 0, 2, 10, 30, 60, 85, 100, 110, 115, 110, 90, 65, 35, 10, 1, 0, 0, 0, 0, 0]
    base_tariff = [6.5]*6 + [8.0]*2 + [9.5]*8 + [10.5]*1 + [14.0]*5 + [10.5]*1 + [8.0]*1

    hours = [HourInput(hour=h, demand_kwh=base_demand[h], solar_kwh=base_solar[h], tariff_bdt_per_kwh=base_tariff[h]) for h in range(24)]
    battery = BatteryInput(
        capacity_kwh=200.0,
        initial_energy_kwh=100.0,
        minimum_energy_kwh=30.0,
        max_charge_kwh_per_hour=50.0,
        max_discharge_kwh_per_hour=50.0,
    )
    directives = []
    plan, tg, tc, pg = optimize_energy_schedule(hours, battery, directives)
    return hours, battery, directives, plan, tg, tc, pg


def test_validator_passes_on_valid(valid_run):
    hours, battery, directives, plan, tg, tc, pg = valid_run
    validate_plan(hours, battery, directives, plan, tg, tc, pg)


def test_validator_catches_energy_balance_violation(valid_run):
    hours, battery, directives, plan, tg, tc, pg = valid_run
    mutated = copy.deepcopy(plan)
    # Tamper with hour 5 grid_kwh without balancing
    mutated[5].grid_kwh += 5.0
    with pytest.raises(PlanValidationError, match="energy balance violated"):
        validate_plan(hours, battery, directives, mutated, tg, tc, pg)


def test_validator_catches_solar_overuse(valid_run):
    hours, battery, directives, plan, tg, tc, pg = valid_run
    mutated = copy.deepcopy(plan)
    # Tamper with hour 12 solar_used to exceed generation
    mutated[12].solar_used_kwh = 200.0  # max generation is 115
    with pytest.raises(PlanValidationError, match="exceeds effective solar"):
        validate_plan(hours, battery, directives, mutated, tg, tc, pg)


def test_validator_catches_no_charge_window_violation(valid_run):
    hours, battery, _, plan, tg, tc, pg = valid_run
    d = DirectiveInterpretation(
        note_index=0,
        applies=True,
        directive_type="no_charge_window",
        structured_adjustment=WindowHoursAdjustment(hours=[10, 11]),
        explanation="",
    )
    mutated = copy.deepcopy(plan)
    mutated[10].battery_action = "charge"
    mutated[10].battery_kwh = 20.0
    with pytest.raises(PlanValidationError, match="charged during no_charge_window"):
        validate_plan(hours, battery, [d], mutated, tg, tc, pg)


def test_validator_catches_end_of_day_neutrality_violation(valid_run):
    hours, battery, directives, plan, tg, tc, pg = valid_run
    mutated = copy.deepcopy(plan)
    # Balanced idle at hour 23: matches demand with grid, keeps battery energy at plan[22] level (150 kWh != 100 kWh initial)
    mutated[23].solar_used_kwh = 0.0
    mutated[23].battery_action = "idle"
    mutated[23].battery_kwh = 0.0
    mutated[23].grid_kwh = hours[23].demand_kwh
    mutated[23].battery_energy_after_kwh = plan[22].battery_energy_after_kwh
    with pytest.raises(PlanValidationError, match="End of day neutrality violated"):
        validate_plan(hours, battery, directives, mutated, tg, tc, pg)


def test_validator_catches_total_cost_mismatch(valid_run):
    hours, battery, directives, plan, tg, tc, pg = valid_run
    with pytest.raises(PlanValidationError, match="total_cost_bdt mismatch"):
        validate_plan(hours, battery, directives, plan, tg, tc + 50.0, pg)
