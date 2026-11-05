"""Requirements for a hypothetical qualified 1S pack. No pack or converter approved."""
import itertools,json,math
from pathlib import Path
aux=3.3*.6/.8+5.3*.131/.75
rows=[]
for im,voc,res,eff in itertools.product([2,3],[3.6,3.8,4.1],[.05,.1,.2],[.8,.85]):
 p=3.8*im/eff+aux;disc=voc*voc-4*res*p
 sys=(voc+math.sqrt(disc))/2 if disc>=0 else None;i=p/sys if sys else None
 rows.append({'modem_A':im,'OCV_V':voc,'shared_R_ohm':res,'assumed_converter_efficiency':eff,'SYS_V':sys,'battery_A':i,'BATFET_loss_at_30mohm_W':i*i*.03 if i else None,'screen_pass':bool(sys and sys>=3.2 and i<=5.4)})
worst=3.8*3/.8+aux
req={'SYS_min_V':3.2,'GSM_system_input_W':worst,'pack_current_at_floor_A':worst/3.2,'SYS_min_for_5_4A_V':worst/5.4,'Rmax_at_3_6V_OCV_and_3_2V_SYS_ohm':(3.6-3.2)/(worst/3.2),'charger_RMS_discharge_limit_A':6,'design_ceiling_with_10percent_reserve_A':5.4}
assert req['pack_current_at_floor_A']>5.4
assert any(x['screen_pass'] for x in rows if x['modem_A']==3)
assert any(not x['screen_pass'] for x in rows if x['modem_A']==3)
r={'requirements':req,'scenarios':rows,'scope':'36 conditional DC scenarios. TPS552892 operating-point efficiency/current limit and pack not qualified. Shared resistance includes cell, PCM, harness, connector, charger and copper. BATFET loss assumes fully on; excludes charging and switching loss. 6A is charger recommended RMS limit, not proof of thermal safety.','pack_approved':False,'fabrication_ready':False}
Path('output/high-current-requirements-v15.json').write_text(json.dumps(r,indent=2));print(json.dumps(req,indent=2))
