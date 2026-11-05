"""Sensitivity analysis, not measured thermal qualification."""
import json
# TI TPS709 DBV RthetaJA 212.1 C/W; board-specific thermal resistance unknown.
r=[]
for vin in [5.25,20,24]:
 for ma in [2,5,10,20]:
  p=(vin-3.234)*ma/1000
  r.append({'vin_V':vin,'load_mA':ma,'dissipation_W':p,'rise_C_at_datasheet_theta':p*212.1,'junction_at_60C':60+p*212.1,'under_125C':60+p*212.1<125})
open('output/aux-thermal-v7.json','w').write(json.dumps({'scope':'load sensitivity; 2-20mA are assumed envelopes, not a completed maximum-current budget; thermal metric is board-dependent','rows':r},indent=2))
assert all(x['under_125C'] for x in r if x['vin_V']==5.25)
assert not all(x['under_125C'] for x in r)
print('PASS: nominal-input sensitivity; identifies 24V/20mA thermal failure scenario')
