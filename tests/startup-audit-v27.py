import json
from pathlib import Path
# Sufficient KILL-rise condition, not a claim about measured parasitics or leakage.
vlogic=3.049;r=101000;leak_allocation=2.1e-6;c_allocation=1e-9;vfinal=vlogic-r*leak_allocation;vrequired=.63+.05
import math
rc_delay=-r*c_allocation*math.log(1-vrequired/vfinal)
assert vfinal>vrequired and rc_delay<.001
out={'KILL_required_high_V_conservative':vrequired,'Vlogic_scenario_min_V':vlogic,'leakage_allocation_A_NOT_verified':leak_allocation,'KILL_node_capacitance_allocation_F_NOT_verified':c_allocation,'KILL_static_final_V':vfinal,'RC_after_logic_rise_s':rc_delay,'minimum_blank_s':.4,'required_logic_rise_s_less_than':.4-rc_delay,'interpretation':'KILL is pulled up by logic rail through100k; MCU firmware does NOT need to assert it within400ms. Converter rail and KILL node must rise in time. ADC/firmware boot delay cannot be substituted for actual rail measurement.','remaining':['qualified supply >=2.7V under load/ramp','buffer thresholds over actual supply trajectory','all-temperature off leakage and KILL parasitics','loaded converter startup','2.2uF PDT timing has no established guaranteed long-press bound','forced long-press may interrupt modem shutdown; controller/firmware contract must account for it'],'hardware_qualified':False}
Path('output/startup-audit-v27.json').write_text(json.dumps(out,indent=2));print('PASS conditional KILL margin; MCU boot is not the blanking dependency; hardware gate retained')
