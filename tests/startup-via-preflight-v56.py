import json,trimesh as tm,numpy as np
from shapely.geometry import Point,box,Polygon
c=json.load(open('routing/usb-layered-v56.json'));j=json.load(open('output/usb-placement-v56.circuit.json'));s=tm.load('output/retainer-fix-v22/assembly.glb',force='scene');hits=[]
for v in c['vias']:
 if not v['name'].startswith('START56'):continue
 for p in j:
  if p['type']!='pcb_smtpad':continue
  g=Polygon([(q['x'],q['y']) for q in p['points']]) if p['shape']=='polygon' else box(p['x']-p['width']/2,p['y']-p['height']/2,p['x']+p['width']/2,p['y']+p['height']/2)
  d=g.distance(Point(v['xy']))-.25
  if d<.15-1e-8:hits.append((v['name'],p['pcb_smtpad_id'],d))
 for n,m in s.geometry.items():
  if 'pcb' in n:continue
  b=m.bounds*1000;a=np.array([[v['xy'][0]-.25,v['xy'][1]-.25,-.835],[v['xy'][0]+.25,v['xy'][1]+.25,.835]])
  if (np.minimum(a[1],b[1])-np.maximum(a[0],b[0])<=1e-5).any():continue
  # broadphase only; shells have cavities, so use exact boolean
  vm=tm.creation.cylinder(radius=.25,height=1.67);vm.apply_translation([*v['xy'],0]);body=m.copy();body.apply_scale(1000)
  h=tm.boolean.intersection([vm,body],engine='manifold')
  if abs(h.volume)>1e-5:hits.append((v['name'],n,float(h.volume)))
assert not hits,hits
print('PASS startup via pad and retained assembly preflight')
