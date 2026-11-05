from pathlib import Path
import json
from shapely.geometry import shape
import cairosvg
root=Path(__file__).resolve().parents[1];items=json.loads((root/'output/usb-layered-v34-geometry.json').read_text());j=json.loads((root/'output/usb-placement-v34.circuit.json').read_text());svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="390" viewBox="0 0 1100 390"><rect width="1100" height="390" fill="#101621"/>']
for k,layer in enumerate(['top','bottom']):
 svg.append(f'<text x="{30+k*550}" y="30" fill="white" font-family="sans-serif" font-size="18">{layer.upper()} — candidate, not released</text><g transform="translate({350+k*550},-650) scale(12,-12)">')
 for x in sorted([x for x in items if x['layer']==layer],key=lambda a:0 if a['kind']=='plane' else 1):
  color='#235a86' if x['net']=='GND' else '#f2a33b';svg.append(shape(x['geometry']).svg(scale_factor=.01,fill_color=color,opacity=.9))
 if layer=='top':
  for p in [x for x in j if x['type']=='pcb_smtpad']:svg.append(f'<rect x="{p["x"]-p["width"]/2}" y="{p["y"]-p["height"]/2}" width="{p["width"]}" height="{p["height"]}" fill="#d7cb8e"/>')
 for y in [-21,-33,-45,-57,-69]:
  for x in [-14,0,14]:
   for dx,dy in [(-3.25,2.25),(3.25,2.25),(-3.25,-2.25),(3.25,-2.25)]:svg.append(f'<circle cx="{x+dx}" cy="{y+dy}" r="1" fill="none" stroke="#ff5577" stroke-width=".06"/>')
 svg.append('</g>')
svg.append('<text x="30" y="375" fill="white" font-family="sans-serif" font-size="14">Blue: GND · Orange: other routed nets · Gold: top pads · Pink: provisional keypad lands; geometry only</text></svg>');text=''.join(svg);(root/'output/usb-layered-v34-preview.svg').write_text(text);cairosvg.svg2png(bytestring=text.encode(),write_to=str(root/'output/usb-layered-v34-preview.png'))
