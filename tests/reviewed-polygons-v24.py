import json,math
from pathlib import Path
j=json.loads(Path('output/RPW0010A-v24.circuit.json').read_text());pads=[x for x in j if x['type']=='pcb_smtpad'];assert len(pads)==10
for n,sx,sy in [(1,1,1),(4,1,-1),(7,-1,-1),(10,-1,1)]:
 p=next(x for x in pads if f'pin{n}' in x['port_hints']);assert p['shape']=='polygon'
 pts=[(x['x']*sx,-x['y']*sy) for x in p['points']]
 assert any(abs(x+.85)<1e-9 and abs(y+.85)<1e-9 for x,y in pts),'sharp concave elbow missing'
 assert abs(min(x for x,y in pts)+1.2)<1e-9 and abs(max(x for x,y in pts)+.6)<1e-9
 assert abs(min(y for x,y in pts)+1.2)<1e-9 and abs(max(y for x,y in pts)+.55)<1e-9
 area=abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(pts,pts[1:]+pts[:1])))/2
 exact=.2675-5*(1-math.pi/4)*.05**2
 assert abs(area-exact)<.00002,(area,exact)
 assert p['soldermask_margin']==.05
print('PASS four L polygons: sharp elbows, exterior fillets, signed placement and area within 0.00002 mm2 of ideal')
