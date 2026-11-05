import json,math
from pathlib import Path
rows=[]
for hours in [48,1000,8760,87600]:
 age=.03*math.log10(hours/48);base=4.7*.9*.85*(1-age)
 rows.append({'elapsed_hours_scenario':hours,'aging_loss_fraction_scenario':age,'unbiased_capacitance_uF_product_model':base,'minimum_required_DC_bias_retention_fraction':1.5/base})
assert all(0<r['minimum_required_DC_bias_retention_fraction']<1 for r in rows)
df_esr=.10/(2*math.pi*1000*4.7e-6)
assert df_esr>.2 # This is not a measured failure: DF alone is insufficient proof.
c=json.loads(Path('routing/usb-layered-v34.json').read_text());r=next(x for x in c['routes'] if x['name']=='DIRECT_LDO_COUT_RETURN');length=sum(math.dist(a,b) for a,b in zip(r['points'],r['points'][1:]));assert r['layer']=='top' and r['pads']==[['C_USB_AUX_OUT',2],['U_USB_AUX',2]]
assert not any(v['name']=='G_AUX_OUT' for v in c['vias'])
out={'MLCC':'C0805C475K3RACTU','manufacturer_source':'https://yageogroup.com/download/specsheet/C0805C475K3RACTU','nominal_uF':4.7,'tolerance_fraction':.1,'TCC_fraction_at_0V':.15,'aging_per_decade_hour':.03,'referee_hours':48,'requirements':{'effective_min_uF':1.5,'effective_max_uF':47,'ESR_max_ohm':.2},'scenario_corners_not_combined_guarantees':rows,'DF_at1kHz_nominal_C_ESR_equivalent_ohm':df_esr,'DF_interpretation':'10% DF condition at1kHz permits >0.2ohm; does not prove failure or bound ESR at the regulator stability frequencies. Manufacturer simulation expressly typical.','polymer_candidate':{'MPN':'T520A226M010ATE080','source':'https://search.kemet.com/download/specsheet/T520A226M010ATE080','tolerance_only_range_uF':[22*.8,22*1.2],'ESR_ohm_at100kHz25C':.08,'allowed_ESR_increase_factor_to_limit':.2/.08,'body_max_mm':[3.4,1.8,1.8],'installed':False,'remaining':['cold/hot/aged ESR over relevant frequencies','capacitance over environment/life','startup with22uF and surge/polarity','new footprint and fit','cost/availability qualification']},'direct_return':{'length_mm':length,'width_mm':r['width'],'DC_resistance_ohm_assuming35um_Cu20C':1.724e-5*length/(r['width']*.035),'scope':'nominal DC estimate only, not AC impedance/loop validation'},'qualified':False}
Path('output/ldo-capacitor-v34.json').write_text(json.dumps(out,indent=2));print('PASS direct return',length,'mm; capacitor qualification remains open; 10-year scenario retention',rows[-1]['minimum_required_DC_bias_retention_fraction'])
