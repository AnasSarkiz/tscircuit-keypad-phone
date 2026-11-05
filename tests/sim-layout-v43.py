"""GCT parent-reviewed component-side layout, converted to bottom-side CAD coordinates."""
import json,copy
from shapely.geometry import box,shape,Point,Polygon
j=json.load(open('output/usb-placement-v43.circuit.json'));c=next(x for x in j if x['type']=='source_component' and x['name']=='J_SIM_CANDIDATE');p=next(x for x in j if x['type']=='pcb_component' and x['source_component_id']==c['source_component_id'])
assert p['layer']=='bottom'
pads={int(x['port_hints'][0][3:]):x for x in j if x['type']=='pcb_smtpad' and x['pcb_component_id']==p['pcb_component_id']}
expected={1:(9.46,41.1),2:(12,41.1),3:(14.54,41.1),5:(9.46,52.9),6:(12,52.9),7:(14.54,52.9),8:(17.3,47),9:(6.7,47)}
def validate(q):
 for n,(x,y) in expected.items():
  assert abs(q[n]['x']-x)<1e-8 and abs(q[n]['y']-y)<1e-8
  assert q[n]['width']==1 and q[n]['height']==(3 if n>=8 else 1.1)
validate(pads)
for wrong in ['unmirrored','gap_as_pitch','swap_RST_CLK']:
 q=copy.deepcopy(pads)
 if wrong=='unmirrored':
  for a in q.values():a['x']=24-a['x']
 elif wrong=='gap_as_pitch':
  for n in [1,2,3,5,6,7]:q[n]['y']=47+(q[n]['y']-47)*10.7/11.8
 else:q[2],q[3]=q[3],q[2]
 try:validate(q)
 except AssertionError:pass
 else:raise AssertionError('bad '+wrong+' accepted')
assert not any(x['type']=='pcb_hole' and x.get('pcb_component_id')==p['pcb_component_id'] for x in j)
keepouts=[box(12-3.575,47-2.70,12+3.575,47+2.15)]
for x in [9.46,12,14.54]:
 for y in [51.2,43.55]:keepouts.append(box(x-.6,y-.5,x+.6,y+.5))
# Conservatively apply projected keepouts to every copper layer, including planes and vias.
geom=json.load(open('output/usb-layered-v43-geometry.json'));tested=0
for item in geom:
 g=shape(item['geometry'])
 for k in keepouts:assert g.intersection(k).area<1e-9,(item['name'],'socket keepout')
 tested+=1
for pad in [x for x in j if x['type']=='pcb_smtpad']:
 if pad['shape']=='polygon':
  g=Polygon([(v['x'],v['y']) for v in pad['points']])
 else:g=box(pad['x']-pad['width']/2,pad['y']-pad['height']/2,pad['x']+pad['width']/2,pad['y']+pad['height']/2)
 for k in keepouts:assert g.intersection(k).area<1e-9,(pad['pcb_smtpad_id'],'socket keepout')
assert len(keepouts)==7
open('output/sim-layout-v43-checks.json','w').write(json.dumps({'copper_items_checked':tested,'keepouts':7,'pad_count':8,'signal_row_center_pitch_mm':11.8,'peg_holes':0,'negative_cases_rejected':3,'source':'parent independent GCT SIM8051-6-0-14-00-A drawing review','insertion_direction':'interpretation only; physical sample/manufacturer confirmation required','mask_paste_courtyard':'unqualified','release':False},indent=2))
print('PASS SIM mirrored pad map,11.8mm pitch,no peg holes,seven projected keepouts and three incorrect layouts rejected')
