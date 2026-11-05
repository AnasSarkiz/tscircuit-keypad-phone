from pathlib import Path
import json,tempfile,subprocess,os
from concurrent.futures import ThreadPoolExecutor
root=Path.cwd();original=json.loads((root/'routing/usb-layered-v54.json').read_text());out={}
cases=[('ctrl_sys_open', 'placed UART endpoint disconnected'), ('ctrl_int_open', 'placed UART endpoint disconnected'), ('ctrl_en_open', 'placed UART endpoint disconnected'), ('ctrl_kill_open', 'placed UART endpoint disconnected'), ('ctrl_pdt_open', 'placed UART endpoint disconnected'), ('enable_output_open', 'placed UART endpoint disconnected'), ('ctrl_ground_open', 'placed ground disconnected'), ('via_pad_short', 'G_NOR_top')]
def run_case(case):
 name,expected=case
 c=json.loads(json.dumps(original))
 if name=='ctrl_sys_open':c['routes']=[r for r in c['routes'] if r['name']!='START54_CTRL_SYS_AUTO']
 if name=='ctrl_int_open':c['routes']=[r for r in c['routes'] if r['name']!='START54_CTRL_INT_AUTO']
 if name=='ctrl_en_open':c['routes']=[r for r in c['routes'] if r['name']!='START54_CTRL_EN_AUTO']
 if name=='ctrl_kill_open':c['routes']=[r for r in c['routes'] if r['name']!='START54_KILL_INNER_AUTO']
 if name=='ctrl_pdt_open':c['routes']=[r for r in c['routes'] if r['name']!='START54_CTRL_PDT_AUTO']
 if name=='enable_output_open':c['routes']=[r for r in c['routes'] if r['name']!='START54_ENABLE_OUTPUT_AUTO']
 if name=='ctrl_ground_open':c['vias']=[v for v in c['vias'] if v['name']!='START54_CTRL_GROUND']
 if name=='via_pad_short':next(v for v in c['vias'] if v['name']=='G_NOR')['xy']=[-8.3,-62.05]
 with tempfile.TemporaryDirectory() as td:
  d=Path(td)
  for sub in ['engineering','routing','output']:(d/sub).mkdir()
  (d/'engineering/usb_layered_v54.py').write_bytes((root/'engineering/usb_layered_v54.py').read_bytes());(d/'routing/usb-layered-v54.json').write_text(json.dumps(c));(d/'output/usb-placement-v54.circuit.json').write_bytes((root/'output/usb-placement-v54.circuit.json').read_bytes())
  p=subprocess.run([str(root/'.venv/bin/python'),str(d/'engineering/usb_layered_v54.py')],capture_output=True,text=True)
  assert p.returncode!=0,name
  assert expected in p.stderr,(name,p.stderr)
  return name,p.stderr.strip().splitlines()[-1]
selected=os.environ.get('NEGATIVE_CASES')
if selected:cases=[c for c in cases if c[0] in selected.split(',')]
with ThreadPoolExecutor(max_workers=3) as pool:out=dict(pool.map(run_case,cases))
(root/'output/usb-layered-negative-v54.json').write_text(json.dumps(out,indent=2));print('PASS',len(out),'selected layered-copper mutations rejected',out)
