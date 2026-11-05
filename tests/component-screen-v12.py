"""Conditional component screens, NOT electrical or physical qualification."""
import json, math, itertools
from pathlib import Path
# Series sums retain the same deterministic worst-case relative bound as each member.
tol=.001+25e-6*100
pairs={"charger_TS_bottom":[30900,240],"logic_feedback_top":[1000000,60000]}
series={}
for name,rs in pairs.items():
 vals=[sum(r*(1+t*tol) for r,t in zip(rs,signs)) for signs in itertools.product([-1,1],repeat=2)]
 nominal=sum(rs)
 assert math.isclose(min(vals),nominal*(1-tol))
 assert math.isclose(max(vals),nominal*(1+tol))
 series[name]={'nominal_ohm':nominal,'min_ohm':min(vals),'max_ohm':max(vals)}
# Assumed USB maximum 5.5 V; charger minimum oscillator 1.32 MHz.
# L minimum combines -20% initial and 20% DC bias. Temperature not characterized.
chg_l=1e-6*.8*.8
chg_ripple=5.5/(4*1.32e6*chg_l)
chg_peak=3.2+chg_ripple/2
assert chg_peak<6.3 # 20%-drop characterization current, not thermal guarantee
# Logic candidate: 2.2 uH, -20% tolerance, -30% bias, allows a lower L than normal operation.
logic_l=2.2e-6*.8*.7
assert logic_l>1e-6
# Deliberately loose PWM ripple bound V/(f*L), not a loop simulation.
logic_ripple_bound=5.5/(2.2e6*logic_l)
logic_peak=3.3*.6/(2.5*.8)+logic_ripple_bound/2
assert logic_peak<6.2
# Receiver 32 ohm +/-15%; input-power limit only, not safe acoustic loudness.
rmin=32*.85
receiver_rms=math.sqrt(.020*rmin)
assert receiver_rms<.8
r={'scope':'Analytical candidate screens; all conditions and temperature limits require validation. No release.',
'series_resistors':series,'resistor_bound':'.1% initial plus 25 ppm/C over assumed 100 C; aging excluded',
'charger':{'L_candidate':'XGL4020-102MEC','L_assumed_H':chg_l,'ripple_A':chg_ripple,'peak_at_3_2A_average_A':chg_peak,'dc_bias_20percent_A':6.3,'blockers':['8 A cycle-by-cycle fault threshold can exceed 20-percent-drop current','temperature/core losses and loop response unverified','5.5 V envelope depends on USB protection validation']},
'logic':{'L_candidate':'XGL4020-222MEC','L_assumed_H':logic_l,'peak_bound_at_0_6A_load_A':logic_peak,'blockers':['0.6 A load assumption must be measured','current-limit overload is outside this normal-load screen','L/C loop response and effective capacitance unverified','stock not confirmed']},
'audio':{'receiver':'AR01232MS-SC12-WP-R','nominal_20mW_Vrms':math.sqrt(.02*32),'20mW_at_min_impedance_Vrms':receiver_rms,'30mW_at_min_impedance_Vrms':math.sqrt(.03*rmin),'blockers':['modem differential full-scale and gain unknown','impedance is frequency dependent; measured power/acoustics required','no safe acoustic volume conclusion']},'fabrication_ready':False}
Path('output/component-screen-v12.json').write_text(json.dumps(r,indent=2))
print(json.dumps(r,indent=2))
