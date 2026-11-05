from pathlib import Path
import json,numpy as np,trimesh as tm
root=Path(__file__).resolve().parents[1];j=json.loads((root/'output/usb-placement-v33.circuit.json').read_text());caps=json.loads((root/'sourcing/capacitor-dimensions-v18.json').read_text());s=tm.load(root/'output/retainer-fix-v22/assembly.glb',force='scene');parts={n:m.copy() for n,m in s.geometry.items()}
for m in parts.values():m.apply_scale(1000)
rows=[];hits=[]
for c in [x for x in j if x['type']=='source_component']:
 m=c['manufacturer_part_number'];p=next(x for x in j if x['type']=='pcb_component' and x['source_component_id']==c['source_component_id'])
 if m in caps:d=[caps[m][k][1] for k in ['length','width','height']];basis='V18 dimensional transcription; exact STEP/overlay pending'
 elif m.startswith(('RC0603','RT0603')):d=[1.7,.9,.55];basis='family maximum body approximation'
 elif m in ['TPS3808G01DBVR','TPS70933DBVR','SN74LVC1G02DBVR']:d=[3.0,3.55,1.45];basis='conservative DBV envelope including mold flash; drawing overlay pending'
 else:d=[3,3,1];basis='provisional3x3x1mm package reserve; not verified tolerance envelope'
 if abs(p.get('rotation',0))%180==90:d[0],d[1]=d[1],d[0]
 b=tm.creation.box(d);pos=[p['center']['x'],p['center']['y'],.8+d[2]/2];b.apply_translation(pos)
 for n,other in parts.items():
  if (np.minimum(b.bounds[1],other.bounds[1])-np.maximum(b.bounds[0],other.bounds[0])<=1e-4).any():continue
  h=tm.boolean.intersection([b,other],engine='manifold')
  if len(h.faces) and abs(h.volume)>.001:hits.append({'component':c['name'],'other':n,'volume_mm3':float(abs(h.volume))})
 parts['usb_candidate_'+c['name']]=b;rows.append({'reference':c['name'],'MPN':m,'center_mm':pos,'body_mm':d,'basis':basis,'side':'top','verified_body':False})
assert not hits,hits
out=root/'output/usb-placement-v33';out.mkdir(exist_ok=True);scene=tm.Scene()
for n,b in parts.items():b.apply_scale(.001);scene.add_geometry(b,node_name=n,geom_name=n)
scene.export(out/'assembly.glb');(out/'fit-check.json').write_text(json.dumps({'entries':rows,'intersections':hits,'scope':'nineteen partial electrical-placement bodies vs63 preexisting meshes; provisional shapes; routing and full-population clearance unqualified','release':False},indent=2));print('PASS partial USB nineteen-body fit against existing63 meshes; not final tolerance validation')
