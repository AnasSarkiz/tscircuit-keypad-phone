import json,csv
from pathlib import Path
j=json.loads(Path('output/usb-integrated.circuit.json').read_text());placed=json.loads(Path('output/usb-placement-v44.circuit.json').read_text());copper=json.loads(Path('output/usb-layered-v44-checks.json').read_text());byid={x[k]:x for x in j for k in [x['type']+'_id'] if k in x};nodes={};nets={}
for p in [x for x in j if x['type']=='source_port']:
 nn={n for t in j if t['type']=='source_trace' and p['source_port_id'] in t.get('connected_source_port_ids',[]) for n in t.get('connected_source_net_ids',[])}
 if not nn:continue
 assert len(nn)==1
 name=byid[p['source_component_id']]['name']+'.pin'+str(p['pin_number']);nodes[name]=name;nets.setdefault(byid[next(iter(nn))]['name'],[]).append(name)
def find(a):
 while nodes[a]!=a:a=nodes[a]
 return a
for net,groups in copper['placed_net_islands'].items():
 if net not in nets:continue
 for names in groups:
  names=[n for n in names if n in nodes]
  assert all(n in nets[net] for n in names)
  for n in names[1:]:nodes[find(n)]=find(names[0])
rows=[]
for net,pp in nets.items():
 groups={}
 for n in pp:groups.setdefault(find(n),[]).append(n)
 rows.append({'net':net,'terminal_count':len(pp),'copper_islands':list(groups.values()),'remaining_minimum_joins':len(groups)-1,'complete_within_USB_netlist':len(groups)==1})
allrefs={x['name'] for x in j if x['type']=='source_component'};pref_all={x['name'] for x in placed if x['type']=='source_component'};pref=pref_all&allrefs;inventory=[x for x in json.load(open('output/power-integrated.circuit.json')) if x['type']=='source_component']
need=sum(max(0,r['terminal_count']-1) for r in rows);left=sum(r['remaining_minimum_joins'] for r in rows)
out={'scope':'USB integrated logical netlist; excludes connector and external phone loads. Connectivity extracted from layered copper intersections and explicit via bridges; not hardware certification. Whole-phone denominator is current integrated candidate, not complete final BOM.','USB_components_total':len(allrefs),'components_placed':len(pref),'components_unplaced':sorted(allrefs-pref),'connected_USB_terminals_total':len(nodes),'terminals_in_multi_pad_copper_islands':sum(len(g) for r in rows for g in r['copper_islands'] if len(g)>1),'minimum_joins_required':need,'minimum_joins_completed':need-left,'minimum_joins_remaining':left,'multi_terminal_nets':sum(r['terminal_count']>1 for r in rows),'multi_terminal_nets_locally_complete':sum(r['terminal_count']>1 and r['complete_within_USB_netlist'] for r in rows),'whole_phone_current_candidate_components':len(inventory),'whole_phone_placed_in_this_candidate':len(pref_all),'nets':rows,'release':False}
Path('output/usb-coverage-v44.json').write_text(json.dumps(out,indent=2));print({k:v for k,v in out.items() if k not in ['nets','components_unplaced','scope']})
