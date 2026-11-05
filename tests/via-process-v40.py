"""Find drill holes intersecting solder lands, distinct from copper-short clearance."""
import json
from pathlib import Path
from shapely.geometry import Point,box,Polygon
j=json.load(open('output/usb-placement-v40.circuit.json'));ids={x[k]:x for x in j for k in [x['type']+'_id'] if k in x};out=[]
for v in json.load(open('routing/usb-layered-v40.json'))['vias']:
 for p in [x for x in j if x['type']=='pcb_smtpad']:
  geom=Polygon([(a['x'],a['y']) for a in p['points']]) if p['shape']=='polygon' else box(p['x']-p['width']/2,p['y']-p['height']/2,p['x']+p['width']/2,p['y']+p['height']/2)
  if geom.intersects(Point(v['xy']).buffer(v['drill']/2)):
   ref=ids[ids[p['pcb_component_id']]['source_component_id']]['name'];out.append({'via':v['name'],'reference':ref,'pin':p['port_hints'][0],'xy':v['xy'],'drill_mm':v['drill'],'process_qualified':False})
assert len(out)>0,'Review process assumptions if layout no longer contains these holes'
Path('output/via-in-pad-v40.json').write_text(json.dumps({'count':len(out),'entries':out,'gate':'No unfilled solder-land holes approved. Filled/capped process, stencil, yield and cost require assembler review; reroute if rejected.','release':False},indent=2))
print('PROCESS GATE:',len(out),'drill/solder-land intersections; geometry is not fabrication acceptance')
