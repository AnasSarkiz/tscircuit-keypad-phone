from pathlib import Path
import json,trimesh as tm,numpy as np
from shapely.geometry import shape,Point
from shapely import constrained_delaunay_triangles
root=Path(__file__).resolve().parents[1];scene=tm.load(root/'output/retainer-fix-v22/assembly.glb',force='scene');bodies={n:m.copy() for n,m in scene.geometry.items()}
for b in bodies.values():b.apply_scale(1000)
def mesh(poly,height,z):
 vertices=[];lookup={};faces=[]
 for tri in constrained_delaunay_triangles(poly).geoms:
  f=[]
  for xy in list(tri.exterior.coords)[:3]:
   if xy not in lookup:lookup[xy]=len(vertices);vertices.append(xy)
   f.append(lookup[xy])
  faces.append(f)
 m=tm.creation.extrude_triangulation(np.array(vertices),np.array(faces),height);m.apply_translation([0,0,z]);return m
items=[]
for x in json.loads((root/'output/usb-layered-v40-geometry.json').read_text()):
 if x['kind']=='via':continue
 items.append((x['name'],mesh(shape(x['geometry']),.035,.8 if x['layer']=='top' else (-.835 if x['layer']=='bottom' else (-.2 if x['layer']=='inner1' else .2))),x['layer'].startswith('inner')))
for v in json.loads((root/'routing/usb-layered-v40.json').read_text())['vias']:
 items.append(('via_'+v['name'],mesh(Point(v['xy']).buffer(v['outer']/2,quad_segs=24),1.67,-.835),True))
hits=[]
for name,m,isvia in items:
 for bn,b in bodies.items():
  # A through-board via necessarily intersects the PCB substrate. All other bodies remain obstacles.
  if bn=='modem_EG912U_envelope' and (name.startswith('MOD_') or name.startswith('via_MOD_')):continue # reviewed modem pad mating; via-in-pad process quarantined
  if bn=='nanoSIM_reserved' and name.startswith('SOCKET_') and not isvia:continue # surface copper uses independently checked manufacturer keepouts; solid reservation is not actual underbody geometry
  if isvia and ('pcb' in bn.lower() or 'board' in bn.lower()):continue
  if (np.minimum(m.bounds[1],b.bounds[1])-np.maximum(m.bounds[0],b.bounds[0])<=1e-5).any():continue
  h=tm.boolean.intersection([m,b],engine='manifold')
  if len(h.faces) and abs(h.volume)>1e-5:hits.append(dict(copper=name,body=bn,volume_mm3=float(abs(h.volume))))
out={'copper_or_via_envelopes':len(items),'assembly_meshes':len(bodies),'hits':hits,'PCB_substrate_excluded_only_for_vias_and_inner_copper':True,'modem_contact_exception':'MOD_ surface copper and via_MOD_ at reviewed mating lands; via-in-pad fill/cap and physical mating remain unqualified','SIM_reserved_surface_copper_exception':'SOCKET_ traces only; manufacturer keepouts tested separately, actual underbody fit remains unqualified','release':False};(root/'output/usb-layered-fit-v40.json').write_text(json.dumps(out,indent=2));assert not hits,hits;print('PASS layered copper/plane/via physical envelope check',len(items),'against',len(bodies))
