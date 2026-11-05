from pathlib import Path
import json,math,trimesh as tm,numpy as np
root=Path(__file__).resolve().parents[1];scene=tm.load(root/'output/retainer-fix-v22/assembly.glb',force='scene');bodies={n:m.copy() for n,m in scene.geometry.items()}
for b in bodies.values():b.apply_scale(1000)
routes=json.loads((root/'routing/usb-local-v30.json').read_text());hits=[];count=0
for r in routes:
 for a,b in zip(r['points'],r['points'][1:]):
  length=math.dist(a,b)
  if length<1e-8:continue
  copper=tm.creation.box([length+.15,.15,.035]);theta=math.atan2(b[1]-a[1],b[0]-a[0]);copper.apply_transform(tm.transformations.rotation_matrix(theta,[0,0,1]));copper.apply_translation([(a[0]+b[0])/2,(a[1]+b[1])/2,.8175]);count+=1
  for name,body in bodies.items():
   if (np.minimum(copper.bounds[1],body.bounds[1])-np.maximum(copper.bounds[0],body.bounds[0])<=1e-5).any():continue
   overlap=tm.boolean.intersection([copper,body],engine='manifold')
   if len(overlap.faces) and abs(overlap.volume)>1e-5:hits.append(dict(route=r['name'],body=name,volume_mm3=float(abs(overlap.volume))))
out={'route_segments_checked':count,'existing_meshes':len(bodies),'copper_thickness_assumed_mm':.035,'hits':hits,'scope':'top copper conservative rectangular segment envelopes vs existing mechanical meshes, not missing component lands or tolerance qualification','release':False}
(root/'output/usb-copper-fit-v30.json').write_text(json.dumps(out,indent=2));assert not hits,hits;print('PASS',count,'copper segment envelopes vs',len(bodies),'assembly meshes')
