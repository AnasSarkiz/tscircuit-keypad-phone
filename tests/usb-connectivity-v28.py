import json
from pathlib import Path
j=json.loads(Path('output/usb-placement-v28.circuit.json').read_text());routes=json.loads(Path('routing/usb-local-v28.json').read_text());byid={x[k]:x for x in j for k in [x['type']+'_id'] if k in x};nodes={};netnodes={}
for p in [x for x in j if x['type']=='pcb_smtpad']:
 port=byid[p['pcb_port_id']]['source_port_id'];nets={n for t in j if t['type']=='source_trace' and port in t.get('connected_source_port_ids',[]) for n in t.get('connected_source_net_ids',[])}
 if not nets:continue
 net=byid[next(iter(nets))]['name'];comp=byid[byid[p['pcb_component_id']]['source_component_id']]['name'];name=comp+'.'+p['port_hints'][0];nodes[name]=name;netnodes.setdefault(net,[]).append(name)
def find(a):
 while nodes[a]!=a:a=nodes[a]
 return a
for r in routes:
 names=[a+'.pin'+str(b) for a,b in r['pads']]
 for n in names[1:]:nodes[find(n)]=find(names[0])
out=[]
for net,nn in netnodes.items():
 groups={}
 for n in nn:groups.setdefault(find(n),[]).append(n)
 out.append(dict(net=net,local_copper_islands=list(groups.values()),island_count=len(groups),external_interface_unqualified=True))
assert next(r for r in out if r['net']=='GND')['island_count']>1
assert next(r for r in out if r['net']=='USB_AUX3V3_PENDING')['island_count']==3
assert next(r for r in out if r['net']=='USB_POR_SENSE')['island_count']==1
Path('output/usb-connectivity-v28.json').write_text(json.dumps({'scope':'manifest contacts only; external components and all missing nets remain open','nets':out,'complete':False},indent=2));print('PASS open-net inventory retains disconnected ground/supply islands and pending external interfaces')
