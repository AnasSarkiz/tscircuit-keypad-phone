"""Insulated-face sensor mounting proposal;no thermal or retention qualification."""
from pathlib import Path
import json,trimesh as tm,numpy as np
s=tm.load('output/usb-placement-v65/assembly.glb',force='scene');parts={n:m.copy() for n,m in s.geometry.items()}
for m in parts.values():m.apply_scale(1000)
parts.pop('external_NTC_reserved',None)
sensor=tm.creation.box([3,10,3]);sensor.apply_translation([0,-35,-3.95])
new={'NTC_V65_body_envelope':sensor}
# Candidate U-turns inside one open retainer bay;40mm centerline each.
for i,(x,radius) in enumerate([(.55,5.0),(-.55,6.1)]):
 points=[[x,-40,-3.95],[x,-44,-3.95]]
 for angle in np.linspace(0,np.pi,65)[1:]:points.append([x+radius-radius*np.cos(angle),-44-radius*np.sin(angle),-3.95])
 points.append([x+2*radius,-44+(40-4-np.pi*radius),-3.95])
 pieces=[]
 for a,b in zip(points,points[1:]):
  delta=np.array(b)-a;length=np.linalg.norm(delta);w=tm.creation.cylinder(radius=.5,height=length,sections=16)
  w.apply_transform(tm.geometry.align_vectors([0,0,1],delta/length));w.apply_translation((np.array(a)+b)/2);pieces.append(w)
 for v in points:
  q=tm.creation.icosphere(subdivisions=1,radius=.5);q.apply_translation(v);pieces.append(q)
 new[f'NTC_V65_wire_reserve_{i}']=tm.util.concatenate(pieces)
hits=[]
for name,m in new.items():
 for n,b in parts.items():
  if (np.minimum(m.bounds[1],b.bounds[1])-np.maximum(m.bounds[0],b.bounds[0])<=1e-5).any():continue
  h=tm.boolean.intersection([m,b],engine='manifold')
  if len(h.faces) and abs(h.volume)>.001:hits.append({'new':name,'existing':n,'volume_mm3':float(abs(h.volume))})
report={'release':False,'sensor_center_mm':[0,-35,-3.95],'sensor_envelope_mm':[3,10,3],'gap_to_secondary_insulator_top_mm':.10,'cell_wrapper_and_secondary_insulator_removed':False,'wire_reserve':'Two40mm centerline1mm diameter U-turn reserves,radii5/6.1mm,first bend4mm from assumed outlet;actual OD/length datum,termination and strain relief unqualified','hits':hits,'qualification':['Exact insulated sensor outline and usable lead length','Adhesive thickness/compression/thermal conductivity and insulating-sheet thermal coupling','Lead attachment,termination,strain relief and electrical connector','Battery swelling/relative tolerance and mechanical retention','Installed temperature error,self-heating,lag and charger fault response'],'decision':'Nominal clearance proposal only;not selected physical assembly'}
Path('output/thermistor-mount-v65.json').write_text(json.dumps(report,indent=2));print(report)
if not hits:
 out=Path('output/thermistor-mount-v65');out.mkdir(exist_ok=True);scene=tm.Scene()
 for n,m in {**parts,**new}.items():m.apply_scale(.001);scene.add_geometry(m,node_name=n,geom_name=n)
 scene.export(out/'assembly.glb')
