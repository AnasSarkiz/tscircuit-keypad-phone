"""Design arithmetic, not a transient/thermal simulation or cell qualification."""
import itertools,json
from pathlib import Path
# Q1 datasheet reference +/-1%; add line and load regulation separately.
# 0.1% divider values are requirements, not assumed for arbitrary substitutes.
vals=[v*(1+rt/rb)*line*load for v,rt,rb,line,load in itertools.product([.495,.505],[1.06e6*.999,1.06e6*1.001],[200e3*.999,200e3*1.001],[.995,1.005],[.995,1.005])]
lo,hi=min(vals),max(vals)
# 50mV is a reserved design budget which hardware must demonstrate.
assert lo-.05>=3.0 and hi+.05<=3.3
assert hi*1.05>3.3 # power-save must not be allowed on the shared rail
# LTE-only branch: 2A modem envelope + .6A logic at 3.15V + .1A LED at3.4V.
# Conservative assumed efficiencies; no claim of measured consumption/runtime.
aux_input=(3.15*.6+3.4*.1)/(.85*3.5)
load=2+aux_input
assert load>2 # excludes original 2A candidate
# Simple modem path resistance allocation; independent of unknown cell impedance.
path_budget=(3.6-3.3-.1)/load
results={'logic_nominal_v':.5*(1+1.06e6/200e3),'corner_count':len(vals),'logic_dc_v':[lo,hi],'with_unverified_50mV_transient_budget_v':[lo-.05,hi+.05],'power_save_upper_example_v':hi*1.05,'logic_mode':'forced PWM required','lte_aux_input_budget_a':aux_input,'lte_total_input_budget_a':load,'gsm_total_input_budget_a':load+1,'protected_pack_target_continuous_a':4,'shared_path_resistance_budget_ohm_at_3V6_ocv_full_LTE_load':path_budget,'limits':['Assumed logic load, efficiency and input voltage must be measured','No DC-bias, ESR, transient, thermal, aging or cold-cell model','3A cylindrical candidate has little current margin for LTE and fails GSM budget','Whole path includes cell protection wiring connector copper and switching element; AC impedance is not DC pulse resistance','No battery runtime prediction']}
Path('output/power-budget.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
