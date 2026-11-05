import json,itertools,math
from pathlib import Path
rows=[]
for eta,backlight,voc,res in itertools.product([.8,.85,.9],[False,True],[3.6,3.8,4.1],[.05,.1,.2]):
 aux=3.3*.6/.8+(5.3*.131/.75 if backlight else 0)
 p=7.6/eta+aux;disc=voc*voc-4*res*p;sys=(voc+math.sqrt(disc))/2 if disc>=0 else None;i=p/sys if sys else None
 rows.append({'efficiency_assumed':eta,'backlight':backlight,'OCV_V':voc,'shared_R_ohm':res,'SYS_V':sys,'pack_A':i,'conditional_screen_pass':bool(sys and sys>=3.2 and i<=3.6)})
eta_needed=7.6/(3.2*3.6-3.3*.6/.8)
r={'scenarios':rows,'required_efficiency_backlight_off_at_SYS3_2V_pack3_6A':eta_needed,'scope':'54 LTE-only DC scenarios; 2A modem at3.8V and 0.6A logic at3.3V. Efficiency, impedance and transients unqualified; existing buck cannot implement this hypothetical regulated rail below dropout. Backlight-off mode is a requirement candidate, not an implemented measured guarantee.','releaseRequires':['persistent LTE-only configuration verified across resets','carrier voice acceptance','actual converter and protection qualification','pack impedance/discharge/PCM characterization','hardware undervoltage monitor and shutdown reserve','backlight-off control verified if used in budget'],'GSM_approved':False,'battery_approved':False,'fabrication_ready':False}
assert 0<eta_needed<1
assert any(x['conditional_screen_pass'] for x in rows)
assert any(not x['conditional_screen_pass'] for x in rows)
Path('output/lte-budget-v16.json').write_text(json.dumps(r,indent=2));print(eta_needed)
