import json,hashlib
from pathlib import Path
from shapely.geometry import LineString
j=json.load(open('output/usb-placement-v59.circuit.json'));c=json.load(open('routing/usb-layered-v59.json'));old=json.load(open('routing/usb-layered-v58.json'));ids={x[x['type']+'_id']:x for x in j if x['type']+'_id' in x}
expect={1:'TEMP_COLD_OK',2:'BAT_NTC',3:'TEMP_COLD_REF',4:'GND',5:'TEMP_HOT_SENSE',6:'TEMP_HOT_REF',7:'TEMP_HOT_OK',8:'CHG_REGN'}
u=next(x for x in j if x['type']=='source_component' and x['name']=='U_TEMP');assert u['manufacturer_part_number']=='TLV9032DR'
pc=next(x for x in j if x['type']=='pcb_component' and x['source_component_id']==u['source_component_id'])
for pin,net in expect.items():
 port=next(x for x in j if x['type']=='source_port' and x['source_component_id']==u['source_component_id'] and x.get('pin_number')==pin)
 ns={ids[n]['name'] for t in j if t['type']=='source_trace' and port['source_port_id'] in t.get('connected_source_port_ids',[]) for n in t.get('connected_source_net_ids',[])};assert ns=={net}
 pad=next(x for x in j if x['type']=='pcb_smtpad' and x['pcb_component_id']==pc['pcb_component_id'] and 'pin'+str(pin) in x['port_hints']);dx=-2.7 if pin<=4 else 2.7;dy=(2.5-pin if pin<=4 else pin-6.5)*1.27
 assert abs(pad['x']-pc['center']['x']-dx)<1e-8 and abs(pad['y']-pc['center']['y']-dy)<1e-8
 assert pad['width']==1.55 and pad['height']==.6
assert next(x for x in j if x['type']=='source_component' and x['name']=='C_TEMP')['manufacturer_part_number']=='C0603C104K5RACTU'
changed={'TEMP58_COLD_REF1_AUTO','TEMP58_HOT_REF_AUTO','TEMP58_HOT_SENSE_AUTO','TEMP58_HOT_OUT_AUTO','TEMP58_REGN_AUTO','C_B_TX_GND'}
current={r['name']:r for r in c['routes']}
for r in old['routes']:
 if r['name'] not in changed:assert current[r['name']]==r,r['name']
for v in old['vias']:
 if v['name']!='C_B_TX_GND':assert next(x for x in c['vias'] if x['name']==v['name'])==v
assert 'TEMP58_HOT_SENSE_AUTO' not in current
lengths={r['name']:LineString(r['points']).length for r in c['routes'] if r['name'].startswith('TEMP59')};assert max(lengths.values())<65,lengths
assert all(r.get('candidate_routed') for r in c['routes'] if r['name'].startswith('TEMP59'))
assert not any(x['type']=='pcb_solder_paste' for x in j)
assert hashlib.sha256(Path('/workspace/anas-phone-study-v58.zip').read_bytes()).hexdigest()=='f376d8412978b473e76661f9964ef68cebf6989b0ffe36151a361e8b2bbacf39'
Path('output/comparator-layout-v59-checks.json').write_text(json.dumps({'manufacturer_pin_table_checked':True,'text_derived_land_envelope_checked':True,'visual_land_overlay':False,'two_MPNs_checked':True,'V58_archive_unchanged':True,'limited_V58_route_changes':sorted(changed),'one_old_ground_via_relocated':True,'route_lengths_mm':lengths,'decoupling_supply_trace_mm':lengths['TEMP59_DECAP_AUTO'],'hardware_timing_qualified':False,'release':False},indent=2));print('PASS mappings, geometry proposal and bounded baseline changes',lengths)
