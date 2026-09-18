import json
from typing import List, Dict, Any
from src.models import (
    BatteryInput,
    DirectiveInterpretation,
    HourInput,
    MaxGridAdjustment,
    MinimumBatteryReserveAdjustment,
    SolarReductionAdjustment,
    WindowHoursAdjustment,
)
from src.optimizer import optimize_energy_schedule
from src.validator import validate_plan

# Standard diurnal profile (24h)
def generate_sample_cases():
    base_demand = [
        35.0, 30.0, 28.0, 25.0, 26.0, 32.0, 45.0, 65.0, 80.0, 95.0, 110.0, 120.0,
        125.0, 120.0, 115.0, 105.0, 95.0, 110.0, 130.0, 125.0, 100.0, 75.0, 55.0, 42.0
    ]
    base_solar = [
        0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 12.0, 35.0, 65.0, 90.0, 105.0, 115.0,
        120.0, 115.0, 95.0, 70.0, 40.0, 15.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0
    ]
    # Peak tariff 17:00 to 23:00, off-peak night
    base_tariff = [
        6.5, 6.5, 6.5, 6.5, 6.5, 6.5, 8.0, 8.0, 9.5, 9.5, 9.5, 9.5,
        9.5, 9.5, 9.5, 9.5, 10.5, 14.0, 14.0, 14.0, 14.0, 14.0, 10.5, 8.0
    ]

    cases_def = [
        # Case 1: Pure baseline, distractor note
        {
            "id": "CASE-001",
            "notes": ["Campus cafeteria serves biryani on Thursday."],
            "directives": [
                DirectiveInterpretation(
                    note_index=0,
                    applies=False,
                    directive_type="no_op",
                    structured_adjustment=None,
                    explanation="Cafeteria menu notice is irrelevant to energy operations.",
                )
            ],
            "demand_mult": 1.0,
            "solar_mult": 1.0,
            "battery": BatteryInput(
                capacity_kwh=200.0,
                initial_energy_kwh=100.0,
                minimum_energy_kwh=30.0,
                max_charge_kwh_per_hour=50.0,
                max_discharge_kwh_per_hour=50.0,
            )
        },
        # Case 2: Solar reduction (80% reduction 13:00 to 15:00)
        {
            "id": "CASE-002",
            "notes": ["Expect an 80% reduction in rooftop solar during the 1-3 PM maintenance window."],
            "directives": [
                DirectiveInterpretation(
                    note_index=0,
                    applies=True,
                    directive_type="solar_reduction",
                    structured_adjustment=SolarReductionAdjustment(hours=[13, 14], factor=0.2),
                    explanation="Solar output reduced by 80%, leaving factor of 0.2 from 1 PM to 3 PM.",
                )
            ],
            "demand_mult": 1.0,
            "solar_mult": 1.0,
            "battery": BatteryInput(
                capacity_kwh=200.0,
                initial_energy_kwh=100.0,
                minimum_energy_kwh=30.0,
                max_charge_kwh_per_hour=50.0,
                max_discharge_kwh_per_hour=50.0,
            )
        },
        # Case 3: Minimum battery reserve (50% capacity from 6 PM until 9 PM)
        {
            "id": "CASE-003",
            "notes": ["Keep at least 50% of battery capacity in reserve from 6 PM until 9 PM."],
            "directives": [
                DirectiveInterpretation(
                    note_index=0,
                    applies=True,
                    directive_type="minimum_battery_reserve",
                    structured_adjustment=MinimumBatteryReserveAdjustment(hours=[18, 19, 20], minimum_energy_kwh=100.0),
                    explanation="Battery reserve set to 50% of 200 kWh capacity (100 kWh) for hours 18-20.",
                )
            ],
            "demand_mult": 1.0,
            "solar_mult": 1.0,
            "battery": BatteryInput(
                capacity_kwh=200.0,
                initial_energy_kwh=100.0,
                minimum_energy_kwh=30.0,
                max_charge_kwh_per_hour=50.0,
                max_discharge_kwh_per_hour=50.0,
            )
        },
        # Case 4: No charge window (10 AM to 2 PM)
        {
            "id": "CASE-004",
            "notes": ["Inverter relay testing: charger isolated from 10:00 to 14:00."],
            "directives": [
                DirectiveInterpretation(
                    note_index=0,
                    applies=True,
                    directive_type="no_charge_window",
                    structured_adjustment=WindowHoursAdjustment(hours=[10, 11, 12, 13]),
                    explanation="Charger isolated prohibits charging between 10:00 and 14:00.",
                )
            ],
            "demand_mult": 0.9,
            "solar_mult": 1.1,
            "battery": BatteryInput(
                capacity_kwh=250.0,
                initial_energy_kwh=120.0,
                minimum_energy_kwh=40.0,
                max_charge_kwh_per_hour=60.0,
                max_discharge_kwh_per_hour=60.0,
            )
        },
        # Case 5: No discharge window (17:00 until 20:00)
        {
            "id": "CASE-005",
            "notes": ["Relay testing – no discharging from 5 PM till 8 PM."],
            "directives": [
                DirectiveInterpretation(
                    note_index=0,
                    applies=True,
                    directive_type="no_discharge_window",
                    structured_adjustment=WindowHoursAdjustment(hours=[17, 18, 19]),
                    explanation="No battery discharge allowed from 17:00 to 20:00.",
                )
            ],
            "demand_mult": 1.0,
            "solar_mult": 1.0,
            "battery": BatteryInput(
                capacity_kwh=200.0,
                initial_energy_kwh=100.0,
                minimum_energy_kwh=30.0,
                max_charge_kwh_per_hour=50.0,
                max_discharge_kwh_per_hour=50.0,
            )
        },
        # Case 6: Max grid window (grid cap at 60 kWh from 12 PM to 4 PM)
        {
            "id": "CASE-006",
            "notes": ["Substation transformer work: grid import must not exceed 60 kWh between 12:00 and 16:00."],
            "directives": [
                DirectiveInterpretation(
                    note_index=0,
                    applies=True,
                    directive_type="max_grid_window",
                    structured_adjustment=MaxGridAdjustment(hours=[12, 13, 14, 15], max_grid_kwh=60.0),
                    explanation="Grid intake capped at 60 kWh during transformer maintenance 12:00 to 16:00.",
                )
            ],
            "demand_mult": 1.1,
            "solar_mult": 1.2,
            "battery": BatteryInput(
                capacity_kwh=300.0,
                initial_energy_kwh=150.0,
                minimum_energy_kwh=50.0,
                max_charge_kwh_per_hour=75.0,
                max_discharge_kwh_per_hour=75.0,
            )
        },
        # Case 7: Two notes (1 valid solar reduction + 1 distractor)
        {
            "id": "CASE-007",
            "notes": [
                "PV production will drop to about 20% between 13:00 and 15:00",
                "CSE Fest registration deadline extended to midnight."
            ],
            "directives": [
                DirectiveInterpretation(
                    note_index=0,
                    applies=True,
                    directive_type="solar_reduction",
                    structured_adjustment=SolarReductionAdjustment(hours=[13, 14], factor=0.2),
                    explanation="Solar output drops to 20% (factor 0.2) between 13:00 and 15:00.",
                ),
                DirectiveInterpretation(
                    note_index=1,
                    applies=False,
                    directive_type="no_op",
                    structured_adjustment=None,
                    explanation="Registration deadline announcement is an informational notice with no operational impact.",
                )
            ],
            "demand_mult": 1.0,
            "solar_mult": 1.0,
            "battery": BatteryInput(
                capacity_kwh=200.0,
                initial_energy_kwh=100.0,
                minimum_energy_kwh=30.0,
                max_charge_kwh_per_hour=50.0,
                max_discharge_kwh_per_hour=50.0,
            )
        },
        # Case 8: Midnight wrap-around window (10 PM to 2 AM no charge)
        {
            "id": "CASE-008",
            "notes": ["Night grid maintenance: no charging allowed from 10 PM to 2 AM."],
            "directives": [
                DirectiveInterpretation(
                    note_index=0,
                    applies=True,
                    directive_type="no_charge_window",
                    structured_adjustment=WindowHoursAdjustment(hours=[0, 1, 22, 23]),
                    explanation="No charge window across midnight 10 PM (22) to 2 AM (2) sorted ascending.",
                )
            ],
            "demand_mult": 0.8,
            "solar_mult": 0.9,
            "battery": BatteryInput(
                capacity_kwh=180.0,
                initial_energy_kwh=90.0,
                minimum_energy_kwh=20.0,
                max_charge_kwh_per_hour=45.0,
                max_discharge_kwh_per_hour=45.0,
            )
        },
        # Case 9: Three notes (solar reduction, minimum reserve, distractor)
        {
            "id": "CASE-009",
            "notes": [
                "Panel washing from one until three will leave roughly one-fifth of normal solar output",
                "Robotics lab seminar at 3 PM in Auditorium 2",
                "Hold 80 kWh reserve in the battery between 18:00 and 22:00"
            ],
            "directives": [
                DirectiveInterpretation(
                    note_index=0,
                    applies=True,
                    directive_type="solar_reduction",
                    structured_adjustment=SolarReductionAdjustment(hours=[13, 14], factor=0.2),
                    explanation="One-fifth remaining translates to factor 0.2 for hours 13 and 14.",
                ),
                DirectiveInterpretation(
                    note_index=1,
                    applies=False,
                    directive_type="no_op",
                    structured_adjustment=None,
                    explanation="Seminar notice is irrelevant to energy dispatch.",
                ),
                DirectiveInterpretation(
                    note_index=2,
                    applies=True,
                    directive_type="minimum_battery_reserve",
                    structured_adjustment=MinimumBatteryReserveAdjustment(hours=[18, 19, 20, 21], minimum_energy_kwh=80.0),
                    explanation="Enforces 80 kWh minimum battery reserve from 18:00 to 22:00.",
                )
            ],
            "demand_mult": 1.0,
            "solar_mult": 1.0,
            "battery": BatteryInput(
                capacity_kwh=250.0,
                initial_energy_kwh=100.0,
                minimum_energy_kwh=30.0,
                max_charge_kwh_per_hour=50.0,
                max_discharge_kwh_per_hour=50.0,
            )
        },
        # Case 10: Words for numbers & fractions ("loses a quarter", "at or below 80 kWh")
        {
            "id": "CASE-010",
            "notes": [
                "Dust storm: solar loses a quarter of output from noon until three PM",
                "Feeder limitation: grid intake must remain at or below 80 kWh from 17:00 to 21:00"
            ],
            "directives": [
                DirectiveInterpretation(
                    note_index=0,
                    applies=True,
                    directive_type="solar_reduction",
                    structured_adjustment=SolarReductionAdjustment(hours=[12, 13, 14], factor=0.75),
                    explanation="Loses a quarter means 0.75 usable solar factor remaining from 12:00 to 15:00.",
                ),
                DirectiveInterpretation(
                    note_index=1,
                    applies=True,
                    directive_type="max_grid_window",
                    structured_adjustment=MaxGridAdjustment(hours=[17, 18, 19, 20], max_grid_kwh=80.0),
                    explanation="Grid power capped at 80 kWh from 17:00 to 21:00.",
                )
            ],
            "demand_mult": 1.0,
            "solar_mult": 1.0,
            "battery": BatteryInput(
                capacity_kwh=220.0,
                initial_energy_kwh=110.0,
                minimum_energy_kwh=35.0,
                max_charge_kwh_per_hour=55.0,
                max_discharge_kwh_per_hour=55.0,
            )
        }
    ]

    public_cases = []

    for c in cases_def:
        print(f"Solving {c['id']}...")
        hours: List[HourInput] = []
        for h in range(24):
            hours.append(
                HourInput(
                    hour=h,
                    demand_kwh=round(base_demand[h] * c["demand_mult"], 2),
                    solar_kwh=round(base_solar[h] * c["solar_mult"], 2),
                    tariff_bdt_per_kwh=round(base_tariff[h], 2),
                )
            )
        battery: BatteryInput = c["battery"]
        directives: List[DirectiveInterpretation] = c["directives"]

        hourly_plan, total_grid, total_cost, peak_grid = optimize_energy_schedule(
            hours, battery, directives
        )
        validate_plan(hours, battery, directives, hourly_plan, total_grid, total_cost, peak_grid)

        # Build output structure
        input_data = {
            "scenario_id": c["id"],
            "operator_notes": c["notes"],
            "hours": [h.model_dump() for h in hours],
            "battery": battery.model_dump(),
        }

        directive_out = []
        for d in directives:
            d_dict = {
                "note_index": d.note_index,
                "applies": d.applies,
                "directive_type": d.directive_type,
                "structured_adjustment": d.structured_adjustment.model_dump() if d.structured_adjustment else None,
                "explanation": d.explanation,
            }
            directive_out.append(d_dict)

        plan_out = [p.model_dump() for p in hourly_plan]

        expected_output = {
            "scenario_id": c["id"],
            "directive_interpretation": directive_out,
            "hourly_plan": plan_out,
            "total_grid_kwh": total_grid,
            "total_cost_bdt": total_cost,
            "peak_grid_kwh": peak_grid,
            "plan_summary": f"Optimized 24h schedule for {c['id']}: total grid {total_grid:.2f} kWh, cost {total_cost:.2f} BDT, peak {peak_grid:.2f} kWh."
        }

        public_cases.append({
            "scenario_id": c["id"],
            "input": input_data,
            "expected_output": expected_output,
        })

    with open("samples/BUP_CSE_FEST_2026_Preli_Public_Sample_Cases.json", "w") as f:
        json.dump(public_cases, f, indent=2)

    print(f"Generated {len(public_cases)} verified public sample cases in samples/BUP_CSE_FEST_2026_Preli_Public_Sample_Cases.json")

if __name__ == "__main__":
    generate_sample_cases()
