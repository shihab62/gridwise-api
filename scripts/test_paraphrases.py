import asyncio
import json
import os
import sys
import time
from typing import Any, Dict, List

from src.guardrails import validate_guardrails
from src.llm_interpreter import interpret_operator_notes
from src.models import BatteryInput


async def run_paraphrase_bench():
    path = "tests/paraphrases.json"
    if not os.path.exists(path):
        print(f"File {path} not found.")
        sys.exit(1)

    with open(path, "r") as f:
        benchmarks = json.load(f)

    print("\n" + "=" * 95)
    print(f" Running Paraphrase Benchmark Suite ({len(benchmarks)} Test Notes)")
    print("=" * 95)

    passed = 0
    results = []

    for item in benchmarks:
        p_id = item["id"]
        note = item["note"]
        cap = item["battery_capacity_kwh"]
        exp = item["expected_directive"]

        battery = BatteryInput(
            capacity_kwh=cap,
            initial_energy_kwh=cap * 0.5,
            minimum_energy_kwh=cap * 0.1,
            max_charge_kwh_per_hour=cap * 0.25,
            max_discharge_kwh_per_hour=cap * 0.25,
        )

        t0 = time.monotonic()
        try:
            directives = await interpret_operator_notes([note], battery)
            lat_ms = (time.monotonic() - t0) * 1000.0

            d = directives[0]
            ok = True
            msg = "OK"

            if d.applies != exp["applies"]:
                ok = False
                msg = f"applies mismatch ({d.applies} != {exp['applies']})"
            elif d.directive_type != exp["directive_type"]:
                ok = False
                msg = f"type mismatch ({d.directive_type} != {exp['directive_type']})"
            elif exp["applies"]:
                adj = d.structured_adjustment
                act_hours = adj.hours if hasattr(adj, "hours") else adj.get("hours", [])
                if act_hours != exp.get("hours", []):
                    ok = False
                    msg = f"hours mismatch ({act_hours} != {exp.get('hours')})"
                elif "factor" in exp:
                    act_factor = adj.factor if hasattr(adj, "factor") else adj.get("factor", 0.0)
                    if abs(act_factor - exp["factor"]) > 0.02:
                        ok = False
                        msg = f"factor mismatch ({act_factor} != {exp['factor']})"
                elif "minimum_energy_kwh" in exp:
                    act_res = adj.minimum_energy_kwh if hasattr(adj, "minimum_energy_kwh") else adj.get("minimum_energy_kwh", 0.0)
                    if abs(act_res - exp["minimum_energy_kwh"]) > 0.05:
                        ok = False
                        msg = f"reserve mismatch ({act_res} != {exp['minimum_energy_kwh']})"
                elif "max_grid_kwh" in exp:
                    act_cap = adj.max_grid_kwh if hasattr(adj, "max_grid_kwh") else adj.get("max_grid_kwh", 0.0)
                    if abs(act_cap - exp["max_grid_kwh"]) > 0.05:
                        ok = False
                        msg = f"grid cap mismatch ({act_cap} != {exp['max_grid_kwh']})"

            if ok:
                passed += 1
                status_str = "PASS"
            else:
                status_str = "FAIL"

            results.append((p_id, note[:42], status_str, f"{lat_ms:.0f}ms", msg))

        except Exception as exc:
            lat_ms = (time.monotonic() - t0) * 1000.0
            results.append((p_id, note[:42], "ERROR", f"{lat_ms:.0f}ms", str(exc)[:30]))

    print(f"{'ID':<6} | {'Operator Note':<44} | {'Status':<7} | {'Latency':<8} | {'Details'}")
    print("-" * 95)
    for r in results:
        print(f"{r[0]:<6} | {r[1]:<44} | {r[2]:<7} | {r[3]:<8} | {r[4]}")

    print("-" * 95)
    acc = (passed / len(benchmarks)) * 100.0
    print(f"Paraphrase Accuracy: {passed}/{len(benchmarks)} ({acc:.1f}%)\n")

    if passed < len(benchmarks) * 0.95:  # require at least 95% pass rate
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(run_paraphrase_bench())
