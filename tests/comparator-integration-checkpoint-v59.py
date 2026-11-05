"""Diagnostic for an incomplete candidate; detected conflicts are failures, not waivers."""
import json,hashlib
from pathlib import Path
from shapely.geometry import Point,LineString,box,Polygon
root=Path(__file__).resolve().parents[1]
j=json.loads((root/'output/usb-placement-v59.circuit.json').read_text());c=json.loads((root/'routing/usb-layered-v59.json').read_text());base=json.loads((root/'routing/usb-layered-v57.json').read_text());ids={x[x['type']+'_id']:x for x in j if x['type']+'_id'in x}
refs={'U_TEMP','C_TEMP'}|{'R_TEMP_'+s for s in ['COLD_TOP','COLD_BOTTOM','COLD_HYST','HOT_TOP','HOT_BOTTOM','HOT_INPUT','HOT_HYST']}
hits=[]
for p in j:
 if p['type']!='pcb_smtpad' or 'x'not in p:continue
 ref=ids[ids[p['pcb_component_id']]['source_component_id']]['name']
 if ref not in refs:continue
 port=ids[p['pcb_port_id']]['source_port_id'];ns={ids[n]['name'] for t in j if t['type']=='source_trace' and port in t.get('connected_source_port_ids',[]) for n in t.get('connected_source_net_ids',[])}
 g=box(p['x']-p['width']/2,p['y']-p['height']/2,p['x']+p['width']/2,p['y']+p['height']/2)
 for q in base['routes']+base['vias']:
  if q['net'] in ns or ('layer'in q and q['layer']!=p['layer']):continue
  h=LineString(q['points']).buffer(q['width']/2) if 'points'in q else Point(q['xy']).buffer(q['outer']/2)
  d=g.distance(h)
  if d<.15-1e-9:hits.append(dict(reference=ref,pin=p['port_hints'][0],obstacle=q['name'],net=q['net'],clearance_mm=d))
for key in ['routes','vias']:
 now={q['name']:q for q in c[key]}
 assert all(now[q['name']]==q for q in base[key]),'V57 baseline changed'
sha=hashlib.sha256(Path('/workspace/anas-phone-study-v58.zip').read_bytes()).hexdigest();assert sha=='f376d8412978b473e76661f9964ef68cebf6989b0ffe36151a361e8b2bbacf39'
new=[r for r in c['routes'] if r['name'].startswith('TEMP59')]
report=dict(status='REJECTED_LAYOUT_CANDIDATE',release=False,baseline='V58 accepted provisional study',baseline_sha256=sha,V57_routing_preserved=True,nominal_body_fit_pass=True,foreign_copper_conflicts=hits,planned_new_route_segments=len(new),segments_marked_routed=sum(bool(r.get('candidate_routed')) for r in new),routing_complete=False,coverage={'accepted_electronics':106,'total_electronics':210,'accepted_joins':276,'total_joins':522,'accepted_open_joins':246,'candidate_electronics':108,'candidate_join_coverage':'not validated'},supersedes_previous_v59_validation=True,valid_current_reports=['usb-placement-v59/fit-check.json','comparator-integration-checkpoint-v59.json'],next_action='Repartition around existing SIM/startup copper, or reroute those affected nets; then run full checks. Do not export fabrication from candidate.')
(root/'output/comparator-integration-checkpoint-v59.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:report[k] for k in ['status','V57_routing_preserved','nominal_body_fit_pass','planned_new_route_segments','segments_marked_routed','routing_complete']}));print('FAIL candidate foreign-copper clearance:',len(hits),'conflicts; full detail in checkpoint JSON')
