"""Independent conservative rectangle/segment checks, no router dependency.
Rounded lands treated as full rectangles; all routes top copper, width0.15mm.
"""
import json,math
from pathlib import Path
j=json.loads(Path('output/usb-placement-v29.circuit.json').read_text());routes=json.loads(Path('routing/usb-local-v29.json').read_text());pads=[x for x in j if x['type']=='pcb_smtpad'];width=.15;clearance=.15
byid={x[k]:x for x in j for k in [x['type']+'_id'] if k in x}
def netof(p):
 port=byid[p['pcb_port_id']]['source_port_id'];nets={n for t in j if t['type']=='source_trace' and port in t.get('connected_source_port_ids',[]) for n in t.get('connected_source_net_ids',[])}
 assert len(nets)<=1
 return next(iter(nets),None)
def pointseg(p,a,b):
 d=[b[i]-a[i] for i in range(2)];q=sum(x*x for x in d);t=max(0,min(1,sum((p[i]-a[i])*d[i] for i in range(2))/q)) if q else 0
 return math.hypot(*(p[i]-a[i]-t*d[i] for i in range(2)))
def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def segdist(a,b,c,d):
 if cross(a,b,c)*cross(a,b,d)<=0 and cross(c,d,a)*cross(c,d,b)<=0 and all(max(min(a[i],b[i]),min(c[i],d[i]))<=min(max(a[i],b[i]),max(c[i],d[i])) for i in range(2)):return 0
 return min(pointseg(a,c,d),pointseg(b,c,d),pointseg(c,a,b),pointseg(d,a,b))
def rectdist(a,b,p):
 x,y,w,h=p['x'],p['y'],p['width']/2,p['height']/2
 if any(x-w<=q[0]<=x+w and y-h<=q[1]<=y+h for q in [a,b]):return 0
 c=[(x-w,y-h),(x+w,y-h),(x+w,y+h),(x-w,y+h)]
 return min(segdist(a,b,c[i],c[(i+1)%4]) for i in range(4))
# Independent checker edge cases.
assert segdist((0,0),(2,2),(0,2),(2,0))==0
assert segdist((0,0),(1,0),(2,0),(3,0))==1
assert pointseg((1,1),(0,0),(2,0))==1
minimum=math.inf
for idx,r in enumerate(routes):
 net=next(x['source_net_id'] for x in j if x['type']=='source_net' and x['name']==r['net']);r['net_id']=net;ports=[]
 for ref,pin in r['pads']:
  s=next(x for x in j if x['type']=='source_component' and x['name']==ref);pc=next(x for x in j if x['type']=='pcb_component' and x['source_component_id']==s['source_component_id']);p=next(x for x in pads if x['pcb_component_id']==pc['pcb_component_id'] and f'pin{pin}' in x['port_hints'])
  assert netof(p)==net,(r['name'],ref,pin,'wrong net')
  assert min(pointseg((p['x'],p['y']),a,b) for a,b in zip(r['points'],r['points'][1:]))<1e-8,'endpoint not contacted'
  ports.append(byid[p['pcb_port_id']]['source_port_id'])
 for a,b in zip(r['points'],r['points'][1:]):
  assert all(-28+width/2<=q[0]<=28-width/2 and -84+width/2<=q[1]<=60-width/2 for q in [a,b]),'board edge'
  for p in pads:
   if netof(p)==net:continue
   gap=rectdist(a,b,p)-width/2;minimum=min(minimum,gap);assert gap>=clearance-1e-8,(r['name'],p['pcb_smtpad_id'],gap)
 for prev in routes[:idx]:
  if prev['net_id']==net:continue
  for a,b in zip(r['points'],r['points'][1:]):
   for c,d in zip(prev['points'],prev['points'][1:]):assert segdist(a,b,c,d)-width>=clearance-1e-8,'trace collision'
 sid=f'source_trace_manual_v29_{idx}';j.append(dict(type='source_trace',source_trace_id=sid,connected_source_port_ids=ports,connected_source_net_ids=[net]))
 j.append(dict(type='pcb_trace',pcb_trace_id=f'pcb_trace_manual_v29_{idx}',source_trace_id=sid,route=[dict(route_type='wire',x=p[0],y=p[1],width=width,layer='top') for p in r['points']]))
# Separate inter-component pad spacing check.
for i,a in enumerate(pads):
 for b in pads[i+1:]:
  if a['pcb_component_id']==b['pcb_component_id']:continue
  gap=math.hypot(max(abs(a['x']-b['x'])-(a['width']+b['width'])/2,0),max(abs(a['y']-b['y'])-(a['height']+b['height'])/2,0));assert gap>=.2-1e-8
out={'routes':len(routes),'minimum_trace_to_foreign_pad_gap_mm':minimum,'width_mm':width,'clearance_rule_mm':clearance,'all_top':True,'complete_connectivity':False,'not_checked':['whole-board copper','ground-plane impedance','SI/EMC','production tolerances','mask/stencil'],'release':False}
Path('output/usb-routed-v29.circuit.json').write_text(json.dumps(j,indent=2));Path('output/usb-routing-v29-checks.json').write_text(json.dumps(out,indent=2));print('PASS',out)
