import math
from typing import List, Literal, Optional, Union
from pydantic import BaseModel, Field, field_validator, model_validator

DirectiveType = Literal[
    "solar_reduction",
    "minimum_battery_reserve",
    "no_charge_window",
    "no_discharge_window",
    "max_grid_window",
    "no_op",
]

BatteryAction = Literal["charge", "discharge", "idle"]


class HourInput(BaseModel):
    hour: int = Field(..., ge=0, le=23, description="Hour of the day (0-23)")
    demand_kwh: float = Field(..., ge=0.0, description="Demand in kWh")
    solar_kwh: float = Field(..., ge=0.0, description="Solar generation in kWh")
    tariff_bdt_per_kwh: float = Field(..., ge=0.0, description="Grid tariff in BDT/kWh")

    @field_validator("demand_kwh", "solar_kwh", "tariff_bdt_per_kwh")
    @classmethod
    def validate_finite(cls, v: float) -> float:
        if not math.isfinite(v):
            raise ValueError("Numeric values must be finite")
        return v


class BatteryInput(BaseModel):
    capacity_kwh: float = Field(..., gt=0.0, description="Total battery capacity in kWh")
    initial_energy_kwh: float = Field(..., ge=0.0, description="Initial battery energy in kWh")
    minimum_energy_kwh: float = Field(..., ge=0.0, description="Minimum allowable battery energy in kWh")
    max_charge_kwh_per_hour: float = Field(..., ge=0.0, description="Max charge rate in kWh/h")
    max_discharge_kwh_per_hour: float = Field(..., ge=0.0, description="Max discharge rate in kWh/h")

    @field_validator(
        "capacity_kwh",
        "initial_energy_kwh",
        "minimum_energy_kwh",
        "max_charge_kwh_per_hour",
        "max_discharge_kwh_per_hour",
    )
    @classmethod
    def validate_finite(cls, v: float) -> float:
        if not math.isfinite(v):
            raise ValueError("Battery parameters must be finite")
        return v


class OptimizeEnergyRequest(BaseModel):
    scenario_id: str = Field(..., min_length=1, description="Unique scenario identifier")
    operator_notes: List[str] = Field(..., min_length=1, max_length=3, description="1 to 3 operator notes")
    hours: List[HourInput] = Field(..., description="24 hourly data entries")
    battery: BatteryInput = Field(..., description="Battery specifications")

    @field_validator("operator_notes")
    @classmethod
    def validate_operator_notes(cls, notes: List[str]) -> List[str]:
        if not notes:
            raise ValueError("operator_notes cannot be empty")
        for i, note in enumerate(notes):
            if not isinstance(note, str) or not note.strip():
                raise ValueError(f"operator_notes[{i}] must be a non-empty string")
        return notes

    @field_validator("hours")
    @classmethod
    def validate_hours(cls, hours: List[HourInput]) -> List[HourInput]:
        if len(hours) != 24:
            raise ValueError(f"Expected exactly 24 hourly entries, got {len(hours)}")
        hour_indices = [h.hour for h in hours]
        if len(set(hour_indices)) != 24 or set(hour_indices) != set(range(24)):
            raise ValueError("hours must contain unique entries for every hour from 0 to 23")
        # Return sorted by hour ascending
        return sorted(hours, key=lambda x: x.hour)

    @model_validator(mode="after")
    def validate_battery_sanity(self) -> "OptimizeEnergyRequest":
        b = self.battery
        if b.minimum_energy_kwh > b.initial_energy_kwh:
            raise ValueError(
                f"Battery minimum_energy_kwh ({b.minimum_energy_kwh}) cannot exceed initial_energy_kwh ({b.initial_energy_kwh})"
            )
        if b.initial_energy_kwh > b.capacity_kwh:
            raise ValueError(
                f"Battery initial_energy_kwh ({b.initial_energy_kwh}) cannot exceed capacity_kwh ({b.capacity_kwh})"
            )
        return self


# Directive structured adjustments
class SolarReductionAdjustment(BaseModel):
    hours: List[int] = Field(..., description="Affected hours (unique, ascending 0-23)")
    factor: float = Field(..., ge=0.0, le=1.0, description="Remaining usable fraction [0, 1]")


class MinimumBatteryReserveAdjustment(BaseModel):
    hours: List[int] = Field(..., description="Affected hours (unique, ascending 0-23)")
    minimum_energy_kwh: float = Field(..., ge=0.0, description="Minimum battery reserve in kWh")


class WindowHoursAdjustment(BaseModel):
    hours: List[int] = Field(..., description="Affected hours (unique, ascending 0-23)")


class MaxGridAdjustment(BaseModel):
    hours: List[int] = Field(..., description="Affected hours (unique, ascending 0-23)")
    max_grid_kwh: float = Field(..., ge=0.0, description="Maximum allowed grid intake in kWh")


StructuredAdjustment = Union[
    SolarReductionAdjustment,
    MinimumBatteryReserveAdjustment,
    WindowHoursAdjustment,
    MaxGridAdjustment,
    None,
]


class DirectiveInterpretation(BaseModel):
    note_index: int = Field(..., ge=0, description="Zero-based note index")
    applies: bool = Field(..., description="Whether the directive applies")
    directive_type: DirectiveType = Field(..., description="Directive type enum")
    structured_adjustment: Optional[StructuredAdjustment] = Field(
        default=None, description="Adjustment parameters, null for no_op"
    )
    explanation: str = Field(..., description="Brief reasoning for the interpretation")


class HourlyPlanItem(BaseModel):
    hour: int = Field(..., ge=0, le=23)
    grid_kwh: float = Field(..., ge=0.0)
    solar_used_kwh: float = Field(..., ge=0.0)
    battery_action: BatteryAction
    battery_kwh: float = Field(..., ge=0.0)
    battery_energy_after_kwh: float = Field(..., ge=0.0)


class OptimizeEnergyResponse(BaseModel):
    scenario_id: str
    directive_interpretation: List[DirectiveInterpretation]
    hourly_plan: List[HourlyPlanItem]
    total_grid_kwh: float
    total_cost_bdt: float
    peak_grid_kwh: float
    plan_summary: str


class ErrorResponse(BaseModel):
    error: str
    detail: str


# Raw internal schema expected from the LLM before normalization
class RawDirectiveItem(BaseModel):
    note_index: int
    relevant: bool
    directive_type: DirectiveType
    start_hour: Optional[int] = Field(default=None, ge=0, le=23)
    end_hour_exclusive: Optional[int] = Field(default=None, ge=0, le=24)
    value: Optional[float] = None
    value_kind: Optional[
        Literal[
            "fraction_remaining",
            "percent_remaining",
            "percent_reduction",
            "kwh",
            "percent_of_capacity",
        ]
    ] = None
    explanation: str = ""


class RawLLMOutput(BaseModel):
    directives: List[RawDirectiveItem]
