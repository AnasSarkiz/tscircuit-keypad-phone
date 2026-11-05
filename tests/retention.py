from pathlib import Path
import trimesh as tm,json
p=Path('output/retained-battery');s=tm.load(p/'assembly.glb',force='scene')
parts={n:m.copy() for n,m in s.geometry.items()}
for m in parts.values():m.apply_scale(1000)
frame=parts['battery_retainer'];hits=[];checks=0
for n,m in parts.items():
 if n=='battery_retainer' or 'reserved' in n or n.startswith(('bolt_','nut_','retainer_')):continue
 checks+=1
 hit=tm.boolean.intersection([frame,m],engine='manifold')
 if len(hit.faces) and abs(hit.volume)>.001:hits.append([n,float(hit.volume)])
report={'checks':checks,'collisions':hits,'exclusions':'fastener intentional interfaces and reserved volumes; separate battery check includes physical fasteners','scope':'nominal geometry only'}
(p/'retainer-checks.json').write_text(json.dumps(report,indent=2));print(report)
assert not hits,hits
