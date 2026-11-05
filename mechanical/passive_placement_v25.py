"""Mechanical capacity study only; not electrical/decoupling/routing placement."""
import json,itertools
from pathlib import Path
import numpy as np
import trimesh as tm
root=Path(__file__).resolve().parents[1];out=root/'output/passive-placement-v25';out.mkdir(exist_ok=True)
s=tm.load(root/'output/retainer-fix-v22/assembly.glb',force='scene');parts={n:m.copy() for n,m in s.geometry.items()}
for m in parts.values():m.apply_scale(1000)
entries=json.loads((root/'output/passive-catalog-v23/mapping.json').read_text())['entries'];placed=[];rejections=[]
slots=iter(itertools.product([-78+i*4.2 for i in range(15)],[-24+i*4.2 for i in range(12)]))
for e in sorted(entries,key=lambda e:-np.prod(e['maximum_body_mm'])):
 dims=e['maximum_body_mm'];success=False
 for y,x in slots:
  z=-.8-dims[2]/2;box=tm.creation.box(dims);box.apply_translation([x,y,z]);hits=[]
  # Exact boolean only if bounding boxes overlap. Contact at PCB face is allowed.
  for n,m in parts.items():
   dep=np.minimum(box.bounds[1],m.bounds[1])-np.maximum(box.bounds[0],m.bounds[0])
   if (dep<=1e-4).any():continue
   h=tm.boolean.intersection([box,m],engine='manifold')
   if len(h.faces) and abs(h.volume)>.001:hits.append(n)
  if hits:rejections.append({'x':x,'y':y,'reference':e['reference'],'hits':hits});continue
  assert box.bounds[0,0]>=-28 and box.bounds[1,0]<=28 and box.bounds[0,1]>=-84 and box.bounds[1,1]<=60
  box.visual.face_colors=[190,140,80,255];parts['candidate_'+e['reference']]=box
  placed.append({**e,'board_position_mm':[x,y],'board_side':'bottom','center_z_mm':z,'placed':True,'placement_status':'MECHANICAL_CAPACITY_ONLY_NOT_ELECTRICAL','body_verified':False,'routing_or_decoupling_validated':False});success=True;break
 if not success:break
scene=tm.Scene()
for n,m in parts.items():
 m.apply_scale(.001);scene.add_geometry(m,node_name=n,geom_name=n)
scene.export(out/'assembly-capacity-only.glb')
report={'status':'MECHANICAL CAPACITY STUDY ONLY; no electrical placements assigned','placed_body_count':len(placed),'required_body_count':len(entries),'entries':placed,'rejected_slots':rejections,'remaining_refs':sorted(set(e['reference'] for e in entries)-set(e['reference'] for e in placed)),'body_only_test':'No >.001mm3 boolean intersections with63 existing meshes or earlier candidate bodies; PCB-face contact allowed; board bounds checked','not_checked':['pad and solder joint clearances','power loop length/decoupling','routing','thermal interaction with battery','actual manufacturer bodies','all remaining source components','production tolerance'],'fabrication_ready':False}
(out/'mapping.json').write_text(json.dumps(report,indent=2));print('Mechanical body placements',len(placed),'of',len(entries),'rejected slots',len(rejections))
assert len(placed)==155
