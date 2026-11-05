"""Flat Jauch 246524 fit branch, NOT a released enclosure.
Maximum after-cycling envelope 59.5 x 78.5 x 7.9 mm. No physical sample verification.
Retains one main PCB, factory-keytop front and all their unresolved constraints.
"""
from pathlib import Path
import json,itertools
import trimesh as tm
import numpy as np
root=Path(__file__).resolve().parents[1];out=root/'output'/'retained-battery';out.mkdir(exist_ok=True)
s=tm.load(root/'output/factory-keypad/assembly.glb',force='scene');p={n:m.copy() for n,m in s.geometry.items()}
for m in p.values():m.apply_scale(1000)
# V1.0 hardware document page 82 requires 3 mm component spacing.
p['modem_EG912U_envelope'].apply_translation([.6,0,0])
def box(sz,c):m=tm.creation.box(sz);m.apply_translation(c);return m
def cyl(r,h,c,sections=64):m=tm.creation.cylinder(radius=r,height=h,sections=sections);m.apply_translation(c);return m
def axial(r,h,c):
 m=cyl(r,h,[0,0,0]);m.apply_transform(tm.transformations.rotation_matrix(np.pi/2,[1,0,0]));m.apply_translation(c);return m
def union(ms):return tm.boolean.union(ms,engine='manifold')
def diff(a,bs):return tm.boolean.difference([a,*bs],engine='manifold')
def rounded(w,h,t,r,z):return union([box([w-2*r,h,t],[0,0,z]),box([w,h-2*r,t],[0,0,z]),*[cyl(r,t,[x,y,z]) for x in [-w/2+r,w/2-r] for y in [-h/2+r,h/2-r]]])
for n in ['battery_2011_fit_only','battery_insulator','battery_connector_reserved']:del p[n]
holes=[(x,y) for x in [-24,24] for y in [-79,54]]
# Broaden front perimeter while retaining all existing apertures and bosses.
# Front side walls are deliberately thicker than rear walls in this fit study.
p['front_shell']=union([p['front_shell'],diff(rounded(66,174,10.5,5,5.25),[rounded(61.98,174.02,12,5,5.25)])])
back=diff(rounded(66,174,17,5,-8.5),[rounded(62,170,20,3,-5)])
back=union([back,*[cyl(3,9.6 if y==-79 else 14.2,[x,y,-10.2 if y==-79 else -7.9]) for x,y in holes],*[cyl(3,9.1,[x,26,-10.45]) for x in [-25,25]]])
back=diff(back,[*[cyl(1.15,50,[x,y,0]) for x,y in holes],*[cyl(2.4,1.8,[x,y,-16.2],6) for x,y in holes]])
back=diff(back,[*[cyl(1.15,20,[x,26,-10]) for x in [-25,25]],*[cyl(2.4,1.8,[x,26,-16.2],6) for x in [-25,25]]])
p['rear_shell']=back
p['battery_246524_max_envelope']=box([59.5,78.5,7.9],[0,-35,-9.95])
p['battery_insulator']=diff(box([60,80,.2],[0,-35,-5.65]),[box([6,7,2],[0,-40,-5.65])])
# Removable, noncompressive cage. Clearance is measured against max cycled cell.
frame=union([*[box([55,6,1.2],[0,y,-4.8]) for y in [-60,-20,-79]],*[box([3,108,1.2],[x,-26,-4.8]) for x in [-26,26]],box([56,6,1.2],[0,26,-5.3])])
frame=diff(frame,[*[cyl(1.15,6,[x,-79,-5]) for x in [-24,24]],*[cyl(1.15,6,[x,26,-5]) for x in [-25,25]]])
p['battery_retainer']=frame
for i,x in enumerate([-24,24]):p[f'retainer_spacer_{i}']=diff(cyl(3,3.4,[x,-79,-2.5]),[cyl(1.15,5,[x,-79,-2.5])])
for i,x in enumerate([-25,25]):
 p[f'retainer_bolt_{i}']=union([cyl(1,12,[x,26,-10.7]),cyl(1.9,2,[x,26,-3.7])])
 p[f'retainer_nut_{i}']=diff(cyl(2.3,1.6,[x,26,-16.2],6),[cyl(1,3,[x,26,-16.2])])
p['external_NTC_reserved']=box([3.7,4,2.4],[0,-40,-4.7])

for i,(x,y) in enumerate(holes,1):
 p[f'bolt_{i}']=union([cyl(1,28,[x,y,-3.5]),cyl(1.9,2,[x,y,11.5])])
 p[f'nut_{i}']=diff(cyl(2.3,1.6,[x,y,-16.2],6),[cyl(1,3,[x,y,-16.2])])
# Collisions of new cell against physical parts, excluding exterior case checked separately.
hits=[]
for name,m in p.items():
 if name=='battery_246524_max_envelope' or 'reserved' in name:continue
 hit=tm.boolean.intersection([p['battery_246524_max_envelope'],m],engine='manifold')
 if len(hit.faces) and abs(hit.volume)>.001:hits.append([name,float(hit.volume)])
assert not hits,hits
scene=tm.Scene();exploded=tm.Scene()
for name,m in p.items():
 assert m.is_watertight,name
 if name in ['rear_shell','front_shell','battery_retainer'] or name.startswith('retainer_spacer'):m.export(out/f'{name}.stl')
 if name=='rear_shell' or name.startswith('battery_cradle'):m.visual.face_colors=[47,61,74,255]
 if name=='battery_246524_max_envelope':m.visual.face_colors=[238,171,54,255]
 a=m.copy();a.apply_scale(.001);scene.add_geometry(a,node_name=name,geom_name=name)
 a=m.copy();a.apply_translation([0,0,-45 if name=='rear_shell' else -25 if name.startswith('battery') else 30 if name=='front_shell' else 0]);a.apply_scale(.001);exploded.add_geometry(a,node_name=name,geom_name=name)
scene.export(out/'assembly.glb');exploded.export(out/'exploded.glb')
report={'status':'preferred flat candidate; not released enclosure','battery':'Jauch 246524 LP735977JH+PCM+2 WIRES 70MM','case_nominal_mm':[66,174,27.5],'cell_max_mm':[59.5,78.5,7.9],'cell_center_mm':[0,-35,-9.95],'cell_to_rear_floor_mm':1.1,'cell_to_insulator_mm':.25,'cell_to_retainer_bar_mm':.6,'cell_side_clearance_mm':1.25,'fastener':'M2x28 nominal envelope; vendor drawing/tolerance unverified','new_cell_boolean_checks':sum(n!='battery_246524_max_envelope' and 'reserved' not in n for n in p),'cell_collisions':hits,'meshes':len(p),'watertight':sum(m.is_watertight for m in p.values()),'not_verified':['retainer prototype tolerance, fatigue and drop loads; no compression intended','lead exit orientation and 70+/-3 mm AWG20 routing','high-current polarized connector','external NTC attachment and wire route; two-wire pack does not expose NTC','thermal separation from charger/modem','front/rear registration seam and tool access','all prior display FPC and acoustic/RF fit gates']}
(out/'checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
