import json,math,itertools
from pathlib import Path
aux=3.3*.1/.8+5.3*.131/.75
rows=[]
for load,eta,vin in itertools.product([2,3],[.8,.85,.9,1.0],[3.0,3.2]):
 i=(3.8*load/eta+aux)/vin
 rows.append(dict(load_A=load,assumed_efficiency=eta,VIN_V=vin,pack_A=i,below_design_3_6A=i<=3.6,below_minimum_PCM_trip_4A=i<4))
assert all(r['pack_A']>4 for r in rows if r['load_A']==3 and r['VIN_V']==3)
p=7.6/.8+aux
required_v=max(3.0,p/3.6)
rmax=required_v*(3.6-required_v)/p
v=(3.6+math.sqrt(3.6**2-4*.2*p))/2
assert v<3 and p/v>3.6
# Divider tolerance, excludes unbounded full-temperature FB leakage, dynamic error.
rhi=845000;rlo=158000;t=.001
lo=.588*(1+rhi*(1-t)/(rlo*(1+t)));hi=.612*(1+rhi*(1+t)/(rlo*(1-t)))
out={'source':'https://www.analog.com/media/en/technical-documentation/data-sheets/3113f.pdf','candidate':'LTC3113IDHD#PBF','selected':False,'guarantees_table_conditions':'VIN3.3V,VOUT3.8V; full-temperature I-grade only where indicated. Not a universal output-current guarantee.','input_limit_min_A':5.8,'input_limit_max_A':9.8,'soft_start_2ms_is_typical':True,'pack_current_sensitivity':rows,'aux_W_assumed':aux,'worst_LTE_power_W':p,'required_SYS_V_for_3_6A':required_v,'Rmax_at_OCV3_6_ohm':rmax,'shared_200mohm_SYS_V':v,'shared_200mohm_pack_A':p/v,'divider_0_1percent_voltage_interval_excluding_FB_leak_dynamic':[lo,hi],'DFN_body_mm':[5,4,.75],'exposed_PGND_pin':17,'footprint_verified':False,'release':False}
Path('output/ltc3113-v27.json').write_text(json.dumps(out,indent=2))
print('PASS candidate rejects 200mohm corner; Rmax',rmax,'required SYS',required_v,'divider',lo,hi)
