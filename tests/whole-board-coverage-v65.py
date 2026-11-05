"""Connectivity of the current integrated candidate, including explicit open endpoints."""
import json,csv
from pathlib import Path
root=Path.cwd();j=json.load(open('output/power-integrated-v45.circuit.json'));placed=json.load(open('output/usb-placement-v65.circuit.json'));copper=json.load(open('output/usb-layered-v65-checks.json'))
comps={x['source_component_id']:x for x in j if x['type']=='source_component'};ports={x['source_port_id']:x for x in j if x['type']=='source_port'};nets={x['source_net_id']:x['name'] for x in j if x['type']=='source_net'};nodes={n:set() for n in nets.values()};used=set()
for t in j:
 if t['type']=='source_trace':
  for p in t['connected_source_port_ids']:
   used.add(p);v=ports[p];label=comps[v['source_component_id']]['name']+'.pin'+str(v['pin_number'])
   for n in t['connected_source_net_ids']:nodes[nets[n]].add(label)
rows=[];need=done=0
for net,terminals in sorted(nodes.items()):
 if not terminals:continue
 groups=[set(g)&terminals for g in copper['placed_net_islands'].get(net,[])];groups=[g for g in groups if g];joined=set().union(*groups) if groups else set();groups += [{p} for p in terminals-joined]
 assert set().union(*groups)==terminals
 required=max(0,len(terminals)-1);completed=len(terminals)-len(groups);need+=required;done+=completed
 rows.append({'net':net,'terminal_count':len(terminals),'minimum_joins_required':required,'minimum_joins_completed':completed,'minimum_joins_open':required-completed,'copper_islands':[sorted(g) for g in groups],'complete_among_declared_terminals':required==completed,'external_single_terminal':len(terminals)==1})
pref={x['name'] for x in placed if x['type']=='source_component'};refs={c['name'] for c in comps.values()};assert pref<=refs
unconnected=[{'reference':comps[v['source_component_id']]['name'],'pin':v.get('pin_number'),'port_name':v.get('name'),'source_port_id':p,'labels':v.get('port_hints',[])} for p,v in ports.items() if p not in used]
out={'scope':'Current PowerIntegrated candidate only; includes unpopulated RF reserves and deliberately open design gates, excludes alternative circuits. Not a complete final phone netlist or hardware certification.','candidate_components':len(comps),'electronic_candidate_components':len(comps)-6,'electronic_candidate_placed':len(pref)-6,'copper_only_test_features':6,'components_placed':len(pref),'components_unplaced':sorted(refs-pref),'declared_connected_terminals':sum(len(v) for v in nodes.values()),'minimum_joins_required':need,'minimum_joins_completed':done,'minimum_joins_open':need-done,'multi_terminal_nets':sum(r['terminal_count']>1 for r in rows),'complete_multi_terminal_nets':sum(r['terminal_count']>1 and r['complete_among_declared_terminals'] for r in rows),'unconnected_declared_ports':unconnected,'nets':rows,'release':False}
Path('output/whole-board-coverage-v65.json').write_text(json.dumps(out,indent=2))
with open('sourcing/whole-board-placement-v65.csv','w') as f:
 w=csv.writer(f);w.writerow(['reference','MPN','placement'])
 for c in sorted(comps.values(),key=lambda c:c['name']):w.writerow([c['name'],c.get('manufacturer_part_number',''),'placed candidate' if c['name'] in pref else 'unplaced'])
with open('output/whole-board-open-connections-v65.csv','w') as f:
 w=csv.writer(f);w.writerow(['net','minimum_connections_open','copper_islands'])
 for r in rows:
  if r['minimum_joins_open']:w.writerow([r['net'],r['minimum_joins_open'],json.dumps(r['copper_islands'])])
print({k:v for k,v in out.items() if isinstance(v,int)})
