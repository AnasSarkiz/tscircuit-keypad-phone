import itertools,json
from pathlib import Path
# Manufacturer body L1.5..1.7, W.7...9, termination.1...4mm.
# Assumed placement error +/- .1mm X/Y. No paste/solder/mask/fab error included.
overlap=lambda a,b:max(0,min(a[1],b[1])-max(a[0],b[0]))
mins=[99,99,99];count=0
for length,width,term,dx,dy in itertools.product([1.5,1.7],[.7,.9],[.1,.4],[-.1,.1],[-.1,.1]):
 for side in [-1,1]:
  terminal=sorted([side*length/2+dx,side*(length/2-term)+dx]);pad=sorted([side*.85-.5,side*.85+.5])
  x=overlap(terminal,pad);y=overlap([dy-width/2,dy+width/2],[-.55,.55]);mins=[min(mins[0],x),min(mins[1],y),min(mins[2],x*y)];count+=1
assert mins[0]>=.1-1e-9 and mins[1]>=.7-1e-9
r={'corners_terminals':count,'minimum_overlap_x_y_area_mm_mm_mm2':mins,'pad_copper_gap_mm':.7,'scope':'Axis-aligned terminal overlap screen only; proposed pads1x1.1mm centered+/-0.85mm. Not supplier land recommendation, IPC assessment or solder-joint validation.','unqualified':['rotation error','copper etch/mask/paste tolerances','reflow and solder volume','courtyard and complete placement','package variant equivalence'],'fabrication_ready':False}
Path('output/resistor-tolerance-v13.json').write_text(json.dumps(r,indent=2));print(r)
