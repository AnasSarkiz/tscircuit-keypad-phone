"""Nominal ordinary-via manufacturing screen, not factory capability approval."""
import json,itertools
from pathlib import Path
from shapely.geometry import box,Point,Polygon,mapping
j=json.load(open('output/usb-placement-v50.circuit.json'));c=json.load(open('routing/usb-layered-v50.json'));pads=[];opens=[];violations=[]
for p in [x for x in j if x['type']=='pcb_smtpad']:
 g=Polygon([(a['x'],a['y']) for a in p['points']]) if p['shape']=='polygon' else box(p['x']-p['width']/2,p['y']-p['height']/2,p['x']+p['width']/2,p['y']+p['height']/2)
 pads.append((p['pcb_smtpad_id'],g));opens.append((p['pcb_smtpad_id'],p['layer'],g.buffer(p.get('soldermask_margin',.025))))
for y in [-21,-33,-45,-57,-69]:
 for x in [-14,0,14]:
  for dx,dy in [(-3.25,2.25),(3.25,2.25),(-3.25,-2.25),(3.25,-2.25)]:
   for ly in ['top','bottom']:opens.append(('KEYPAD_RESERVED',ly,Point(x+dx,y+dy).buffer(1.05,quad_segs=32)))
intersections=[];minimum_pad_gap=100
for v in c['vias']:
 disk=Point(v['xy']).buffer(v['drill']/2,quad_segs=32);outer=Point(v['xy']).buffer(v['outer']/2,quad_segs=32)
 for name,g in pads:
  minimum_pad_gap=min(minimum_pad_gap,outer.distance(g))
  if disk.intersects(g):intersections.append([v['name'],name])
 for ly in ['top','bottom']:opens.append((v['name'],ly,Point(v['xy']).buffer(v['outer']/2+.025,quad_segs=32)))
min_drill=100
for a,b in itertools.combinations(c['vias'],2):
 gap=Point(a['xy']).distance(Point(b['xy']))-(a['drill']+b['drill'])/2;min_drill=min(min_drill,gap)
 if gap<.25-1e-8:violations.append(['drill_spacing',a['name'],b['name'],gap])
min_web=100
for a,b in itertools.combinations(opens,2):
 if a[1]!=b[1]:continue
 gap=a[2].distance(b[2]);min_web=min(min_web,gap)
 if gap<.10-1e-8:violations.append(['mask_web',a[0],b[0],a[1],gap])
out={'drill_in_land_intersections':intersections,'minimum_via_annulus_to_smt_land_mm':minimum_pad_gap,'minimum_drill_edge_spacing_mm':min_drill,'minimum_nominal_mask_web_mm':min_web,'violations':violations,'proposed_rules':{'drill_edge_spacing_mm':.25,'mask_web_mm':.10,'unspecified_pad_mask_expansion_mm':.025,'untented_via_mask_expansion_mm':.025},'filled_capped_vias_assumed':False,'factory_rules_approved':False,'limitations':['Nominal dimensions only; registration/drill tolerances and assembler approval unresolved','Mask proposal not a fabrication export','Keypad footprint remains provisional'],'release':False}
Path('output/solder-mask-proposal-v50.json').write_text(json.dumps({'scope':'Nominal proposed openings, not Gerber or factory-approved mask','openings':[{'name':n,'layer':l,'geometry':mapping(g)} for n,l,g in opens],'release':False}))
Path('output/manufacturing-v50.json').write_text(json.dumps(out,indent=2));print({k:v for k,v in out.items() if k not in ['limitations','violations','proposed_rules']});print('violations',violations[:12]);assert not intersections;assert not violations
