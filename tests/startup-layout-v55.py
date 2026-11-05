from pathlib import Path
import json,hashlib
from shapely.geometry import LineString
j=json.load(open('output/usb-placement-v55.circuit.json'));c=json.load(open('routing/usb-layered-v55.json'));old=json.load(open('routing/usb-layered-v53.json'));ids={x[x['type']+'_id']:x for x in j if x['type']+'_id' in x}
assert [r for r in c['routes'] if not r['name'].startswith('START55_')]==old['routes']
assert [v for v in c['vias'] if not v['name'].startswith('START55_')]==old['vias']
expected={'U_BUTTON_BRANCH':('LTC2954ITS8-1#TRMPBF',{1:'SYS_CANDIDATE',2:'BUTTON_BRANCH_UNQUALIFIED',4:'GND',5:'BUTTON_INT_N',6:'BUTTON_ENABLE_RAW',7:'BUTTON_PDT_BRANCH',8:'BUTTON_KILL_BRANCH'}),'U_BUTTON_EN_BUFFER':('SN74LVC1G17DBVR',{2:'BUTTON_ENABLE_RAW',3:'GND',4:'LOGIC_ENABLE',5:'SYS_CANDIDATE'}),'R_BUTTON_EN_UP':('RC0603FR-0710KL',{1:'SYS_CANDIDATE',2:'BUTTON_ENABLE_RAW'}),'R_BUTTON_EN_DOWN':('RT0603BRD07100KL',{1:'BUTTON_ENABLE_RAW',2:'GND'}),'R_EN_OFF':('RT0603BRD07100KL',{1:'LOGIC_ENABLE',2:'GND'}),'C_BUTTON_BUFFER':('C0603C104K5RACTU',{1:'SYS_CANDIDATE',2:'GND'}),'C_BUTTON_BYPASS':('C0603C104K5RACTU',{1:'SYS_CANDIDATE',2:'GND'}),'C_BUTTON_PDT':('C0805C225K5RACTU',{1:'BUTTON_PDT_BRANCH',2:'GND'})}
for ref,(mpn,pins) in expected.items():
 u=next(x for x in j if x['type']=='source_component' and x['name']==ref);assert u['manufacturer_part_number']==mpn,(ref,u.get('manufacturer_part_number'))
 for pin,net in pins.items():
  port=next(x for x in j if x['type']=='source_port' and x['source_component_id']==u['source_component_id'] and x.get('pin_number')==pin)
  nets={ids[n]['name'] for t in j if t['type']=='source_trace' and port['source_port_id'] in t.get('connected_source_port_ids',[]) for n in t.get('connected_source_net_ids',[])};assert nets=={net},(ref,pin,nets)
u=next(x for x in j if x['type']=='source_component' and x['name']=='U_BUTTON_BRANCH');pc=next(x for x in j if x['type']=='pcb_component' and x['source_component_id']==u['source_component_id']);pads={int(x['port_hints'][0][3:]):x for x in j if x['type']=='pcb_smtpad' and x['pcb_component_id']==pc['pcb_component_id']};assert set(pads)==set(range(1,9))
audit=json.load(open('sourcing/startup-land-audit-v54.json'))
for pin,xy in audit['top_view_y_down_pin_centers'].items():
 p=pads[int(pin)];assert abs(p['x']-(-16+xy[0]))<1e-8 and abs(p['y']-(52-xy[1]))<1e-8
 assert p['width']==1.22 and p['height']==.4
assert pads[1]['x']<pads[8]['x'];assert pads[1]['y']>pads[4]['y']
assert not (pads[8]['x']<pads[1]['x']) # mirror negative
lengths={r['name']:LineString(r['points']).length for r in c['routes'] if r['name'].startswith('START55_')};limits={'START55_KILL_BOTTOM_AUTO':100,'START55_INT_BOTTOM_AUTO':100};assert all(length<limits.get(name,65) for name,length in lengths.items()),lengths # explicit geometric detour allowance, not electrical qualification
sha=hashlib.sha256(Path('/workspace/anas-phone-study-v53.zip').read_bytes()).hexdigest();assert sha=='6be1d93da30fb13fc3e6961867af7efbd278361a981bb18ae41f6e5780f0e65c'
assert not any(x['type']=='pcb_solder_paste' for x in j)
Path('output/startup-layout-v55-checks.json').write_text(json.dumps({'eight_new_parts_MPN_pin_nets_checked':True,'TS8_reference_lands_and_top_orientation_checked':True,'TS8_width_is_MAX_not_released_nominal':True,'V53_routes_and_vias_unchanged':True,'new_route_lengths_mm':lengths,'baseline_sha256':sha,'PB_physical_button_unresolved':True,'SYS_feed_and_logic_regulator_unplaced':True,'startup_behavior_qualified':False,'long_route_exceptions_mm':limits,'long_route_timing_noise_review_required':True,'release':False},indent=2));print('PASS startup layout mapping, reference geometry, quarantine, route bounds and V53 archive integrity',lengths)
