"""Generate unplaced body envelopes, not manufacturer STEP or routed-board placement."""
import json
from pathlib import Path
import trimesh as tm
root=Path(__file__).resolve().parents[1];out=root/'output/passive-catalog-v23';out.mkdir(exist_ok=True)
j=json.loads((root/'output/power-integrated.circuit.json').read_text());caps=json.loads((root/'sourcing/capacitor-dimensions-v18.json').read_text());rows=[];s=tm.Scene()
for c in j:
 if c['type']!='source_component':continue
 m=c.get('manufacturer_part_number','');d=None
 if m in caps:
  v=caps[m];d=[v[k][1] for k in ['length','width','height']];source=v['source'];basis='exact-MPN dimensions transcribed in V18; verify drawing and manufacturing tolerance'
 elif m.startswith(('RT0603','RC0603')):
  d=[1.7,.9,.55];source='https://yageogroup.com/component-documentation/download/specsheet/'+('RT0603BRD0710KL' if m.startswith('RT') else 'RC0603FR-0710KL');basis='family representative maximum body dimensions; individual MPN confirmation still required'
 if d is None:continue
 i=len(rows);mesh=tm.creation.box(d);mesh.visual.face_colors=[55,77,92,255] if m.startswith(('RT','RC')) else [177,142,86,255]
 mesh.apply_translation([(i%12)*5,(i//12)*5,d[2]/2]);mesh.apply_scale(.001);s.add_geometry(mesh,node_name=c['name'],geom_name=c['name'])
 rows.append({'reference':c['name'],'MPN':m,'maximum_body_mm':d,'source':source,'evidence':basis,'geometry':'simplified box; terminals absent','board_position':None,'board_side':None,'placed':False,'atlas_grid_index':i})
assert len(rows)==155 and len({r['reference'] for r in rows})==155
s.export(out/'UNPLACED-body-atlas.glb');(out/'mapping.json').write_text(json.dumps({'status':'UNPLACED catalog only; atlas coordinates are not PCB coordinates','entries':rows,'count':len(rows),'full_board_spatial_validation':False},indent=2))
for n,m in s.geometry.items():assert m.is_watertight
print('PASS 155 unique unplaced body-envelope mappings; no PCB placements added')
