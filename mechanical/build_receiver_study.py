"""Unverified direct-main-PCB receiver mounting proposal; NOT production geometry.
Contact pads, spring stroke and compression are intentionally NOT invented.
"""
from pathlib import Path
import json
import trimesh as tm
root=Path(__file__).resolve().parents[1];out=root/'output/receiver-study';out.mkdir(exist_ok=True)
s=tm.load(root/'output/retained-battery/assembly.glb',force='scene');parts={n:m.copy() for n,m in s.geometry.items()}
for m in parts.values():m.apply_scale(1000)
def box(sz,c):m=tm.creation.box(sz);m.apply_translation(c);return m
def diff(a,b):return tm.boolean.difference([a,*b],engine='manifold')
# Datum proposal: PCB upper face .8; receiver envelope rests there. This does
# NOT establish the manufacturer's compressed seating height.
old_bounds=parts['receiver_AR01232'].bounds.copy()
parts['receiver_AR01232'].apply_translation([0,0,-4.4])
parts['receiver_AR01232'].visual.face_colors=[210,110,35,255]
# Rectangular guide with .5 mm nominal clearance per side. Stops below front face.
# Using a 12x6x3 reference envelope only; all dimensions await the drawing.
guide=diff(box([16,10,2.5],[0,57,2.05]),[box([13,7,4],[0,57,2.05])])
# Acoustic duct starts .2 mm above envelope, stops at original shell inner roof8.5.
# Removable rigid duct is a planning solid, not bonded/watertight or acoustic proof.
duct=diff(box([16,10,4.5],[0,57,6.25]),[box([11,3,6],[0,57,6.25])])
# Reserve compliant gasket footprint; no compression/force claim.
gasket=diff(box([13,7,.2],[0,57,3.9]),[box([11,3,1],[0,57,3.9])])
parts['receiver_guide_UNVERIFIED']=guide
parts['receiver_duct_UNVERIFIED']=duct
parts['receiver_gasket_RESERVED']=gasket
for n in ['receiver_guide_UNVERIFIED','receiver_duct_UNVERIFIED']:parts[n].visual.face_colors=[80,130,180,255]
parts['receiver_gasket_RESERVED'].visual.face_colors=[220,150,40,255]
# New guides/duct vs existing component envelopes; housing/PCB touch boundaries.
hits=[];checks=0
newnames=['receiver_AR01232','receiver_guide_UNVERIFIED','receiver_duct_UNVERIFIED','receiver_gasket_RESERVED']
for n in newnames:
 for other,m in parts.items():
  if other in newnames:continue
  hit=tm.boolean.intersection([parts[n],m],engine='manifold');checks+=1
  if len(hit.faces) and abs(hit.volume)>.001:hits.append([n,other,float(hit.volume)])
assert not hits,hits
scene=tm.Scene();exploded=tm.Scene()
for n,m in parts.items():
 assert m.is_watertight,n
 a=m.copy();a.apply_scale(.001);scene.add_geometry(a,node_name=n,geom_name=n)
 b=m.copy();b.apply_translation([0,0,35 if n=='front_shell' else 20 if n in newnames else -40 if n=='rear_shell' else 0]);b.apply_scale(.001);exploded.add_geometry(b,node_name=n,geom_name=n)
scene.export(out/'assembly.glb');exploded.export(out/'exploded.glb')
# Only proposal geometry, label filenames to prevent accidental manufacture.
for n in ['receiver_guide_UNVERIFIED','receiver_duct_UNVERIFIED']:parts[n].export(out/(n+'.stl'))
report={'status':'DO NOT FABRICATE: parameterized mounting concept awaiting actual contact drawing and sample', 'preferred_assembly_changed':False,'old_receiver_to_pcb_gap_mm':float(old_bounds[0,2]-.8),'proposed_reference_envelope_mm':[12,6,3],'receiver_reference_bottom_z_mm':.8,'receiver_reference_top_z_mm':3.8,'duct_mm':[16,10,4.5],'duct_inner_mm':[11,3],'nominal_lateral_guide_clearance_mm':.5,'boolean_checks':checks,'collisions':hits,'watertight_meshes':len(parts),'missing':['contact pad XY geometry and positive-contact viewpoint','free and compressed spring heights, force/travel and overtravel stop','tolerance stack, PCB bending and receiver body allowance','main-board gold pad finish and mask/paste exclusion','guide/duct fastener attachment and assembly access','gasket compression curve, acoustic leakage and front opening alignment','physical continuity, shock/drop, buzz/rattle and acoustic test'],'fabrication_ready':False}
(out/'checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
