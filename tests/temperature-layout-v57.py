import json,hashlib
from pathlib import Path
from shapely.geometry import LineString
j=json.load(open('output/usb-placement-v57.circuit.json'));c=json.load(open('routing/usb-layered-v57.json'));old=json.load(open('routing/usb-layered-v56.json'));ids={x[x['type']+'_id']:x for x in j if x['type']+'_id' in x}
assert [r for r in c['routes'] if not r['name'].startswith('TEMP57')]==old['routes']
assert [v for v in c['vias'] if not v['name'].startswith('TEMP57')]==old['vias']
expect={'Q_TEMP_COLD':{1:'TEMP_COLD_OK',2:'CE_MID1',3:'CHARGE_DISABLE'},'Q_TEMP_HOT':{1:'TEMP_HOT_OK',2:'CE_MID2',3:'CE_MID1'},'Q_TEMP_REQUEST':{1:'CHARGE_REQUEST_QUALIFIED_PENDING',2:'GND',3:'CE_MID2'},'R_TEMP_COLD_GATE':{1:'TEMP_COLD_OK',2:'GND'},'R_TEMP_HOT_GATE':{1:'TEMP_HOT_OK',2:'GND'},'R_TEMP_REQUEST_OFF':{1:'CHARGE_REQUEST_QUALIFIED_PENDING',2:'GND'}}
for ref,pins in expect.items():
 u=next(x for x in j if x['type']=='source_component' and x['name']==ref);assert u['manufacturer_part_number']==('AO3400A' if ref.startswith('Q_') else 'RT0603BRD07100KL')
 for pin,net in pins.items():
  port=next(x for x in j if x['type']=='source_port' and x['source_component_id']==u['source_component_id'] and x.get('pin_number')==pin)
  ns={ids[n]['name'] for t in j if t['type']=='source_trace' and port['source_port_id'] in t.get('connected_source_port_ids',[]) for n in t.get('connected_source_net_ids',[])};assert ns=={net}
 if ref.startswith('Q_'):
  pc=next(x for x in j if x['type']=='pcb_component' and x['source_component_id']==u['source_component_id']);ps={int(x['port_hints'][0][3:]):x for x in j if x['type']=='pcb_smtpad' and x['pcb_component_id']==pc['pcb_component_id']}
  for pin,(dx,dy) in {1:(-.95,-1.2),2:(.95,-1.2),3:(0,1.2)}.items():
   p=ps[pin];assert abs(p['x']-pc['center']['x']-dx)<1e-8 and abs(p['y']-pc['center']['y']-dy)<1e-8;assert p['width']==p['height']==.8
  assert ps[1]['x']<ps[2]['x'] # mirrored G/S fails this invariant
assert not any(x['type']=='pcb_solder_paste' for x in j)
lengths={r['name']:LineString(r['points']).length for r in c['routes'] if r['name'].startswith('TEMP57')};assert max(lengths.values())<15,lengths
assert hashlib.sha256(Path('/workspace/anas-phone-study-v56.zip').read_bytes()).hexdigest()=='a592a0c4f8b9c6ab5ff1380cd4eb62f6f50995e6d07e347285c94bd11b8ef93f'
Path('output/temperature-layout-v57-checks.json').write_text(json.dumps({'six_MPN_pin_net_maps_checked':True,'AO3400A_top_GSD_geometry_checked':True,'V56_routes_vias_archive_unchanged':True,'route_lengths_mm':lengths,'body_diode_orientation_preserved':True,'partial_power_and_CE_behavior_qualified':False,'gate_drivers_and_charger_unplaced':True,'release':False},indent=2));print('PASS six component mappings, AO orientation, route bounds and V56 preservation',lengths)
