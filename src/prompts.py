SYSTEM_PROMPT = """You are the expert grid operation natural-language directive interpreter for the GridWise energy management system.
Your job is to read 1 to 3 operator notes and translate EACH note into exactly ONE structured directive specification using an internal representation.

CRITICAL DIRECTIVE RULES:
1. Supported Directive Types (ONLY these 6 types are allowed - NEVER invent any other type):
   - "solar_reduction": Usable rooftop solar generation is curtailed or reduced during a window.
   - "minimum_battery_reserve": Battery state of charge must remain at or above a threshold (either in kWh or percent of battery capacity).
   - "no_charge_window": Battery charging is prohibited / isolated / disabled during a window.
   - "no_discharge_window": Battery discharging is prohibited / isolated / disabled during a window.
   - "max_grid_window": Grid power import must not exceed a specified ceiling (kWh) during a window.
   - "no_op": The note is an informational announcement, unrelated notice (menus, seminars, contests, deadlines), or has no operational constraint.

2. Time Windows:
   - All time windows are START-INCLUSIVE and END-EXCLUSIVE in 24-hour clock format.
   - "start_hour": integer 0 to 23.
   - "end_hour_exclusive": integer 0 to 24 (use 24 if window extends through end of day 23:59).
   - Examples:
     * "1 PM to 3 PM" -> start_hour: 13, end_hour_exclusive: 15 (covers hours 13 and 14).
     * "6 PM until 9 PM" -> start_hour: 18, end_hour_exclusive: 21 (covers hours 18, 19, 20).
     * "2 AM until 5 AM" -> start_hour: 2, end_hour_exclusive: 5 (covers hours 2, 3, 4).
     * "noon until three PM" -> start_hour: 12, end_hour_exclusive: 15.
     * Midnight wrap-around: "10 PM to 2 AM" -> start_hour: 22, end_hour_exclusive: 2.
   - When AM/PM is ambiguous, infer from context (e.g. solar cleaning/work occurs during daylight hours).

3. Value and Value Kinds:
   - For solar_reduction:
     * "drops to 20%" / "leave one-fifth": value=20, value_kind="percent_remaining" (or value=0.2, value_kind="fraction_remaining").
     * "80% reduction" / "reduced by 80%": value=80, value_kind="percent_reduction".
     * "half": value=0.5, value_kind="fraction_remaining".
     * "loses a quarter": value=25, value_kind="percent_reduction" (or value=0.75, value_kind="fraction_remaining").
   - For minimum_battery_reserve:
     * "Keep 50% in reserve": value=50, value_kind="percent_of_capacity".
     * "Reserve 80 kWh": value=80, value_kind="kwh".
   - For max_grid_window:
     * "at or below 60 kWh" / "must not exceed 60 kWh": value=60, value_kind="kwh".
   - For no_charge_window and no_discharge_window:
     * value=null, value_kind=null.
   - For no_op:
     * relevant=false, directive_type="no_op", start_hour=null, end_hour_exclusive=null, value=null, value_kind=null.

4. Output Format:
   You MUST return valid JSON adhering strictly to this schema:
   {
     "directives": [
       {
         "note_index": 0,
         "relevant": true,
         "directive_type": "solar_reduction",
         "start_hour": 13,
         "end_hour_exclusive": 15,
         "value": 20,
         "value_kind": "percent_remaining",
         "explanation": "Clear brief explanation"
       }
     ]
   }
   There must be EXACTLY one entry per note in order 0..N-1.
   Do not include Markdown code blocks or any extraneous text. Only output raw valid JSON.
"""

FEW_SHOT_EXAMPLES = [
    {
        "notes": ["PV production will drop to about 20% between 13:00 and 15:00"],
        "battery_capacity_kwh": 200.0,
        "output": {
            "directives": [
                {
                    "note_index": 0,
                    "relevant": True,
                    "directive_type": "solar_reduction",
                    "start_hour": 13,
                    "end_hour_exclusive": 15,
                    "value": 20.0,
                    "value_kind": "percent_remaining",
                    "explanation": "Solar output drops to 20% between 13:00 and 15:00."
                }
            ]
        }
    },
    {
        "notes": ["Expect an 80% reduction in rooftop solar during the 1-3 PM maintenance window"],
        "battery_capacity_kwh": 200.0,
        "output": {
            "directives": [
                {
                    "note_index": 0,
                    "relevant": True,
                    "directive_type": "solar_reduction",
                    "start_hour": 13,
                    "end_hour_exclusive": 15,
                    "value": 80.0,
                    "value_kind": "percent_reduction",
                    "explanation": "80% curtailment in rooftop solar during 1 PM to 3 PM."
                }
            ]
        }
    },
    {
        "notes": ["Panel washing from one until three will leave roughly one-fifth of normal solar output"],
        "battery_capacity_kwh": 200.0,
        "output": {
            "directives": [
                {
                    "note_index": 0,
                    "relevant": True,
                    "directive_type": "solar_reduction",
                    "start_hour": 13,
                    "end_hour_exclusive": 15,
                    "value": 0.2,
                    "value_kind": "fraction_remaining",
                    "explanation": "One-fifth output remains from 13:00 to 15:00."
                }
            ]
        }
    },
    {
        "notes": ["Keep at least 50% of battery capacity in reserve from 6 PM until 9 PM"],
        "battery_capacity_kwh": 200.0,
        "output": {
            "directives": [
                {
                    "note_index": 0,
                    "relevant": True,
                    "directive_type": "minimum_battery_reserve",
                    "start_hour": 18,
                    "end_hour_exclusive": 21,
                    "value": 50.0,
                    "value_kind": "percent_of_capacity",
                    "explanation": "50% capacity reserve required from 18:00 to 21:00."
                }
            ]
        }
    },
    {
        "notes": ["Inverter relay testing: charger isolated from 10:00 to 14:00"],
        "battery_capacity_kwh": 250.0,
        "output": {
            "directives": [
                {
                    "note_index": 0,
                    "relevant": True,
                    "directive_type": "no_charge_window",
                    "start_hour": 10,
                    "end_hour_exclusive": 14,
                    "value": None,
                    "value_kind": None,
                    "explanation": "Battery charging is disabled between 10:00 and 14:00."
                }
            ]
        }
    },
    {
        "notes": ["Relay testing – no discharging from 5 PM till 8 PM"],
        "battery_capacity_kwh": 200.0,
        "output": {
            "directives": [
                {
                    "note_index": 0,
                    "relevant": True,
                    "directive_type": "no_discharge_window",
                    "start_hour": 17,
                    "end_hour_exclusive": 20,
                    "value": None,
                    "value_kind": None,
                    "explanation": "Battery discharging is forbidden between 17:00 and 20:00."
                }
            ]
        }
    },
    {
        "notes": ["Substation transformer work: grid import must not exceed 60 kWh between 12:00 and 16:00"],
        "battery_capacity_kwh": 300.0,
        "output": {
            "directives": [
                {
                    "note_index": 0,
                    "relevant": True,
                    "directive_type": "max_grid_window",
                    "start_hour": 12,
                    "end_hour_exclusive": 16,
                    "value": 60.0,
                    "value_kind": "kwh",
                    "explanation": "Grid import capped at 60 kWh from 12:00 to 16:00."
                }
            ]
        }
    },
    {
        "notes": ["Night grid maintenance: no charging allowed from 10 PM to 2 AM"],
        "battery_capacity_kwh": 180.0,
        "output": {
            "directives": [
                {
                    "note_index": 0,
                    "relevant": True,
                    "directive_type": "no_charge_window",
                    "start_hour": 22,
                    "end_hour_exclusive": 2,
                    "value": None,
                    "value_kind": None,
                    "explanation": "Charging prohibited across midnight from 22:00 to 02:00."
                }
            ]
        }
    },
    {
        "notes": [
            "Campus cafeteria serves biryani on Thursday.",
            "CSE Fest registration deadline extended to midnight."
        ],
        "battery_capacity_kwh": 200.0,
        "output": {
            "directives": [
                {
                    "note_index": 0,
                    "relevant": False,
                    "directive_type": "no_op",
                    "start_hour": None,
                    "end_hour_exclusive": None,
                    "value": None,
                    "value_kind": None,
                    "explanation": "Cafeteria menu notice is not an energy directive."
                },
                {
                    "note_index": 1,
                    "relevant": False,
                    "directive_type": "no_op",
                    "start_hour": None,
                    "end_hour_exclusive": None,
                    "value": None,
                    "value_kind": None,
                    "explanation": "Registration notice has no effect on grid operations."
                }
            ]
        }
    }
]
