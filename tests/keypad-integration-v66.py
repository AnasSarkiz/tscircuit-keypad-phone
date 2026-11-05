from pathlib import Path
import json,hashlib
from shapely.geometry import Point,shape
j=json.load(open('output/usb-placement-v66.circuit.json'));ids={x[x['type']+'_id']:x for x in j if x['type']+'_id' in x}
geom=json.load(open('output/usb-layered-v66-geometry.json'));c=json.load(open('routing/usb-layered-v66.json'));old=json.load(open('routing/usb-layered-v65.json'))
changed={'MCU_CTS_LONG_AUTO','MCU_VDD_AUTO'}
assert {r['name'] for r in c['routes'][:len(old['routes'])]}=={r['name'] for r in old['routes']}
for a,b in zip(c['routes'],old['routes']):
 if a['name'] not in changed:assert a==b
 else:assert a['net']==b['net'] and a['layer']==b['layer'] and a['width']==b['width'] and a['points'][0]==b['points'][0] and a['points'][-1]==b['points'][-1]
assert c['vias'][:len(old['vias'])]==old['vias']
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
delta=plane(geom).symmetric_difference(plane(json.load(open('output/usb-layered-v65-geometry.json')))).area;assert delta<30 # only new via antipads; independent plane continuity and neck checks required
assert hashlib.sha256(Path('/workspace/anas-phone-study-v65.zip').read_bytes()).hexdigest()=='d0dab9808fa1f8e6d33aca38c564552dd185630ac7682f4b00b0df2c7a697571'
out={'all60finished_holes_and_pin_nets_checked':True,'V65_route_changes':sorted(changed),'V65_vias_preserved':True,'V65_archive_unchanged':True,'foreign_geometry_drill_checks':count,'minimum_switch_finished_hole_to_foreign_geometry_mm':minimum,'ground_plane_change_mm2':delta,'main_board_keypad_local_segments':len([r for r in c['routes'] if r['name'].startswith('KEY65')]),'MCU_matrix_connections_complete':True,'factory_plating_and_hole_tolerance_qualified':False,'release':False}
groups=json.load(open('output/usb-layered-v66-checks.json'))['placed_net_islands']
for net in ['ROW0','ROW1','ROW2','ROW3','ROW4','COL0','COL1','COL2','BUTTON_BRANCH_UNQUALIFIED']:assert len(groups[net])==1,(net,groups[net])
Path('output/keypad-integration-v66.json').write_text(json.dumps(out,indent=2));print(out)
