import json
from pathlib import Path
from shapely.geometry import shape,Point
from shapely.ops import unary_union
p=Path('output');a=json.loads((p/'usb-layered-v57-geometry.json').read_text());b=json.loads((p/'usb-layered-v58-geometry.json').read_text());old=shape(next(x for x in a if x['kind']=='plane')['geometry']);new=shape(next(x for x in b if x['kind']=='plane')['geometry']);c=json.load(open('routing/usb-layered-v58.json'))
vs=[v for v in c['vias'] if v['name'].startswith('TEMP58') and v['net']!='GND'];assert len(vs)==4
holes=unary_union([Point(v['xy']).buffer(v['outer']/2,quad_segs=32).buffer(.2,quad_segs=16) for v in vs]);expected=old.difference(holes)
assert new.symmetric_difference(expected).area<1e-8
out={'new_signal_via_antipads':4,'new_ground_vias':2,'removed_plane_area_mm2':old.area-new.area,'unexpected_plane_change_mm2':new.symmetric_difference(expected).area,'new_signal_slots':0,'release':False};(p/'ground-delta-v58.json').write_text(json.dumps(out,indent=2));print(out)
