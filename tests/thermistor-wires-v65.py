import json,math
from pathlib import Path
from shapely.geometry import LineString
curves=[]
for x,r in [(.55,5.),(-.55,6.1)]:
 pts=[(x,-40),(x,-44)]+[(x+r-r*math.cos(i*math.pi/64),-44-r*math.sin(i*math.pi/64)) for i in range(1,65)]+[(x+2*r,-44+(40-4-math.pi*r))]
 curves.append(LineString(pts));assert abs(curves[-1].length-40)<.003
margin=curves[0].distance(curves[1])-1;assert margin>.09
Path('output/thermistor-wire-clearance-v65.json').write_text(json.dumps({'nominal_surface_gap_mm':margin,'centerline_lengths_mm':[c.length for c in curves],'scope':'Planar chord approximation;nominal1mmOD only;not manufacturing tolerance,retention or thermal qualification','release':False},indent=2));print('PASS nominal wire spacing',margin)
