import json,itertools,math
from pathlib import Path
parts=json.loads(Path('sourcing/capacitor-dimensions-v14.json').read_text())
lands={'0603':(.85,1,1.15),'0805':(1.05,1.2,1.65),'1210':(1.65,1.3,3)}
overlap=lambda a,b:max(0,min(a[1],b[1])-max(a[0],b[0]))
rows=[]
for mpn,d in parts.items():
 c,pw,ph=lands[d['case']];mins=[99,99,99];n=0
 for l,w,b,dx,dy,side in itertools.product(d['length'],d['width'],d['terminal'],[-.1,.1],[-.1,.1],[-1,1]):
  x=overlap(sorted([side*l/2+dx,side*(l/2-b)+dx]),[side*c-pw/2,side*c+pw/2]);y=overlap([dy-w/2,dy+w/2],[-ph/2,ph/2]);mins=[min(mins[0],x),min(mins[1],y),min(mins[2],x*y)];n+=1
 assert mins[0]>.1 and mins[1]>.6,(mpn,mins)
 rows.append({'MPN':mpn,'terminal_corner_cases':n,'minimum_overlap_x_y_area':mins,'copper_gap_mm':2*c-pw,'maximum_body_mm':[d[k][1] for k in ['length','width','height']]})
factor=.9*.85*(1-.03*math.log10(87600/48))
caprows=[{'nominal_uF':c,'before_DC_bias_uF':c*factor,'minimum_bias_retention_to_meet_1_5uF':1.5/(c*factor)} for c in [2.2,4.7]]
assert caprows[1]['minimum_bias_retention_to_meet_1_5uF']<.47
r={'land_results':rows,'scope':'Axis-aligned +/-0.1mm placement assumption only. Not solder validation. Bounds treated independently conservatively. Rotation, etch, paste, mask and reflow unqualified.','USB_aux_output':{'required_effective_uF':1.5,'maximum_ESR_ohm':.2,'assumed_age_hours':87600,'reference_hours':48,'tolerance_factor':.9,'temperature_factor':.85,'aging_per_decade':.03,'candidates':caprows,'selected_nominal_uF':4.7,'DC_bias_and_ESR_guarantee_available':False},'fabrication_ready':False}
Path('output/capacitor-screen-v14.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
