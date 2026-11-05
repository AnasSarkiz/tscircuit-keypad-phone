"""Placement transform against the independently reviewed V1.0 copper transcription."""
import json,copy
j=json.load(open('output/usb-placement-v41.circuit.json'));data=json.load(open('sourcing/modem-pad-transcription-v19.json'));c=next(x for x in j if x['type']=='source_component' and x['name']=='U_MODEM_LOGICAL_ONLY');p=next(x for x in j if x['type']=='pcb_component' and x['source_component_id']==c['source_component_id']);assert p['layer']=='bottom'
pads={int(x['port_hints'][0][3:]):x for x in j if x['type']=='pcb_smtpad' and x['pcb_component_id']==p['pcb_component_id']};assert len(pads)==126
for d in data['pads']:
 a=pads[d['pin']];assert abs(a['x']-(12-d['x']))<1e-8 and abs(a['y']-(6-d['y_down']))<1e-8
 assert a['width']==d['width'] and a['height']==d['height']
# Independent anchors from the parent-reviewed Figure42 transcription, not a uniform LGA.
anchors={1:(21.175,15.7),15:(21.175,-.3),17:(21.175,-2.5),43:(2.825,9.1),44:(2.825,10.2),45:(2.825,11.3),46:(2.825,12.4),29:(7.05,-5.025)}
def anchor_check(q):
 for n,(x,y) in anchors.items():assert abs(q[n]['x']-x)<1e-8 and abs(q[n]['y']-y)<1e-8
anchor_check(pads)
for fault in ['unmirrored','swap_SIM_RST_DATA']:
 bad=copy.deepcopy(pads)
 if fault=='unmirrored':
  for a in bad.values():a['x']=24-a['x']
 else:bad[44],bad[45]=bad[45],bad[44]
 try:anchor_check(bad)
 except AssertionError:pass
 else:raise AssertionError('accepted '+fault)
checks=json.load(open('output/usb-layered-v41-checks.json'))
for n in ['MODEM_PWRKEY_OD','MODEM_RESET_OD','USIM1_RST_MODEM_PENDING','USIM1_CLK_MODEM_PENDING','USIM1_DATA_MODEM_PENDING','USIM1_VDD_PENDING','MODEM_VDD_EXT_1V8']:
 assert len(checks['placed_net_islands'][n])==1,n
config=json.load(open('routing/usb-layered-v41.json'));vias=config['vias']
assert not any(v['name']=='MOD_GND_67' for v in vias),'display support collision regression'
assert any(r['name']=='MOD_GND_67_LINK' for r in config['routes'])
print('PASS126-pad bottom transform, independent pin anchors, mirror/SIM swaps rejected, complete placed SIM/control/EXT nets and display-support via regression; module variant/process unqualified')
