"""Conditional RC exploration, explicitly not a hardware timing qualification."""
import json,math
from pathlib import Path
from math import dist
blank=json.load(open('output/startup-blanking-v55.json'));routes=json.load(open('routing/usb-layered-v55.json'))['routes']
vmin=blank['conditional_logic_rail_low_V'];rmax=100100;threshold=.68
# This excludes ground shift, nonlinear leakage, pin capacitance spread and EMI.
def crossing_s(cap_f,sink_a):
 if cap_f is None or sink_a is None:return None
 final=vmin-sink_a*rmax
 if final<=threshold:return math.inf
 return -rmax*cap_f*math.log1p(-threshold/final)
assert crossing_s(None,None) is None
assert math.isinf(crossing_s(100e-12,25e-6))
assert crossing_s(1e-9,20e-6)>crossing_s(100e-12,20e-6)>crossing_s(100e-12,0)
rows=[dict(assumed_capacitance_pF=c,assumed_sink_uA=i,conditional_threshold_crossing_us=crossing_s(c*1e-12,i*1e-6)*1e6) for c in [100,1000] for i in [0,10,20]]
lengths={n:sum(sum(dist(a,b) for a,b in zip(t['points'],t['points'][1:])) for t in routes if t['net']==n) for n in ['BUTTON_INT_N','BUTTON_KILL_BRANCH']}
out={'conditional_examples_only':True,'assumptions_not_verified':True,'route_copper_length_sum_mm':lengths,'examples':rows,'model_limits':['Step rail assumption; actual rail ramp remains unknown','No guaranteed total load capacitance or leakage at actual bias/temperature','No EMI/crosstalk/ground-shift assessment; routed length is not a capacitance guarantee','Actual400ms KILL qualification remains UNKNOWN'],'geometry_exceptions':['88mm KILL bottom segment','95.4mm INT bottom segment'],'release':False}
Path('output/startup-rc-budget-v55.json').write_text(json.dumps(out,indent=2));print('PASS conditional model regression; hardware qualification remains UNKNOWN',lengths)
