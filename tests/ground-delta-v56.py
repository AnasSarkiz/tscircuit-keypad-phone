import json
from pathlib import Path
from shapely.geometry import shape,Point
from shapely.ops import unary_union
old=shape(next(x['geometry'] for x in json.load(open('output/usb-layered-v55-geometry.json')) if x['name']=='LOCAL_GROUND_POUR'))
new=shape(next(x['geometry'] for x in json.load(open('output/usb-layered-v56-geometry.json')) if x['name']=='LOCAL_GROUND_POUR'))
c=json.load(open('routing/usb-layered-v56.json'));vias=[v for v in c['vias'] if v['name'] in ['START56_KILL_BRIDGE','START56_INT_BRIDGE']];assert len(vias)==2
holes=unary_union([Point(v['xy']).buffer(v['outer']/2,quad_segs=32).buffer(.2,quad_segs=16) for v in vias])
assert new.difference(old).area<1e-8
assert old.difference(new).symmetric_difference(old.intersection(holes)).area<1e-8
assert not any(r['layer']=='inner1' and r['name'].startswith('START56') for r in c['routes'])
Path('output/ground-delta-v56.json').write_text(json.dumps({'only_two_added_via_antipads_change_GND':True,'removed_ground_area_mm2':old.difference(new).area,'new_signal_slots':0,'plane_connectivity_screen':'see usb-layered-v56-checks.json','not_SI_EMI_validation':True,'release':False},indent=2));print('PASS ground difference exactly two new via antipads',old.difference(new).area)
