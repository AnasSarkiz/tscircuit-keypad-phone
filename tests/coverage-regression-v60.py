import json
from pathlib import Path
old=json.load(open('output/usb-layered-v58-checks.json'))['placed_net_islands'];new=json.load(open('output/usb-layered-v60-checks.json'))['placed_net_islands']
count=0
for net,groups in old.items():
 for group in groups:
  assert any(set(group)<=set(g) for g in new.get(net,[])),(net,group)
  count+=1
Path('output/coverage-regression-v60.json').write_text(json.dumps({'previous_V58_islands_preserved':count,'no_previous_join_lost':True,'release':False},indent=2));print('PASS',count,'previous V58 copper groups retained')
