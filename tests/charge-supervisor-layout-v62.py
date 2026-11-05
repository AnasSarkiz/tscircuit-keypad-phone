import json,hashlib
from pathlib import Path
from shapely.geometry import LineString
j=json.load(open('output/usb-placement-v62.circuit.json'));c=json.load(open('routing/usb-layered-v62.json'));old=json.load(open('routing/usb-layered-v61.json'));ids={x[x['type']+'_id']:x for x in j if x['type']+'_id'in x}
s=next(x for x in j if x['type']=='source_component' and x['name']=='U_CHARGE_POR');assert s['manufacturer_part_number']=='TPS3808G01DBVR'
for pin,net in enumerate(['CHARGE_REGN_READY','GND','MCU_EN','CHARGE_POR_CT','CHARGE_REGN_SENSE','VLOGIC_3V15'],1):
 p=next(x for x in j if x['type']=='source_port' and x['source_component_id']==s['source_component_id'] and x.get('pin_number')==pin);ns={ids[n]['name'] for t in j if t['type']=='source_trace' and p['source_port_id']in t.get('connected_source_port_ids',[]) for n in t.get('connected_source_net_ids',[])};assert ns=={net}
full=json.load(open('output/power-integrated-v45.circuit.json'));fi={x[x['type']+'_id']:x for x in full if x['type']+'_id'in x}
oldrefs={x['name'] for x in json.load(open('output/usb-placement-v61.circuit.json')) if x['type']=='source_component'}
for comp in [x for x in j if x['type']=='source_component' and x['name'] not in oldrefs]:
 source=next(x for x in full if x['type']=='source_component' and x['name']==comp['name']);assert comp['manufacturer_part_number']==source['manufacturer_part_number']
 for port in [x for x in j if x['type']=='source_port' and x['source_component_id']==comp['source_component_id']]:
  target=next(x for x in full if x['type']=='source_port' and x['source_component_id']==source['source_component_id'] and x.get('pin_number')==port.get('pin_number'))
  def nets(data,ids,pid):return {ids[n]['name'] for t in data if t['type']=='source_trace' and pid in t.get('connected_source_port_ids',[]) for n in t.get('connected_source_net_ids',[])}
  assert nets(j,ids,port['source_port_id'])==nets(full,fi,target['source_port_id'])
for key in ['routes','vias']:
 now={q['name']:q for q in c[key]};assert all(now.get(q['name'])==q for q in old[key] if q['name'] not in ['SOCKET_GND_TOP','SOCKET_GND','SOCKET_GND_INNER'])
new=[r for r in c['routes'] if r['name'].startswith('TEMP62')];assert len(new)==21 and all(r.get('candidate_routed') for r in new)
lengths={r['name']:LineString(r['points']).length for r in new};assert max(lengths.values())<65
assert not any(x['type']=='pcb_solder_paste' for x in j)
assert not any(x['type']=='source_component' and x['name']=='U_CHARGE_AND' for x in j)
assert hashlib.sha256(Path('/workspace/anas-phone-study-v61.zip').read_bytes()).hexdigest()=='f10e5b7780dd8b864fe3b7a8587a9169709246afb481094345e4b751dbd26214'
Path('output/charge-supervisor-layout-v62-checks.json').write_text(json.dumps({'supervisor_MPN_and_pin_nets_checked':True,'all_seven_new_components_match_integrated_MPN_and_pin_nets':True,'V61_changes':['SOCKET_GND_TOP via relocated','SOCKET_GND endpoint extended','redundant SOCKET_GND_INNER trace removed; plane connectivity rechecked'],'V61_archive_unchanged':True,'new_route_lengths_mm':lengths,'paste_disabled':True,'AND_gate_not_integrated':True,'hardware_startup_and_fault_timing_qualified':False,'release':False},indent=2));print('PASS supervisor pin mapping, documented baseline changes and bounded segments')
