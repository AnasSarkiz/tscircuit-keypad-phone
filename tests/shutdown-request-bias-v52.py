from pathlib import Path
import hashlib,json
from shapely.geometry import LineString
j=json.load(open('output/usb-placement-v52.circuit.json'));c=json.load(open('routing/usb-layered-v52.json'));prior=json.load(open('routing/usb-layered-v50.json'));ids={x[x['type']+'_id']:x for x in j if x['type']+'_id' in x}
assert [r for r in c['routes'] if not r['name'].startswith('MCU_KILL52_')]==prior['routes']
assert [v for v in c['vias'] if not v['name'].startswith('MCU_KILL52_')]==prior['vias']
u=next(x for x in j if x['type']=='source_component' and x['name']=='R_BUTTON_KILL_OFF');assert u['manufacturer_part_number']=='RT0603BRD07100KL'
for pin,net in [(1,'SYSTEM_OFF_REQUEST'),(2,'GND')]:
 port=next(x for x in j if x['type']=='source_port' and x['source_component_id']==u['source_component_id'] and x['pin_number']==pin)
 nets={ids[n]['name'] for t in j if t['type']=='source_trace' and port['source_port_id'] in t.get('connected_source_port_ids',[]) for n in t.get('connected_source_net_ids',[])}
 assert nets=={net}
lengths={r['name']:LineString(r['points']).length for r in c['routes'] if r['name'].startswith('MCU_KILL52_')};assert max(lengths.values())<20
assert hashlib.sha256(Path('/workspace/anas-phone-study-v50.zip').read_bytes()).hexdigest()=='be413b408fa0b6cd129748c7a4f2b5f2bbbd4e3175e5eb013e295d7f2da46f0e'
assert not any(x.get('manufacturer_part_number')=='SN74LVC1G97DBVR' for x in j)
Path('output/shutdown-request-bias-v52.json').write_text(json.dumps({'old_routes_and_vias_unchanged':True,'correct_MPN_and_nets':True,'new_route_lengths_mm':lengths,'Schmitt_alternative_not_integrated':True,'scope':'Existing pull-down placement only; does not prove startup, shutdown or MCU fault behavior.','release':False},indent=2));print('PASS request bias pin mapping, short routes, V50 integrity; alternative remains isolated')
