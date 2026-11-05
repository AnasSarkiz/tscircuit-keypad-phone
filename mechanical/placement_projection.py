"""Project existing envelopes onto board planes. No new package footprints or routing."""
from pathlib import Path
import trimesh as tm, json, html
root=Path(__file__).resolve().parents[1]
s=tm.load(root/'output/retained-battery/assembly.glb',force='scene')
selected=[]
for name,m in s.geometry.items():
 if any(k in name.lower() for k in ['modem','mcu','power','display_nhd','fpc','usb','sim','receiver','microphone','antenna','b3f','ntc']):
  b=m.bounds*1000
  selected.append({'name':name,'bounds_mm':b.tolist(),'side':'front' if b[:,2].mean()>0 else 'rear','status':'existing fit envelope, not verified land pattern'})
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="900" viewBox="0 0 1200 900"><rect width="1200" height="900" fill="#fafbfc"/><g font-family="sans-serif" fill="#172b4d"><text x="30" y="35" font-size="23">One-board placement constraints — unresolved fit study</text><text x="30" y="62" font-size="14">Both panels viewed from front; rear is NOT mirrored for manufacture. All rectangles are envelopes.</text>']
for side,cx in [('front',180),('rear',500)]:
 cy=390;scale=3.8
 def rect(bounds,fill,stroke,dash=''):
  (x0,y0),(x1,y1)=bounds
  return f'<rect x="{cx+x0*scale}" y="{cy-y1*scale}" width="{(x1-x0)*scale}" height="{(y1-y0)*scale}" fill="{fill}" fill-opacity=".25" stroke="{stroke}" stroke-dasharray="{dash}"/>'
 svg.append(f'<text x="{cx-65}" y="142" font-size="18">{side.upper()} — X right</text>')
 svg.append(rect([[-28,-84],[28,60]],'#aaddcc','#18705b'))
 for x in [-24,24]:
  for y in [-79,54]:svg.append(f'<circle cx="{cx+x*scale}" cy="{cy-y*scale}" r="4.37" fill="white" stroke="black"/>')
 for i,item in enumerate(selected,1):
  if item['side']!=side:continue
  b=item['bounds_mm'];svg.append(rect([[b[0][0],b[0][1]],[b[1][0],b[1][1]]],'#ffbb66','#a34f00','3 2'))
  svg.append(f'<text x="{cx+(b[0][0]+b[1][0])/2*scale}" y="{cy-(b[0][1]+b[1][1])/2*scale}" font-size="11">{i}</text>')
for i,item in enumerate(selected,1):svg.append(f'<text x="680" y="{105+i*20}" font-size="12">{i}. {html.escape(item["name"])}</text>')
svg+=['<text x="30" y="770" font-size="16">NOT a placement release: expanded power/control circuits are not fitted into the reserved block.</text>','<text x="30" y="795" font-size="14">Missing: exact land patterns, copper keepouts, cable bends, service access, tolerances, RF review and physical samples.</text>','<text x="30" y="820" font-size="14">Case: 66 × 174 × 27.5 mm; PCB: 56 × 144 × 1.6 mm. Antenna extends beyond board into case.</text>','</g></svg>']
(root/'output/placement-constraints-v10.svg').write_text(''.join(svg))
(root/'output/placement-constraints-v10.json').write_text(json.dumps(selected,indent=2))
print('Projected',len(selected),'existing envelopes; no footprints invented.')
