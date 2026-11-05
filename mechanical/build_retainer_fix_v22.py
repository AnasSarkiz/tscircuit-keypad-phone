"""Correct modeled retainer bolt-head interference; prototype/process unqualified."""
from pathlib import Path
import trimesh as tm,json
root=Path(__file__).resolve().parents[1];out=root/'output'/'retainer-fix-v22';out.mkdir(exist_ok=True)
s=tm.load(root/'output/retained-battery/assembly.glb',force='scene');parts={n:m.copy() for n,m in s.geometry.items()}
for m in parts.values():m.apply_scale(1000)
parts['modem_EG912U_envelope'].apply_translation([.4,0,0])
old=parts['battery_retainer'];cuts=[]
for x in [-25,25]:
 c=tm.creation.cylinder(radius=2.1,height=3,sections=64);c.apply_translation([x,26,-3.2]);cuts.append(c)
new=tm.boolean.difference([old,*cuts],engine='manifold');assert new.is_watertight and new.volume>0
parts['battery_retainer']=new
for i in [0,1]:
 hit=tm.boolean.intersection([new,parts[f'retainer_bolt_{i}']],engine='manifold');assert abs(hit.volume)<.001
new.export(out/'battery_retainer.stl');scene=tm.Scene();exploded=tm.Scene()
for name,m in parts.items():
 e=m.copy();e.apply_translation([0,0,-45 if name=='rear_shell' else -25 if name.startswith('battery') else 30 if name=='front_shell' else 0]);e.apply_scale(.001);exploded.add_geometry(e,node_name=name,geom_name=name)
 m.apply_scale(.001);scene.add_geometry(m,node_name=name,geom_name=name)
scene.export(out/'assembly.glb');exploded.export(out/'exploded.glb')
(out/'changes.json').write_text(json.dumps({'source':'output/retained-battery/assembly.glb','change':'two modeled head-clearance recesses; modem shifted +0.4mm X; no screw displacement','modem_center_mm':[12,6,-2],'modem_left_nominal_gap_mm':3.5,'modem_right_courtyard_to_board_edge_mm':.5,'relative_edge_position_uncertainty_screen_mm':.3,'modem_screened_gap_mm':3.2,'centers_xy_mm':[[-25,26],[25,26]],'radius_mm':2.1,'floor_z_mm':-4.7,'nominal_head_radius_mm':1.9,'radial_clearance_mm':.2,'max_removed_top_depth_mm':.5,'underlying_crossbar_thickness_mm':1.2,'removed_volume_mm3':float(old.volume-new.volume),'not_verified':['printed tolerance','load capacity/fatigue','real fastener head diameter and bearing contact','tool access','actual battery/PCB/harness fit'],'released':False},indent=2))
print('PASS modeled bolt-head collision removed; retainer remains watertight')
