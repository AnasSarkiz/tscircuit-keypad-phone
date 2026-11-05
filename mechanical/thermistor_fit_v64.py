"""Conservative sensor envelope screening,not a retained or thermally validated assembly."""
import trimesh as tm,json
from pathlib import Path
s=tm.load('output/retainer-fix-v22/assembly.glb',force='scene');parts={n:m.copy() for n,m in s.geometry.items()}
for m in parts.values():m.apply_scale(1000)
parts.pop('external_NTC_reserved',None) # replace prior placeholder,not an obstacle
positions={'front_broad_face':[0,-35,-4.5],'rear_broad_face':[0,-35,-15.4],'right_edge':[31.25,-35,-9.95]}
rows=[]
for name,xyz in positions.items():
 b=tm.creation.box([3,10,3]);b.apply_translation(xyz);hits=[]
 for n,m in parts.items():
  if (b.bounds[0]>=m.bounds[1]).any() or (m.bounds[0]>=b.bounds[1]).any():continue
  h=tm.boolean.intersection([b,m],engine='manifold')
  if len(h.faces) and abs(h.volume)>.001:hits.append({'part':n,'overlap_mm3':abs(h.volume)})
 rows.append({'position':name,'center_mm':xyz,'envelope_mm':[3,10,3],'collisions':hits})
assert all(r['collisions'] for r in rows),'unexpected fit:needs review'
Path('output/thermistor-fit-v64.json').write_text(json.dumps({'sensor':'NTCLE413E2103H400A','scope':'Three conservative axis-aligned bounding-box candidates tangent to pack envelope;not exact STEP,not proof no placement anywhere can work','cases':rows,'release':False,'decision':'Do not silently add sensor to existing pack/retainer stack. Need attachment pocket,retainer/case revision or smaller documented sensor and thermal validation.'},indent=2))
print(rows)
