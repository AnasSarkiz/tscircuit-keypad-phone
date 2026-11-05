from pathlib import Path
import json,tempfile,subprocess,os
from concurrent.futures import ThreadPoolExecutor
root=Path.cwd();original=json.loads((root/'routing/usb-layered-v58.json').read_text());out={}
cases=[(n,'placed ground disconnected' if 'GND' in n else 'placed temperature interlock endpoint disconnected') for n in ['COLD_REF1','COLD_REF2','COLD_OUT','HOT_REF','HOT_SENSE','HOT_OUT','REGN','COLD_BRIDGE','HOT_BRIDGE','COLD_END','HOT_END','COLD_GND','HOT_GND']]
def run_case(case):
 name,expected=case
 c=json.loads(json.dumps(original))
 c['routes']=[r for r in c['routes'] if r['name']!='TEMP58_'+name+'_AUTO']
 with tempfile.TemporaryDirectory() as td:
  d=Path(td)
  for sub in ['engineering','routing','output']:(d/sub).mkdir()
  (d/'engineering/usb_layered_v58.py').write_bytes((root/'engineering/usb_layered_v58.py').read_bytes());(d/'routing/usb-layered-v58.json').write_text(json.dumps(c));(d/'output/usb-placement-v58.circuit.json').write_bytes((root/'output/usb-placement-v58.circuit.json').read_bytes())
  p=subprocess.run([str(root/'.venv/bin/python'),str(d/'engineering/usb_layered_v58.py')],capture_output=True,text=True)
  assert p.returncode!=0,name
  assert expected in p.stderr,(name,p.stderr)
  result=p.stderr.strip().splitlines()[-1]
  (root/'output'/('fault-v58-'+name+'.json')).write_text(json.dumps({'name':name,'expected':expected,'result':result,'routing_sha256':__import__('hashlib').sha256((root/'routing/usb-layered-v58.json').read_bytes()).hexdigest()}))
  return name,result
selected=os.environ.get('NEGATIVE_CASES')
if selected:cases=[c for c in cases if c[0] in selected.split(',')]
with ThreadPoolExecutor(max_workers=3) as pool:out=dict(pool.map(run_case,cases))
(root/'output/usb-layered-negative-v58.json').write_text(json.dumps(out,indent=2));print('PASS',len(out),'selected layered-copper mutations rejected',out)
