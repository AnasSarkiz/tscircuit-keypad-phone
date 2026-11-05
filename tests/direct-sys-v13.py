"""Direct SYS-to-modem switch branch; conditional screening, NOT release."""
import math,json,itertools
from pathlib import Path
aux=3.3*.6/.8+5.3*.131/.75
rows=[]
for im,voc,r in itertools.product([2,3],[4.1,3.8,3.6],[.05,.1,.2]):
 # I=Im+Paux/SYS; SYS=Voc-I*R. High-voltage stable solution.
 b=voc-r*im;disc=b*b-4*r*aux
 sys=(b+math.sqrt(disc))/2 if disc>=0 else None
 current=im+aux/sys if sys else None
 # .03ohm switch allocation +.03ohm RF/BB distribution; .1V transient allocation.
 vmod=sys-im*.06-.1 if sys else None
 rows.append({'modem_A':im,'cell_OCV_V':voc,'shared_R_ohm':r,'SYS_V':sys,'pack_A':current,'module_min_allocated_V':vmod,'PCM_margin_A':4-current if current else None,'screen_pass':bool(current and current<4 and vmod>=3.3)})
case=next(x for x in rows if x['modem_A']==2 and x['cell_OCV_V']==3.8 and x['shared_R_ohm']==.1)
assert case['pack_A']<3.1 and not case['screen_pass']
assert any(x['screen_pass'] for x in rows)
# Requirements derived at minimum permitted module voltage, not a chosen trip circuit.
sysfloor=3.3+2*.06+.1
packatfloor=2+aux/sysfloor
ocvfloor=sysfloor+.1*packatfloor
r={'scope':'Comparison branch only: take modem load from charger SYS, not BAT, preserving charger load accounting. Switch and monitor not integrated.', 'assumptions':'auxiliary loads/efficiencies unchanged V11; modem constant-current envelope 2A/3A; .03 ohm switch and .03 ohm routing allocations; .1 V unserved-transient budget. No actual impedance/efficiency certification.', 'scenarios':rows,'LTE_required_SYS_V':sysfloor,'LTE_required_OCV_at_100mohm_V':ocvfloor,'example_3_8V_100mohm':case,'blockers':['TPS22992 VIN must not exceed VBIAS; 3.15 V logic is unsuitable bias for a 4.1 V SYS','SYS 50mV-over-battery statement is typical, not a guaranteed upper bound','VSET short selects4.35V, exceeding modem range; independent OVP coordination needed','hardware UVLO and orderly shutdown reserve not designed','non-S load switch has no short-circuit current limiter','switch hot-R bounds across chosen bias range, inrush/QOD and modem bulk require qualification','current battery still unqualified; persistent LTE-only state unverified'],'battery_approved':False,'fabrication_ready':False}
Path('output/direct-sys-v13.json').write_text(json.dumps(r,indent=2));print(json.dumps({k:v for k,v in r.items() if k!='scenarios'},indent=2))
