"""Necessary DC bounds; not converter, cell, startup or transient qualification."""
import json,math
from pathlib import Path
rows=[]
for eta in [.8,.85,.9]:
 for backlight in [False,True]:
  power=7.6/eta+3.3*.6/.8+(5.3*.131/.75 if backlight else 0)
  # At 3.6A pack allocation, actual SYS must exceed both 3.2V and P/I.
  floor=max(3.2,power/3.6)
  for voc in [3.2,3.6,3.8,4.1]:
   r=(voc-floor)*floor/power
   feasible=r>=0
   if feasible:
    # Independent load-line solution at the limiting resistance.
    root=(voc+math.sqrt(voc*voc-4*r*power))/2
    assert abs(root-floor)<1e-10
    assert power/root<=3.6+1e-10 and root>=3.2-1e-10
    # A resistance above the bound must violate at least one limit.
    bad=r+.001;disc=voc*voc-4*bad*power
    if disc>=0:
     v=(voc+math.sqrt(disc))/2
     assert v<3.2 or power/v>3.6
   rows.append(dict(efficiency_assumed=eta,backlight=backlight,OCV_V=voc,required_SYS_min_V=floor,maximum_shared_resistance_ohm=r if feasible else None,conditional_DC_feasible=feasible))
assert any(not r['conditional_DC_feasible'] for r in rows)
Path('output/lte-envelope-v17.json').write_text(json.dumps({'cases':rows,'scope':'Necessary steady-state load-line bounds; shared resistance includes cell, protection, harness, charger BATFET and PCB. No transient allocation or efficiency guarantee. Not a battery approval.','qualified':False},indent=2))
print('PASS 24 load-line boundary and adverse-resistance checks; hardware remains unqualified')
