from pathlib import Path
import json,hashlib
from shapely.geometry import Point,shape
j=json.load(open('output/usb-placement-v65.circuit.json'));ids={x[x['type']+'_id']:x for x in j if x['type']+'_id' in x}
geom=json.load(open('output/usb-layered-v65-geometry.json'));c=json.load(open('routing/usb-layered-v65.json'));old=json.load(open('routing/usb-layered-v62.json'))
assert c['routes'][:len(old['routes'])]==old['routes'] and c['vias'][:len(old['vias'])]==old['vias']
holes=[x for x in j if x['type']=='pcb_plated_hole'];assert len(holes)==60
minimum=100;count=0
for h in holes:
 comp=ids[ids[h['pcb_component_id']]['source_component_id']]['name'];i=int(comp[2:])-1;row=i//3;col=i%3
 logical=next(k for k in h['port_hints'] if k in ['pin1','pin2']);xy=([-14,0,14][col],[-21,-33,-45,-57,-69][row]);assert abs(abs(h['x']-xy[0])-3.25)<1e-9
 assert abs(h['y']-xy[1]-(2.25 if logical=='pin1' else -2.25))<1e-9
 assert h['hole_diameter']==1 and h['outer_diameter']==2
 port=ids[h['pcb_port_id']]['source_port_id'];nets={ids[n]['name'] for t in j if t['type']=='source_trace' and port in t.get('connected_source_port_ids',[]) for n in t.get('connected_source_net_ids',[])}
 expected=('BUTTON_BRANCH_UNQUALIFIED' if logical=='pin1' else 'GND') if i==2 else ('ROW'+str(row) if logical=='pin1' else 'COL'+str(col));assert nets=={expected}
 for g in geom:
  if g['net']==expected:continue
  gap=Point(h['x'],h['y']).distance(shape(g['geometry']))-.5;minimum=min(minimum,gap);count+=1
  assert gap>=.2-1e-8,(comp,g['name'],gap)
plane=lambda data:shape(next(g for g in data if g['kind']=='plane')['geometry'])
delta=plane(geom).symmetric_difference(plane(json.load(open('output/usb-layered-v62-geometry.json')))).area;assert delta<1e-8
assert hashlib.sha256(Path('/workspace/anas-phone-study-v62.zip').read_bytes()).hexdigest()=='8eae07c9cce903ba9731381f8877069207ed9877bd1c482c01543da1def15dcd'
out={'all60finished_holes_and_pin_nets_checked':True,'all_V62_routes_vias_preserved':True,'V62_archive_unchanged':True,'foreign_geometry_drill_checks':count,'minimum_switch_finished_hole_to_foreign_geometry_mm':minimum,'ground_plane_change_mm2':delta,'main_board_keypad_local_segments':len([r for r in c['routes'] if r['name'].startswith('KEY65')]),'MCU_matrix_connections_complete':False,'factory_plating_and_hole_tolerance_qualified':False,'release':False}
Path('output/keypad-integration-v65.json').write_text(json.dumps(out,indent=2));print(out)
