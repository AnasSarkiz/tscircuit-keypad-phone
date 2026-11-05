"""Independent emitted-copper screen: circular pads and straight wire segments only."""
import json, math
from pathlib import Path
j=json.loads(Path('output/keypad-routing-v12.circuit.json').read_text())
alltype=lambda t:[x for x in j if x['type']==t]
parent={x['source_port_id']:x['source_port_id'] for x in alltype('source_port')}
def root(x):
 while parent[x]!=x:x=parent[x]
 return x
def union(a,b):parent[root(a)]=root(b)
for c in alltype('source_component'):
 for group in c.get('internally_connected_source_port_ids',[]):
  for p in group[1:]:union(group[0],p)
net={}
for t in alltype('source_trace'):
 for p in t['connected_source_port_ids']:
  ns=t['connected_source_net_ids'];assert len(ns)==1
  k=root(p)
  assert k not in net or net[k]==ns[0]
  net[k]=ns[0]
ports={p['pcb_port_id']:p for p in alltype('pcb_port')}
portnet={k:net[root(p['source_port_id'])] for k,p in ports.items()}
segments=[]
for t in alltype('pcb_trace'):
 a,b=t['connectsTo'];assert portnet[a]==portnet[b]
 assert math.dist((ports[a]['x'],ports[a]['y']),(t['route'][0]['x'],t['route'][0]['y']))<1e-6
 assert math.dist((ports[b]['x'],ports[b]['y']),(t['route'][-1]['x'],t['route'][-1]['y']))<1e-6
 for p,q in zip(t['route'],t['route'][1:]):
  assert p['route_type']==q['route_type']=='wire' and p['layer']==q['layer']
  segments.append(((p['x'],p['y']),(q['x'],q['y']),max(p['width'],q['width'])/2,p['layer'],portnet[a]))
 union(ports[a]['source_port_id'],ports[b]['source_port_id'])
for n in set(portnet.values()):assert len({root(p['source_port_id']) for k,p in ports.items() if portnet[k]==n})==1,'disconnected net'
def pd(p,a,b):
 v=(b[0]-a[0],b[1]-a[1]);d=v[0]**2+v[1]**2
 t=max(0,min(1,((p[0]-a[0])*v[0]+(p[1]-a[1])*v[1])/d)) if d else 0
 return math.dist(p,(a[0]+t*v[0],a[1]+t*v[1]))
def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def sd(a,b,c,d):
 if cross(a,b,c)*cross(a,b,d)<0 and cross(c,d,a)*cross(c,d,b)<0:return 0
 return min(pd(a,c,d),pd(b,c,d),pd(c,a,b),pd(d,a,b))
minimum=999
for i,(a,b,r,layer,n) in enumerate(segments):
 for p in alltype('pcb_plated_hole'):
  if portnet[p['pcb_port_id']]!=n:
   gap=pd((p['x'],p['y']),a,b)-r-p['outer_diameter']/2
   minimum=min(minimum,gap)
 for c,d,s,other,m in segments[i+1:]:
  if layer==other and n!=m:minimum=min(minimum,sd(a,b,c,d)-r-s)
 for x,y in [a,b]:assert -28+r<=x<=28-r and -84+r<=y<=60-r
assert minimum>=.15-1e-6,minimum
report={'traces':len(alltype('pcb_trace')),'segments':len(segments),'nets_connected':len(set(portnet.values())),'minimum_different_net_trace_clearance_mm':minimum,'screen_clearance_mm':.15,'scope':'Endpoint and net graph plus straight-segment/round-pad clearance; excludes mask, drill tolerances, rear parts, RF and whole-phone constraints','fabrication_ready':False}
Path('output/keypad-independent-v12.json').write_text(json.dumps(report,indent=2));print(report)
