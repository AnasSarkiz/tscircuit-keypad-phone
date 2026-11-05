from pathlib import Path
import json,tempfile,subprocess
root=Path.cwd();original=json.loads((root/'routing/usb-layered-v33.json').read_text());out={}
for name,expected in [('bad_annulus','AssertionError'),('via_pad_short','G_NOR_top'),('split_plane','ground via on discarded island'),('missing_ground_via','placed ground disconnected'),('supply_open','placed supply disconnected')]:
 c=json.loads(json.dumps(original))
 if name=='bad_annulus':c['vias'][0]['drill']=.3
 if name=='via_pad_short':next(v for v in c['vias'] if v['name']=='G_NOR')['xy']=[-8.3,-62.05]
 if name=='split_plane':c['ground_boundary']=[-24,-80.5,0,-60.5]
 if name=='missing_ground_via':c['vias']=[v for v in c['vias'] if v['name']!='G_CC_CAP']
 if name=='supply_open':c['routes']=[r for r in c['routes'] if r['name']!='AUX_SUPPLY_BRIDGE']
 with tempfile.TemporaryDirectory() as td:
  d=Path(td)
  for sub in ['engineering','routing','output']:(d/sub).mkdir()
  (d/'engineering/usb_layered_v33.py').write_bytes((root/'engineering/usb_layered_v33.py').read_bytes());(d/'routing/usb-layered-v33.json').write_text(json.dumps(c));(d/'output/usb-placement-v33.circuit.json').write_bytes((root/'output/usb-placement-v33.circuit.json').read_bytes())
  p=subprocess.run([str(root/'.venv/bin/python'),str(d/'engineering/usb_layered_v33.py')],capture_output=True,text=True)
  assert p.returncode!=0,name
  assert expected in p.stderr,(name,p.stderr)
  out[name]=p.stderr.strip().splitlines()[-1]
(root/'output/usb-layered-negative-v33.json').write_text(json.dumps(out,indent=2));print('PASS five layered-copper mutations rejected',out)
