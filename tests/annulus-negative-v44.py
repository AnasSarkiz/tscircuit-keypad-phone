import json,tempfile,subprocess
from pathlib import Path
root=Path.cwd();c=json.load(open('routing/usb-layered-v44.json'));c['vias'][0]['outer']=.45
with tempfile.TemporaryDirectory() as td:
 d=Path(td)
 for f in ['engineering','output','routing']:(d/f).mkdir()
 (d/'engineering/usb_layered_v44.py').write_bytes((root/'engineering/usb_layered_v44.py').read_bytes())
 (d/'output/usb-placement-v44.circuit.json').write_bytes((root/'output/usb-placement-v44.circuit.json').read_bytes())
 (d/'routing/usb-layered-v44.json').write_text(json.dumps(c))
 p=subprocess.run([str(root/'.venv/bin/python'),str(d/'engineering/usb_layered_v44.py')],capture_output=True,text=True)
 assert p.returncode!=0 and '>=.15-1e-9' in p.stderr
 Path('output/annulus-negative-v44.json').write_text(json.dumps({'old_0_125mm_nominal_annulus_rejected':True,'error':p.stderr.strip().splitlines()[-1],'release':False},indent=2))
 print('PASS old0.45/0.20 via rejected by0.15mm nominal annulus rule')
