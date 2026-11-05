import trimesh as tm,json
from pathlib import Path
s=tm.load('output/retainer-fix-v22/assembly.glb',force='scene');parts={n:m.copy() for n,m in s.geometry.items()}
for m in parts.values():m.apply_scale(1000)
rows=[]
for i in range(1,16):
 sw=parts[f'SW{i}_B3F'];cap=parts[f'keycap_{i}'];assert abs(sw.bounds[1,2]-8.1)<1e-5
 hits=[]
 for tolerance in [-.2,.2]:
  for travel in [0,-.45]:
   c=cap.copy();c.apply_translation([0,0,tolerance+travel]);h=tm.boolean.intersection([c,parts['front_shell']],engine='manifold')
   volume=abs(h.volume) if len(h.faces) else 0
   hits.append({'height_shift_mm':tolerance,'travel_mm':travel,'panel_overlap_mm3':volume})
 assert all(h['panel_overlap_mm3']<.001 for h in hits)
 rows.append({'switch':i,'existing_plunger_height_above_PCB_mm':float(sw.bounds[1,2]-.8),'reviewed_height_range_mm':[7.1,7.5],'candidate_body_width_max_mm':6.2,'cap_panel_cases':hits})
Path('output/keypad-height-v64.json').write_text(json.dumps({'release':False,'checks':rows,'panel_cases_passed':60,'scope':'Retained assembly already uses7.3mm nominal plunger,not4.3mm. Cap-height translations plus0/.45mm travel avoid nominal panel in60cases. Not full body tolerance/cap-socket/force/tilt validation.','remaining':['Exact plunger/keytop mating and seating-depth tolerances','Switch base/body maximum envelope and full component interference','Panel fabrication tolerance and off-axis operation','Overtravel stops and physical force/travel tests'],'assembly_changed':False},indent=2))
print('PASS15nominal7.3mm plungers;60translated cap/panel cases;physical mating not qualified')
