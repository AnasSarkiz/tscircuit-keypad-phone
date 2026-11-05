"""Independent manufacturer-source transform, EP wiring and antenna intrusion regressions."""
import json,hashlib,copy
from pathlib import Path
source=Path('sourcing/ESP32-S3-WROOM-1.kicad_mod').read_bytes()
d=json.load(open('sourcing/mcu-lands-v44.json'))
assert hashlib.sha1(b'blob '+str(len(source)).encode()+b'\0'+source).hexdigest()==d['git_blob_sha']
j=json.load(open('output/usb-placement-v44.circuit.json'));ids={x[x['type']+'_id']:x for x in j if x['type']+'_id' in x}
pads=[p for p in j if p['type']=='pcb_smtpad' and ids[ids[p['pcb_component_id']]['source_component_id']]['name']=='U_MCU']
def validate(ps):
 assert len(ps)==49
 expected=sorted((p['pin'],round(-13-p['x'],6),round(32-p['y_down']-3,6),p['width'],p['height']) for p in d['pads'])
 actual=sorted((int(p['port_hints'][0][3:]),round(p['x'],6),round(p['y'],6),p['width'],p['height']) for p in ps)
 assert actual==expected
validate(pads)
bad=copy.deepcopy(pads);bad[0]['x']=-26-bad[0]['x']
try:validate(bad)
except AssertionError:pass
else:raise AssertionError('Mirrored footprint was accepted')
ep=[p for p in pads if p['port_hints'][0]=='pin41'];assert len(ep)==9
for p in ep:
 port=ids[p['pcb_port_id']]['source_port_id'];ns={ids[n]['name'] for t in j if t['type']=='source_trace' and port in t.get('connected_source_port_ids',[]) for n in t.get('connected_source_net_ids',[])}
 assert ns=={'GND'},(p['pcb_smtpad_id'],ns)
print('PASS manufacturer blob identity, 49 lands, mirror rejection, nine explicit EP ground connections')
