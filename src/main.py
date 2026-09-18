import asyncio
import logging
import time
from typing import Any, Dict

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

from src import config
from src.guardrails import GuardrailValidationError
from src.llm_interpreter import interpret_operator_notes
from src.models import (
    ErrorResponse,
    OptimizeEnergyRequest,
    OptimizeEnergyResponse,
)
from src.optimizer import InfeasiblePlanError, optimize_energy_schedule
from src.validator import PlanValidationError, validate_plan

# Configure structured logging
class ScenarioLogFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, "scenario_id"):
            record.scenario_id = "-"
        return True

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(scenario_id)s] %(message)s",
)
for handler in logging.root.handlers:
    handler.addFilter(ScenarioLogFilter())
logger = logging.getLogger("gridwise")

app = FastAPI(
    title="GridWise LLM API",
    description="Energy management & schedule optimizer API with LLM operator-note interpretation and HiGHS LP solver",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Custom Exception Handlers for Exact Status Codes & Error Schema ---

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Return 400 for malformed JSON or structurally invalid requests."""
    error_msg = "; ".join([f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()])
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "Malformed or structurally invalid request", "detail": error_msg},
    )


@app.exception_handler(InfeasiblePlanError)
async def infeasible_plan_exception_handler(request: Request, exc: InfeasiblePlanError):
    """Return 422 for semantically well-formed but physically infeasible scenarios."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "Infeasible scenario", "detail": str(exc)},
    )


@app.exception_handler(GuardrailValidationError)
async def guardrail_exception_handler(request: Request, exc: GuardrailValidationError):
    """Return 422 for guardrail violations."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "Guardrail validation failure", "detail": str(exc)},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Catch-all: return 500 without leaking stack traces or secrets."""
    logger.error(f"Internal server error: {type(exc).__name__}: {str(exc)}", extra={"scenario_id": "system"})
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "detail": "An unexpected error occurred during schedule optimization.",
        },
    )


# --- Endpoints ---

@app.get("/health", tags=["Health"])
async def health_check():
    """
    GET /health -> 200 {"status":"ok"}.
    Must be ready immediately on start and must NOT depend on LLM.
    """
    return {"status": "ok"}


@app.post(
    "/optimize-energy",
    response_model=OptimizeEnergyResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Malformed JSON or structural validation error"},
        422: {"model": ErrorResponse, "description": "Semantically invalid or physically infeasible scenario"},
        500: {"model": ErrorResponse, "description": "Controlled internal error"},
    },
    tags=["Optimization"],
)
async def optimize_energy(req: OptimizeEnergyRequest):
    """
    POST /optimize-energy -> JSON in, JSON out.
    Pipeline:
      1. Request validation (Pydantic models)
      2. LLM operator-note interpretation
      3. Deterministic guardrail enforcement
      4. Exact Linear Programming optimization (HiGHS LP)
      5. Final independent validator replay
      6. Return canonical response
    """
    scenario_id = req.scenario_id
    t_start = time.monotonic()
    extra_log = {"scenario_id": scenario_id}
    logger.info(f"Received request for scenario {scenario_id} with {len(req.operator_notes)} notes", extra=extra_log)

    try:
        # Enforce request-level timeout limit (25s)
        async with asyncio.timeout(config.REQUEST_TIMEOUT_LIMIT):
            # Step 1: Interpret operator notes via LLM
            t_llm_start = time.monotonic()
            directives = await interpret_operator_notes(req.operator_notes, req.battery)
            llm_duration = time.monotonic() - t_llm_start
            logger.info(f"LLM interpreted {len(directives)} directives in {llm_duration:.3f}s", extra=extra_log)

            # Step 2: Math Optimizer (Exact HiGHS Linear Program)
            t_opt_start = time.monotonic()
            try:
                hourly_plan, total_grid, total_cost, peak_grid = optimize_energy_schedule(
                    req.hours, req.battery, directives
                )
            except InfeasiblePlanError as inf_err:
                logger.warning(f"Initial optimization infeasible: {inf_err}", extra=extra_log)
                raise inf_err

            opt_duration = time.monotonic() - t_opt_start
            logger.info(f"HiGHS LP solved in {opt_duration:.3f}s: total_cost={total_cost:.2f} BDT", extra=extra_log)

            # Step 3: Final Validator (Independent physics and constraint replay)
            try:
                validate_plan(
                    req.hours,
                    req.battery,
                    directives,
                    hourly_plan,
                    total_grid,
                    total_cost,
                    peak_grid,
                    tolerance=0.01,
                )
            except PlanValidationError as val_err:
                logger.error(f"Plan validation failed: {val_err}", extra=extra_log)
                raise RuntimeError(f"Plan validation failed: {val_err}")

            total_duration = time.monotonic() - t_start
            logger.info(f"Successfully finished scenario {scenario_id} in {total_duration:.3f}s", extra=extra_log)

            # Generate informative plan summary
            active_directives_desc = [
                d.directive_type for d in directives if d.applies
            ]
            applied_str = ", ".join(active_directives_desc) if active_directives_desc else "None (standard operation)"
            plan_summary = (
                f"Optimized 24h schedule for {scenario_id}: "
                f"total grid import {total_grid:.2f} kWh, total cost {total_cost:.2f} BDT, peak grid {peak_grid:.2f} kWh. "
                f"Active directives applied: {applied_str}."
            )

            return OptimizeEnergyResponse(
                scenario_id=scenario_id,
                directive_interpretation=directives,
                hourly_plan=hourly_plan,
                total_grid_kwh=total_grid,
                total_cost_bdt=total_cost,
                peak_grid_kwh=peak_grid,
                plan_summary=plan_summary,
            )

    except TimeoutError:
        logger.error("Request exceeded 25s timeout limit", extra=extra_log)
        return JSONResponse(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            content={"error": "Timeout", "detail": "Energy schedule optimization exceeded 25 seconds"},
        )


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def web_ui():
    """Interactive preview dashboard and testing console for GridWise LLM API."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>GridWise LLM - API Console</title>
      <script src="https://cdn.tailwindcss.com"></script>
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
      <style>body { font-family: 'Plus Jakarta Sans', sans-serif; }</style>
    </head>
    <body class="bg-slate-50 text-slate-800 min-h-screen">
      <div class="max-w-6xl mx-auto px-4 py-8">
        <header class="flex justify-between items-center pb-6 border-b border-slate-200">
          <div>
            <div class="flex items-center gap-3">
              <span class="inline-block w-3.5 h-3.5 rounded-full bg-emerald-500 animate-pulse"></span>
              <h1 class="text-2xl font-bold tracking-tight text-slate-900">GridWise LLM API</h1>
            </div>
            <p class="text-sm text-slate-500 mt-1">BUP CSE Fest 2026 Hackathon &bull; Smart Campus Microgrid Optimizer</p>
          </div>
          <div class="flex items-center gap-3">
            <a href="/docs" target="_blank" class="px-3.5 py-1.5 text-xs font-semibold bg-slate-200 hover:bg-slate-300 text-slate-700 rounded-lg transition-colors">
              Interactive OpenAPI Docs
            </a>
            <span class="px-2.5 py-1 text-xs font-medium bg-emerald-100 text-emerald-800 rounded-full">
              Status: Operational
            </span>
          </div>
        </header>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 my-8">
          <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
            <div class="text-xs uppercase font-semibold text-slate-500 tracking-wider">Exact Endpoints</div>
            <div class="mt-2 space-y-2">
              <div class="flex items-center justify-between text-sm font-mono bg-slate-50 p-2 rounded border border-slate-100">
                <span class="text-emerald-600 font-bold">GET</span>
                <span class="text-slate-700">/health</span>
              </div>
              <div class="flex items-center justify-between text-sm font-mono bg-slate-50 p-2 rounded border border-slate-100">
                <span class="text-blue-600 font-bold">POST</span>
                <span class="text-slate-700">/optimize-energy</span>
              </div>
            </div>
          </div>

          <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
            <div class="text-xs uppercase font-semibold text-slate-500 tracking-wider">Optimizer Engine</div>
            <div class="mt-2 text-sm text-slate-600 space-y-1">
              <div class="flex justify-between"><span>Solver:</span><strong class="text-slate-800">HiGHS (Exact LP)</strong></div>
              <div class="flex justify-between"><span>Variables:</span><strong class="text-slate-800">96 LP variables</strong></div>
              <div class="flex justify-between"><span>Constraints:</span><strong class="text-slate-800">49 Equality Equations</strong></div>
            </div>
          </div>

          <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
            <div class="text-xs uppercase font-semibold text-slate-500 tracking-wider">Guardrails & Directives</div>
            <div class="mt-2 text-sm text-slate-600 space-y-1">
              <div>&bull; solar_reduction (factor [0, 1])</div>
              <div>&bull; minimum_battery_reserve (kWh / %)</div>
              <div>&bull; no_charge / no_discharge_window</div>
              <div>&bull; max_grid_window &bull; no_op distractor</div>
            </div>
          </div>
        </div>

        <section class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-lg font-bold text-slate-900">Live API Tester (Scenario Runner)</h2>
            <button id="testBtn" onclick="runHealthCheck()" class="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white text-sm font-semibold rounded-lg transition-colors">
              Run Health & Sample Verification
            </button>
          </div>
          <div id="outputContainer" class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-xs overflow-x-auto min-h-[160px]">
            Ready to test. Click button above or execute curl / scripts.
          </div>
        </section>
      </div>

      <script>
        async function runHealthCheck() {
          const out = document.getElementById('outputContainer');
          out.textContent = "Checking /health endpoint...";
          try {
            const hRes = await fetch('/health');
            const hData = await hRes.json();
            out.textContent = "Health check response: " + JSON.stringify(hData, null, 2) + "\\n\\nTesting sample payload against /optimize-energy...";

            const sampleReq = {
              scenario_id: "BROWSER-TEST-001",
              operator_notes: ["Expect an 80% reduction in rooftop solar during the 1-3 PM maintenance window."],
              hours: Array.from({length: 24}, (_, i) => ({
                hour: i,
                demand_kwh: [30, 28, 25, 24, 25, 30, 45, 60, 75, 90, 105, 115, 120, 115, 105, 95, 85, 100, 120, 110, 90, 70, 50, 38][i],
                solar_kwh: [0, 0, 0, 0, 0, 2, 10, 30, 60, 85, 100, 110, 115, 110, 90, 65, 35, 10, 1, 0, 0, 0, 0, 0][i],
                tariff_bdt_per_kwh: [6.5, 6.5, 6.5, 6.5, 6.5, 6.5, 8.0, 8.0, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5, 10.5, 14.0, 14.0, 14.0, 14.0, 14.0, 10.5, 8.0][i]
              })),
              battery: {
                capacity_kwh: 200.0,
                initial_energy_kwh: 100.0,
                minimum_energy_kwh: 30.0,
                max_charge_kwh_per_hour: 50.0,
                max_discharge_kwh_per_hour: 50.0
              }
            };

            const optRes = await fetch('/optimize-energy', {
              method: 'POST',
              headers: {'Content-Type': 'application/json'},
              body: JSON.stringify(sampleReq)
            });
            const optData = await optRes.json();
            out.textContent = "SUCCESS! Health OK (200).\\n\\nPOST /optimize-energy Response (Status: " + optRes.status + "):\\n" + JSON.stringify(optData, null, 2);
          } catch (err) {
            out.textContent = "Error during test: " + err.message;
          }
        }
      </script>
    </body>
    </html>
    """


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.PORT)
