from pathlib import Path
import json,hashlib
from shapely.geometry import LineString
j=json.load(open('output/usb-placement-v53.circuit.json'));c=json.load(open('routing/usb-layered-v53.json'));old=json.load(open('routing/usb-layered-v52.json'));ids={x[x['type']+'_id']:x for x in j if x['type']+'_id' in x}
assert [r for r in c['routes'] if not r['name'].startswith('MCU_START53_') and r['name'] not in ['MCU_RESET_LONG_AUTO','MCU_DBG_EN_AUTO','MCU_DBG_VREF_AUTO']]==[r for r in old['routes'] if r['name'] not in ['MCU_RESET_LONG_AUTO','MCU_DBG_EN_AUTO','MCU_DBG_VREF_AUTO']]
assert [v for v in c['vias'] if not v['name'].startswith('MCU_START53_')]==old['vias']
expected={'Q_BUTTON_KILL':('AO3400A',{1:'SYSTEM_OFF_REQUEST',2:'GND',3:'BUTTON_KILL_BRANCH'}),'R_BUTTON_INT_UP':('RT0603BRD07100KL',{1:'VLOGIC_3V15',2:'BUTTON_INT_N'}),'R_BUTTON_KILL_UP':('RT0603BRD07100KL',{1:'VLOGIC_3V15',2:'BUTTON_KILL_BRANCH'})}
for ref,(mpn,pins) in expected.items():
 u=next(x for x in j if x['type']=='source_component' and x['name']==ref);assert u['manufacturer_part_number']==mpn
 for pin,net in pins.items():
  port=next(x for x in j if x['type']=='source_port' and x['source_component_id']==u['source_component_id'] and x.get('pin_number')==pin)
  nets={ids[n]['name'] for t in j if t['type']=='source_trace' and port['source_port_id'] in t.get('connected_source_port_ids',[]) for n in t.get('connected_source_net_ids',[])};assert nets=={net}
for name in ['MCU_RESET_LONG_AUTO','MCU_DBG_EN_AUTO','MCU_DBG_VREF_AUTO']:
 before=next(r for r in old['routes'] if r['name']==name);after=next(r for r in c['routes'] if r['name']==name)
 assert before['points'][0]==after['points'][0] and before['points'][-1]==after['points'][-1]
 assert before['net']==after['net'] and before['layer']==after['layer'] and before['pads']==after['pads']
 assert LineString(after['points']).length<=LineString(before['points']).length+3
q=next(x for x in j if x['type']=='source_component' and x['name']=='Q_BUTTON_KILL');pc=next(x for x in j if x['type']=='pcb_component' and x['source_component_id']==q['source_component_id']);pads={int(x['port_hints'][0][3:]):x for x in j if x['type']=='pcb_smtpad' and x['pcb_component_id']==pc['pcb_component_id']}
for pin,x,y in [(1,-9.95,21.8),(2,-8.05,21.8),(3,-9,24.2)]:assert abs(pads[pin]['x']-x)<1e-8 and abs(pads[pin]['y']-y)<1e-8 and pads[pin]['width']==.8 and pads[pin]['height']==.8
assert pads[1]['x']<pads[2]['x'];assert not pads[2]['x']<pads[1]['x'] # mirror rejected
lengths={r['name']:LineString(r['points']).length for r in c['routes'] if r['name'].startswith('MCU_START53_')};assert max(lengths.values())<65
sha=hashlib.sha256(Path('/workspace/anas-phone-study-v52.zip').read_bytes()).hexdigest();assert sha=='1590af948fad914444c41bf6f2e7688a285fdd121984ea508afadb7c30a560e2'
assert not any(x.get('name')=='U_BUTTON_BRANCH' for x in j if x['type']=='source_component')
Path('output/startup-interface-v53-checks.json').write_text(json.dumps({'MPN_and_nets_checked':True,'AO3400A_geometry_and_orientation_checked':True,'V52_routes_unchanged_except_three_local_trace_adjustments':True,'controller_remains_unplaced':True,'new_route_lengths_mm':lengths,'baseline_sha256':sha,'scope':'Physical interface connectivity only; startup and brownout behavior not qualified','release':False},indent=2));print('PASS startup interface pin/net/orientation, route bounds and V52 integrity',lengths)
