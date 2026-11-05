import json
from pathlib import Path
j=json.load(open('output/power-integrated.circuit.json'));comps={x['source_component_id']:x for x in j if x['type']=='source_component'};ports={x['source_port_id']:x for x in j if x['type']=='source_port'};nets={x['source_net_id']:x['name'] for x in j if x['type']=='source_net'};pn={}
for t in j:
 if t['type']=='source_trace':
  for p in t['connected_source_port_ids']:pn.setdefault(p,set()).update(nets[n] for n in t['connected_source_net_ids'])
res=[]
for cid,c in comps.items():
 if c.get('resistance') is not None:
  ns=set().union(*(pn.get(p,set()) for p,v in ports.items() if v['source_component_id']==cid))
  if 'LCD_RST_N' in ns:res.append({'reference':c['name'],'ohms':c['resistance'],'nets':sorted(ns)})
assert len(res)==1 and set(res[0]['nets'])=={'LCD_RST_N','GND'},res
assert not any(c['name']=='R_MCU_LCD_RST_N' for c in comps.values())
out={'previous_nominal_reset_voltage_V':3.15*100000/(10000+100000),'remaining_reset_resistors':res,'intended_default':'nominal low; input leakage and startup timing unqualified','whole_candidate_components':len(comps),'release':False}
Path('output/lcd-reset-default-v36.json').write_text(json.dumps(out,indent=2));print('PASS opposing reset pull-up removed; nominal default only, leakage/startup gate remains')
