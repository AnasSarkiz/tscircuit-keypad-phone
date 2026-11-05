"""Inventory gaps explicitly. This is not ERC or evidence that wiring is correct."""
import json,csv
from pathlib import Path
j=json.loads(Path('output/power-integrated.circuit.json').read_text());comps={x['source_component_id']:x for x in j if x['type']=='source_component'}
ports={x['source_port_id']:x for x in j if x['type']=='source_port'}
traces=[x for x in j if x['type']=='source_trace'];nets=[x for x in j if x['type']=='source_net']
rows=[]
for n in nets:
 ids={p for t in traces if n['source_net_id'] in t['connected_source_net_ids'] for p in t['connected_source_port_ids']}
 endpoints=sorted(comps[ports[p]['source_component_id']]['name']+'.'+str(ports[p].get('pin_number')) for p in ids)
 rows.append({'net':n['name'],'endpoints':endpoints,'review_required':any(v in n['name'] for v in ['PENDING','UNQUALIFIED']) or len(ids)<2})
missing=[{'reference':c['name'],'type':c.get('ftype'),'value':c.get('resistance',c.get('capacitance',c.get('inductance')))} for c in comps.values() if not c.get('manufacturer_part_number')]
r={'scope':'Source-net inventory only; endpoints may be passive or outputs, so endpoint count is not ERC. No routing/footprint validation.','components':len(comps),'nets':rows,'components_without_MPN':missing,'fabrication_ready':False}
Path('output/completeness-audit.json').write_text(json.dumps(r,indent=2))
with Path('sourcing/integrated-inventory-v12.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['reference','type','MPN','value','qualification'])
 for c in comps.values():w.writerow([c['name'],c.get('ftype',''),c.get('manufacturer_part_number','UNASSIGNED'),c.get('resistance',c.get('capacitance',c.get('inductance',''))),'candidate; no released footprint or complete electrical qualification'])
print(f"Audit: {len(comps)} components; {len(missing)} without assigned MPN; {sum(r['review_required'] for r in rows)} nets flagged for manual review (not errors automatically).")
