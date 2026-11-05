from pathlib import Path
import json
from shapely.geometry import shape,Polygon
import cairosvg
root=Path(__file__).resolve().parents[1];items=json.loads((root/'output/usb-layered-v58-geometry.json').read_text());j=json.loads((root/'output/usb-placement-v58.circuit.json').read_text());svg=['<svg xmlns="http://www.w3.org/2000/svg" width="2200" height="1000" viewBox="0 0 2200 1000"><rect width="2200" height="1000" fill="#101621"/>']
for k,layer in enumerate(['top','bottom','inner1','inner2']):
 svg.append(f'<text x="{30+k*550}" y="30" fill="white" font-family="sans-serif" font-size="18">{layer.upper()} — candidate, not released</text><g transform="translate({280+k*550},400) scale(6,-6)">')
 for x in sorted([x for x in items if x['layer']==layer],key=lambda a:0 if a['kind']=='plane' else 1):
  color='#235a86' if x['net']=='GND' else '#f2a33b';svg.append(shape(x['geometry']).svg(scale_factor=.01,fill_color=color,opacity=.9))
 if layer in ['top','bottom']:
  for p in [x for x in j if x['type']=='pcb_smtpad' and x['layer']==layer]:
   if p['shape']=='polygon':
    svg.append(Polygon([(q['x'],q['y']) for q in p['points']]).svg(scale_factor=.01,fill_color='#d7cb8e'));continue
   svg.append(f'<rect x="{p["x"]-p["width"]/2}" y="{p["y"]-p["height"]/2}" width="{p["width"]}" height="{p["height"]}" fill="#d7cb8e"/>')
 svg.append('<rect x="-28" y="-84" width="56" height="144" fill="none" stroke="#677488" stroke-width=".12"/>')
 for x,y,w,h in [(8.425,44.3,7.15,4.85)]+[(x-.6,y-.5,1.2,1) for x in [9.46,12,14.54] for y in [51.2,43.55]]:svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#b489ef" stroke-width=".12"/>')
 for y in [-21,-33,-45,-57,-69]:
  for x in [-14,0,14]:
   for dx,dy in [(-3.25,2.25),(3.25,2.25),(-3.25,-2.25),(3.25,-2.25)]:svg.append(f'<circle cx="{x+dx}" cy="{y+dy}" r="1" fill="none" stroke="#ff5577" stroke-width=".06"/>')
 svg.append('</g>')
svg.append('<text x="30" y="980" fill="white" font-family="sans-serif" font-size="14">Blue: GND · Orange: other routed nets · Gold: component pads · Pink: keypad lands · Purple: SIM keepouts; geometry only</text></svg>');text=''.join(svg);(root/'output/usb-layered-v58-preview.svg').write_text(text);cairosvg.svg2png(bytestring=text.encode(),write_to=str(root/'output/usb-layered-v58-preview.png'))
