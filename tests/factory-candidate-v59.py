import json,itertools
from pathlib import Path
from shapely.geometry import shape,mapping
r=json.load(open('sourcing/factory-candidate-v45.json'));c=json.load(open('routing/usb-layered-v59.json'));main=json.load(open('output/solder-mask-proposal-v59.json'))
# Existing openings include0.025mm default or explicit0.05mm. Expand non-keypad openings by0.005mm; explicit0.05 becomes0.055, conservative but must be reviewed.
opens=[dict(o,geometry=mapping(shape(o['geometry']).buffer(0 if o['name']=='KEYPAD_RESERVED' else .005))) for o in main['openings']]
minimum=100
for a,b in itertools.combinations(opens,2):
 if a['layer']==b['layer']:minimum=min(minimum,shape(a['geometry']).distance(shape(b['geometry'])))
ring=min((v['outer']-v['drill'])/2 for v in c['vias']);width=min(t['width'] for t in c['routes']);g=json.load(open('output/usb-layered-v59-checks.json'));f=json.load(open('output/factory-screen-v59.json'))
assert ring>r['M7_outer_annulus_strictly_greater_mm'];assert width>.125;assert g['minimum_foreign_copper_gap_mm']>.125;assert f['minimum_via_hole_to_foreign_trace_or_plane_mm']>.25;assert minimum>.075
assert 1.6/.2<12.5
j=json.load(open('output/usb-placement-v59.circuit.json'));ids={x[x['type']+'_id']:x for x in j if x['type']+'_id' in x}
cc=[p for p in j if p['type']=='pcb_smtpad' and ids[ids[p['pcb_component_id']]['source_component_id']]['name']=='U_CC_PROTECT' and p['port_hints'][0]!='pin21']
assert len(cc)==20 and all(min(p['width'],p['height'])>=r['minimum_SMD_width_mm'] for p in cc)
side=[p for p in cc if p['port_hints'][0] in ['pin1','pin2','pin3','pin4','pin5']]
ys=sorted(p['y'] for p in side);assert all(abs(b-a-.4)<1e-8 for a,b in zip(ys,ys[1:]))
out={'candidate':r['candidate'],'nominal_annulus_mm':ring,'minimum_route_width_mm':width,'minimum_foreign_gap_mm':g['minimum_foreign_copper_gap_mm'],'minimum_hole_to_foreign_trace_plane_mm':f['minimum_via_hole_to_foreign_trace_or_plane_mm'],'minimum_candidate_mask_web_mm':minimum,'CC_pad_width_mm':.2,'CC_pitch_mm':.4,'nominal_screens_pass':True,'supplier_approved':False,'scope':'Candidate subset only; solder-mask-defined components, pad-hole convention, unplaced circuits and actual factory CAM remain gates','release':False}
Path('output/factory-candidate-v59.json').write_text(json.dumps(out,indent=2));Path('output/factory-candidate-mask-v59.json').write_text(json.dumps({'openings':opens,'release':False,'supplier_approved':False}));print(out)
