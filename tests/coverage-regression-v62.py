import json
from pathlib import Path
old=json.load(open('output/usb-layered-v61-checks.json'))['placed_net_islands'];new=json.load(open('output/usb-layered-v62-checks.json'))['placed_net_islands']
count=0
for net,groups in old.items():
 for group in groups:
  assert any(set(group)<=set(g) for g in new.get(net,[])),(net,group)
  count+=1
Path('output/coverage-regression-v62.json').write_text(json.dumps({'previous_V61_islands_preserved':count,'no_previous_join_lost':True,'release':False},indent=2));print('PASS',count,'previous V61 copper groups retained')
