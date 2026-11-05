"""Assumption-based geometric screen, NOT manufacturer/process qualification."""
import math,json
from pathlib import Path
# Maximum terminal rectangle .87 x 1.82, nominal centers +/-1.625.
# Assumed entire-package rotation +/-5deg and placement +/-0.1mm.
# Terminal positional tolerances/axis identification remain unverified.
points=[]
for sign in [-1,1]:
 for deg in range(-500,501):
  a=math.radians(deg/100)
  for dx in [-.435,.435]:
   for dy in [-.91,.91]:
    x=sign*1.625+dx;y=dy
    points.append((abs(x*math.cos(a)-y*math.sin(a)-sign*1.625)+.1,abs(x*math.sin(a)+y*math.cos(a))+.1))
x=max(p[0] for p in points);y=max(p[1] for p in points)
assert x<=1.3/2 and y<=2.5/2
assert y>2.3/2 # Initial proposal failed this assumed rotation screen.
lo=.47*.8;loaded=lo*.9
assert lo>=.37 and loaded<.37
out={'assumed_required_land_width_mm':2*x,'assumed_required_land_height_mm':2*y,'proposal_mm':[1.3,2.5],'initial_2_3mm_height_failed':True,'qualification':False,'TPS63802_inductor_screen':{'initial_min_uH':lo,'at_assumed_10_percent_drop_uH':loaded,'required_min_uH':.37,'max_remaining_drop_fraction':1-.37/lo,'qualified':False}}
Path('output/inductor-corners-v20.json').write_text(json.dumps(out,indent=2));print(out)
