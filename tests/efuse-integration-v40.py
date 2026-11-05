"""Independent pad mapping, translated compound geometry and required control continuity."""
import json
from shapely.geometry import Polygon
from pathlib import Path
root=Path.cwd();j=json.loads((root/'output/usb-placement-v40.circuit.json').read_text());ids={x[k]:x for x in j for k in [x['type']+'_id'] if k in x}
u=next(x for x in j if x['type']=='source_component' and x['name']=='U_USB_PROTECT');p=next(x for x in j if x['type']=='pcb_component' and x['source_component_id']==u['source_component_id']);pads=[x for x in j if x['type']=='pcb_smtpad' and x['pcb_component_id']==p['pcb_component_id']];assert len(pads)==10
expected={1:'USB_3A_ENABLE_PENDING',2:'USB_OVLO',4:'USB_FAULT_N',5:'USB_VBUS_RAW',6:'USB_5V_QUALIFIED',7:'USB_DVDT',8:'GND',9:'USB_ILM'}
for a in pads:
 pin=int(a['port_hints'][0][3:]);port=ids[a['pcb_port_id']]['source_port_id'];nets={ids[n]['name'] for t in j if t['type']=='source_trace' and port in t.get('connected_source_port_ids',[]) for n in t.get('connected_source_net_ids',[])}
 assert nets==({expected[pin]} if pin in expected else set()),(pin,nets)
data=json.loads((root/'sourcing/reviewed-lands-v24.json').read_text())['packages']['RPW0010A']
for q in data['polygons']:
 a=next(a for a in pads if a['port_hints']==['pin'+str(q['pin'])]);poly=Polygon([(v['x'],v['y']) for v in a['points']]);want=Polygon([(20+v['x'],-75-v['y_down']) for v in q['points']]);assert poly.symmetric_difference(want).area<1e-9
assert not [x for x in j if x['type']=='pcb_solder_paste']
checks=json.loads((root/'output/usb-layered-v40-checks.json').read_text())
for net in ['USB_CC_FAULT_N','USB_3A_ENABLE_PENDING','USB_OVLO','USB_ILM','USB_DVDT','USB_FAULT_N','USB_CC1_RAW','USB_CC2_RAW']:
 assert len(checks['placed_net_islands'][net])==1,net
assert checks['keypad_PTH_lands_reserved']==60
assert next(x for x in j if x['type']=='pcb_board')['num_layers']==4
full=json.loads((root/'output/usb-layered-v40.circuit.json').read_text())
assert all(v['layers']==['top','inner1','inner2','bottom'] for v in full if v['type']=='pcb_via')
assert all(p['layer']=='inner1' for p in full if p['type']=='pcb_copper_pour')
print('PASS ten eFuse pads, four compound polygons, exact pin/net mapping, no paste, eight control/CC nets, four-layer stack and60 keypad reservations; power/thermal/process unqualified')
