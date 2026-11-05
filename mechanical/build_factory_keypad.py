"""Alternative purchased-keytop fit assembly. Baseline preserved in output/.
B3F-1050 + B32-2010: manufacturer-supported family pairing, envelopes only.
Panel and hole dimensions still require printed coupon and sample validation.
"""
from pathlib import Path
import json
import trimesh as tm
root=Path(__file__).resolve().parents[1]
out=root/'output'/'factory-keypad';out.mkdir(exist_ok=True)
scene=tm.load(root/'output/assembly.glb',force='scene')
parts={n:m.copy() for n,m in scene.geometry.items()}
for m in parts.values():m.apply_scale(1000)
def box(s,c):m=tm.creation.box(s);m.apply_translation(c);return m
def cyl(r,h,c):m=tm.creation.cylinder(radius=r,height=h,sections=48);m.apply_translation(c);return m
def union(ms):return tm.boolean.union(ms,engine='manifold')
def diff(a,bs):return tm.boolean.difference([a,*bs],engine='manifold')
xy=[(x,y) for y in [-21,-33,-45,-57,-69] for x in [-14,0,14]]
front=union([parts['front_shell'],*[box([10,11,2],[x,y,9.5]) for x,y in xy]])
# Panel outside at 9.6, inside at 8.5: 1.1 nominal thickness. Case rim unchanged.
front=diff(front,[box([46,63,2],[0,-45,10.6]),*[cyl(3.25,8,[x,y,9]) for x,y in xy]])
front.visual.face_colors=[47,61,74,255];parts['front_shell']=front
for i,(x,y) in enumerate(xy,1):
 sw=union([box([6,6,4.3],[x,y,2.95]),box([2.4,2.4,3.05],[x,y,6.575])])
 sw.visual.face_colors=[30,34,40,255];parts[f'SW{i}_B3F']=sw
 cap=diff(cyl(3,5.5,[x,y,8.05]),[box([2.5,2.5,2.85],[x,y,6.675])])
 cap.visual.face_colors=[60,65,75,255];parts[f'keycap_{i}']=cap
collisions=[]
for name in [f'SW{i}_B3F' for i in range(1,16)]+[f'keycap_{i}' for i in range(1,16)]:
 for dz in [0,-.45]:
  m=parts[name].copy();m.apply_translation([0,0,dz])
  hit=tm.boolean.intersection([m,front],engine='manifold')
  if len(hit.faces) and abs(hit.volume)>.001:collisions.append([name,dz,float(hit.volume)])
assembly=tm.Scene();exploded=tm.Scene()
for name,m in parts.items():
 assert m.is_watertight,name
 if name=='front_shell' or name.startswith('keycap'):m.export(out/f'{name}.stl')
 g=m.copy();g.apply_scale(.001);assembly.add_geometry(g,node_name=name,geom_name=name)
 e=m.copy();e.apply_translation([0,0,40 if name=='front_shell' else 25 if name.startswith('keycap') else -35 if name=='rear_shell' else 0]);e.apply_scale(.001);exploded.add_geometry(e,node_name=name,geom_name=name)
assembly.export(out/'assembly.glb');exploded.export(out/'exploded.glb')
# Five printer-clearance trials, row from -X to +X: 6.3,6.4,6.5,6.6,6.7 mm.
coupon=diff(box([68,16,1.1],[0,0,.55]),[cyl(d/2,4,[x,0,0]) for x,d in zip([-24,-12,0,12,24],[6.3,6.4,6.5,6.6,6.7])]);assert coupon.is_watertight;coupon.export(out/'keytop-hole-coupon.stl')
report={'status':'alternative purchased-keytop geometry; no physical mating validation','switch':'B3F-1050','keytop':'B32-2010','assembled_cap_height_above_PCB_mm':10,'height_tolerance_mm':.4,'panel_top_world_z_mm':9.6,'nominal_protrusion_mm':1.2,'minimum_protrusion_at_max_specified_pretravel_mm':.35,'hole_diameter_mm':6.5,'cap_max_diameter_mm':6.1,'radial_clearance_before_print_error_mm':.2,'nominal_panel_thickness_mm':1.1,'meshes':len(parts),'watertight':sum(m.is_watertight for m in parts.values()),'panel_motion_intersection_checks':60,'collisions':collisions,'limitations':['Switch body/plunger and keytop socket are simplified envelopes','Travel checked geometrically at 0 and 0.45mm, not throughout tilt or lateral motion; pretravel is not an overtravel limit','6mm buttons smaller than original custom 9x10mm keys; usability/legends unresolved','Press fit retention and panel tolerance need real samples','Battery and remaining assembly retain baseline blockers']}
assert not collisions,collisions
(out/'checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
