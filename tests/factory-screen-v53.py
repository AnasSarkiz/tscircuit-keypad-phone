"""Read-only published JLCPCB rule screen; not a factory DFM submission/approval."""
import json
from pathlib import Path
from shapely.geometry import shape,Point
c=json.load(open('routing/usb-layered-v53.json'));geom=json.load(open('output/usb-layered-v53-geometry.json'));m=json.load(open('output/manufacturing-v53.json'));checks=json.load(open('output/usb-layered-v53-checks.json'))
viol=[];minimum=100
for v in c['vias']:
 for item in geom:
  if item['net']==v['net'] or item['kind'] not in ['trace','plane']:continue
  gap=Point(v['xy']).distance(shape(item['geometry']))-v['drill']/2
  minimum=min(minimum,gap)
  if gap<.2-1e-8:viol.append({'rule':'via_hole_to_foreign_copper_0.2','via':v['name'],'other':item['name'],'layer':item['layer'],'gap_mm':gap})
for key,value,limit in [('mask_web',m['minimum_nominal_mask_web_mm'],.1),('copper',checks['minimum_foreign_copper_gap_mm'],.15)]:
 if value<limit-1e-8:viol.append({'rule':key,'actual':value,'minimum':limit})
j=json.load(open('output/usb-placement-v53.circuit.json'));ids={x[x['type']+'_id']:x for x in j if x['type']+'_id' in x}
narrow=[]
for p in j:
 if p['type']=='pcb_smtpad' and p['shape']=='rect' and min(p['width'],p['height'])<.25-1e-8:
  ref=ids[ids[p['pcb_component_id']]['source_component_id']]['name'];narrow.append({'reference':ref,'pad':p['port_hints'][0],'width_mm':p['width'],'height_mm':p['height']})
out={'fine_pitch_pads_below_published_generic_0_25mm_width':narrow,'source':'https://jlcpcb.com/capabilities/pcb-capabilities','checked_date':'2026-11-05','candidate_process':'4-layer, 1 oz outer copper, green LPI, routed outline; exact stackup and assembly not selected','minimum_via_hole_to_foreign_trace_or_plane_mm':minimum,'minimum_nominal_mask_web_mm':m['minimum_nominal_mask_web_mm'],'minimum_foreign_copper_gap_mm':checks['minimum_foreign_copper_gap_mm'],'violations':viol,'factory_approval':False,'release':False,'unresolved':['Via ring now 0.15 mm nominal; final fabrication drill/registration review remains required.','No actual DFM upload, stackup, quote, stencil, assembly panel or registration approval.','Keypad PTH hole geometry and mating remain provisional.','Minimum pad widths and solder-mask-defined fine-pitch lands require part-specific process review.']}
Path('output/factory-screen-v53.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));assert not viol
