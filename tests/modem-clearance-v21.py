from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from engineering.modem_clearance import enforce
m=dict(ref='MODEM',x=0,y=0,width=25,height=29,rotation=0,layer='top')
def part(**kw):return dict(ref='R1',x=16,y=0,width=1,height=1,rotation=0,layer='top',verified_body=True,**kw)
def rejected(mm,ps,refs):
 try:enforce(mm,ps,refs)
 except ValueError:return True
 return False
assert enforce(m,[part()],['R1'])['same_face_clearance_pass'] # exactly3mm
p=part();p['x']=15.999;assert rejected(m,[p],['R1'])
p['x']=16.001;assert not rejected(m,[p],['R1'])
p['x']=0;assert rejected(m,[p],['R1'])
p['layer']='bottom';assert not rejected(m,[p],['R1']) # not a 3D-clearance claim
p=part();p['verified_body']=False;assert rejected(m,[p],['R1'])
assert rejected(m,[],['R1']);assert rejected(m,[part(),part()],['R1'])
assert rejected({**m,'width':19.5},[part()],['R1'])
p=part();p.update(x=0,y=16,rotation=90);assert rejected({**m,'rotation':90},[p],['R1']) is False
p['y']=15.99;assert rejected({**m,'rotation':90},[p],['R1'])
p=part();p['rotation']=45;assert rejected(m,[p],['R1'])
p['x']=float('nan');assert rejected(m,[p],['R1'])
Path('output/modem-clearance-v21.json').write_text(json.dumps({'boundary_and_negative_tests':'passed','whole_board_placement':'BLOCKED: complete verified body envelopes absent','courtyard_mm':[31,35],'paste':'disabled; no stencil output'},indent=2))
print('PASS clearance boundaries, 90/45deg rotation, missing/unverified/duplicate/NaN guards; full board NOT passed')
