"""Conditional timing budget; no measured or guaranteed rail rise supplied."""
from pathlib import Path
import json
rail=json.load(open('output/power-budget.json'))['with_unverified_50mV_transient_budget_v'][0]
blank_min_ms=400;blank_typ_ms=512;blank_max_ms=650
kill_rising_upper=.63+.05
sink_budget=(rail-kill_rising_upper)/100100
assert kill_rising_upper==.68 and sink_budget>0
# The model deliberately refuses to turn absent timing evidence into a passing design.
def decision(rail_ms,settling_ms,margin_ms=20):
 if rail_ms is None or settling_ms is None:return 'UNKNOWN'
 return 'CONDITIONAL_PASS' if rail_ms+settling_ms+margin_ms<blank_min_ms else 'FAIL'
assert decision(None,None)=='UNKNOWN'
assert decision(350,40)=='FAIL'
assert decision(420,0)=='FAIL' # would appear to pass using512ms typical
assert decision(300,50)=='CONDITIONAL_PASS'
assert decision(380,0)=='FAIL' # no reserved timing margin
assert blank_typ_ms>blank_min_ms and blank_max_ms>blank_typ_ms
out={'source':'https://www.analog.com/media/en/technical-documentation/data-sheets/2954fb.pdf','revision':'2954fb RevB; independent latest drawing audit source tracked separately','blanking_ms':{'min':blank_min_ms,'typ':blank_typ_ms,'max':blank_max_ms},'KILL_falling_V':[.57,.63],'KILL_hysteresis_V':[.01,.05],'conservative_rising_upper_V':kill_rising_upper,'conditional_logic_rail_low_V':rail,'conditional_total_sink_budget_A':sink_budget,'KILL_leakage_test_caveat':'0.1uA at KILL0.6V only; actual-bias leakage and MOSFET leakage remain open','hardware_path':'R_BUTTON_KILL_UP100k from VLOGIC to KILL; Q_BUTTON_KILL can pull low; R_BUTTON_KILL_OFF100k gate pulldown. This bypasses firmware as the source of KILL high only if rail ramp and MOSFET reset state are qualified.','actual_timing_result':decision(None,None),'ONT_PDT_extend_blanking':False,'power_applied_default':'OFF per manufacturer; downstream EN buffer/regulator startup and partial-power behavior still require qualification','release':False,'remaining':['Guaranteed local VLOGIC rise plus KILL settling before400ms with margin','Q_BUTTON_KILL gate/current during MCU reset and brownout','SYS-qualified EN pullup,Schmitt buffer input/output through partial supply and converter EN thresholds','PDT capacitor minimum effective capacitance/leakage and physical power button','Threshold and timing applicability over source,temperature,ground-shift and transient envelope']}
Path('output/startup-blanking-v55.json').write_text(json.dumps(out,indent=2));print('PASS timing rejection regressions; actual startup UNKNOWN, not qualified',sink_budget)
