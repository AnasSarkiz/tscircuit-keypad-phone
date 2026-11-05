import json
from pathlib import Path
from shapely.geometry import LineString
c=json.load(open('routing/usb-layered-v56.json'));hits=[]
bridges=[r for r in c['routes'] if r['layer']=='inner1' and r['name'] in ['START56_KILL_BRIDGE_AUTO','START56_INT_BRIDGE_AUTO']]
for b in bridges:
 slot=LineString(b['points']).buffer(b['width']/2+.2)
 for r in c['routes']:
  if r['layer']=='inner1' or r['net'] in [b['net'],'GND']:continue
  cross=slot.intersection(LineString(r['points']).buffer(r['width']/2))
  if not cross.is_empty and cross.area>1e-8:hits.append({'slot':b['name'],'trace':r['name'],'net':r['net'],'layer':r['layer'],'projected_overlap_mm2':cross.area})
out={'projected_foreign_trace_overlaps':hits,'scope':'Planar overlap with new inner1 clearance slots; ignores actual stackup/field distribution. No overlap is not SI/EMI qualification; overlap needs return-path review.','release':False}
Path('output/return-path-projection-v56.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
