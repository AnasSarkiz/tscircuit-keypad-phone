"""Conditional source requirements, not a simulated converter or pack qualification."""
import json,math,itertools
from pathlib import Path
aux=3.3*.6/.8+5.3*.131/.75
rows=[]
for mode,im,voc,r in itertools.product(['direct_SYS','regulated_3_8V'],[2,3],[4.1,3.8,3.6],[.05,.1,.2]):
 if mode=='direct_SYS':
  b=voc-r*im;disc=b*b-4*r*aux;sys=(b+math.sqrt(disc))/2 if disc>=0 else None;i=im+aux/sys if sys else None;vm=sys-im*.06-.1 if sys else None
 else:
  p=3.8*im/.85+aux;disc=voc*voc-4*r*p;sys=(voc+math.sqrt(disc))/2 if disc>=0 else None;i=p/sys if sys else None;vm=3.8*.98-im*.03-.1 if sys else None
 rows.append(dict(architecture=mode,modem_A=im,OCV_V=voc,shared_R_ohm=r,SYS_V=sys,pack_A=i,module_allocated_min_V=vm,conditional_screen_pass=bool(i and i<=3.6 and vm>=3.3)))
# 10% reserve below 4 A minimum PCM trip; engineering target, not manufacturer approval.
p=3.8*2/.85+aux;required_sys=p/3.6;required_ocv=required_sys+.1*3.6
r={'assumptions':{'auxiliary_input_W':aux,'buckboost_efficiency':.85,'regulated_accuracy_fraction':.02,'pack_design_ceiling_A':3.6,'note':'Efficiency and impedance are assumptions; transient budgets not measurements. Direct SYS allocations same as V13. Regulated output assumed achievable; no converter selected.'},'scenarios':rows,'regulated_LTE_min_SYS_for_3_6A_budget_V':required_sys,'regulated_LTE_min_OCV_for_100mohm_V':required_ocv,'architecture_decision':'Neither branch approved. A buck-boost corrects dropout in principle but increases pack demand; cannot validate it using converter headline amperes. Direct SYS needs coordinated upper/lower protection and shutdown reserve.','fabrication_ready':False}
assert not next(x for x in rows if x['architecture']=='direct_SYS' and x['modem_A']==2 and x['OCV_V']==3.8 and x['shared_R_ohm']==.1)['conditional_screen_pass']
assert not next(x for x in rows if x['architecture']=='regulated_3_8V' and x['modem_A']==3 and x['OCV_V']==3.6 and x['shared_R_ohm']==.1)['conditional_screen_pass']
Path('output/power-architecture-v14.json').write_text(json.dumps(r,indent=2));print({k:v for k,v in r.items() if k!='scenarios'})
