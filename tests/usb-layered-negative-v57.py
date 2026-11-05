from pathlib import Path
import json,tempfile,subprocess,os
from concurrent.futures import ThreadPoolExecutor
root=Path.cwd();original=json.loads((root/'routing/usb-layered-v57.json').read_text());out={}
cases=[('cold_gate_open', 'placed temperature interlock endpoint disconnected'), ('hot_gate_open', 'placed temperature interlock endpoint disconnected'), ('request_gate_open', 'placed temperature interlock endpoint disconnected'), ('mid1_open', 'placed temperature interlock endpoint disconnected'), ('mid2_open', 'placed temperature interlock endpoint disconnected'), ('source_ground_open', 'placed ground disconnected'), ('cold_ground_open', 'placed ground disconnected'), ('hot_ground_open', 'placed ground disconnected'), ('request_ground_open', 'placed ground disconnected'), ('via_pad_short', 'G_NOR_top')]
def run_case(case):
 name,expected=case
 c=json.loads(json.dumps(original))
 if name=='cold_gate_open':c['routes']=[r for r in c['routes'] if r['name']!='TEMP57_COLD_GATE_AUTO']
 if name=='hot_gate_open':c['routes']=[r for r in c['routes'] if r['name']!='TEMP57_HOT_GATE_AUTO']
 if name=='request_gate_open':c['routes']=[r for r in c['routes'] if r['name']!='TEMP57_REQUEST_GATE_AUTO']
 if name=='mid1_open':c['routes']=[r for r in c['routes'] if r['name']!='TEMP57_MID1_AUTO']
 if name=='mid2_open':c['routes']=[r for r in c['routes'] if r['name']!='TEMP57_MID2_AUTO']
 if name=='source_ground_open':c['routes']=[r for r in c['routes'] if r['name']!='TEMP57_SOURCE_GROUND_AUTO']
 if name=='cold_ground_open':c['vias']=[v for v in c['vias'] if v['name']!='TEMP57_COLD_GND']
 if name=='hot_ground_open':c['vias']=[v for v in c['vias'] if v['name']!='TEMP57_HOT_GND']
 if name=='request_ground_open':c['vias']=[v for v in c['vias'] if v['name']!='TEMP57_REQUEST_GND']
 if name=='via_pad_short':next(v for v in c['vias'] if v['name']=='G_NOR')['xy']=[-8.3,-62.05]
 with tempfile.TemporaryDirectory() as td:
  d=Path(td)
  for sub in ['engineering','routing','output']:(d/sub).mkdir()
  (d/'engineering/usb_layered_v57.py').write_bytes((root/'engineering/usb_layered_v57.py').read_bytes());(d/'routing/usb-layered-v57.json').write_text(json.dumps(c));(d/'output/usb-placement-v57.circuit.json').write_bytes((root/'output/usb-placement-v57.circuit.json').read_bytes())
  p=subprocess.run([str(root/'.venv/bin/python'),str(d/'engineering/usb_layered_v57.py')],capture_output=True,text=True)
  assert p.returncode!=0,name
  assert expected in p.stderr,(name,p.stderr)
  result=p.stderr.strip().splitlines()[-1]
  (root/'output'/('fault-v57-'+name+'.json')).write_text(json.dumps({'name':name,'expected':expected,'result':result,'routing_sha256':__import__('hashlib').sha256((root/'routing/usb-layered-v57.json').read_bytes()).hexdigest()}))
  return name,result
selected=os.environ.get('NEGATIVE_CASES')
if selected:cases=[c for c in cases if c[0] in selected.split(',')]
with ThreadPoolExecutor(max_workers=3) as pool:out=dict(pool.map(run_case,cases))
(root/'output/usb-layered-negative-v57.json').write_text(json.dumps(out,indent=2));print('PASS',len(out),'selected layered-copper mutations rejected',out)
