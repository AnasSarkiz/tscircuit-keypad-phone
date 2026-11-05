from pathlib import Path
import json,numpy as np,trimesh as tm
root=Path(__file__).resolve().parents[1];j=json.loads((root/'output/usb-placement-v66.circuit.json').read_text());caps=json.loads((root/'sourcing/capacitor-dimensions-v18.json').read_text());s=tm.load(root/'output/retainer-fix-v22/assembly.glb',force='scene');parts={n:m.copy() for n,m in s.geometry.items()}
for m in parts.values():m.apply_scale(1000)
parts.pop('modem_EG912U_envelope')
parts.pop('MCU_S3_envelope')
for i in range(1,16):parts.pop(f'SW{i}_B3F')
parts.pop('nanoSIM_reserved') # replaced with explicitly sized candidate envelope below
rows=[];hits=[]
for c in [x for x in j if x['type']=='source_component']:
 if c['name'].startswith('TP_'):continue # copper-only PCB features, zero purchased body
 m=c['manufacturer_part_number'];p=next(x for x in j if x['type']=='pcb_component' and x['source_component_id']==c['source_component_id'])
 if m=='B3F-1050':d=[6.2,6.2,7.5];basis='Reviewed6.2mm width/7.5mm height;4.5mm base and2.6mm plunger reserve remain engineering assumptions'
 elif m in caps:d=[caps[m][k][1] for k in ['length','width','height']];basis='V18 dimensional transcription; exact STEP/overlay pending'
 elif m.startswith(('RC0603','RT0603')):d=[1.7,.9,.55];basis='family maximum body approximation'
 elif m in ['TPS3808G01DBVR','TPS70933DBVR','SN74LVC1G02DBVR','SN74AXC1T45DBVR','SN74LVC1G17DBVR']:d=[3.0,3.55,1.45];basis='conservative DBV envelope including mold flash; drawing overlay pending'
 elif m=='LTC2954ITS8-1#TRMPBF':d=[3.85,3.154,1.0];basis='TS8 lead span maximum;2.9mm body plus0.254mm mold allowance; physical sample and process not qualified'
 elif m=='ESP32-S3-WROOM-1-N16':d=[18,25.5,3.2];basis='manufacturer module nominal outline with provisional height allowance; not tolerance/RF validation'
 elif m.startswith('EG912U'):d=[25,29,2.4];basis='reviewed V1.0 nominal modem body; variant and tolerance qualification pending'
 elif m=='SIM8051-6-0-14-00-A':d=[15,17,2];basis='existing conservative socket reservation; detailed STEP/physical insertion not qualified'
 elif m=='TLV9032DR':d=[6.49,5.3,1.75];basis='TI SOIC8 text-derived envelope with lead-span allowance; visual/tolerance audit pending'
 elif m=='AO3400A':d=[3.354,3.0,1.25];basis='AOS PO-00001 N package bound plus mold allowance; process unqualified'
 elif m=='TPD3E001DRLR':d=[2,2,.8];basis='conservative DRL5 reserve, exact visual package audit pending'
 else:d=[3,3,1];basis='provisional3x3x1mm package reserve; not verified tolerance envelope'
 if abs(p.get('rotation',0))%180==90:d[0],d[1]=d[1],d[0]
 b=tm.creation.box(d);pos=[p['center']['x'],p['center']['y'],(.8+d[2]/2)*(1 if p.get('layer','top')=='top' else -1)];
 if m=='ESP32-S3-WROOM-1-N16':pos[1]=32 # physical body center differs from copper bounding-box center
 b.apply_translation(pos)
 if m=='B3F-1050':
  base=tm.creation.box([6.2,6.2,4.5]);base.apply_translation([pos[0],pos[1],3.05])
  stem=tm.creation.box([2.6,2.6,3.2]);stem.apply_translation([pos[0],pos[1],6.7])
  b=tm.boolean.union([base,stem],engine='manifold')
 for n,other in parts.items():
  if m=='B3F-1050' and n=='keycap_'+c['name'][2:]:continue # intentional mating;V64 height test,not physical qualification
  if (np.minimum(b.bounds[1],other.bounds[1])-np.maximum(b.bounds[0],other.bounds[0])<=1e-4).any():continue
  h=tm.boolean.intersection([b,other],engine='manifold')
  if len(h.faces) and abs(h.volume)>.001:hits.append({'component':c['name'],'other':n,'volume_mm3':float(abs(h.volume))})
 parts['usb_candidate_'+c['name']]=b;rows.append({'reference':c['name'],'MPN':m,'center_mm':pos,'body_mm':d,'basis':basis,'side':p.get('layer','top'),'verified_body':False})
assert not hits,hits
out=root/'output/usb-placement-v66';out.mkdir(exist_ok=True);scene=tm.Scene()
for n,b in parts.items():b.apply_scale(.001);scene.add_geometry(b,node_name=n,geom_name=n)
scene.export(out/'assembly.glb');(out/'fit-check.json').write_text(json.dumps({'copper_only_test_features':6,'entries':rows,'intersections':hits,'scope':'133 partial electrical-placement bodies vs45 retained base meshes; old SIM reservation replaced; provisional shapes; routing and full-population clearance unqualified','release':False},indent=2));print('PASS partial USB 133-body fit against45 retained base meshes and each other; SIM reservation replaced; not final tolerance validation')
