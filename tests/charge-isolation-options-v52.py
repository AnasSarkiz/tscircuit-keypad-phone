from pathlib import Path
import json
j=json.load(open('sourcing/charge-isolation-options-v52.json'))
b=j['conditional_CE_budget'];budget=(b['SYS_assumption_V']-b['CE_high_V'])/b['pullup_max_ohm']
assert abs(budget*1e6-b['total_sink_limit_uA'])<1e-6
assert b['universal_guarantee'] is False and j['release'] is False
# Sensitivity illustration, not a qualified composite switch leakage model.
# Two10uA sink contributions plus1uA CE leakage consume the entire assumed budget.
v=3.4-100100*21e-6
assert v<1.3
# VDD=0 protection rated3.6V cannot support a4.2V signal claim.
assert 4.2>3.6
# Lowering pullup resistance helps static margin only; it cannot establish ramp isolation.
v47=3.4-(47000*1.001)*21e-6
assert v47>1.3
out={'conditional_budget_uA':budget*1e6,'illustrative_21uA_sink_CE_V':v,'illustrative_47k_CE_V':v47,'47k_selected':False,'partial_power_qualified':False,'integration_allowed':False,'tests':'Budget arithmetic; reject21uA sum at assumed3.4V/100.1k; reject4.2V signal under3.6V powered-off rating; resistor sensitivity does not imply selection','release':False}
Path('output/charge-isolation-options-v52-checks.json').write_text(json.dumps(out,indent=2));print(out)
