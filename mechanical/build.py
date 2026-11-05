"""Preliminary fit assembly. mm; right handed, X right, Y toward earpiece,
Z toward user. PCB mid-plane is Z=0. Purchased parts are envelope models.
STL uses mm; GLB uses metres. No mating/thermal/RF certification implied.
"""
from pathlib import Path
import json, itertools
import numpy as np
import trimesh as tm

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output'; OUT.mkdir(exist_ok=True)
parts={}
colors={'case':[47,61,74,255], 'pcb':[32,130,102,255], 'metal':[170,179,190,255], 'amber':[238,171,54,255], 'black':[30,34,40,255]}
def box(size, center):
    m=tm.creation.box(size); m.apply_translation(center); return m
def cyl(r,h,center,sections=32):
    m=tm.creation.cylinder(radius=r,height=h,sections=sections); m.apply_translation(center); return m
def union(ms): return tm.boolean.union(ms,engine='manifold')
def diff(a,bs): return tm.boolean.difference([a,*bs],engine='manifold')
def rounded(w,h,t,r,z):
    return union([box([w-2*r,h,t],[0,0,z]),box([w,h-2*r,t],[0,0,z]), *[cyl(r,t,[x,y,z]) for x in [-w/2+r,w/2-r] for y in [-h/2+r,h/2-r]]])
def add(name,m,color='metal',status='custom preliminary geometry'):
    m.visual.face_colors=colors.get(color,color) if isinstance(color,str) else color
    parts[name]={'mesh':m,'status':status}

holes=[(x,y) for x in [-24,24] for y in [-79,54]]
keys=[(c,r,x,y,label) for r,(y,labels) in enumerate(zip([-21,-33,-45,-57,-69],[['CALL','OK','END'],['1','2','3'],['4','5','6'],['7','8','9'],['*','0','#']])) for c,(x,label) in enumerate(zip([-14,0,14],labels))]
bores=[cyl(1.15,40,[x,y,0]) for x,y in holes]
# Two open shells; 2 mm walls. 2 mm rear floor; 2 mm front roof.
back=diff(rounded(62,174,13.5,5,-6.75),[rounded(58,170,16,3,-3.5)])
back=union([back,*[cyl(3,10.7,[x,y,-6.15]) for x,y in holes]])
back=diff(back,[*bores,*[cyl(2.4,1.8,[x,y,-12.7],6) for x,y in holes]])
front=diff(rounded(62,174,10.5,5,5.25),[rounded(58,170,12,3,2.5)])
front=union([front,*[cyl(3,7.7,[x,y,4.65]) for x,y in holes]])
# Generous prototype openings; window is aligned by eye to display active-area
# envelope only, not yet to the asymmetric manufacturer's active-area datum.
front=diff(front,[*bores,box([30,38,6],[0,24,10]),box([33.4,41.4,.9],[0,24,10.1]),box([13,3,6],[0,57,10]),cyl(1,6,[14,-79,10]),*[box([9.6,10.6,6],[x,y,10]) for c,r,x,y,l in keys]])
usb_open=box([11,8,5],[0,-86,2.8])
front=diff(front,[usb_open]); back=diff(back,[usb_open])
add('rear_shell',back,'case'); add('front_shell',front,'case')
board=diff(box([56,144,1.6],[0,-12,0]),bores)
add('pcb_envelope',board,'pcb','mechanical blank only; electrical board not released')
add('display_NHD_1_8',box([34.7,46.75,2.7],[0,24,6.15]),'black','datasheet outline; includes thickness allowance; FPC NOT verified')
add('display_lens',box([33,41,.8],[0,24,10.1]),[110,180,205,100],'custom polycarbonate lens; adhesive and active-area alignment TBD')
tray=diff(box([38,50,1],[0,24,4.3]),[box([31,43,3],[0,24,4.3]),box([16,12,3],[0,1,4.3])])
tray=union([tray,*[box([2,2,3],[x,y,2.3]) for x in [-18,18] for y in [4,44]]])
add('display_support',tray,'case','custom support; 0.35 mm side clearance; tape/shim fit trial needed')
# Flex routing corridor deliberately rendered translucent, not as a bent cable.
add('display_FPC_reserved',box([16,17,2],[0,-7,2.3]),[240,130,50,75],'reserved corridor; bend radius, latch access and contact-side mating unverified')
add('battery_2011_fit_only',box([36,60,7],[0,-42,-6.5]),'amber','Adafruit 2011 body only; NOT approved for modem current; wire exit not included')
add('battery_insulator',box([39,64,.5],[0,-42,-2.55]),'case','insulating tray; attach at perimeter, never compress pouch')
add('modem_EG912U_envelope',box([25,29,2.4],[11,6,-2]),'metal','exact candidate body envelope; land pattern and firmware variant not released')
add('MCU_S3_envelope',box([18,25.5,3.2],[-13,32,-2.4]),'metal','ESP32-S3-WROOM-1-N16 envelope; antenna keepout not validated')
add('power_reserved',box([18,20,4],[-13,4,-2.8]),[180,100,80,150],'allocation only; charger/regulators/passives not placed')
add('antenna_FXP40_reserved',box([46.2,12.1,.2],[0,77,8.4]),'amber','larger of conflicting datasheet widths; RF performance and metal spacing unverified')
add('receiver_AR01232',box([12,6,3],[0,57,6.7]),'black','PUI AR01232MS-SC12-WP-R envelope; spring contacts need precise compression')
add('microphone_CMC5044',cyl(3,5.2,[14,-79,3.4]),'metal','6 mm body; grommet and lead route TBD')
add('usb_power_reserved',box([10,8,4],[0,-81,2.8]),'metal','UJC-HP-3-SMT-TR provisional envelope; exact drawing not traced')
add('nanoSIM_reserved',box([15,17,2],[12,47,-1.8]),'metal','Molex 1042240820 reserved volume, not exact model; remove back for access')
add('battery_connector_reserved',box([8,10,6],[23,-30,-4]),'metal','JST PH fit-only; 2 A family rating insufficient for unrestricted 3 A modem design')
for c,r,x,y,label in keys:
    add(f'SW{r*3+c+1}_B3F',box([6,6,4.3],[x,y,2.95]),'black','B3F-1000 simplified body; lead tips require trim and inspection')
    cap=union([box([9,10,3.4],[x,y,9.3]),box([11,11.5,.6],[x,y,7.3]),box([2.5,2.5,1.7],[x,y,6.15])])
    add(f'keycap_{r*3+c+1}',cap,'case','custom retained piston; 0.2 mm nominal actuator gap; needs TPU return web and travel trial')
for i,(x,y) in enumerate(holes):
    add(f'bolt_{i+1}',union([cyl(1,25,[x,y,-2]),cyl(1.9,2,[x,y,11.5])]),'metal','ISO 4762 M2x25 nominal envelope; vendor and head drawing TBD')
    add(f'nut_{i+1}',diff(cyl(2.3,1.6,[x,y,-12.7],6),[cyl(1,3,[x,y,-12.7])]),'metal','ISO 4032 M2 nominal envelope; anti-rotation pocket needs tolerance coupon')

scene=tm.Scene(); exploded=tm.Scene()
metadata=[]
for name,p in parts.items():
    m=p['mesh']; m.export(OUT/f'{name}.stl')
    metadata.append({'name':name,'bounds_mm':m.bounds.tolist(),'watertight':bool(m.is_watertight),'volume_mm3':float(m.volume),'status':p['status']})
    g=m.copy(); g.apply_scale(.001); scene.add_geometry(g,node_name=name,geom_name=name)
    e=m.copy()
    dz=40 if name=='front_shell' else 25 if name.startswith('keycap') or name in ['display_lens','display_NHD_1_8','receiver_AR01232'] else -35 if name=='rear_shell' else -20 if name.startswith('battery') else 0
    e.apply_translation([0,0,dz]); e.apply_scale(.001); exploded.add_geometry(e,node_name=name,geom_name=name)
scene.export(OUT/'assembly.glb'); exploded.export(OUT/'exploded.glb')
(OUT/'assembly-manifest.json').write_text(json.dumps(metadata,indent=2))
# Envelope collision tests exclude intentional shell/fastener/support mating and
# reserved routing regions. This is not full collision or tolerance validation.
checked=['display_NHD_1_8','battery_2011_fit_only','modem_EG912U_envelope','MCU_S3_envelope','power_reserved','antenna_FXP40_reserved','receiver_AR01232','microphone_CMC5044','usb_power_reserved','nanoSIM_reserved','battery_connector_reserved']+[f'SW{i}_B3F' for i in range(1,16)]
collisions=[]
for a,b in itertools.combinations(checked,2):
    overlap=np.minimum(parts[a]['mesh'].bounds[1],parts[b]['mesh'].bounds[1])-np.maximum(parts[a]['mesh'].bounds[0],parts[b]['mesh'].bounds[0])
    if np.all(overlap>1e-4): collisions.append([a,b,overlap.tolist()])
report={'check':'component envelope AABB intersections only','pairs_checked':len(checked)*(len(checked)-1)//2,'collisions':collisions,'watertight_meshes':sum(p['mesh'].is_watertight for p in parts.values()),'mesh_count':len(parts),'not_checked':['FPC mating/bends','wire routes','battery swelling specification','key force and travel','RF keepouts/performance','spring contact compression','manufacturing tolerance stack','electrical PCB clearances'],'antenna_to_board_y_gap_mm':70.95-60,'battery_to_board_z_gap_mm':2.2,'case_nominal_mm':[62,174,24],'bolt_head_protrusion_mm':2,'bolt_tip_protrusion_mm':1}
(OUT/'mechanical-checks.json').write_text(json.dumps(report,indent=2))
shell_collisions=[]
for name in checked+[f'keycap_{i}' for i in range(1,16)]+['display_lens']:
    for shell in ['front_shell','rear_shell']:
        hit=tm.boolean.intersection([parts[name]['mesh'],parts[shell]['mesh']],engine='manifold')
        if hit.volume>0.001: shell_collisions.append([name,shell,float(hit.volume)])
report['shell_intersection_checks']=2*(len(checked)+16)
report['shell_collisions']=shell_collisions
(OUT/'mechanical-checks.json').write_text(json.dumps(report,indent=2))
assert not shell_collisions,shell_collisions
assert not collisions, collisions
assert all(p['mesh'].is_watertight for p in parts.values())
print(json.dumps(report,indent=2))

# Standalone dimensioned overview, front view looking toward -Z.
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="900" viewBox="0 0 1100 900"><rect width="1100" height="900" fill="#f4f5f7"/><style>text{font-family:Arial;fill:#243344} .s{font-size:15px}</style><text x="40" y="45" font-size="28">ANAS / PHONE — Mechanical fit study 0.1</text><text x="40" y="73" class="s">Preliminary envelopes • not a verified assembly • dimensions in mm</text>']
def rect(x,y,w,h,fill,stroke='#536472'):
    svg.append(f'<rect x="{190+3*(x-w/2)}" y="{405-3*(y+h/2)}" width="{w*3}" height="{h*3}" rx="3" fill="{fill}" stroke="{stroke}"/>')
rect(0,0,62,174,'#d5dee5'); rect(0,-12,56,144,'#b8dccc');rect(0,77,46.2,12.1,'#edb84c');rect(0,24,34.7,46.75,'#31495f');rect(0,57,12,6,'#243344')
for c,r,x,y,l in keys:
    rect(x,y,9,10,'white');svg.append(f'<text x="{190+x*3}" y="{410-y*3}" text-anchor="middle" font-size="{7 if len(l)>1 else 14}">{l}</text>')
for x,y in holes:svg.append(f'<circle cx="{190+x*3}" cy="{405-y*3}" r="3.45" fill="white" stroke="#222"/>')
svg+=['<text x="95" y="705" class="s">62 W × 174 H × 24 D</text>','<text x="95" y="730" class="s">56 × 144 × 1.6 board blank</text>']
notes=['One rigid main PCB; top switches + display, rear electronics.','Display: 34.7 × 46.75; reserve 2.7 thickness.','Battery: 36 × 60 × 7 at rear, fit-only candidate.','Modem: 25 × 29 × 2.4, EG912U-GL candidate.','Antenna: reserve 46.2 × 12.1; actual width conflict to resolve.','Key grid: 14 horizontal / 12 vertical pitch, 15 keys.','M2 through-fasteners: (±24,54), (±24,−79).','Rear access: battery, SIM, service/debug connection.','Gates: cell pulse rating, FPC fold, key travel, RF/carrier.','PCB routing stays blocked until these gates close.']
for i,n in enumerate(notes):svg.append(f'<text x="360" y="{160+i*39}" class="s">{n}</text>')
svg.append('<text x="360" y="610" class="s">Stack: front +10.5 / PCB ±0.8 / rear −13.5</text><text x="360" y="640" class="s">Case dimensions exclude bolt heads and tips.</text></svg>')
(OUT/'assembly-overview.svg').write_text(''.join(svg))
