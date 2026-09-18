// Generated sample scenarios
export const SAMPLE_SCENARIOS = [
  {
    "scenario_id": "CASE-001",
    "input": {
      "scenario_id": "CASE-001",
      "operator_notes": [
        "Campus cafeteria serves biryani on Thursday."
      ],
      "hours": [
        {
          "hour": 0,
          "demand_kwh": 35.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 1,
          "demand_kwh": 30.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 2,
          "demand_kwh": 28.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 3,
          "demand_kwh": 25.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 4,
          "demand_kwh": 26.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 5,
          "demand_kwh": 32.0,
          "solar_kwh": 2.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 6,
          "demand_kwh": 45.0,
          "solar_kwh": 12.0,
          "tariff_bdt_per_kwh": 8.0
        },
        {
          "hour": 7,
          "demand_kwh": 65.0,
          "solar_kwh": 35.0,
          "tariff_bdt_per_kwh": 8.0
        },
        {
          "hour": 8,
          "demand_kwh": 80.0,
          "solar_kwh": 65.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 9,
          "demand_kwh": 95.0,
          "solar_kwh": 90.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 10,
          "demand_kwh": 110.0,
          "solar_kwh": 105.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 11,
          "demand_kwh": 120.0,
          "solar_kwh": 115.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 12,
          "demand_kwh": 125.0,
          "solar_kwh": 120.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 13,
          "demand_kwh": 120.0,
          "solar_kwh": 115.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 14,
          "demand_kwh": 115.0,
          "solar_kwh": 95.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 15,
          "demand_kwh": 105.0,
          "solar_kwh": 70.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 16,
          "demand_kwh": 95.0,
          "solar_kwh": 40.0,
          "tariff_bdt_per_kwh": 10.5
        },
        {
          "hour": 17,
          "demand_kwh": 110.0,
          "solar_kwh": 15.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 18,
          "demand_kwh": 130.0,
          "solar_kwh": 2.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 19,
          "demand_kwh": 125.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 20,
          "demand_kwh": 100.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 21,
          "demand_kwh": 75.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 22,
          "demand_kwh": 55.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 10.5
        },
        {
          "hour": 23,
          "demand_kwh": 42.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 8.0
        }
      ],
      "battery": {
        "capacity_kwh": 200.0,
        "initial_energy_kwh": 100.0,
        "minimum_energy_kwh": 30.0,
        "max_charge_kwh_per_hour": 50.0,
        "max_discharge_kwh_per_hour": 50.0
      }
    },
    "expected_output": {
      "scenario_id": "CASE-001",
      "directive_interpretation": [
        {
          "note_index": 0,
          "applies": false,
          "directive_type": "no_op",
          "structured_adjustment": null,
          "explanation": "Cafeteria menu notice is irrelevant to energy operations."
        }
      ],
      "hourly_plan": [
        {
          "hour": 0,
          "grid_kwh": 85.0,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 150.0
        },
        {
          "hour": 1,
          "grid_kwh": 30.0,
          "solar_used_kwh": 0.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 150.0
        },
        {
          "hour": 2,
          "grid_kwh": 78.0,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 3,
          "grid_kwh": 25.0,
          "solar_used_kwh": 0.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 4,
          "grid_kwh": 26.0,
          "solar_used_kwh": 0.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 5,
          "grid_kwh": 30.0,
          "solar_used_kwh": 2.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 6,
          "grid_kwh": 0.0,
          "solar_used_kwh": 12.0,
          "battery_action": "discharge",
          "battery_kwh": 33.0,
          "battery_energy_after_kwh": 167.0
        },
        {
          "hour": 7,
          "grid_kwh": 63.0,
          "solar_used_kwh": 35.0,
          "battery_action": "charge",
          "battery_kwh": 33.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 8,
          "grid_kwh": 0.0,
          "solar_used_kwh": 65.0,
          "battery_action": "discharge",
          "battery_kwh": 15.0,
          "battery_energy_after_kwh": 185.0
        },
        {
          "hour": 9,
          "grid_kwh": 0.0,
          "solar_used_kwh": 90.0,
          "battery_action": "discharge",
          "battery_kwh": 5.0,
          "battery_energy_after_kwh": 180.0
        },
        {
          "hour": 10,
          "grid_kwh": 0.0,
          "solar_used_kwh": 105.0,
          "battery_action": "discharge",
          "battery_kwh": 5.0,
          "battery_energy_after_kwh": 175.0
        },
        {
          "hour": 11,
          "grid_kwh": 0.0,
          "solar_used_kwh": 115.0,
          "battery_action": "discharge",
          "battery_kwh": 5.0,
          "battery_energy_after_kwh": 170.0
        },
        {
          "hour": 12,
          "grid_kwh": 0.0,
          "solar_used_kwh": 120.0,
          "battery_action": "discharge",
          "battery_kwh": 5.0,
          "battery_energy_after_kwh": 165.0
        },
        {
          "hour": 13,
          "grid_kwh": 40.0,
          "solar_used_kwh": 115.0,
          "battery_action": "charge",
          "battery_kwh": 35.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 14,
          "grid_kwh": 0.0,
          "solar_used_kwh": 95.0,
          "battery_action": "discharge",
          "battery_kwh": 20.0,
          "battery_energy_after_kwh": 180.0
        },
        {
          "hour": 15,
          "grid_kwh": 55.0,
          "solar_used_kwh": 70.0,
          "battery_action": "charge",
          "battery_kwh": 20.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 16,
          "grid_kwh": 55.0,
          "solar_used_kwh": 40.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 17,
          "grid_kwh": 45.0,
          "solar_used_kwh": 15.0,
          "battery_action": "discharge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 150.0
        },
        {
          "hour": 18,
          "grid_kwh": 78.0,
          "solar_used_kwh": 2.0,
          "battery_action": "discharge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 100.0
        },
        {
          "hour": 19,
          "grid_kwh": 75.0,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 50.0
        },
        {
          "hour": 20,
          "grid_kwh": 80.0,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 20.0,
          "battery_energy_after_kwh": 30.0
        },
        {
          "hour": 21,
          "grid_kwh": 75.0,
          "solar_used_kwh": 0.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 30.0
        },
        {
          "hour": 22,
          "grid_kwh": 75.0,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 20.0,
          "battery_energy_after_kwh": 50.0
        },
        {
          "hour": 23,
          "grid_kwh": 92.0,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 100.0
        }
      ],
      "total_grid_kwh": 1007.0,
      "total_cost_bdt": 10230.5,
      "peak_grid_kwh": 92.0,
      "plan_summary": "Optimized 24h schedule for CASE-001: total grid 1007.00 kWh, cost 10230.50 BDT, peak 92.00 kWh."
    }
  },
  {
    "scenario_id": "CASE-002",
    "input": {
      "scenario_id": "CASE-002",
      "operator_notes": [
        "Expect an 80% reduction in rooftop solar during the 1-3 PM maintenance window."
      ],
      "hours": [
        {
          "hour": 0,
          "demand_kwh": 35.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 1,
          "demand_kwh": 30.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 2,
          "demand_kwh": 28.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 3,
          "demand_kwh": 25.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 4,
          "demand_kwh": 26.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 5,
          "demand_kwh": 32.0,
          "solar_kwh": 2.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 6,
          "demand_kwh": 45.0,
          "solar_kwh": 12.0,
          "tariff_bdt_per_kwh": 8.0
        },
        {
          "hour": 7,
          "demand_kwh": 65.0,
          "solar_kwh": 35.0,
          "tariff_bdt_per_kwh": 8.0
        },
        {
          "hour": 8,
          "demand_kwh": 80.0,
          "solar_kwh": 65.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 9,
          "demand_kwh": 95.0,
          "solar_kwh": 90.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 10,
          "demand_kwh": 110.0,
          "solar_kwh": 105.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 11,
          "demand_kwh": 120.0,
          "solar_kwh": 115.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 12,
          "demand_kwh": 125.0,
          "solar_kwh": 120.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 13,
          "demand_kwh": 120.0,
          "solar_kwh": 115.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 14,
          "demand_kwh": 115.0,
          "solar_kwh": 95.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 15,
          "demand_kwh": 105.0,
          "solar_kwh": 70.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 16,
          "demand_kwh": 95.0,
          "solar_kwh": 40.0,
          "tariff_bdt_per_kwh": 10.5
        },
        {
          "hour": 17,
          "demand_kwh": 110.0,
          "solar_kwh": 15.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 18,
          "demand_kwh": 130.0,
          "solar_kwh": 2.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 19,
          "demand_kwh": 125.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 20,
          "demand_kwh": 100.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 21,
          "demand_kwh": 75.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 22,
          "demand_kwh": 55.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 10.5
        },
        {
          "hour": 23,
          "demand_kwh": 42.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 8.0
        }
      ],
      "battery": {
        "capacity_kwh": 200.0,
        "initial_energy_kwh": 100.0,
        "minimum_energy_kwh": 30.0,
        "max_charge_kwh_per_hour": 50.0,
        "max_discharge_kwh_per_hour": 50.0
      }
    },
    "expected_output": {
      "scenario_id": "CASE-002",
      "directive_interpretation": [
        {
          "note_index": 0,
          "applies": true,
          "directive_type": "solar_reduction",
          "structured_adjustment": {
            "hours": [
              13,
              14
            ],
            "factor": 0.2
          },
          "explanation": "Solar output reduced by 80%, leaving factor of 0.2 from 1 PM to 3 PM."
        }
      ],
      "hourly_plan": [
        {
          "hour": 0,
          "grid_kwh": 85.0,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 150.0
        },
        {
          "hour": 1,
          "grid_kwh": 30.0,
          "solar_used_kwh": 0.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 150.0
        },
        {
          "hour": 2,
          "grid_kwh": 78.0,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 3,
          "grid_kwh": 1.0,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 24.0,
          "battery_energy_after_kwh": 176.0
        },
        {
          "hour": 4,
          "grid_kwh": 0.0,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 26.0,
          "battery_energy_after_kwh": 150.0
        },
        {
          "hour": 5,
          "grid_kwh": 80.0,
          "solar_used_kwh": 2.0,
          "battery_action": "charge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 6,
          "grid_kwh": 33.0,
          "solar_used_kwh": 12.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 7,
          "grid_kwh": 30.0,
          "solar_used_kwh": 35.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 8,
          "grid_kwh": 0.0,
          "solar_used_kwh": 65.0,
          "battery_action": "discharge",
          "battery_kwh": 15.0,
          "battery_energy_after_kwh": 185.0
        },
        {
          "hour": 9,
          "grid_kwh": 0.0,
          "solar_used_kwh": 90.0,
          "battery_action": "discharge",
          "battery_kwh": 5.0,
          "battery_energy_after_kwh": 180.0
        },
        {
          "hour": 10,
          "grid_kwh": 0.0,
          "solar_used_kwh": 105.0,
          "battery_action": "discharge",
          "battery_kwh": 5.0,
          "battery_energy_after_kwh": 175.0
        },
        {
          "hour": 11,
          "grid_kwh": 0.0,
          "solar_used_kwh": 115.0,
          "battery_action": "discharge",
          "battery_kwh": 5.0,
          "battery_energy_after_kwh": 170.0
        },
        {
          "hour": 12,
          "grid_kwh": 35.0,
          "solar_used_kwh": 120.0,
          "battery_action": "charge",
          "battery_kwh": 30.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 13,
          "grid_kwh": 47.0,
          "solar_used_kwh": 23.0,
          "battery_action": "discharge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 150.0
        },
        {
          "hour": 14,
          "grid_kwh": 146.0,
          "solar_used_kwh": 19.0,
          "battery_action": "charge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 15,
          "grid_kwh": 35.0,
          "solar_used_kwh": 70.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 16,
          "grid_kwh": 55.0,
          "solar_used_kwh": 40.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 17,
          "grid_kwh": 45.0,
          "solar_used_kwh": 15.0,
          "battery_action": "discharge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 150.0
        },
        {
          "hour": 18,
          "grid_kwh": 108.0,
          "solar_used_kwh": 2.0,
          "battery_action": "discharge",
          "battery_kwh": 20.0,
          "battery_energy_after_kwh": 130.0
        },
        {
          "hour": 19,
          "grid_kwh": 75.0,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 80.0
        },
        {
          "hour": 20,
          "grid_kwh": 50.0,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 30.0
        },
        {
          "hour": 21,
          "grid_kwh": 75.0,
          "solar_used_kwh": 0.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 30.0
        },
        {
          "hour": 22,
          "grid_kwh": 75.0,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 20.0,
          "battery_energy_after_kwh": 50.0
        },
        {
          "hour": 23,
          "grid_kwh": 92.0,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 100.0
        }
      ],
      "total_grid_kwh": 1175.0,
      "total_cost_bdt": 11826.5,
      "peak_grid_kwh": 146.0,
      "plan_summary": "Optimized 24h schedule for CASE-002: total grid 1175.00 kWh, cost 11826.50 BDT, peak 146.00 kWh."
    }
  },
  {
    "scenario_id": "CASE-003",
    "input": {
      "scenario_id": "CASE-003",
      "operator_notes": [
        "Keep at least 50% of battery capacity in reserve from 6 PM until 9 PM."
      ],
      "hours": [
        {
          "hour": 0,
          "demand_kwh": 35.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 1,
          "demand_kwh": 30.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 2,
          "demand_kwh": 28.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 3,
          "demand_kwh": 25.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 4,
          "demand_kwh": 26.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 5,
          "demand_kwh": 32.0,
          "solar_kwh": 2.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 6,
          "demand_kwh": 45.0,
          "solar_kwh": 12.0,
          "tariff_bdt_per_kwh": 8.0
        },
        {
          "hour": 7,
          "demand_kwh": 65.0,
          "solar_kwh": 35.0,
          "tariff_bdt_per_kwh": 8.0
        },
        {
          "hour": 8,
          "demand_kwh": 80.0,
          "solar_kwh": 65.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 9,
          "demand_kwh": 95.0,
          "solar_kwh": 90.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 10,
          "demand_kwh": 110.0,
          "solar_kwh": 105.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 11,
          "demand_kwh": 120.0,
          "solar_kwh": 115.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 12,
          "demand_kwh": 125.0,
          "solar_kwh": 120.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 13,
          "demand_kwh": 120.0,
          "solar_kwh": 115.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 14,
          "demand_kwh": 115.0,
          "solar_kwh": 95.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 15,
          "demand_kwh": 105.0,
          "solar_kwh": 70.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 16,
          "demand_kwh": 95.0,
          "solar_kwh": 40.0,
          "tariff_bdt_per_kwh": 10.5
        },
        {
          "hour": 17,
          "demand_kwh": 110.0,
          "solar_kwh": 15.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 18,
          "demand_kwh": 130.0,
          "solar_kwh": 2.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 19,
          "demand_kwh": 125.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 20,
          "demand_kwh": 100.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 21,
          "demand_kwh": 75.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 22,
          "demand_kwh": 55.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 10.5
        },
        {
          "hour": 23,
          "demand_kwh": 42.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 8.0
        }
      ],
      "battery": {
        "capacity_kwh": 200.0,
        "initial_energy_kwh": 100.0,
        "minimum_energy_kwh": 30.0,
        "max_charge_kwh_per_hour": 50.0,
        "max_discharge_kwh_per_hour": 50.0
      }
    },
    "expected_output": {
      "scenario_id": "CASE-003",
      "directive_interpretation": [
        {
          "note_index": 0,
          "applies": true,
          "directive_type": "minimum_battery_reserve",
          "structured_adjustment": {
            "hours": [
              18,
              19,
              20
            ],
            "minimum_energy_kwh": 100.0
          },
          "explanation": "Battery reserve set to 50% of 200 kWh capacity (100 kWh) for hours 18-20."
        }
      ],
      "hourly_plan": [
        {
          "hour": 0,
          "grid_kwh": 85.0,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 150.0
        },
        {
          "hour": 1,
          "grid_kwh": 30.0,
          "solar_used_kwh": 0.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 150.0
        },
        {
          "hour": 2,
          "grid_kwh": 78.0,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 3,
          "grid_kwh": 25.0,
          "solar_used_kwh": 0.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 4,
          "grid_kwh": 26.0,
          "solar_used_kwh": 0.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 5,
          "grid_kwh": 30.0,
          "solar_used_kwh": 2.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 6,
          "grid_kwh": 33.0,
          "solar_used_kwh": 12.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 7,
          "grid_kwh": 30.0,
          "solar_used_kwh": 35.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 8,
          "grid_kwh": 0.0,
          "solar_used_kwh": 65.0,
          "battery_action": "discharge",
          "battery_kwh": 15.0,
          "battery_energy_after_kwh": 185.0
        },
        {
          "hour": 9,
          "grid_kwh": 0.0,
          "solar_used_kwh": 90.0,
          "battery_action": "discharge",
          "battery_kwh": 5.0,
          "battery_energy_after_kwh": 180.0
        },
        {
          "hour": 10,
          "grid_kwh": 0.0,
          "solar_used_kwh": 105.0,
          "battery_action": "discharge",
          "battery_kwh": 5.0,
          "battery_energy_after_kwh": 175.0
        },
        {
          "hour": 11,
          "grid_kwh": 0.0,
          "solar_used_kwh": 115.0,
          "battery_action": "discharge",
          "battery_kwh": 5.0,
          "battery_energy_after_kwh": 170.0
        },
        {
          "hour": 12,
          "grid_kwh": 35.0,
          "solar_used_kwh": 120.0,
          "battery_action": "charge",
          "battery_kwh": 30.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 13,
          "grid_kwh": 0.0,
          "solar_used_kwh": 115.0,
          "battery_action": "discharge",
          "battery_kwh": 5.0,
          "battery_energy_after_kwh": 195.0
        },
        {
          "hour": 14,
          "grid_kwh": 0.0,
          "solar_used_kwh": 95.0,
          "battery_action": "discharge",
          "battery_kwh": 20.0,
          "battery_energy_after_kwh": 175.0
        },
        {
          "hour": 15,
          "grid_kwh": 60.0,
          "solar_used_kwh": 70.0,
          "battery_action": "charge",
          "battery_kwh": 25.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 16,
          "grid_kwh": 55.0,
          "solar_used_kwh": 40.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 17,
          "grid_kwh": 45.0,
          "solar_used_kwh": 15.0,
          "battery_action": "discharge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 150.0
        },
        {
          "hour": 18,
          "grid_kwh": 178.0,
          "solar_used_kwh": 2.0,
          "battery_action": "charge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 19,
          "grid_kwh": 75.0,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 150.0
        },
        {
          "hour": 20,
          "grid_kwh": 50.0,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 100.0
        },
        {
          "hour": 21,
          "grid_kwh": 25.0,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 50.0
        },
        {
          "hour": 22,
          "grid_kwh": 55.0,
          "solar_used_kwh": 0.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 50.0
        },
        {
          "hour": 23,
          "grid_kwh": 92.0,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 100.0
        }
      ],
      "total_grid_kwh": 1007.0,
      "total_cost_bdt": 10300.5,
      "peak_grid_kwh": 178.0,
      "plan_summary": "Optimized 24h schedule for CASE-003: total grid 1007.00 kWh, cost 10300.50 BDT, peak 178.00 kWh."
    }
  },
  {
    "scenario_id": "CASE-004",
    "input": {
      "scenario_id": "CASE-004",
      "operator_notes": [
        "Inverter relay testing: charger isolated from 10:00 to 14:00."
      ],
      "hours": [
        {
          "hour": 0,
          "demand_kwh": 31.5,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 1,
          "demand_kwh": 27.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 2,
          "demand_kwh": 25.2,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 3,
          "demand_kwh": 22.5,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 4,
          "demand_kwh": 23.4,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 5,
          "demand_kwh": 28.8,
          "solar_kwh": 2.2,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 6,
          "demand_kwh": 40.5,
          "solar_kwh": 13.2,
          "tariff_bdt_per_kwh": 8.0
        },
        {
          "hour": 7,
          "demand_kwh": 58.5,
          "solar_kwh": 38.5,
          "tariff_bdt_per_kwh": 8.0
        },
        {
          "hour": 8,
          "demand_kwh": 72.0,
          "solar_kwh": 71.5,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 9,
          "demand_kwh": 85.5,
          "solar_kwh": 99.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 10,
          "demand_kwh": 99.0,
          "solar_kwh": 115.5,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 11,
          "demand_kwh": 108.0,
          "solar_kwh": 126.5,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 12,
          "demand_kwh": 112.5,
          "solar_kwh": 132.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 13,
          "demand_kwh": 108.0,
          "solar_kwh": 126.5,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 14,
          "demand_kwh": 103.5,
          "solar_kwh": 104.5,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 15,
          "demand_kwh": 94.5,
          "solar_kwh": 77.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 16,
          "demand_kwh": 85.5,
          "solar_kwh": 44.0,
          "tariff_bdt_per_kwh": 10.5
        },
        {
          "hour": 17,
          "demand_kwh": 99.0,
          "solar_kwh": 16.5,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 18,
          "demand_kwh": 117.0,
          "solar_kwh": 2.2,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 19,
          "demand_kwh": 112.5,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 20,
          "demand_kwh": 90.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 21,
          "demand_kwh": 67.5,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 22,
          "demand_kwh": 49.5,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 10.5
        },
        {
          "hour": 23,
          "demand_kwh": 37.8,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 8.0
        }
      ],
      "battery": {
        "capacity_kwh": 250.0,
        "initial_energy_kwh": 120.0,
        "minimum_energy_kwh": 40.0,
        "max_charge_kwh_per_hour": 60.0,
        "max_discharge_kwh_per_hour": 60.0
      }
    },
    "expected_output": {
      "scenario_id": "CASE-004",
      "directive_interpretation": [
        {
          "note_index": 0,
          "applies": true,
          "directive_type": "no_charge_window",
          "structured_adjustment": {
            "hours": [
              10,
              11,
              12,
              13
            ]
          },
          "explanation": "Charger isolated prohibits charging between 10:00 and 14:00."
        }
      ],
      "hourly_plan": [
        {
          "hour": 0,
          "grid_kwh": 91.5,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 60.0,
          "battery_energy_after_kwh": 180.0
        },
        {
          "hour": 1,
          "grid_kwh": 37.0,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 10.0,
          "battery_energy_after_kwh": 190.0
        },
        {
          "hour": 2,
          "grid_kwh": 85.2,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 60.0,
          "battery_energy_after_kwh": 250.0
        },
        {
          "hour": 3,
          "grid_kwh": 22.5,
          "solar_used_kwh": 0.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 250.0
        },
        {
          "hour": 4,
          "grid_kwh": 23.4,
          "solar_used_kwh": 0.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 250.0
        },
        {
          "hour": 5,
          "grid_kwh": 26.6,
          "solar_used_kwh": 2.2,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 250.0
        },
        {
          "hour": 6,
          "grid_kwh": 0.0,
          "solar_used_kwh": 13.2,
          "battery_action": "discharge",
          "battery_kwh": 27.3,
          "battery_energy_after_kwh": 222.7
        },
        {
          "hour": 7,
          "grid_kwh": 33.3,
          "solar_used_kwh": 38.5,
          "battery_action": "charge",
          "battery_kwh": 13.3,
          "battery_energy_after_kwh": 236.0
        },
        {
          "hour": 8,
          "grid_kwh": 0.0,
          "solar_used_kwh": 71.5,
          "battery_action": "discharge",
          "battery_kwh": 0.5,
          "battery_energy_after_kwh": 235.5
        },
        {
          "hour": 9,
          "grid_kwh": 0.0,
          "solar_used_kwh": 99.0,
          "battery_action": "charge",
          "battery_kwh": 13.5,
          "battery_energy_after_kwh": 249.0
        },
        {
          "hour": 10,
          "grid_kwh": 0.0,
          "solar_used_kwh": 99.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 249.0
        },
        {
          "hour": 11,
          "grid_kwh": 0.0,
          "solar_used_kwh": 108.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 249.0
        },
        {
          "hour": 12,
          "grid_kwh": 0.0,
          "solar_used_kwh": 112.5,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 249.0
        },
        {
          "hour": 13,
          "grid_kwh": 0.0,
          "solar_used_kwh": 108.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 249.0
        },
        {
          "hour": 14,
          "grid_kwh": 0.0,
          "solar_used_kwh": 104.5,
          "battery_action": "charge",
          "battery_kwh": 1.0,
          "battery_energy_after_kwh": 250.0
        },
        {
          "hour": 15,
          "grid_kwh": 17.5,
          "solar_used_kwh": 77.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 250.0
        },
        {
          "hour": 16,
          "grid_kwh": 41.5,
          "solar_used_kwh": 44.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 250.0
        },
        {
          "hour": 17,
          "grid_kwh": 22.5,
          "solar_used_kwh": 16.5,
          "battery_action": "discharge",
          "battery_kwh": 60.0,
          "battery_energy_after_kwh": 190.0
        },
        {
          "hour": 18,
          "grid_kwh": 84.8,
          "solar_used_kwh": 2.2,
          "battery_action": "discharge",
          "battery_kwh": 30.0,
          "battery_energy_after_kwh": 160.0
        },
        {
          "hour": 19,
          "grid_kwh": 52.5,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 60.0,
          "battery_energy_after_kwh": 100.0
        },
        {
          "hour": 20,
          "grid_kwh": 30.0,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 60.0,
          "battery_energy_after_kwh": 40.0
        },
        {
          "hour": 21,
          "grid_kwh": 67.5,
          "solar_used_kwh": 0.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 40.0
        },
        {
          "hour": 22,
          "grid_kwh": 69.5,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 20.0,
          "battery_energy_after_kwh": 60.0
        },
        {
          "hour": 23,
          "grid_kwh": 97.8,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 60.0,
          "battery_energy_after_kwh": 120.0
        }
      ],
      "total_grid_kwh": 803.1,
      "total_cost_bdt": 7843.05,
      "peak_grid_kwh": 97.8,
      "plan_summary": "Optimized 24h schedule for CASE-004: total grid 803.10 kWh, cost 7843.05 BDT, peak 97.80 kWh."
    }
  },
  {
    "scenario_id": "CASE-005",
    "input": {
      "scenario_id": "CASE-005",
      "operator_notes": [
        "Relay testing \u2013 no discharging from 5 PM till 8 PM."
      ],
      "hours": [
        {
          "hour": 0,
          "demand_kwh": 35.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 1,
          "demand_kwh": 30.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 2,
          "demand_kwh": 28.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 3,
          "demand_kwh": 25.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 4,
          "demand_kwh": 26.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 5,
          "demand_kwh": 32.0,
          "solar_kwh": 2.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 6,
          "demand_kwh": 45.0,
          "solar_kwh": 12.0,
          "tariff_bdt_per_kwh": 8.0
        },
        {
          "hour": 7,
          "demand_kwh": 65.0,
          "solar_kwh": 35.0,
          "tariff_bdt_per_kwh": 8.0
        },
        {
          "hour": 8,
          "demand_kwh": 80.0,
          "solar_kwh": 65.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 9,
          "demand_kwh": 95.0,
          "solar_kwh": 90.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 10,
          "demand_kwh": 110.0,
          "solar_kwh": 105.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 11,
          "demand_kwh": 120.0,
          "solar_kwh": 115.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 12,
          "demand_kwh": 125.0,
          "solar_kwh": 120.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 13,
          "demand_kwh": 120.0,
          "solar_kwh": 115.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 14,
          "demand_kwh": 115.0,
          "solar_kwh": 95.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 15,
          "demand_kwh": 105.0,
          "solar_kwh": 70.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 16,
          "demand_kwh": 95.0,
          "solar_kwh": 40.0,
          "tariff_bdt_per_kwh": 10.5
        },
        {
          "hour": 17,
          "demand_kwh": 110.0,
          "solar_kwh": 15.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 18,
          "demand_kwh": 130.0,
          "solar_kwh": 2.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 19,
          "demand_kwh": 125.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 20,
          "demand_kwh": 100.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 21,
          "demand_kwh": 75.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 22,
          "demand_kwh": 55.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 10.5
        },
        {
          "hour": 23,
          "demand_kwh": 42.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 8.0
        }
      ],
      "battery": {
        "capacity_kwh": 200.0,
        "initial_energy_kwh": 100.0,
        "minimum_energy_kwh": 30.0,
        "max_charge_kwh_per_hour": 50.0,
        "max_discharge_kwh_per_hour": 50.0
      }
    },
    "expected_output": {
      "scenario_id": "CASE-005",
      "directive_interpretation": [
        {
          "note_index": 0,
          "applies": true,
          "directive_type": "no_discharge_window",
          "structured_adjustment": {
            "hours": [
              17,
              18,
              19
            ]
          },
          "explanation": "No battery discharge allowed from 17:00 to 20:00."
        }
      ],
      "hourly_plan": [
        {
          "hour": 0,
          "grid_kwh": 85.0,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 150.0
        },
        {
          "hour": 1,
          "grid_kwh": 30.0,
          "solar_used_kwh": 0.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 150.0
        },
        {
          "hour": 2,
          "grid_kwh": 78.0,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 3,
          "grid_kwh": 1.0,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 24.0,
          "battery_energy_after_kwh": 176.0
        },
        {
          "hour": 4,
          "grid_kwh": 0.0,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 26.0,
          "battery_energy_after_kwh": 150.0
        },
        {
          "hour": 5,
          "grid_kwh": 80.0,
          "solar_used_kwh": 2.0,
          "battery_action": "charge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 6,
          "grid_kwh": 33.0,
          "solar_used_kwh": 12.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 7,
          "grid_kwh": 30.0,
          "solar_used_kwh": 35.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 8,
          "grid_kwh": 0.0,
          "solar_used_kwh": 65.0,
          "battery_action": "discharge",
          "battery_kwh": 15.0,
          "battery_energy_after_kwh": 185.0
        },
        {
          "hour": 9,
          "grid_kwh": 0.0,
          "solar_used_kwh": 90.0,
          "battery_action": "discharge",
          "battery_kwh": 5.0,
          "battery_energy_after_kwh": 180.0
        },
        {
          "hour": 10,
          "grid_kwh": 0.0,
          "solar_used_kwh": 105.0,
          "battery_action": "discharge",
          "battery_kwh": 5.0,
          "battery_energy_after_kwh": 175.0
        },
        {
          "hour": 11,
          "grid_kwh": 0.0,
          "solar_used_kwh": 115.0,
          "battery_action": "discharge",
          "battery_kwh": 5.0,
          "battery_energy_after_kwh": 170.0
        },
        {
          "hour": 12,
          "grid_kwh": 10.0,
          "solar_used_kwh": 120.0,
          "battery_action": "charge",
          "battery_kwh": 5.0,
          "battery_energy_after_kwh": 175.0
        },
        {
          "hour": 13,
          "grid_kwh": 0.0,
          "solar_used_kwh": 115.0,
          "battery_action": "discharge",
          "battery_kwh": 5.0,
          "battery_energy_after_kwh": 170.0
        },
        {
          "hour": 14,
          "grid_kwh": 0.0,
          "solar_used_kwh": 95.0,
          "battery_action": "discharge",
          "battery_kwh": 20.0,
          "battery_energy_after_kwh": 150.0
        },
        {
          "hour": 15,
          "grid_kwh": 85.0,
          "solar_used_kwh": 70.0,
          "battery_action": "charge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 16,
          "grid_kwh": 5.0,
          "solar_used_kwh": 40.0,
          "battery_action": "discharge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 150.0
        },
        {
          "hour": 17,
          "grid_kwh": 95.0,
          "solar_used_kwh": 15.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 150.0
        },
        {
          "hour": 18,
          "grid_kwh": 128.0,
          "solar_used_kwh": 2.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 150.0
        },
        {
          "hour": 19,
          "grid_kwh": 125.0,
          "solar_used_kwh": 0.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 150.0
        },
        {
          "hour": 20,
          "grid_kwh": 50.0,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 100.0
        },
        {
          "hour": 21,
          "grid_kwh": 25.0,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 50.0
        },
        {
          "hour": 22,
          "grid_kwh": 55.0,
          "solar_used_kwh": 0.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 50.0
        },
        {
          "hour": 23,
          "grid_kwh": 92.0,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 100.0
        }
      ],
      "total_grid_kwh": 1007.0,
      "total_cost_bdt": 10475.5,
      "peak_grid_kwh": 128.0,
      "plan_summary": "Optimized 24h schedule for CASE-005: total grid 1007.00 kWh, cost 10475.50 BDT, peak 128.00 kWh."
    }
  },
  {
    "scenario_id": "CASE-006",
    "input": {
      "scenario_id": "CASE-006",
      "operator_notes": [
        "Substation transformer work: grid import must not exceed 60 kWh between 12:00 and 16:00."
      ],
      "hours": [
        {
          "hour": 0,
          "demand_kwh": 38.5,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 1,
          "demand_kwh": 33.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 2,
          "demand_kwh": 30.8,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 3,
          "demand_kwh": 27.5,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 4,
          "demand_kwh": 28.6,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 5,
          "demand_kwh": 35.2,
          "solar_kwh": 2.4,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 6,
          "demand_kwh": 49.5,
          "solar_kwh": 14.4,
          "tariff_bdt_per_kwh": 8.0
        },
        {
          "hour": 7,
          "demand_kwh": 71.5,
          "solar_kwh": 42.0,
          "tariff_bdt_per_kwh": 8.0
        },
        {
          "hour": 8,
          "demand_kwh": 88.0,
          "solar_kwh": 78.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 9,
          "demand_kwh": 104.5,
          "solar_kwh": 108.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 10,
          "demand_kwh": 121.0,
          "solar_kwh": 126.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 11,
          "demand_kwh": 132.0,
          "solar_kwh": 138.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 12,
          "demand_kwh": 137.5,
          "solar_kwh": 144.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 13,
          "demand_kwh": 132.0,
          "solar_kwh": 138.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 14,
          "demand_kwh": 126.5,
          "solar_kwh": 114.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 15,
          "demand_kwh": 115.5,
          "solar_kwh": 84.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 16,
          "demand_kwh": 104.5,
          "solar_kwh": 48.0,
          "tariff_bdt_per_kwh": 10.5
        },
        {
          "hour": 17,
          "demand_kwh": 121.0,
          "solar_kwh": 18.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 18,
          "demand_kwh": 143.0,
          "solar_kwh": 2.4,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 19,
          "demand_kwh": 137.5,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 20,
          "demand_kwh": 110.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 21,
          "demand_kwh": 82.5,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 22,
          "demand_kwh": 60.5,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 10.5
        },
        {
          "hour": 23,
          "demand_kwh": 46.2,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 8.0
        }
      ],
      "battery": {
        "capacity_kwh": 300.0,
        "initial_energy_kwh": 150.0,
        "minimum_energy_kwh": 50.0,
        "max_charge_kwh_per_hour": 75.0,
        "max_discharge_kwh_per_hour": 75.0
      }
    },
    "expected_output": {
      "scenario_id": "CASE-006",
      "directive_interpretation": [
        {
          "note_index": 0,
          "applies": true,
          "directive_type": "max_grid_window",
          "structured_adjustment": {
            "hours": [
              12,
              13,
              14,
              15
            ],
            "max_grid_kwh": 60.0
          },
          "explanation": "Grid intake capped at 60 kWh during transformer maintenance 12:00 to 16:00."
        }
      ],
      "hourly_plan": [
        {
          "hour": 0,
          "grid_kwh": 113.5,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 75.0,
          "battery_energy_after_kwh": 225.0
        },
        {
          "hour": 1,
          "grid_kwh": 14.1,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 18.9,
          "battery_energy_after_kwh": 206.1
        },
        {
          "hour": 2,
          "grid_kwh": 105.8,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 75.0,
          "battery_energy_after_kwh": 281.1
        },
        {
          "hour": 3,
          "grid_kwh": 0.0,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 27.5,
          "battery_energy_after_kwh": 253.6
        },
        {
          "hour": 4,
          "grid_kwh": 0.0,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 28.6,
          "battery_energy_after_kwh": 225.0
        },
        {
          "hour": 5,
          "grid_kwh": 107.8,
          "solar_used_kwh": 2.4,
          "battery_action": "charge",
          "battery_kwh": 75.0,
          "battery_energy_after_kwh": 300.0
        },
        {
          "hour": 6,
          "grid_kwh": 0.0,
          "solar_used_kwh": 14.4,
          "battery_action": "discharge",
          "battery_kwh": 35.1,
          "battery_energy_after_kwh": 264.9
        },
        {
          "hour": 7,
          "grid_kwh": 47.6,
          "solar_used_kwh": 42.0,
          "battery_action": "charge",
          "battery_kwh": 18.1,
          "battery_energy_after_kwh": 283.0
        },
        {
          "hour": 8,
          "grid_kwh": 0.0,
          "solar_used_kwh": 78.0,
          "battery_action": "discharge",
          "battery_kwh": 10.0,
          "battery_energy_after_kwh": 273.0
        },
        {
          "hour": 9,
          "grid_kwh": 0.0,
          "solar_used_kwh": 108.0,
          "battery_action": "charge",
          "battery_kwh": 3.5,
          "battery_energy_after_kwh": 276.5
        },
        {
          "hour": 10,
          "grid_kwh": 0.0,
          "solar_used_kwh": 126.0,
          "battery_action": "charge",
          "battery_kwh": 5.0,
          "battery_energy_after_kwh": 281.5
        },
        {
          "hour": 11,
          "grid_kwh": 0.0,
          "solar_used_kwh": 138.0,
          "battery_action": "charge",
          "battery_kwh": 6.0,
          "battery_energy_after_kwh": 287.5
        },
        {
          "hour": 12,
          "grid_kwh": 0.0,
          "solar_used_kwh": 144.0,
          "battery_action": "charge",
          "battery_kwh": 6.5,
          "battery_energy_after_kwh": 294.0
        },
        {
          "hour": 13,
          "grid_kwh": 0.0,
          "solar_used_kwh": 138.0,
          "battery_action": "charge",
          "battery_kwh": 6.0,
          "battery_energy_after_kwh": 300.0
        },
        {
          "hour": 14,
          "grid_kwh": 0.0,
          "solar_used_kwh": 114.0,
          "battery_action": "discharge",
          "battery_kwh": 12.5,
          "battery_energy_after_kwh": 287.5
        },
        {
          "hour": 15,
          "grid_kwh": 44.0,
          "solar_used_kwh": 84.0,
          "battery_action": "charge",
          "battery_kwh": 12.5,
          "battery_energy_after_kwh": 300.0
        },
        {
          "hour": 16,
          "grid_kwh": 56.5,
          "solar_used_kwh": 48.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 300.0
        },
        {
          "hour": 17,
          "grid_kwh": 78.0,
          "solar_used_kwh": 18.0,
          "battery_action": "discharge",
          "battery_kwh": 25.0,
          "battery_energy_after_kwh": 275.0
        },
        {
          "hour": 18,
          "grid_kwh": 65.6,
          "solar_used_kwh": 2.4,
          "battery_action": "discharge",
          "battery_kwh": 75.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 19,
          "grid_kwh": 62.5,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 75.0,
          "battery_energy_after_kwh": 125.0
        },
        {
          "hour": 20,
          "grid_kwh": 35.0,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 75.0,
          "battery_energy_after_kwh": 50.0
        },
        {
          "hour": 21,
          "grid_kwh": 82.5,
          "solar_used_kwh": 0.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 50.0
        },
        {
          "hour": 22,
          "grid_kwh": 85.5,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 25.0,
          "battery_energy_after_kwh": 75.0
        },
        {
          "hour": 23,
          "grid_kwh": 121.2,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 75.0,
          "battery_energy_after_kwh": 150.0
        }
      ],
      "total_grid_kwh": 1019.6,
      "total_cost_bdt": 10007.6,
      "peak_grid_kwh": 121.2,
      "plan_summary": "Optimized 24h schedule for CASE-006: total grid 1019.60 kWh, cost 10007.60 BDT, peak 121.20 kWh."
    }
  },
  {
    "scenario_id": "CASE-007",
    "input": {
      "scenario_id": "CASE-007",
      "operator_notes": [
        "PV production will drop to about 20% between 13:00 and 15:00",
        "CSE Fest registration deadline extended to midnight."
      ],
      "hours": [
        {
          "hour": 0,
          "demand_kwh": 35.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 1,
          "demand_kwh": 30.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 2,
          "demand_kwh": 28.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 3,
          "demand_kwh": 25.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 4,
          "demand_kwh": 26.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 5,
          "demand_kwh": 32.0,
          "solar_kwh": 2.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 6,
          "demand_kwh": 45.0,
          "solar_kwh": 12.0,
          "tariff_bdt_per_kwh": 8.0
        },
        {
          "hour": 7,
          "demand_kwh": 65.0,
          "solar_kwh": 35.0,
          "tariff_bdt_per_kwh": 8.0
        },
        {
          "hour": 8,
          "demand_kwh": 80.0,
          "solar_kwh": 65.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 9,
          "demand_kwh": 95.0,
          "solar_kwh": 90.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 10,
          "demand_kwh": 110.0,
          "solar_kwh": 105.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 11,
          "demand_kwh": 120.0,
          "solar_kwh": 115.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 12,
          "demand_kwh": 125.0,
          "solar_kwh": 120.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 13,
          "demand_kwh": 120.0,
          "solar_kwh": 115.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 14,
          "demand_kwh": 115.0,
          "solar_kwh": 95.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 15,
          "demand_kwh": 105.0,
          "solar_kwh": 70.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 16,
          "demand_kwh": 95.0,
          "solar_kwh": 40.0,
          "tariff_bdt_per_kwh": 10.5
        },
        {
          "hour": 17,
          "demand_kwh": 110.0,
          "solar_kwh": 15.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 18,
          "demand_kwh": 130.0,
          "solar_kwh": 2.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 19,
          "demand_kwh": 125.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 20,
          "demand_kwh": 100.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 21,
          "demand_kwh": 75.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 22,
          "demand_kwh": 55.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 10.5
        },
        {
          "hour": 23,
          "demand_kwh": 42.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 8.0
        }
      ],
      "battery": {
        "capacity_kwh": 200.0,
        "initial_energy_kwh": 100.0,
        "minimum_energy_kwh": 30.0,
        "max_charge_kwh_per_hour": 50.0,
        "max_discharge_kwh_per_hour": 50.0
      }
    },
    "expected_output": {
      "scenario_id": "CASE-007",
      "directive_interpretation": [
        {
          "note_index": 0,
          "applies": true,
          "directive_type": "solar_reduction",
          "structured_adjustment": {
            "hours": [
              13,
              14
            ],
            "factor": 0.2
          },
          "explanation": "Solar output drops to 20% (factor 0.2) between 13:00 and 15:00."
        },
        {
          "note_index": 1,
          "applies": false,
          "directive_type": "no_op",
          "structured_adjustment": null,
          "explanation": "Registration deadline announcement is an informational notice with no operational impact."
        }
      ],
      "hourly_plan": [
        {
          "hour": 0,
          "grid_kwh": 85.0,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 150.0
        },
        {
          "hour": 1,
          "grid_kwh": 30.0,
          "solar_used_kwh": 0.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 150.0
        },
        {
          "hour": 2,
          "grid_kwh": 78.0,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 3,
          "grid_kwh": 1.0,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 24.0,
          "battery_energy_after_kwh": 176.0
        },
        {
          "hour": 4,
          "grid_kwh": 0.0,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 26.0,
          "battery_energy_after_kwh": 150.0
        },
        {
          "hour": 5,
          "grid_kwh": 80.0,
          "solar_used_kwh": 2.0,
          "battery_action": "charge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 6,
          "grid_kwh": 33.0,
          "solar_used_kwh": 12.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 7,
          "grid_kwh": 30.0,
          "solar_used_kwh": 35.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 8,
          "grid_kwh": 0.0,
          "solar_used_kwh": 65.0,
          "battery_action": "discharge",
          "battery_kwh": 15.0,
          "battery_energy_after_kwh": 185.0
        },
        {
          "hour": 9,
          "grid_kwh": 0.0,
          "solar_used_kwh": 90.0,
          "battery_action": "discharge",
          "battery_kwh": 5.0,
          "battery_energy_after_kwh": 180.0
        },
        {
          "hour": 10,
          "grid_kwh": 0.0,
          "solar_used_kwh": 105.0,
          "battery_action": "discharge",
          "battery_kwh": 5.0,
          "battery_energy_after_kwh": 175.0
        },
        {
          "hour": 11,
          "grid_kwh": 0.0,
          "solar_used_kwh": 115.0,
          "battery_action": "discharge",
          "battery_kwh": 5.0,
          "battery_energy_after_kwh": 170.0
        },
        {
          "hour": 12,
          "grid_kwh": 35.0,
          "solar_used_kwh": 120.0,
          "battery_action": "charge",
          "battery_kwh": 30.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 13,
          "grid_kwh": 47.0,
          "solar_used_kwh": 23.0,
          "battery_action": "discharge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 150.0
        },
        {
          "hour": 14,
          "grid_kwh": 146.0,
          "solar_used_kwh": 19.0,
          "battery_action": "charge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 15,
          "grid_kwh": 35.0,
          "solar_used_kwh": 70.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 16,
          "grid_kwh": 55.0,
          "solar_used_kwh": 40.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 17,
          "grid_kwh": 45.0,
          "solar_used_kwh": 15.0,
          "battery_action": "discharge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 150.0
        },
        {
          "hour": 18,
          "grid_kwh": 108.0,
          "solar_used_kwh": 2.0,
          "battery_action": "discharge",
          "battery_kwh": 20.0,
          "battery_energy_after_kwh": 130.0
        },
        {
          "hour": 19,
          "grid_kwh": 75.0,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 80.0
        },
        {
          "hour": 20,
          "grid_kwh": 50.0,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 30.0
        },
        {
          "hour": 21,
          "grid_kwh": 75.0,
          "solar_used_kwh": 0.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 30.0
        },
        {
          "hour": 22,
          "grid_kwh": 75.0,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 20.0,
          "battery_energy_after_kwh": 50.0
        },
        {
          "hour": 23,
          "grid_kwh": 92.0,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 100.0
        }
      ],
      "total_grid_kwh": 1175.0,
      "total_cost_bdt": 11826.5,
      "peak_grid_kwh": 146.0,
      "plan_summary": "Optimized 24h schedule for CASE-007: total grid 1175.00 kWh, cost 11826.50 BDT, peak 146.00 kWh."
    }
  },
  {
    "scenario_id": "CASE-008",
    "input": {
      "scenario_id": "CASE-008",
      "operator_notes": [
        "Night grid maintenance: no charging allowed from 10 PM to 2 AM."
      ],
      "hours": [
        {
          "hour": 0,
          "demand_kwh": 28.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 1,
          "demand_kwh": 24.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 2,
          "demand_kwh": 22.4,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 3,
          "demand_kwh": 20.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 4,
          "demand_kwh": 20.8,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 5,
          "demand_kwh": 25.6,
          "solar_kwh": 1.8,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 6,
          "demand_kwh": 36.0,
          "solar_kwh": 10.8,
          "tariff_bdt_per_kwh": 8.0
        },
        {
          "hour": 7,
          "demand_kwh": 52.0,
          "solar_kwh": 31.5,
          "tariff_bdt_per_kwh": 8.0
        },
        {
          "hour": 8,
          "demand_kwh": 64.0,
          "solar_kwh": 58.5,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 9,
          "demand_kwh": 76.0,
          "solar_kwh": 81.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 10,
          "demand_kwh": 88.0,
          "solar_kwh": 94.5,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 11,
          "demand_kwh": 96.0,
          "solar_kwh": 103.5,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 12,
          "demand_kwh": 100.0,
          "solar_kwh": 108.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 13,
          "demand_kwh": 96.0,
          "solar_kwh": 103.5,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 14,
          "demand_kwh": 92.0,
          "solar_kwh": 85.5,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 15,
          "demand_kwh": 84.0,
          "solar_kwh": 63.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 16,
          "demand_kwh": 76.0,
          "solar_kwh": 36.0,
          "tariff_bdt_per_kwh": 10.5
        },
        {
          "hour": 17,
          "demand_kwh": 88.0,
          "solar_kwh": 13.5,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 18,
          "demand_kwh": 104.0,
          "solar_kwh": 1.8,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 19,
          "demand_kwh": 100.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 20,
          "demand_kwh": 80.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 21,
          "demand_kwh": 60.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 22,
          "demand_kwh": 44.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 10.5
        },
        {
          "hour": 23,
          "demand_kwh": 33.6,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 8.0
        }
      ],
      "battery": {
        "capacity_kwh": 180.0,
        "initial_energy_kwh": 90.0,
        "minimum_energy_kwh": 20.0,
        "max_charge_kwh_per_hour": 45.0,
        "max_discharge_kwh_per_hour": 45.0
      }
    },
    "expected_output": {
      "scenario_id": "CASE-008",
      "directive_interpretation": [
        {
          "note_index": 0,
          "applies": true,
          "directive_type": "no_charge_window",
          "structured_adjustment": {
            "hours": [
              0,
              1,
              22,
              23
            ]
          },
          "explanation": "No charge window across midnight 10 PM (22) to 2 AM (2) sorted ascending."
        }
      ],
      "hourly_plan": [
        {
          "hour": 0,
          "grid_kwh": 28.0,
          "solar_used_kwh": 0.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 90.0
        },
        {
          "hour": 1,
          "grid_kwh": 24.0,
          "solar_used_kwh": 0.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 90.0
        },
        {
          "hour": 2,
          "grid_kwh": 67.4,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 45.0,
          "battery_energy_after_kwh": 135.0
        },
        {
          "hour": 3,
          "grid_kwh": 65.0,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 45.0,
          "battery_energy_after_kwh": 180.0
        },
        {
          "hour": 4,
          "grid_kwh": 20.8,
          "solar_used_kwh": 0.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 180.0
        },
        {
          "hour": 5,
          "grid_kwh": 23.8,
          "solar_used_kwh": 1.8,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 180.0
        },
        {
          "hour": 6,
          "grid_kwh": 0.0,
          "solar_used_kwh": 10.8,
          "battery_action": "discharge",
          "battery_kwh": 25.2,
          "battery_energy_after_kwh": 154.8
        },
        {
          "hour": 7,
          "grid_kwh": 16.7,
          "solar_used_kwh": 31.5,
          "battery_action": "discharge",
          "battery_kwh": 3.8,
          "battery_energy_after_kwh": 151.0
        },
        {
          "hour": 8,
          "grid_kwh": 0.0,
          "solar_used_kwh": 58.5,
          "battery_action": "discharge",
          "battery_kwh": 5.5,
          "battery_energy_after_kwh": 145.5
        },
        {
          "hour": 9,
          "grid_kwh": 0.0,
          "solar_used_kwh": 81.0,
          "battery_action": "charge",
          "battery_kwh": 5.0,
          "battery_energy_after_kwh": 150.5
        },
        {
          "hour": 10,
          "grid_kwh": 0.0,
          "solar_used_kwh": 94.5,
          "battery_action": "charge",
          "battery_kwh": 6.5,
          "battery_energy_after_kwh": 157.0
        },
        {
          "hour": 11,
          "grid_kwh": 0.0,
          "solar_used_kwh": 103.5,
          "battery_action": "charge",
          "battery_kwh": 7.5,
          "battery_energy_after_kwh": 164.5
        },
        {
          "hour": 12,
          "grid_kwh": 0.0,
          "solar_used_kwh": 108.0,
          "battery_action": "charge",
          "battery_kwh": 8.0,
          "battery_energy_after_kwh": 172.5
        },
        {
          "hour": 13,
          "grid_kwh": 0.0,
          "solar_used_kwh": 103.5,
          "battery_action": "charge",
          "battery_kwh": 7.5,
          "battery_energy_after_kwh": 180.0
        },
        {
          "hour": 14,
          "grid_kwh": 0.0,
          "solar_used_kwh": 85.5,
          "battery_action": "discharge",
          "battery_kwh": 6.5,
          "battery_energy_after_kwh": 173.5
        },
        {
          "hour": 15,
          "grid_kwh": 27.5,
          "solar_used_kwh": 63.0,
          "battery_action": "charge",
          "battery_kwh": 6.5,
          "battery_energy_after_kwh": 180.0
        },
        {
          "hour": 16,
          "grid_kwh": 40.0,
          "solar_used_kwh": 36.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 180.0
        },
        {
          "hour": 17,
          "grid_kwh": 29.5,
          "solar_used_kwh": 13.5,
          "battery_action": "discharge",
          "battery_kwh": 45.0,
          "battery_energy_after_kwh": 135.0
        },
        {
          "hour": 18,
          "grid_kwh": 57.2,
          "solar_used_kwh": 1.8,
          "battery_action": "discharge",
          "battery_kwh": 45.0,
          "battery_energy_after_kwh": 90.0
        },
        {
          "hour": 19,
          "grid_kwh": 55.0,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 45.0,
          "battery_energy_after_kwh": 45.0
        },
        {
          "hour": 20,
          "grid_kwh": 80.0,
          "solar_used_kwh": 0.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 45.0
        },
        {
          "hour": 21,
          "grid_kwh": 105.0,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 45.0,
          "battery_energy_after_kwh": 90.0
        },
        {
          "hour": 22,
          "grid_kwh": 44.0,
          "solar_used_kwh": 0.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 90.0
        },
        {
          "hour": 23,
          "grid_kwh": 33.6,
          "solar_used_kwh": 0.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 90.0
        }
      ],
      "total_grid_kwh": 717.5,
      "total_cost_bdt": 7607.95,
      "peak_grid_kwh": 105.0,
      "plan_summary": "Optimized 24h schedule for CASE-008: total grid 717.50 kWh, cost 7607.95 BDT, peak 105.00 kWh."
    }
  },
  {
    "scenario_id": "CASE-009",
    "input": {
      "scenario_id": "CASE-009",
      "operator_notes": [
        "Panel washing from one until three will leave roughly one-fifth of normal solar output",
        "Robotics lab seminar at 3 PM in Auditorium 2",
        "Hold 80 kWh reserve in the battery between 18:00 and 22:00"
      ],
      "hours": [
        {
          "hour": 0,
          "demand_kwh": 35.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 1,
          "demand_kwh": 30.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 2,
          "demand_kwh": 28.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 3,
          "demand_kwh": 25.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 4,
          "demand_kwh": 26.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 5,
          "demand_kwh": 32.0,
          "solar_kwh": 2.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 6,
          "demand_kwh": 45.0,
          "solar_kwh": 12.0,
          "tariff_bdt_per_kwh": 8.0
        },
        {
          "hour": 7,
          "demand_kwh": 65.0,
          "solar_kwh": 35.0,
          "tariff_bdt_per_kwh": 8.0
        },
        {
          "hour": 8,
          "demand_kwh": 80.0,
          "solar_kwh": 65.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 9,
          "demand_kwh": 95.0,
          "solar_kwh": 90.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 10,
          "demand_kwh": 110.0,
          "solar_kwh": 105.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 11,
          "demand_kwh": 120.0,
          "solar_kwh": 115.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 12,
          "demand_kwh": 125.0,
          "solar_kwh": 120.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 13,
          "demand_kwh": 120.0,
          "solar_kwh": 115.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 14,
          "demand_kwh": 115.0,
          "solar_kwh": 95.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 15,
          "demand_kwh": 105.0,
          "solar_kwh": 70.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 16,
          "demand_kwh": 95.0,
          "solar_kwh": 40.0,
          "tariff_bdt_per_kwh": 10.5
        },
        {
          "hour": 17,
          "demand_kwh": 110.0,
          "solar_kwh": 15.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 18,
          "demand_kwh": 130.0,
          "solar_kwh": 2.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 19,
          "demand_kwh": 125.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 20,
          "demand_kwh": 100.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 21,
          "demand_kwh": 75.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 22,
          "demand_kwh": 55.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 10.5
        },
        {
          "hour": 23,
          "demand_kwh": 42.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 8.0
        }
      ],
      "battery": {
        "capacity_kwh": 250.0,
        "initial_energy_kwh": 100.0,
        "minimum_energy_kwh": 30.0,
        "max_charge_kwh_per_hour": 50.0,
        "max_discharge_kwh_per_hour": 50.0
      }
    },
    "expected_output": {
      "scenario_id": "CASE-009",
      "directive_interpretation": [
        {
          "note_index": 0,
          "applies": true,
          "directive_type": "solar_reduction",
          "structured_adjustment": {
            "hours": [
              13,
              14
            ],
            "factor": 0.2
          },
          "explanation": "One-fifth remaining translates to factor 0.2 for hours 13 and 14."
        },
        {
          "note_index": 1,
          "applies": false,
          "directive_type": "no_op",
          "structured_adjustment": null,
          "explanation": "Seminar notice is irrelevant to energy dispatch."
        },
        {
          "note_index": 2,
          "applies": true,
          "directive_type": "minimum_battery_reserve",
          "structured_adjustment": {
            "hours": [
              18,
              19,
              20,
              21
            ],
            "minimum_energy_kwh": 80.0
          },
          "explanation": "Enforces 80 kWh minimum battery reserve from 18:00 to 22:00."
        }
      ],
      "hourly_plan": [
        {
          "hour": 0,
          "grid_kwh": 85.0,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 150.0
        },
        {
          "hour": 1,
          "grid_kwh": 80.0,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 2,
          "grid_kwh": 78.0,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 250.0
        },
        {
          "hour": 3,
          "grid_kwh": 1.0,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 24.0,
          "battery_energy_after_kwh": 226.0
        },
        {
          "hour": 4,
          "grid_kwh": 0.0,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 26.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 5,
          "grid_kwh": 80.0,
          "solar_used_kwh": 2.0,
          "battery_action": "charge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 250.0
        },
        {
          "hour": 6,
          "grid_kwh": 33.0,
          "solar_used_kwh": 12.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 250.0
        },
        {
          "hour": 7,
          "grid_kwh": 30.0,
          "solar_used_kwh": 35.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 250.0
        },
        {
          "hour": 8,
          "grid_kwh": 0.0,
          "solar_used_kwh": 65.0,
          "battery_action": "discharge",
          "battery_kwh": 15.0,
          "battery_energy_after_kwh": 235.0
        },
        {
          "hour": 9,
          "grid_kwh": 0.0,
          "solar_used_kwh": 90.0,
          "battery_action": "discharge",
          "battery_kwh": 5.0,
          "battery_energy_after_kwh": 230.0
        },
        {
          "hour": 10,
          "grid_kwh": 0.0,
          "solar_used_kwh": 105.0,
          "battery_action": "discharge",
          "battery_kwh": 5.0,
          "battery_energy_after_kwh": 225.0
        },
        {
          "hour": 11,
          "grid_kwh": 0.0,
          "solar_used_kwh": 115.0,
          "battery_action": "discharge",
          "battery_kwh": 5.0,
          "battery_energy_after_kwh": 220.0
        },
        {
          "hour": 12,
          "grid_kwh": 35.0,
          "solar_used_kwh": 120.0,
          "battery_action": "charge",
          "battery_kwh": 30.0,
          "battery_energy_after_kwh": 250.0
        },
        {
          "hour": 13,
          "grid_kwh": 47.0,
          "solar_used_kwh": 23.0,
          "battery_action": "discharge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 14,
          "grid_kwh": 146.0,
          "solar_used_kwh": 19.0,
          "battery_action": "charge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 250.0
        },
        {
          "hour": 15,
          "grid_kwh": 35.0,
          "solar_used_kwh": 70.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 250.0
        },
        {
          "hour": 16,
          "grid_kwh": 55.0,
          "solar_used_kwh": 40.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 250.0
        },
        {
          "hour": 17,
          "grid_kwh": 45.0,
          "solar_used_kwh": 15.0,
          "battery_action": "discharge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 18,
          "grid_kwh": 108.0,
          "solar_used_kwh": 2.0,
          "battery_action": "discharge",
          "battery_kwh": 20.0,
          "battery_energy_after_kwh": 180.0
        },
        {
          "hour": 19,
          "grid_kwh": 75.0,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 130.0
        },
        {
          "hour": 20,
          "grid_kwh": 50.0,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 80.0
        },
        {
          "hour": 21,
          "grid_kwh": 75.0,
          "solar_used_kwh": 0.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 80.0
        },
        {
          "hour": 22,
          "grid_kwh": 25.0,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 30.0,
          "battery_energy_after_kwh": 50.0
        },
        {
          "hour": 23,
          "grid_kwh": 92.0,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 50.0,
          "battery_energy_after_kwh": 100.0
        }
      ],
      "total_grid_kwh": 1175.0,
      "total_cost_bdt": 11626.5,
      "peak_grid_kwh": 146.0,
      "plan_summary": "Optimized 24h schedule for CASE-009: total grid 1175.00 kWh, cost 11626.50 BDT, peak 146.00 kWh."
    }
  },
  {
    "scenario_id": "CASE-010",
    "input": {
      "scenario_id": "CASE-010",
      "operator_notes": [
        "Dust storm: solar loses a quarter of output from noon until three PM",
        "Feeder limitation: grid intake must remain at or below 80 kWh from 17:00 to 21:00"
      ],
      "hours": [
        {
          "hour": 0,
          "demand_kwh": 35.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 1,
          "demand_kwh": 30.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 2,
          "demand_kwh": 28.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 3,
          "demand_kwh": 25.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 4,
          "demand_kwh": 26.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 5,
          "demand_kwh": 32.0,
          "solar_kwh": 2.0,
          "tariff_bdt_per_kwh": 6.5
        },
        {
          "hour": 6,
          "demand_kwh": 45.0,
          "solar_kwh": 12.0,
          "tariff_bdt_per_kwh": 8.0
        },
        {
          "hour": 7,
          "demand_kwh": 65.0,
          "solar_kwh": 35.0,
          "tariff_bdt_per_kwh": 8.0
        },
        {
          "hour": 8,
          "demand_kwh": 80.0,
          "solar_kwh": 65.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 9,
          "demand_kwh": 95.0,
          "solar_kwh": 90.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 10,
          "demand_kwh": 110.0,
          "solar_kwh": 105.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 11,
          "demand_kwh": 120.0,
          "solar_kwh": 115.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 12,
          "demand_kwh": 125.0,
          "solar_kwh": 120.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 13,
          "demand_kwh": 120.0,
          "solar_kwh": 115.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 14,
          "demand_kwh": 115.0,
          "solar_kwh": 95.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 15,
          "demand_kwh": 105.0,
          "solar_kwh": 70.0,
          "tariff_bdt_per_kwh": 9.5
        },
        {
          "hour": 16,
          "demand_kwh": 95.0,
          "solar_kwh": 40.0,
          "tariff_bdt_per_kwh": 10.5
        },
        {
          "hour": 17,
          "demand_kwh": 110.0,
          "solar_kwh": 15.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 18,
          "demand_kwh": 130.0,
          "solar_kwh": 2.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 19,
          "demand_kwh": 125.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 20,
          "demand_kwh": 100.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 21,
          "demand_kwh": 75.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 14.0
        },
        {
          "hour": 22,
          "demand_kwh": 55.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 10.5
        },
        {
          "hour": 23,
          "demand_kwh": 42.0,
          "solar_kwh": 0.0,
          "tariff_bdt_per_kwh": 8.0
        }
      ],
      "battery": {
        "capacity_kwh": 220.0,
        "initial_energy_kwh": 110.0,
        "minimum_energy_kwh": 35.0,
        "max_charge_kwh_per_hour": 55.0,
        "max_discharge_kwh_per_hour": 55.0
      }
    },
    "expected_output": {
      "scenario_id": "CASE-010",
      "directive_interpretation": [
        {
          "note_index": 0,
          "applies": true,
          "directive_type": "solar_reduction",
          "structured_adjustment": {
            "hours": [
              12,
              13,
              14
            ],
            "factor": 0.75
          },
          "explanation": "Loses a quarter means 0.75 usable solar factor remaining from 12:00 to 15:00."
        },
        {
          "note_index": 1,
          "applies": true,
          "directive_type": "max_grid_window",
          "structured_adjustment": {
            "hours": [
              17,
              18,
              19,
              20
            ],
            "max_grid_kwh": 80.0
          },
          "explanation": "Grid power capped at 80 kWh from 17:00 to 21:00."
        }
      ],
      "hourly_plan": [
        {
          "hour": 0,
          "grid_kwh": 90.0,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 55.0,
          "battery_energy_after_kwh": 165.0
        },
        {
          "hour": 1,
          "grid_kwh": 30.0,
          "solar_used_kwh": 0.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 165.0
        },
        {
          "hour": 2,
          "grid_kwh": 83.0,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 55.0,
          "battery_energy_after_kwh": 220.0
        },
        {
          "hour": 3,
          "grid_kwh": 25.0,
          "solar_used_kwh": 0.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 220.0
        },
        {
          "hour": 4,
          "grid_kwh": 26.0,
          "solar_used_kwh": 0.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 220.0
        },
        {
          "hour": 5,
          "grid_kwh": 30.0,
          "solar_used_kwh": 2.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 220.0
        },
        {
          "hour": 6,
          "grid_kwh": 0.0,
          "solar_used_kwh": 12.0,
          "battery_action": "discharge",
          "battery_kwh": 33.0,
          "battery_energy_after_kwh": 187.0
        },
        {
          "hour": 7,
          "grid_kwh": 63.0,
          "solar_used_kwh": 35.0,
          "battery_action": "charge",
          "battery_kwh": 33.0,
          "battery_energy_after_kwh": 220.0
        },
        {
          "hour": 8,
          "grid_kwh": 0.0,
          "solar_used_kwh": 65.0,
          "battery_action": "discharge",
          "battery_kwh": 15.0,
          "battery_energy_after_kwh": 205.0
        },
        {
          "hour": 9,
          "grid_kwh": 0.0,
          "solar_used_kwh": 90.0,
          "battery_action": "discharge",
          "battery_kwh": 5.0,
          "battery_energy_after_kwh": 200.0
        },
        {
          "hour": 10,
          "grid_kwh": 0.0,
          "solar_used_kwh": 105.0,
          "battery_action": "discharge",
          "battery_kwh": 5.0,
          "battery_energy_after_kwh": 195.0
        },
        {
          "hour": 11,
          "grid_kwh": 0.0,
          "solar_used_kwh": 115.0,
          "battery_action": "discharge",
          "battery_kwh": 5.0,
          "battery_energy_after_kwh": 190.0
        },
        {
          "hour": 12,
          "grid_kwh": 0.0,
          "solar_used_kwh": 90.0,
          "battery_action": "discharge",
          "battery_kwh": 35.0,
          "battery_energy_after_kwh": 155.0
        },
        {
          "hour": 13,
          "grid_kwh": 88.75,
          "solar_used_kwh": 86.25,
          "battery_action": "charge",
          "battery_kwh": 55.0,
          "battery_energy_after_kwh": 210.0
        },
        {
          "hour": 14,
          "grid_kwh": 53.75,
          "solar_used_kwh": 71.25,
          "battery_action": "charge",
          "battery_kwh": 10.0,
          "battery_energy_after_kwh": 220.0
        },
        {
          "hour": 15,
          "grid_kwh": 35.0,
          "solar_used_kwh": 70.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 220.0
        },
        {
          "hour": 16,
          "grid_kwh": 55.0,
          "solar_used_kwh": 40.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 220.0
        },
        {
          "hour": 17,
          "grid_kwh": 40.0,
          "solar_used_kwh": 15.0,
          "battery_action": "discharge",
          "battery_kwh": 55.0,
          "battery_energy_after_kwh": 165.0
        },
        {
          "hour": 18,
          "grid_kwh": 73.0,
          "solar_used_kwh": 2.0,
          "battery_action": "discharge",
          "battery_kwh": 55.0,
          "battery_energy_after_kwh": 110.0
        },
        {
          "hour": 19,
          "grid_kwh": 70.0,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 55.0,
          "battery_energy_after_kwh": 55.0
        },
        {
          "hour": 20,
          "grid_kwh": 80.0,
          "solar_used_kwh": 0.0,
          "battery_action": "discharge",
          "battery_kwh": 20.0,
          "battery_energy_after_kwh": 35.0
        },
        {
          "hour": 21,
          "grid_kwh": 75.0,
          "solar_used_kwh": 0.0,
          "battery_action": "idle",
          "battery_kwh": 0.0,
          "battery_energy_after_kwh": 35.0
        },
        {
          "hour": 22,
          "grid_kwh": 75.0,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 20.0,
          "battery_energy_after_kwh": 55.0
        },
        {
          "hour": 23,
          "grid_kwh": 97.0,
          "solar_used_kwh": 0.0,
          "battery_action": "charge",
          "battery_kwh": 55.0,
          "battery_energy_after_kwh": 110.0
        }
      ],
      "total_grid_kwh": 1089.5,
      "total_cost_bdt": 10909.25,
      "peak_grid_kwh": 97.0,
      "plan_summary": "Optimized 24h schedule for CASE-010: total grid 1089.50 kWh, cost 10909.25 BDT, peak 97.00 kWh."
    }
  }
];
