from pathlib import Path
import json,tempfile,subprocess
root=Path.cwd();original=json.loads((root/'routing/usb-layered-v37.json').read_text());out={}
for name,expected in [('bad_annulus','AssertionError'),('via_pad_short','G_NOR_top'),('split_plane','ground via on discarded island'),('missing_ground_via','placed ground disconnected'),('supply_open','placed supply disconnected'),('translator_bus_open','placed translator supply disconnected'),('modem_gate_open','placed modem control disconnected'),('sim_bypass_open','placed SIM circuit disconnected')]:
 c=json.loads(json.dumps(original))
 if name=='bad_annulus':c['vias'][0]['drill']=.3
 if name=='via_pad_short':next(v for v in c['vias'] if v['name']=='G_NOR')['xy']=[-8.3,-62.05]
 if name=='split_plane':c['ground_boundary']=[-24,-80.5,0,-60.5]
 if name=='missing_ground_via':c['vias']=[v for v in c['vias'] if v['name']!='G_CC_CAP']
 if name=='sim_bypass_open':c['routes']=[r for r in c['routes'] if r['name']!='SIM_VDD_BYPASS']
 if name=='modem_gate_open':c['routes']=[r for r in c['routes'] if r['name']!='RESET_GATE_DEFAULT']
 if name=='translator_bus_open':c['routes']=[r for r in c['routes'] if r['name']!='MODEM_EXT_TRANSLATOR_BUS']
 if name=='supply_open':c['routes']=[r for r in c['routes'] if r['name']!='AUX_SUPPLY_BRIDGE']
 with tempfile.TemporaryDirectory() as td:
  d=Path(td)
  for sub in ['engineering','routing','output']:(d/sub).mkdir()
  (d/'engineering/usb_layered_v37.py').write_bytes((root/'engineering/usb_layered_v37.py').read_bytes());(d/'routing/usb-layered-v37.json').write_text(json.dumps(c));(d/'output/usb-placement-v37.circuit.json').write_bytes((root/'output/usb-placement-v37.circuit.json').read_bytes())
  p=subprocess.run([str(root/'.venv/bin/python'),str(d/'engineering/usb_layered_v37.py')],capture_output=True,text=True)
  assert p.returncode!=0,name
  assert expected in p.stderr,(name,p.stderr)
  out[name]=p.stderr.strip().splitlines()[-1]
(root/'output/usb-layered-negative-v37.json').write_text(json.dumps(out,indent=2));print('PASS eight layered-copper mutations rejected',out)
