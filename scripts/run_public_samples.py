import json
import os
import sys
import time
from typing import Any, Dict, List, Tuple

import httpx

from src.models import (
    BatteryInput,
    DirectiveInterpretation,
    HourInput,
    HourlyPlanItem,
)
from src.validator import validate_plan

BASE_URL = os.getenv("APP_URL", "http://localhost:3000").rstrip("/")
SAMPLE_FILE = "samples/BUP_CSE_FEST_2026_Preli_Public_Sample_Cases.json"
if not os.path.exists(SAMPLE_FILE):
    SAMPLE_FILE = "docs/BUP_CSE_FEST_2026_Preli_Public_Sample_Cases.json"


def compare_directives(actual: List[Dict[str, Any]], expected: List[Dict[str, Any]], tol: float = 0.01) -> Tuple[bool, str]:
    if len(actual) != len(expected):
        return False, f"Count mismatch: actual {len(actual)} vs expected {len(expected)}"

    for i, (act, exp) in enumerate(zip(actual, expected)):
        if act.get("note_index") != exp.get("note_index"):
            return False, f"Note {i}: note_index mismatch ({act.get('note_index')} != {exp.get('note_index')})"
        if act.get("applies") != exp.get("applies"):
            return False, f"Note {i}: applies mismatch ({act.get('applies')} != {exp.get('applies')})"
        if act.get("directive_type") != exp.get("directive_type"):
            return False, f"Note {i}: directive_type mismatch ({act.get('directive_type')} != {exp.get('directive_type')})"

        act_adj = act.get("structured_adjustment")
        exp_adj = exp.get("structured_adjustment")

        if (act_adj is None) != (exp_adj is None):
            return False, f"Note {i}: structured_adjustment nullness mismatch"

        if act_adj and exp_adj:
            act_hours = act_adj.get("hours", [])
            exp_hours = exp_adj.get("hours", [])
            if act_hours != exp_hours:
                return False, f"Note {i}: hours mismatch ({act_hours} != {exp_hours})"

            for key in ["factor", "minimum_energy_kwh", "max_grid_kwh"]:
                if key in exp_adj:
                    if key not in act_adj:
                        return False, f"Note {i}: missing key '{key}' in actual adjustment"
                    diff = abs(float(act_adj[key]) - float(exp_adj[key]))
                    if diff > tol:
                        return False, f"Note {i}: {key} mismatch ({act_adj[key]} vs {exp_adj[key]}, diff={diff:.4f})"

    return True, "OK"


def run_tests():
    if not os.path.exists(SAMPLE_FILE):
        print(f"ERROR: Sample cases file '{SAMPLE_FILE}' not found.")
        sys.exit(1)

    with open(SAMPLE_FILE, "r") as f:
        cases = json.load(f)

    print("\n" + "=" * 95)
    print(f" BUP CSE Fest 2026 Hackathon - Public Samples Test Suite ({len(cases)} Cases)")
    print(f" Target API: {BASE_URL}")
    print("=" * 95)

    is_in_process = False
    try:
        client = httpx.Client(timeout=35.0)
        h_res = client.get(f"{BASE_URL}/health")
        if h_res.status_code == 200 and h_res.json().get("status") == "ok":
            print(f"Connected to live server at {BASE_URL}")
            print("Health Check: [PASSED] (status: ok)\n")
        else:
            raise RuntimeError(f"Bad health response: {h_res.status_code}")
    except Exception as e:
        print(f"Notice: Live server at {BASE_URL} not reachable ({e}). Switching to in-process FastAPI TestClient...")
        from fastapi.testclient import TestClient
        from src.main import app
        client = TestClient(app)
        is_in_process = True
        h_res = client.get("/health")
        if h_res.status_code != 200 or h_res.json().get("status") != "ok":
            print(f"In-process health check failed: {h_res.status_code}")
            sys.exit(1)
        print("In-process Health Check: [PASSED] (status: ok)\n")

    results = []
    total_passed = 0

    header = f"{'Case ID':<12} | {'Directives':<12} | {'Plan Replay':<12} | {'Expected Cost':<14} | {'Actual Cost':<14} | {'Latency':<9} | {'Status'}"
    print(header)
    print("-" * 95)

    for case in cases:
        sc_id = case["scenario_id"]
        inp = case["input"]
        expected = case["expected_output"]

        t0 = time.monotonic()
        try:
            url_path = "/optimize-energy" if is_in_process else f"{BASE_URL}/optimize-energy"
            resp = client.post(url_path, json=inp)
            lat_ms = (time.monotonic() - t0) * 1000.0

            if resp.status_code != 200:
                results.append((sc_id, "FAIL", "N/A", f"{expected['total_cost_bdt']:.2f}", "ERR", f"{lat_ms:.0f}ms", f"HTTP {resp.status_code}"))
                continue

            data = resp.json()

            # Verify directives
            dir_ok, dir_msg = compare_directives(
                data["directive_interpretation"],
                expected["directive_interpretation"],
            )

            # Replay validator
            hours_obj = [HourInput(**h) for h in inp["hours"]]
            bat_obj = BatteryInput(**inp["battery"])
            dir_objs = [DirectiveInterpretation(**d) for d in data["directive_interpretation"]]
            plan_objs = [HourlyPlanItem(**p) for p in data["hourly_plan"]]

            plan_ok = True
            plan_msg = "OK"
            try:
                validate_plan(
                    hours_obj,
                    bat_obj,
                    dir_objs,
                    plan_objs,
                    data["total_grid_kwh"],
                    data["total_cost_bdt"],
                    data["peak_grid_kwh"],
                    tolerance=0.01,
                )
            except Exception as v_err:
                plan_ok = False
                plan_msg = str(v_err)[:25]

            act_cost = data["total_cost_bdt"]
            exp_cost = expected["total_cost_bdt"]
            cost_diff = abs(act_cost - exp_cost)
            # Acceptable if within 0.01 BDT or better if plan is valid
            cost_ok = (cost_diff <= 0.01) or (act_cost <= exp_cost and plan_ok)

            overall_pass = dir_ok and plan_ok and cost_ok
            if overall_pass:
                total_passed += 1
                status_str = "PASS"
            else:
                status_str = "FAIL"

            results.append((
                sc_id,
                "PASS" if dir_ok else "FAIL",
                "PASS" if plan_ok else "FAIL",
                f"{exp_cost:.2f} BDT",
                f"{act_cost:.2f} BDT",
                f"{lat_ms:.0f}ms",
                status_str,
            ))

        except Exception as exc:
            lat_ms = (time.monotonic() - t0) * 1000.0
            results.append((sc_id, "ERROR", "ERROR", f"{expected['total_cost_bdt']:.2f}", "EXC", f"{lat_ms:.0f}ms", str(exc)[:20]))

    for r in results:
        print(f"{r[0]:<12} | {r[1]:<12} | {r[2]:<12} | {r[3]:<14} | {r[4]:<14} | {r[5]:<9} | {r[6]}")

    print("-" * 95)
    print(f"Summary: {total_passed}/{len(cases)} public sample cases PASSED.\n")

    if total_passed < len(cases):
        sys.exit(1)


if __name__ == "__main__":
    from typing import Tuple
    run_tests()
