from pathlib import Path
import hashlib,json
from shapely.geometry import LineString
j=json.load(open('output/usb-placement-v50.circuit.json'));c=json.load(open('routing/usb-layered-v50.json'));prior=json.load(open('routing/usb-layered-v49.json'));ids={x[x['type']+'_id']:x for x in j if x['type']+'_id' in x}
assert [r for r in c['routes'] if not r['name'].startswith('MCU_CHARGE50_')]==prior['routes']
assert [v for v in c['vias'] if not v['name'].startswith('MCU_CHARGE50_')]==prior['vias']
u=next(x for x in j if x['type']=='source_component' and x['name']=='R_CHARGE_REQUEST_OFF');assert u['manufacturer_part_number']=='RT0603BRD07100KL'
for pin,net in [(1,'CHARGE_REQUEST_MCU'),(2,'GND')]:
 port=next(x for x in j if x['type']=='source_port' and x['source_component_id']==u['source_component_id'] and x['pin_number']==pin)
 nets={ids[n]['name'] for t in j if t['type']=='source_trace' and port['source_port_id'] in t.get('connected_source_port_ids',[]) for n in t.get('connected_source_net_ids',[])}
 assert nets=={net}
lengths={r['name']:LineString(r['points']).length for r in c['routes'] if r['name'].startswith('MCU_CHARGE50_')};assert max(lengths.values())<10
assert hashlib.sha256(Path('/workspace/anas-phone-study-v49.zip').read_bytes()).hexdigest()=='f395c6e6e29c5375d6d69a3188504861172ef026ff2e169cdb0a579fda5738bc'
assert not any(x.get('manufacturer_part_number')=='SN74LVC1G97DBVR' for x in j)
Path('output/charge-request-bias-v50.json').write_text(json.dumps({'old_routes_and_vias_unchanged':True,'correct_MPN_and_nets':True,'new_route_lengths_mm':lengths,'Schmitt_alternative_not_integrated':True,'scope':'Existing pull-down placement only; does not prove charge-disable or MCU fault behavior.','release':False},indent=2));print('PASS request bias pin mapping, short routes, V49 integrity; alternative remains isolated')
