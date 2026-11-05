import json,math
from pathlib import Path
c=json.load(open('routing/usb-layered-v44.json'));r=next(r for r in c['routes'] if r['name']=='MCU_VDD_AUTO');d=json.load(open('output/mcu-supply-route-v44.json'))
l=sum(math.dist(a,b) for a,b in zip(r['points'],r['points'][1:]));assert abs(l-d['length_mm'])<1e-8;assert r['width']==.5 and r['layer']=='bottom'
assert l<d['prior_0_25mm_inner_route_length_mm']
assert not d['release'] and d['excluded']
print('PASS shorter 0.5mm MCU feed; illustrative DC drop only, supply unqualified')
