from pathlib import Path
import json,math
from shapely.geometry import shape,Point,box
old=json.loads(Path('output/usb-layered-v33-geometry.json').read_text());new=json.loads(Path('output/usb-layered-v39-geometry.json').read_text())
oldplane=shape(next(x['geometry'] for x in old if x['kind']=='plane'));newplane=shape(next(x['geometry'] for x in new if x['kind']=='plane'));hits=[]
for row,y in enumerate([-21,-33,-45,-57,-69]):
 for col,x in enumerate([-14,0,14]):
  for k,(dx,dy) in enumerate([(-3.25,2.25),(3.25,2.25),(-3.25,-2.25),(3.25,-2.25)]):
   pad=Point(x+dx,y+dy).buffer(1/math.cos(math.pi/128),quad_segs=32)
   if oldplane.intersects(pad):hits.append(f'SW{row*3+col+1}/land{k}')
   assert newplane.distance(pad)>=.15-1e-8
assert len(hits)==10,hits
# V33 cap output pad overlaps the provisional SW14 lower-left copper clearance.
j=json.load(open('output/usb-placement-v33.circuit.json'));s=next(x for x in j if x['type']=='source_component' and x['name']=='C_USB_AUX_OUT');pc=next(x for x in j if x['type']=='pcb_component' and x['source_component_id']==s['source_component_id']);p=next(x for x in j if x['type']=='pcb_smtpad' and x['pcb_component_id']==pc['pcb_component_id'] and 'pin1' in x['port_hints']);pad=box(p['x']-p['width']/2,p['y']-p['height']/2,p['x']+p['width']/2,p['y']+p['height']/2);gap=pad.distance(Point(-3.25,-71.25).buffer(1,quad_segs=32));assert gap<.15
Path('output/keypad-copper-regression-v39.json').write_text(json.dumps({'prior_V33_plane_intersected_lands':hits,'prior_V33_cap_to_SW14_land_gap_mm':gap,'V39_all60_keypad_land_clearance_checked':True,'scope':'Existing provisional B3F footprint, not newly manufacturer-qualified; prior partial USB checks omitted it'},indent=2));print('PASS V33 detects10 plane/keypad overlaps and cap conflict; V39 keeps clear')
