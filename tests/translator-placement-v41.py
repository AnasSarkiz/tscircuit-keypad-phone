import json
from pathlib import Path
from shapely.geometry import box,Point
j=json.load(open('output/usb-placement-v41.circuit.json'));ids={x[k]:x for x in j for k in [x['type']+'_id'] if k in x}
for i,ch in enumerate(['TX','RX','RTS','CTS','STATUS']):
 y=[-12,-18,-27,-39,-51][i];u=next(x for x in j if x['type']=='source_component' and x['name']=='U_'+ch);pc=next(x for x in j if x['type']=='pcb_component' and x['source_component_id']==u['source_component_id']);assert pc['layer']=='bottom'
 pads=[x for x in j if x['type']=='pcb_smtpad' and x['pcb_component_id']==pc['pcb_component_id']];assert len(pads)==6
 for n,dx,dy in [(1,1.3,.95),(2,1.3,0),(3,1.3,-.95),(4,-1.3,-.95),(5,-1.3,0),(6,-1.3,.95)]:
  p=next(p for p in pads if p['port_hints']==['pin'+str(n)]);assert p['layer']=='bottom';assert abs(p['x']-(-14+dx))<1e-8 and abs(p['y']-(y+dy))<1e-8
# Conservative switch-lead extrusion: keep bottom bodies clear of the entire2mm PTH land projection.
fit=json.load(open('output/usb-placement-v41/fit-check.json'))
for e in fit['entries']:
 if e['side']!='bottom' or e['reference']=='U_MODEM_LOGICAL_ONLY':continue
 x,y,z=e['center_mm'];a,b,h=e['body_mm'];shape=box(x-a/2,y-b/2,x+a/2,y+b/2)
 for sy in [-21,-33,-45,-57,-69]:
  for sx in [-14,0,14]:
   for dx,dy in [(-3.25,2.25),(3.25,2.25),(-3.25,-2.25),(3.25,-2.25)]:assert shape.distance(Point(sx+dx,sy+dy))>=1.2-1e-8,(e['reference'],sx+dx,sy+dy)
modem=box(-.5,-8.5,24.5,20.5)
for e in fit['entries']:
 if e['side']!='bottom' or e['reference']=='U_MODEM_LOGICAL_ONLY':continue
 x,y,z=e['center_mm'];a,b,h=e['body_mm'];assert box(x-a/2,y-b/2,x+a/2,y+b/2).distance(modem)>=3-1e-8,(e['reference'],'modem clearance')
checks=json.load(open('output/usb-layered-v41-checks.json'))
for n in ['VLOGIC_3V15','MODEM_VDD_EXT_1V8']:assert len(checks['placed_net_islands'][n])==1,n
print('PASS bottom-mirrored pin geometry, conservative keypad-lead body clearance and two isolated translator supply buses; external endpoints remain open')
