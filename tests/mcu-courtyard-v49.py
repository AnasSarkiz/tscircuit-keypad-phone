"""Manufacturer courtyard with stroke envelope, independently enforced against placed bottom bodies."""
import json,copy
from pathlib import Path
from shapely.geometry import box
j=json.load(open('output/usb-placement-v49/fit-check.json'))
# Source F.CrtYd x+/-9.8, y=-16.05..10.55, stroke0.12.
# Same bottom-body transform as the footprint test, retaining line stroke.
q=box(-22.86,18.39,-3.14,45.11)
def check(entries):
 checked=0
 for e in entries:
  if e['reference']=='U_MCU' or e['side']!='bottom':continue
  x,y,z=e['center_mm'];w,h,_=e['body_mm'];assert not q.intersects(box(x-w/2,y-h/2,x+w/2,y+h/2)),e['reference'];checked+=1
 return checked
n=check(j['entries']);bad=copy.deepcopy(j['entries']);e=next(e for e in bad if e['side']=='bottom' and e['reference']!='U_MCU');e['center_mm']=[-13,32,-1]
try:check(bad)
except AssertionError:pass
else:raise AssertionError('Courtyard intrusion accepted')
Path('output/mcu-courtyard-v49.json').write_text(json.dumps({'checked_bottom_bodies':n,'courtyard_envelope_mm':list(q.bounds),'intrusion_negative_test_rejected':True,'scope':'Manufacturer courtyard versus current provisional package bodies only; not full population, mating or tolerance validation','release':False},indent=2))
print('PASS manufacturer MCU courtyard against',n,'bottom bodies; deliberate intrusion rejected')
