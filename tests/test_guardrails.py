import pytest
from src.guardrails import (
    GuardrailValidationError,
    expand_hours,
    normalize_raw_directive,
    validate_guardrails,
)
from src.models import (
    BatteryInput,
    DirectiveInterpretation,
    RawDirectiveItem,
    SolarReductionAdjustment,
)


@pytest.fixture
def sample_battery():
    return BatteryInput(
        capacity_kwh=200.0,
        initial_energy_kwh=100.0,
        minimum_energy_kwh=20.0,
        max_charge_kwh_per_hour=50.0,
        max_discharge_kwh_per_hour=50.0,
    )


def test_expand_hours_normal():
    assert expand_hours(13, 15) == [13, 14]
    assert expand_hours(0, 3) == [0, 1, 2]
    assert expand_hours(18, 21) == [18, 19, 20]


def test_expand_hours_midnight_wrap():
    # 22:00 to 02:00 -> [0, 1, 22, 23]
    hours = expand_hours(22, 2)
    assert hours == [0, 1, 22, 23]


def test_expand_hours_invalid():
    with pytest.raises(GuardrailValidationError):
        expand_hours(15, 15)  # empty window
    with pytest.raises(GuardrailValidationError):
        expand_hours(-1, 5)  # negative start
    with pytest.raises(GuardrailValidationError):
        expand_hours(10, 25)  # > 24


def test_normalize_solar_reduction(sample_battery):
    raw = RawDirectiveItem(
        note_index=0,
        relevant=True,
        directive_type="solar_reduction",
        start_hour=13,
        end_hour_exclusive=15,
        value=80.0,
        value_kind="percent_reduction",
        explanation="80% reduction leaves 0.2 factor",
    )
    norm = normalize_raw_directive(raw, sample_battery)
    assert norm.applies is True
    assert norm.directive_type == "solar_reduction"
    assert norm.structured_adjustment.factor == pytest.approx(0.2, abs=1e-4)
    assert norm.structured_adjustment.hours == [13, 14]


def test_normalize_battery_reserve_percent(sample_battery):
    raw = RawDirectiveItem(
        note_index=0,
        relevant=True,
        directive_type="minimum_battery_reserve",
        start_hour=18,
        end_hour_exclusive=21,
        value=50.0,
        value_kind="percent_of_capacity",
        explanation="50% of 200 kWh = 100 kWh",
    )
    norm = normalize_raw_directive(raw, sample_battery)
    assert norm.applies is True
    assert norm.structured_adjustment.minimum_energy_kwh == pytest.approx(100.0, abs=1e-4)
    assert norm.structured_adjustment.hours == [18, 19, 20]


def test_normalize_reserve_exceeds_capacity(sample_battery):
    raw = RawDirectiveItem(
        note_index=0,
        relevant=True,
        directive_type="minimum_battery_reserve",
        start_hour=18,
        end_hour_exclusive=21,
        value=250.0,
        value_kind="kwh",
    )
    with pytest.raises(GuardrailValidationError):
        normalize_raw_directive(raw, sample_battery)


def test_normalize_no_op(sample_battery):
    raw = RawDirectiveItem(
        note_index=0,
        relevant=False,
        directive_type="no_op",
        start_hour=None,
        end_hour_exclusive=None,
        value=None,
        value_kind=None,
        explanation="Irrelevant note",
    )
    norm = normalize_raw_directive(raw, sample_battery)
    assert norm.applies is False
    assert norm.directive_type == "no_op"
    assert norm.structured_adjustment is None


def test_validate_guardrails_mismatched_index(sample_battery):
    directives = [
        DirectiveInterpretation(
            note_index=1,  # should be 0
            applies=False,
            directive_type="no_op",
            structured_adjustment=None,
            explanation="",
        )
    ]
    with pytest.raises(GuardrailValidationError):
        validate_guardrails(directives, 1, sample_battery)


def test_validate_guardrails_no_op_with_applies_true(sample_battery):
    directives = [
        DirectiveInterpretation(
            note_index=0,
            applies=True,  # illegal for no_op
            directive_type="no_op",
            structured_adjustment=None,
            explanation="",
        )
    ]
    with pytest.raises(GuardrailValidationError):
        validate_guardrails(directives, 1, sample_battery)
