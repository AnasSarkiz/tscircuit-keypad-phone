import itertools,json
rt=845000;rb=100000;t=.0035
lo=.405*.98*(1+rt*(1-t)/(rb*(1+t)))-25e-9*rt*(1+t)
hi=.405*1.02*(1+rt*(1+t)/(rb*(1-t)))*1.03+25e-9*rt*(1+t)
assert lo>2.5
assert hi<4.58
# 3.0V conservative shared logic minimum; logic gate VOH at <=100uA load.
gate_high_min=3.0-.15
assert gate_high_min>2.5 # AO3400A specified Rds at2.5V
assert .1<.65 # AO3400A min VGS(th), low current logic output VOL
# Sensitivity at5uA OFF-switch leakage plus charger CE input leakage.
# Extracted AOS table gives5uA at55C; no125C guarantee is inferred.
ce_high_min=3.0-(5e-6+1e-6)*100000*1.01
assert ce_high_min>1.3
rows=[]
for request,regn,cold,hot in itertools.product([False,True],repeat=4):
 ce_low=request and regn and cold and hot
 rows.append(dict(request=request,regn_ready=regn,cold_ok=cold,hot_ok=hot,charging_permitted=ce_low))
result={'REGN_falling_min_V':lo,'REGN_release_max_V':hi,'REGN_min_at_5V_input_V':4.58,'MOS_gate_high_min_V':gate_high_min,'CE_high_min_with_one_switch_off_V':ce_high_min,'truth_table':rows,'scope':'DC and Boolean model only; 5uA leakage is not qualified over the full intended temperature range; supply ramp, gate capacitance, delay, physical temperature coupling, watchdog and thermal behavior remain unvalidated'}
open('output/charge-enable-v9.json','w').write(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
