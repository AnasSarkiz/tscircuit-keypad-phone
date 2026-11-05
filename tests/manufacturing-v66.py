"""Nominal ordinary-via manufacturing screen, not factory capability approval."""
import json,itertools
from pathlib import Path
from shapely.geometry import box,Point,Polygon,mapping
j=json.load(open('output/usb-placement-v66.circuit.json'));c=json.load(open('routing/usb-layered-v66.json'));pads=[];opens=[];violations=[]
for p in [x for x in j if x['type']=='pcb_smtpad']:
 g=Polygon([(a['x'],a['y']) for a in p['points']]) if p['shape']=='polygon' else box(p['x']-p['width']/2,p['y']-p['height']/2,p['x']+p['width']/2,p['y']+p['height']/2)
 pads.append((p['pcb_smtpad_id'],g));opens.append((p['pcb_smtpad_id'],p['layer'],g.buffer(p.get('soldermask_margin',.025))))
pth=[p for p in j if p['type']=='pcb_plated_hole'];assert len(pth)==60
for p in pth:
 assert p['hole_diameter']==1 and p['outer_diameter']==2
 for ly in ['top','bottom']:opens.append(('KEYPAD_PTH_'+p['pcb_plated_hole_id'],ly,Point(p['x'],p['y']).buffer(1.05,quad_segs=32)))
intersections=[];minimum_pad_gap=100
for v in c['vias']:
 disk=Point(v['xy']).buffer(v['drill']/2,quad_segs=32);outer=Point(v['xy']).buffer(v['outer']/2,quad_segs=32)
 for name,g in pads:
  minimum_pad_gap=min(minimum_pad_gap,outer.distance(g))
  if disk.intersects(g):intersections.append([v['name'],name])
 for ly in ['top','bottom']:opens.append((v['name'],ly,Point(v['xy']).buffer(v['outer']/2+.025,quad_segs=32)))
# Include all60switch holes in drill/land checks,not just ordinary vias.
for v in c['vias']:
 for p in pth:
  if Point(v['xy']).buffer(v['drill']/2).intersects(Point(p['x'],p['y']).buffer(p['outer_diameter']/2)):
   intersections.append([v['name'],p['pcb_plated_hole_id']])
for p in pth:
 for name,g in pads:
  if Point(p['x'],p['y']).buffer(p['hole_diameter']/2).intersects(g):intersections.append([p['pcb_plated_hole_id'],name])
all_drills=c['vias']+[{'name':p['pcb_plated_hole_id'],'xy':[p['x'],p['y']],'drill':p['hole_diameter']} for p in pth]
min_drill=100
for a,b in itertools.combinations(all_drills,2):
 gap=Point(a['xy']).distance(Point(b['xy']))-(a['drill']+b['drill'])/2;min_drill=min(min_drill,gap)
 if gap<.25-1e-8:violations.append(['drill_spacing',a['name'],b['name'],gap])
min_web=100
for a,b in itertools.combinations(opens,2):
 if a[1]!=b[1]:continue
 gap=a[2].distance(b[2]);min_web=min(min_web,gap)
 if gap<.10-1e-8:violations.append(['mask_web',a[0],b[0],a[1],gap])
out={'switch_finished_holes_checked':len(pth),'all_drills_checked':len(all_drills),'drill_in_land_intersections':intersections,'minimum_via_annulus_to_smt_land_mm':minimum_pad_gap,'minimum_drill_edge_spacing_mm':min_drill,'minimum_nominal_mask_web_mm':min_web,'violations':violations,'proposed_rules':{'drill_edge_spacing_mm':.25,'mask_web_mm':.10,'unspecified_pad_mask_expansion_mm':.025,'untented_via_mask_expansion_mm':.025},'filled_capped_vias_assumed':False,'factory_rules_approved':False,'limitations':['Nominal dimensions only; registration/drill tolerances and assembler approval unresolved','Mask proposal not a fabrication export','Keypad footprint remains provisional'],'release':False}
Path('output/solder-mask-proposal-v66.json').write_text(json.dumps({'scope':'Nominal proposed openings, not Gerber or factory-approved mask','openings':[{'name':n,'layer':l,'geometry':mapping(g)} for n,l,g in opens],'release':False}))
Path('output/manufacturing-v66.json').write_text(json.dumps(out,indent=2));print({k:v for k,v in out.items() if k not in ['limitations','violations','proposed_rules']});print('violations',violations[:12]);assert not intersections;assert not violations
