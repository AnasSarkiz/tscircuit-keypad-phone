import json,hashlib
from pathlib import Path
from shapely.geometry import LineString
j=json.load(open('output/usb-placement-v61.circuit.json'));c=json.load(open('routing/usb-layered-v61.json'));old=json.load(open('routing/usb-layered-v60.json'));ids={x[x['type']+'_id']:x for x in j if x['type']+'_id'in x}
for ref,mpn,nets in [('R_CHG_TS_TOP','RT0603BRD075K3L',['CHG_REGN','BAT_NTC']),('R_CHG_TS_BOTTOM','RT0603BRD0730K9L',['BAT_NTC','TS_SERIES']),('R_CHG_TS_TRIM','RT0603BRD07240RL',['TS_SERIES','GND'])]:
 s=next(x for x in j if x['type']=='source_component' and x['name']==ref);assert s['manufacturer_part_number']==mpn
 for pin,net in enumerate(nets,1):
  port=next(x for x in j if x['type']=='source_port' and x['source_component_id']==s['source_component_id'] and x.get('pin_number')==pin)
  ns={ids[n]['name'] for t in j if t['type']=='source_trace' and port['source_port_id']in t.get('connected_source_port_ids',[]) for n in t.get('connected_source_net_ids',[])};assert ns=={net}
for key in ['routes','vias']:
 now={q['name']:q for q in c[key]}
 assert all(now[q['name']]==q for q in old[key])
new=[r for r in c['routes'] if r['name'].startswith('TEMP61')];assert len(new)==6 and all(r.get('candidate_routed') for r in new)
lengths={r['name']:LineString(r['points']).length for r in new};assert max(lengths.values())<30
assert not any(x['type']=='pcb_solder_paste' for x in j)
assert hashlib.sha256(Path('/workspace/anas-phone-study-v60.zip').read_bytes()).hexdigest()=='dddaa351b83f7718f746b75815b28e4f4b43fc79a6f2a256456671ee8b471906'
Path('output/sensor-bias-layout-v61-checks.json').write_text(json.dumps({'exact_MPN_pin_nets_checked':True,'V60_routes_and_vias_unchanged':True,'V60_archive_unchanged':True,'new_route_lengths_mm':lengths,'paste_disabled':True,'hardware_protection_qualified':False,'release':False},indent=2));print('PASS bias network pin mapping and baseline preservation',lengths)
