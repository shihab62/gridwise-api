import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.models import DirectiveInterpretation, SolarReductionAdjustment

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_optimize_energy_malformed_json_returns_400():
    response = client.post(
        "/optimize-energy",
        content="this is not json",
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 400
    data = response.json()
    assert "error" in data


def test_optimize_energy_missing_hours_returns_400():
    payload = {
        "scenario_id": "TEST-BAD-01",
        "operator_notes": ["Note 1"],
        "hours": [],  # requires 24
        "battery": {
            "capacity_kwh": 100,
            "initial_energy_kwh": 50,
            "minimum_energy_kwh": 20,
            "max_charge_kwh_per_hour": 25,
            "max_discharge_kwh_per_hour": 25,
        },
    }
    response = client.post("/optimize-energy", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert "error" in data


def test_optimize_energy_invalid_battery_sanity_returns_400_or_422():
    # minimum_energy (80) > initial_energy (50)
    payload = {
        "scenario_id": "TEST-BAD-02",
        "operator_notes": ["Note 1"],
        "hours": [{"hour": i, "demand_kwh": 10, "solar_kwh": 5, "tariff_bdt_per_kwh": 8} for i in range(24)],
        "battery": {
            "capacity_kwh": 100,
            "initial_energy_kwh": 50,
            "minimum_energy_kwh": 80,
            "max_charge_kwh_per_hour": 25,
            "max_discharge_kwh_per_hour": 25,
        },
    }
    response = client.post("/optimize-energy", json=payload)
    # Fails Pydantic validation
    assert response.status_code in [400, 422]
    data = response.json()
    assert "error" in data


def test_optimize_energy_successful_mocked(monkeypatch):
    async def mock_interpret(notes, battery):
        return [
            DirectiveInterpretation(
                note_index=0,
                applies=True,
                directive_type="solar_reduction",
                structured_adjustment=SolarReductionAdjustment(hours=[13, 14], factor=0.2),
                explanation="Mocked solar reduction",
            )
        ]

    monkeypatch.setattr("src.main.interpret_operator_notes", mock_interpret)

    payload = {
        "scenario_id": "MOCK-CASE-001",
        "operator_notes": ["Expect an 80% reduction in rooftop solar during the 1-3 PM maintenance window."],
        "hours": [
            {
                "hour": i,
                "demand_kwh": 30.0,
                "solar_kwh": 20.0 if 8 <= i <= 16 else 0.0,
                "tariff_bdt_per_kwh": 10.0,
            }
            for i in range(24)
        ],
        "battery": {
            "capacity_kwh": 200.0,
            "initial_energy_kwh": 100.0,
            "minimum_energy_kwh": 30.0,
            "max_charge_kwh_per_hour": 50.0,
            "max_discharge_kwh_per_hour": 50.0,
        },
    }

    response = client.post("/optimize-energy", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["scenario_id"] == "MOCK-CASE-001"
    assert len(data["directive_interpretation"]) == 1
    assert len(data["hourly_plan"]) == 24
    assert "total_cost_bdt" in data
    assert "plan_summary" in data
