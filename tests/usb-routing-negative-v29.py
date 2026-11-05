import json,subprocess,tempfile
from pathlib import Path
root=Path.cwd();script=root/'tests/usb-routing-v29.py';original=json.loads((root/'routing/usb-local-v29.json').read_text());cases={}
for name in ['wrong_net','foreign_pad','outside_board','missed_endpoint','trace_crossing']:
 r=json.loads(json.dumps(original))
 if name=='wrong_net':r[0]['net']='GND'
 if name=='foreign_pad':r[0]['points'].insert(1,[5.6,-75.4])
 if name=='outside_board':r[0]['points'].insert(1,[29,-75])
 if name=='missed_endpoint':r[0]['points'][-1]=[4.8,-75]
 if name=='trace_crossing':r[3]['points']=[r[3]['points'][0],[-13.15,-77],[-16,-77],[-13.15,-77],r[3]['points'][-1]]
 with tempfile.TemporaryDirectory() as td:
  d=Path(td);(d/'output').mkdir();(d/'routing').mkdir();(d/'output/usb-placement-v29.circuit.json').write_bytes((root/'output/usb-placement-v29.circuit.json').read_bytes());(d/'routing/usb-local-v29.json').write_text(json.dumps(r))
  p=subprocess.run(['python3',str(script)],cwd=d,capture_output=True,text=True);assert p.returncode!=0,name
  cases[name]=p.stderr.strip().splitlines()[-1]
  expected={'wrong_net':'wrong net','foreign_pad':'pcb_smtpad_3','outside_board':'board edge','missed_endpoint':'endpoint not contacted','trace_crossing':'trace collision'}[name]
  assert expected in cases[name],(name,cases[name])
(root/'output/usb-routing-negative-v29.json').write_text(json.dumps(cases,indent=2));print('PASS five intentionally invalid layouts rejected:',cases)
