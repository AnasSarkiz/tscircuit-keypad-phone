import itertools,json
from pathlib import Path
# Selected 0.1% resistors, +/-25ppm/C; screening resistor temperature -40..85C.
# Drift is bounded independently per resistor, no assumed matching.
tol=.001+25e-6*65
v=[fb*(1+rt/rb)+ib*rt for fb,rt,rb,ib in itertools.product([.495,.505],[66500*(1-tol),66500*(1+tol)],[10000*(1-tol),10000*(1+tol)],[-1e-7,1e-7])]
assert len(v)==16 and min(v)>3.7 and max(v)<3.95
Path('output/feedback-v21.json').write_text(json.dumps({'nominal_V':3.825,'screened_min_V':min(v),'screened_max_V':max(v),'resistor_temperature_C':[-40,85],'resistor_TCR_assumption_ppm_per_C':25,'qualification':False,'excluded':['load/line regulation bounds','ripple/transients','aging','actual resistor temperature','fault protection']},indent=2))
print('PASS 16 feedback corners',min(v),max(v))
