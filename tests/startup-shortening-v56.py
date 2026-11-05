import json,hashlib,math
from pathlib import Path
old=json.load(open('routing/usb-layered-v55.json'));new=json.load(open('routing/usb-layered-v56.json'));normalize=lambda x:json.loads(json.dumps(x).replace('START56','START55'))
norm=normalize(new);removed={'START55_KILL_BOTTOM_AUTO','START55_INT_BOTTOM_AUTO'}
for r in old['routes']:
 if r['name'] not in removed:assert r==next(q for q in norm['routes'] if q['name']==r['name']),r['name']
for v in old['vias']:assert v==next(q for q in norm['vias'] if q['name']==v['name']),v['name']
assert len(new['vias'])==len(old['vias'])+2
assert old['ground_boundary']==new['ground_boundary']
assert hashlib.sha256(Path('/workspace/anas-phone-study-v55.zip').read_bytes()).hexdigest()=='6792c017112bfe37a3a0891635558bbf65369a181f74d191ec5d7751bf0e1522'
def length(r):return sum(math.dist(a,b) for a,b in zip(r['points'],r['points'][1:]))
rows=[]
for signal,net in [('KILL','BUTTON_KILL_BRANCH'),('INT','BUTTON_INT_N')]:
 oldrun=length(next(r for r in old['routes'] if r['name']==f'START55_{signal}_BOTTOM_AUTO'))
 newrun=sum(length(r) for r in new['routes'] if r['name'] in [f'START56_{signal}_LONG_AUTO',f'START56_{signal}_BRIDGE_AUTO'])
 assert newrun<oldrun
 assert all(length(r)<65 for r in new['routes'] if r['name'].startswith('START56_'))
 rows.append(dict(signal=signal,old_replaced_run_mm=oldrun,new_combined_run_mm=newrun,old_total_net_copper_mm=sum(length(r) for r in old['routes'] if r['net']==net),new_total_net_copper_mm=sum(length(r) for r in new['routes'] if r['net']==net)))
Path('output/startup-shortening-v56.json').write_text(json.dumps({'all_other_V55_routes_and_vias_unchanged':True,'new_vias':2,'comparison':rows,'65mm_segment_heuristic_restored':True,'electrical_qualified':False,'release':False},indent=2));print('PASS V55 rollback and unchanged-route checks; shorter combined runs',rows)
