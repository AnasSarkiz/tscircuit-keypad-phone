"""Whole existing assembly mesh audit. This does NOT cover the unplaced full netlist."""
from pathlib import Path
import itertools,json,sys
import numpy as np
import trimesh as tm
root=Path(__file__).resolve().parents[1]
input_path=root/(sys.argv[1] if len(sys.argv)>1 else 'output/retained-battery/assembly.glb')
suffix='-fixed' if len(sys.argv)>1 else ''
s=tm.load(input_path,force='scene')
parts={n:m.copy() for n,m in s.geometry.items()}
for m in parts.values():
 assert m.is_watertight and np.isfinite(m.vertices).all()
 m.apply_scale(1000)
hits=[];broad=0
for (a,ma),(b,mb) in itertools.combinations(parts.items(),2):
 depth=np.minimum(ma.bounds[1],mb.bounds[1])-np.maximum(ma.bounds[0],mb.bounds[0])
 if np.any(depth<=1e-4):continue
 broad+=1
 hit=tm.boolean.intersection([ma,mb],engine='manifold')
 if len(hit.faces) and abs(hit.volume)>.001:
  hits.append({'a':a,'b':b,'intersection_mm3':float(abs(hit.volume)),'status':'REVIEW: may include intended mount contact or coarse envelope; not auto-approved'})
mod=parts['modem_EG912U_envelope'].bounds
clear=[]
for n in ['MCU_S3_envelope','power_reserved','nanoSIM_reserved','external_NTC_reserved']:
 b=parts[n].bounds;dx=max(b[0,0]-mod[1,0],mod[0,0]-b[1,0],0);dy=max(b[0,1]-mod[1,1],mod[0,1]-b[1,1],0)
 clear.append({'name':n,'XY_nearest_rectangle_gap_mm':float(np.hypot(dx,dy)),'axis_gaps_mm':[float(dx),float(dy)],'at_least_3mm_nominal':bool(np.hypot(dx,dy)>=3),'body_verified':False})
assert all(x['at_least_3mm_nominal'] for x in clear)
report={'input':str(input_path.relative_to(root)),'assembly_mesh_count':len(parts),'all_pair_candidates':len(parts)*(len(parts)-1)//2,'aabb_candidates':broad,'intersections_over_0_001_mm3':hits,'modem_nominal_clearances':clear,'status':'NOT RELEASED: intersections require review; envelopes and full population incomplete','scope':'All existing assembly meshes only. Does not imply all211 source components modeled or placed; fit/stencil/power/carrier gates remain.'}
(root/f'output/spatial-audit-v22{suffix}.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
