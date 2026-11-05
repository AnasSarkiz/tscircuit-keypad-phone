"""Wired Jauch 253338 fit branch, NOT a released enclosure.
Max pack envelope 22 x 76 mm. No stock/quote or physical sample verification.
Retains one main PCB, factory-keytop front and all their unresolved constraints.
"""
from pathlib import Path
import json,itertools
import trimesh as tm
import numpy as np
root=Path(__file__).resolve().parents[1];out=root/'output'/'wired-battery';out.mkdir(exist_ok=True)
s=tm.load(root/'output/factory-keypad/assembly.glb',force='scene');p={n:m.copy() for n,m in s.geometry.items()}
for m in p.values():m.apply_scale(1000)
def box(sz,c):m=tm.creation.box(sz);m.apply_translation(c);return m
def cyl(r,h,c,sections=64):m=tm.creation.cylinder(radius=r,height=h,sections=sections);m.apply_translation(c);return m
def axial(r,h,c):
 m=cyl(r,h,[0,0,0]);m.apply_transform(tm.transformations.rotation_matrix(np.pi/2,[1,0,0]));m.apply_translation(c);return m
def union(ms):return tm.boolean.union(ms,engine='manifold')
def diff(a,bs):return tm.boolean.difference([a,*bs],engine='manifold')
def rounded(w,h,t,r,z):return union([box([w-2*r,h,t],[0,0,z]),box([w,h-2*r,t],[0,0,z]),*[cyl(r,t,[x,y,z]) for x in [-w/2+r,w/2-r] for y in [-h/2+r,h/2-r]]])
for n in ['battery_2011_fit_only','battery_insulator','battery_connector_reserved']:del p[n]
holes=[(x,y) for x in [-24,24] for y in [-79,54]]
back=diff(rounded(62,174,28.5,5,-14.25),[rounded(58,170,30,3,-11.5)])
back=union([back,*[cyl(3,25.7,[x,y,-13.65]) for x,y in holes]])
back=diff(back,[*[cyl(1.15,70,[x,y,0]) for x,y in holes],*[cyl(2.4,1.8,[x,y,-27.7],6) for x,y in holes]])
p['rear_shell']=back
p['battery_253338_max_envelope']=axial(11,76,[8,-40,-15])
p['battery_insulator']=box([26,80,.5],[8,-40,-2.55])
for i,y in enumerate([-65,-18]):
 p[f'battery_cradle_{i}']=diff(box([26,8,8],[8,y,-22.5]),[axial(11.2,12,[8,y,-15])])
for i,(x,y) in enumerate(holes,1):
 p[f'bolt_{i}']=union([cyl(1,40,[x,y,-9.5]),cyl(1.9,2,[x,y,11.5])])
 p[f'nut_{i}']=diff(cyl(2.3,1.6,[x,y,-27.7],6),[cyl(1,3,[x,y,-27.7])])
# Collisions of new cell against physical parts, excluding exterior case checked separately.
hits=[]
for name,m in p.items():
 if name=='battery_253338_max_envelope' or 'reserved' in name:continue
 hit=tm.boolean.intersection([p['battery_253338_max_envelope'],m],engine='manifold')
 if len(hit.faces) and abs(hit.volume)>.001:hits.append([name,float(hit.volume)])
assert not hits,hits
scene=tm.Scene();exploded=tm.Scene()
for name,m in p.items():
 assert m.is_watertight,name
 if name=='rear_shell' or name.startswith('battery_cradle'):m.export(out/f'{name}.stl')
 if name=='rear_shell' or name.startswith('battery_cradle'):m.visual.face_colors=[47,61,74,255]
 if name=='battery_253338_max_envelope':m.visual.face_colors=[238,171,54,255]
 a=m.copy();a.apply_scale(.001);scene.add_geometry(a,node_name=name,geom_name=name)
 a=m.copy();a.apply_translation([0,0,-45 if name=='rear_shell' else -25 if name.startswith('battery') else 30 if name=='front_shell' else 0]);a.apply_scale(.001);exploded.add_geometry(a,node_name=name,geom_name=name)
scene.export(out/'assembly.glb');exploded.export(out/'exploded.glb')
report={'status':'candidate fit branch only; procurement, retention and wire routing open','battery':'Jauch 253338 LI21700JD-50E 1s1p','case_nominal_mm':[62,174,39],'cell_max_diameter_mm':22,'cell_max_length_mm':76,'cell_axis':'Y','cell_center_mm':[8,-40,-15],'cell_to_rear_floor_mm':.5,'cell_to_insulator_mm':1.2,'fastener':'M2x40 nominal envelope; vendor drawing/tolerance unverified','new_cell_boolean_checks':sum(n!='battery_253338_max_envelope' and 'reserved' not in n for n in p),'cell_collisions':hits,'meshes':len(p),'watertight':sum(m.is_watertight for m in p.values()),'not_verified':['pack availability/price and shipment eligibility','70+/-5 mm AWG20 wire route and strain relief','high-current polarized connector selection','cradle padding, axial restraint and drop loads','assembly sequence/tool access','battery temperature sensing wiring','other pre-existing assembly gates']}
(out/'checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
