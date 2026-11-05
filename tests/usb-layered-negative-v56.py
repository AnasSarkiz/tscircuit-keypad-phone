from pathlib import Path
import json,tempfile,subprocess,os
from concurrent.futures import ThreadPoolExecutor
root=Path.cwd();original=json.loads((root/'routing/usb-layered-v56.json').read_text());out={}
cases=[('kill_bridge_open','placed UART endpoint disconnected'),('int_bridge_open','placed UART endpoint disconnected'),('sys_bottom_open','placed UART endpoint disconnected'),('int_bottom_open','placed UART endpoint disconnected'),('ctrl_sys_open', 'placed UART endpoint disconnected'), ('ctrl_int_open', 'placed UART endpoint disconnected'), ('ctrl_en_open', 'placed UART endpoint disconnected'), ('ctrl_kill_open', 'placed UART endpoint disconnected'), ('ctrl_pdt_open', 'placed UART endpoint disconnected'), ('enable_output_open', 'placed UART endpoint disconnected'), ('ctrl_ground_open', 'placed ground disconnected'), ('via_pad_short', 'G_NOR_top')]
def run_case(case):
 name,expected=case
 c=json.loads(json.dumps(original))
 if name=='kill_bridge_open':c['routes']=[r for r in c['routes'] if r['name']!='START56_KILL_BRIDGE_AUTO']
 if name=='int_bridge_open':c['routes']=[r for r in c['routes'] if r['name']!='START56_INT_BRIDGE_AUTO']
 if name=='sys_bottom_open':c['routes']=[r for r in c['routes'] if r['name']!='START56_SYS_BOTTOM_AUTO']
 if name=='int_bottom_open':c['routes']=[r for r in c['routes'] if r['name']!='START56_INT_LONG_AUTO']
 if name=='ctrl_sys_open':c['routes']=[r for r in c['routes'] if r['name'] not in ['START56_CTRL_SYS_AUTO','START56_CTRL_VIN_AUTO']]
 if name=='ctrl_int_open':c['routes']=[r for r in c['routes'] if r['name']!='START56_CTRL_INT_AUTO']
 if name=='ctrl_en_open':c['routes']=[r for r in c['routes'] if not (r['name'].startswith('START56_') and r['net']=='BUTTON_ENABLE_RAW')]
 if name=='ctrl_kill_open':c['routes']=[r for r in c['routes'] if r['name']!='START56_KILL_LONG_AUTO']
 if name=='ctrl_pdt_open':c['routes']=[r for r in c['routes'] if r['name']!='START56_CTRL_PDT_AUTO']
 if name=='enable_output_open':c['routes']=[r for r in c['routes'] if r['name']!='START56_ENABLE_OUTPUT_AUTO']
 if name=='ctrl_ground_open':
  c['routes']=[r for r in c['routes'] if not (r['name'].startswith('START56_') and r['net']=='GND')]
  c['vias']=[v for v in c['vias'] if not (v['name'].startswith('START56_') and v['net']=='GND')]
 if name=='via_pad_short':next(v for v in c['vias'] if v['name']=='G_NOR')['xy']=[-8.3,-62.05]
 with tempfile.TemporaryDirectory() as td:
  d=Path(td)
  for sub in ['engineering','routing','output']:(d/sub).mkdir()
  (d/'engineering/usb_layered_v56.py').write_bytes((root/'engineering/usb_layered_v56.py').read_bytes());(d/'routing/usb-layered-v56.json').write_text(json.dumps(c));(d/'output/usb-placement-v56.circuit.json').write_bytes((root/'output/usb-placement-v56.circuit.json').read_bytes())
  p=subprocess.run([str(root/'.venv/bin/python'),str(d/'engineering/usb_layered_v56.py')],capture_output=True,text=True)
  assert p.returncode!=0,name
  assert expected in p.stderr,(name,p.stderr)
  result=p.stderr.strip().splitlines()[-1]
  (root/'output'/('fault-v56-'+name+'.json')).write_text(json.dumps({'name':name,'expected':expected,'result':result,'routing_sha256':__import__('hashlib').sha256((root/'routing/usb-layered-v56.json').read_bytes()).hexdigest()}))
  return name,result
selected=os.environ.get('NEGATIVE_CASES')
if selected:cases=[c for c in cases if c[0] in selected.split(',')]
with ThreadPoolExecutor(max_workers=3) as pool:out=dict(pool.map(run_case,cases))
(root/'output/usb-layered-negative-v56.json').write_text(json.dumps(out,indent=2));print('PASS',len(out),'selected layered-copper mutations rejected',out)
