import json,itertools,math
from pathlib import Path
rows=[]
for im,eta,bl,voc,r in itertools.product([1,1.2,2],[.8,.85,.9],[False,True],[3.6,3.8,4.1],[.05,.1,.2]):
 p=3.8*im/eta+3.3*.1/.8+(5.3*.131/.75 if bl else 0);v=(voc+math.sqrt(voc*voc-4*r*p))/2;i=p/v
 rows.append(dict(modem_scenario_A=im,eta_assumed=eta,backlight=bl,OCV_V=voc,shared_R_ohm=r,SYS_V=v,pack_A=i,conditional_pass=v>=3.2 and i<=3.6))
counts={str(im):sum(x['conditional_pass'] for x in rows if x['modem_scenario_A']==im) for im in [1,1.2,2]}
assert counts['1']==54 and counts['1.2']<54 and counts['2']==44
out={'source_caveat':'A7672S_V1.00 says>=1A supply; Table8 lists1A as TYP not MAX. No guaranteed peak envelope or current SKU/firmware match established. 1.2A is sensitivity, not a vendor limit.','conditional_pass_counts_out_of54':counts,'cases':rows,'maximum_modem_A_for_worst_shared_R_corner_at_assumed80percent_efficiency':(.8*(3.2*(3.6-3.2)/.2-3.3*.1/.8-5.3*.131/.75)/3.8),'carrier_approved':False,'replacement_selected':False,'power_architecture_qualified':False}
Path('output/modem-alternative-v26.json').write_text(json.dumps(out,indent=2));print(counts,out['maximum_modem_A_for_worst_shared_R_corner_at_assumed80percent_efficiency'])
