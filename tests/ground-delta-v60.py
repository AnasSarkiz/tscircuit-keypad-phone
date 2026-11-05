import json
from pathlib import Path
from shapely.geometry import shape,Point
from shapely.ops import unary_union
p=Path('output');a=json.loads((p/'usb-layered-v57-geometry.json').read_text());b=json.loads((p/'usb-layered-v60-geometry.json').read_text());old=shape(next(x for x in a if x['kind']=='plane')['geometry']);new=shape(next(x for x in b if x['kind']=='plane')['geometry']);c=json.load(open('routing/usb-layered-v60.json'))
vs=[v for v in c['vias'] if v['name'].startswith('TEMP60') and v['net']!='GND'];assert len(vs)==11
holes=unary_union([Point(v['xy']).buffer(v['outer']/2,quad_segs=32).buffer(.2,quad_segs=16) for v in vs]);expected=old.difference(holes)
discarded=0.0
if expected.geom_type=='MultiPolygon':
 largest=max(expected.geoms,key=lambda q:q.area);discarded=expected.area-largest.area;expected=largest
assert new.symmetric_difference(expected).area<1e-8
assert abs(discarded-(json.load(open('output/usb-layered-v60-checks.json'))['discarded_floating_plane_area_mm2']-json.load(open('output/usb-layered-v57-checks.json'))['discarded_floating_plane_area_mm2']))<1e-8
out={'new_signal_via_antipads':len(vs),'new_ground_vias':4,'removed_plane_area_mm2':old.area-new.area,'unexpected_plane_change_mm2':new.symmetric_difference(expected).area,'new_signal_slots':0,'new_discarded_unconnected_island_area_mm2':discarded,'release':False};(p/'ground-delta-v60.json').write_text(json.dumps(out,indent=2));print(out)
