from pathlib import Path
import json,tempfile,subprocess,os
from concurrent.futures import ThreadPoolExecutor
root=Path.cwd();original=json.loads((root/'routing/usb-layered-v61.json').read_text());out={}
cases=[(n,'placed ground disconnected' if n=='GND' else 'G_NOR_top' if n=='via_pad_short' else 'placed temperature interlock endpoint disconnected') for n in ['REGN','NTC_BRIDGE','NTC_B','PARALLEL','SERIES','GND','via_pad_short']]
def run_case(case):
 name,expected=case
 c=json.loads(json.dumps(original))
 c['routes']=[r for r in c['routes'] if r['name']!='TEMP61_'+name+'_AUTO']
 if name=='via_pad_short':next(v for v in c['vias'] if v['name']=='G_NOR')['xy']=[-8.3,-62.05]
 with tempfile.TemporaryDirectory() as td:
  d=Path(td)
  for sub in ['engineering','routing','output']:(d/sub).mkdir()
  (d/'engineering/usb_layered_v61.py').write_bytes((root/'engineering/usb_layered_v61.py').read_bytes());(d/'routing/usb-layered-v61.json').write_text(json.dumps(c));(d/'output/usb-placement-v61.circuit.json').write_bytes((root/'output/usb-placement-v61.circuit.json').read_bytes())
  p=subprocess.run([str(root/'.venv/bin/python'),str(d/'engineering/usb_layered_v61.py')],capture_output=True,text=True)
  assert p.returncode!=0,name
  assert expected in p.stderr,(name,p.stderr)
  result=p.stderr.strip().splitlines()[-1]
  (root/'output'/('fault-v61-'+name+'.json')).write_text(json.dumps({'name':name,'expected':expected,'result':result,'routing_sha256':__import__('hashlib').sha256((root/'routing/usb-layered-v61.json').read_bytes()).hexdigest()}))
  return name,result
selected=os.environ.get('NEGATIVE_CASES')
if selected:cases=[c for c in cases if c[0] in selected.split(',')]
with ThreadPoolExecutor(max_workers=3) as pool:out=dict(pool.map(run_case,cases))
(root/'output/usb-layered-negative-v61.json').write_text(json.dumps(out,indent=2));print('PASS',len(out),'selected layered-copper mutations rejected',out)
