"""Independent bottom-mirror oracle from parent-reviewed AOS top/component-view drawing."""
import json,copy
j=json.load(open('output/usb-placement-v42.circuit.json'));comps={x['name']:x for x in j if x['type']=='source_component'}
for s,y in [('KEY',-18),('RESET',-30.3)]:
 c=comps['Q_MODEM_'+s];p=next(x for x in j if x['type']=='pcb_component' and x['source_component_id']==c['source_component_id']);assert p['layer']=='bottom'
 pads={int(x['port_hints'][0][3:]):x for x in j if x['type']=='pcb_smtpad' and x['pcb_component_id']==p['pcb_component_id']}
 # AOS top view Ydown G(-.95,+1.2), S(+.95,+1.2), D(0,-1.2).
 # CAD Yup and bottom mirroring yield this independent expected map.
 expected={1:(.95,y-1.2),2:(-.95,y-1.2),3:(0,y+1.2)}
 def check(q):
  for n,(x0,y0) in expected.items():
   assert abs(q[n]['x']-x0)<1e-8 and abs(q[n]['y']-y0)<1e-8
   assert q[n]['width']==.8 and q[n]['height']==.8
 check(pads)
 for mutation in ['unmirrored','swap_gate_source','swap_drain_gate']:
  bad=copy.deepcopy(pads)
  if mutation=='unmirrored':
   for v in bad.values():v['x']=-v['x']
  else:
   a,b=(1,2) if mutation=='swap_gate_source' else (1,3);bad[a],bad[b]=bad[b],bad[a]
  try:check(bad)
  except AssertionError:pass
  else:raise AssertionError(mutation+' not rejected')
 ports={x['pin_number']:x for x in j if x['type']=='source_port' and x['source_component_id']==c['source_component_id']}
 netnames={x['source_net_id']:x['name'] for x in j if x['type']=='source_net'}
 for pin,net in {1:'MODEM_'+s+'_GATE',2:'GND',3:('MODEM_PWRKEY_OD' if s=='KEY' else 'MODEM_RESET_OD')}.items():
  found={netnames[n] for t in j if t['type']=='source_trace' and ports[pin]['source_port_id'] in t.get('connected_source_port_ids',[]) for n in t.get('connected_source_net_ids',[])};assert found=={net}
print('PASS two AO3400A bottom mappings and G/S/D nets; six mirrored/swapped negative cases rejected; mask/paste and electrical behavior unqualified')
