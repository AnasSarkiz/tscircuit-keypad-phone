import json,hashlib
from pathlib import Path
from shapely.geometry import LineString
j=json.load(open('output/usb-placement-v48.circuit.json'))
c=json.load(open('routing/usb-layered-v48.json'));old=json.load(open('routing/usb-layered-v45.json'))
new_names={'MCU_DBG_BL_OFF_AUTO','MCU_DBG_BL_GROUND'}
assert [r for r in c['routes'] if r['name'] not in new_names]==old['routes']
assert [v for v in c['vias'] if v['name']!='MCU_DBG_BL_GROUND']==old['vias']
u=next(x for x in j if x['type']=='source_component' and x['name']=='R_BACKLIGHT_OFF')
assert u['manufacturer_part_number']=='RT0603BRD07100KL'
ids={x[x['type']+'_id']:x for x in j if x['type']+'_id' in x}
for pin,net in [(1,'BACKLIGHT_PWM'),(2,'GND')]:
 port=next(x for x in j if x['type']=='source_port' and x['source_component_id']==u['source_component_id'] and x['pin_number']==pin)
 nets={ids[n]['name'] for t in j if t['type']=='source_trace' and port['source_port_id'] in t.get('connected_source_port_ids',[]) for n in t.get('connected_source_net_ids',[])}
 assert nets=={net}
coverage=json.load(open('output/whole-board-coverage-v48.json'))
assert coverage['minimum_joins_completed']==226 and coverage['minimum_joins_open']==296
assert not next(n for n in coverage['nets'] if n['net']=='BACKLIGHT_PWM')['complete_among_declared_terminals']
assert hashlib.sha256(Path('/workspace/anas-phone-study-v45.zip').read_bytes()).hexdigest()=='e0faeecc476359034e176f2e176ea5002fa4675454559bb7ba96cc5102cf1f61'
out={'part':'R_BACKLIGHT_OFF','MPN':u['manufacturer_part_number'],'prior_routes_and_vias_unchanged':True,'V45_archive_intact':True,'new_route_lengths_mm':{r['name']:LineString(r['points']).length for r in c['routes'] if r['name'] in new_names},'scope':'PWM pulldown joined to MCU and plane; backlight driver remains unplaced. Leakage/loaded logic, reset behavior and full backlight function unqualified.','release':False}
Path('output/backlight-bias-v48.json').write_text(json.dumps(out,indent=2));print('PASS existing routes unchanged; exact resistor/net mapping; +2 joins; full PWM net still open; V45 archive intact')
