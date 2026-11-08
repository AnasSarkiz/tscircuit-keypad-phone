"""Partial four-layer copper construction and independent geometry validation.
Process dimensions are engineering choices, not fabrication qualification.
"""
import json,math
from pathlib import Path
from shapely.geometry import Point,LineString,box,Polygon,mapping
from shapely.ops import unary_union, nearest_points
from shapely import constrained_delaunay_triangles
root=Path(__file__).resolve().parents[1]
j=json.loads((root/'output/usb-placement-v66.circuit.json').read_text());config=json.loads((root/'routing/usb-layered-v66.json').read_text());ids={x[k]:x for x in j for k in [x['type']+'_id'] if k in x};netids={x['name']:x['source_net_id'] for x in j if x['type']=='source_net'}
assert all(r.get('candidate_routed') is not False for r in config['routes']), 'Unrouted candidate cannot be validated'
# Core0.0.2302 represents repeated package terminals through internal groups.
# Resolve those groups explicitly; a missing direct trace is not evidence of NC.
source_parent={x['source_port_id']:x['source_port_id'] for x in j if x['type']=='source_port'}
def source_find(n):
 while source_parent[n]!=n:n=source_parent[n]
 return n
for component in [x for x in j if x['type']=='source_component']:
 for group in component.get('internally_connected_source_port_ids',[]):
  assert all(n in source_parent and ids[n]['source_component_id']==component['source_component_id'] for n in group),'invalid internal terminal group'
  for n in group[1:]:source_parent[source_find(n)]=source_find(group[0])
source_nets={}
for t in [x for x in j if x['type']=='source_trace']:
 for n in t['connected_source_port_ids']:source_nets.setdefault(source_find(n),set()).update(t.get('connected_source_net_ids',[]))
assert all(len(ns)<=1 for ns in source_nets.values()),'conflicting source net assignments'
def port_nets(pcb_port_id):
 assert pcb_port_id in ids,'unmapped physical port'
 port=ids[pcb_port_id]['source_port_id']
 return source_nets.get(source_find(port),set())
items=[];padnodes={}
def add(name,net,layer,shape,kind):items.append(dict(name=name,net=net,layer=layer,shape=shape,kind=kind))
for p in [x for x in j if x['type']=='pcb_smtpad']:
 p.setdefault('soldermask_margin',.025) # explicit proposed mask expansion; factory approval remains open
 nn=port_nets(p['pcb_port_id']);net=ids[next(iter(nn))]['name'] if nn else 'NC_'+p['pcb_smtpad_id'];ref=ids[ids[p['pcb_component_id']]['source_component_id']]['name'];name=ref+'.'+p['port_hints'][0]
 if name in padnodes:name+='@'+p['pcb_smtpad_id']
 shape=Polygon([(q['x'],q['y']) for q in p['points']]) if p['shape']=='polygon' else box(p['x']-p['width']/2,p['y']-p['height']/2,p['x']+p['width']/2,p['y']+p['height']/2);add(name,net,p['layer'],shape,'probe_pad' if ref.startswith('TP_') else 'pad');padnodes[name]=len(items)-1
for i,r in enumerate(config['routes']):
 line=LineString(r['points']);shape=line.buffer(r['width']/2,quad_segs=16);add(r['name'],r['net'],r['layer'],shape,'trace')
 for ref,pin in r['pads']:
  p=items[padnodes[ref+'.pin'+str(pin)]];assert p['net']==r['net'];assert p['layer']==r['layer'];assert shape.intersects(p['shape']),'missed pad'
 sid=f'source_trace_v66_{i}';j.append(dict(type='source_trace',source_trace_id=sid,connected_source_port_ids=[],connected_source_net_ids=[netids[r['net']]]));j.append(dict(type='pcb_trace',pcb_trace_id=f'pcb_trace_v66_{i}',source_trace_id=sid,route=[dict(route_type='wire',x=q[0],y=q[1],width=r['width'],layer=r['layer']) for q in r['points']]))
# Real plated switch lands,with explicit component internal commoning.
keypad_lands=[];keypad_bridges=[];keypad_internal={}
for p in [x for x in j if x['type']=='pcb_plated_hole']:
 assert p['hole_diameter']==1 and p['outer_diameter']==2
 ref=ids[ids[p['pcb_component_id']]['source_component_id']]['name'];logical=next(h for h in p['port_hints'] if h in ['pin1','pin2'])
 nn=port_nets(p['pcb_port_id']);assert len(nn)==1
 net=ids[next(iter(nn))]['name'];base=len(items);keypad_lands.append((p['x'],p['y']))
 for layer in ['top','inner1','inner2','bottom']:
  name=ref+'.'+logical+'@'+p['pcb_plated_hole_id']+'_'+layer
  add(name,net,layer,Point(p['x'],p['y']).buffer(1/math.cos(math.pi/128),quad_segs=32),'external_pad')
  padnodes[name]=len(items)-1
 keypad_bridges.extend((base,base+i) for i in [1,2,3]);keypad_internal.setdefault((ref,logical),[]).append(base)
assert len(keypad_lands)==60
via_pairs=[]
for v in config['vias']:
 assert v['drill']>=.2 and (v['outer']-v['drill'])/2>=.15-1e-9
 shape=Point(v['xy']).buffer(v['outer']/2,quad_segs=32);via_pairs.extend([(len(items),len(items)+i) for i in (1,2,3)])
 for layer in ['top','inner1','inner2','bottom']:add(v['name']+'_'+layer,v['net'],layer,shape,'via')
 j.append(dict(type='pcb_via',pcb_via_id='via_v66_'+v['name'],x=v['xy'][0],y=v['xy'][1],outer_diameter=v['outer'],hole_diameter=v['drill'],layers=['top','inner1','inner2','bottom'],topmost_drill_layer='top',bottommost_drill_layer='bottom',through_hole=True))
plane=box(*config['ground_boundary']);bx,by,br=config['bolt_exclusion'];plane=plane.difference(Point(bx,by).buffer(br,quad_segs=48));plane=plane.difference(Point(24,-79).buffer(4,quad_segs=48))
for x in [-24,24]:plane=plane.difference(Point(x,54).buffer(4,quad_segs=48))
for item in items:
 if item['layer']=='inner1' and (item['net']!='GND' or item['kind']=='external_pad'):plane=plane.difference(item['shape'].buffer(.2,quad_segs=16))
for bounds in config.get('copper_keepouts',[]):plane=plane.difference(box(*bounds))
discarded_island_area=0.0
if plane.geom_type=='MultiPolygon':
 pieces=list(plane.geoms);selected=max(pieces,key=lambda p:p.area);discarded_island_area=plane.area-selected.area;plane=selected
assert plane.geom_type=='Polygon','invalid ground plane'
for v in config['vias']:
 if v['net']=='GND' and box(*config['ground_boundary']).covers(Point(v['xy'])):assert plane.intersects(Point(v['xy']).buffer(v['outer']/2)),('ground via on discarded island',v['name'])
assert plane.buffer(-.1).geom_type=='Polygon','ground neck narrower than .2mm screening'
add('LOCAL_GROUND_POUR','GND','inner1',plane,'plane')
# Export exact plane by covered triangles: no implicit fill across antipads/bolt cutout.
triangles=list(constrained_delaunay_triangles(plane).geoms)
assert plane.symmetric_difference(unary_union(triangles)).area<1e-8
for i,t in enumerate(triangles):j.append(dict(type='pcb_copper_pour',pcb_copper_pour_id=f'pour_v66_{i}',shape='polygon',layer='inner1',source_net_id=netids['GND'],covered_with_solder_mask=True,points=[dict(x=x,y=y) for x,y in list(t.exterior.coords)[:-1]]))
minimum=math.inf;checked=0;clearance_conflicts=[]
for i,a in enumerate(items):
 assert box(-27.75,-83.75,27.75,59.75).covers(a['shape']),('edge',a['name'])
 for b in items[i+1:]:
  if a['layer']!=b['layer'] or a['net']==b['net']:continue
  d=a['shape'].distance(b['shape']);minimum=min(minimum,d);checked+=1
  if d<.15-1e-8:
   pa,pb=nearest_points(a['shape'],b['shape']);clearance_conflicts.append({'a':a['name'],'b':b['name'],'layer':a['layer'],'net_a':a['net'],'net_b':b['net'],'gap_mm':d,'nearest':[[pa.x,pa.y],[pb.x,pb.y]]})
(root/'output/routing-migration-conflicts.json').write_text(json.dumps({'required_gap_mm':.15,'conflicts':clearance_conflicts},indent=2))
assert not clearance_conflicts,('copper clearance failures',len(clearance_conflicts),clearance_conflicts[:3])
for item in items:
 for bounds in config.get('copper_keepouts',[]):assert item['shape'].intersection(box(*bounds)).area<1e-8,('antenna_keepout',item['name'])
# Extract actual connectivity from copper intersections; vias are explicit layer bridges.
parent=list(range(len(items)))
def find(n):
 while parent[n]!=n:n=parent[n]
 return n
def join(a,b):parent[find(a)]=find(b)
for i,a in enumerate(items):
 for k in range(i):
  b=items[k]
  if a['net']==b['net'] and a['layer']==b['layer'] and a['shape'].intersects(b['shape']):join(i,k)
for a,b in via_pairs+keypad_bridges:join(a,b)
# These joins represent actual permanently common terminals inside each switch,
# not fabricated copper or the normally-open contact between rows.
for indexes in keypad_internal.values():
 assert len(indexes)==2
 assert len({items[i]['net'] for i in indexes})==1,'switch common terminals assigned different nets'
 join(*indexes)
groups={}
for name,n in padnodes.items():
 if items[n]['net'].startswith('NC_'):continue
 groups.setdefault(items[n]['net'],{}).setdefault(find(n),[]).append(name.split('@')[0])
assert len(groups['GND'])==1,'placed ground disconnected'
for row in range(5):
 expected={f'SW{row*3+c+1}.pin1' for c in range(2 if row==0 else 3)}
 assert any(expected<=set(g) for g in groups['ROW'+str(row)].values()),'keypad row incomplete'
for col in range(3):
 expected={f'SW{row*3+col+1}.pin2' for row in range(1 if col==2 else 0,5)}
 assert any(expected<=set(g) for g in groups['COL'+str(col)].values()),'keypad column incomplete'

assert len(groups['USB_AUX3V3_PENDING'])==1,'placed supply disconnected'
for net in ['VLOGIC_3V15','MODEM_VDD_EXT_1V8']:
 assert len(groups[net])==1,'placed translator supply disconnected'
for net in ['ON_OFF_MCU','RESET_MCU','MODEM_KEY_GATE','MODEM_RESET_GATE']:
 assert len(groups[net])==1,'placed modem control disconnected'
for net in ['USIM1_RST_SOCKET_PENDING','USIM1_CLK_SOCKET_PENDING','USIM1_DATA_SOCKET_PENDING','USIM1_VDD_PENDING']:
 assert len(groups[net])==1,'placed SIM circuit disconnected'
for net in ['MODEM_PWRKEY_OD','MODEM_RESET_OD','USIM1_RST_MODEM_PENDING','USIM1_CLK_MODEM_PENDING','USIM1_DATA_MODEM_PENDING']:
 assert len(groups[net])==1,'placed modem endpoint disconnected'
for net in ['TEMP_COLD_OK','TEMP_HOT_OK','CHARGE_REQUEST_QUALIFIED_PENDING','CE_MID1','CE_MID2','TEMP_COLD_REF','TEMP_HOT_REF','TEMP_HOT_SENSE','CHG_REGN','BAT_NTC','TS_SERIES','CHARGE_REGN_READY','CHARGE_POR_CT','CHARGE_REGN_SENSE']:
 assert len(groups[net])==1,'placed temperature interlock endpoint disconnected'
for net in ['MODEM_RX','MODEM_TX','MODEM_RTS','MODEM_CTS','MODEM_STATUS','HOST_TX','HOST_RX','HOST_RTS','HOST_CTS','MODEM_STATUS_HOST_PENDING','MCU_EN','MCU_BOOT_N','DEBUG_RX_3V15','DEBUG_TX_3V15','LCD_CS_N','BACKLIGHT_PWM','LCD_RST_N','CHARGE_REQUEST_MCU','SYSTEM_OFF_REQUEST','BUTTON_INT_N','BUTTON_KILL_BRANCH','BUTTON_ENABLE_RAW','LOGIC_ENABLE','SYS_CANDIDATE','BUTTON_PDT_BRANCH']:
 assert len(groups[net])==1,'placed UART endpoint disconnected'
for net in ['ROW0','ROW1','ROW2','ROW3','ROW4','COL0','COL1','COL2','BUTTON_BRANCH_UNQUALIFIED']:
 assert len(groups[net])==1,'keypad MCU or button connection incomplete '+net
# Check every ground via reaches the connected plane, not merely an isolated disk.
plane_root=find(len(items)-1)
for a,b in via_pairs:
 if items[a]['net']=='GND':assert find(a)==plane_root
out={'placed_net_islands':{n:list(g.values()) for n,g in groups.items()},'minimum_foreign_copper_gap_mm':minimum,'foreign_geometry_pairs_checked':checked,'via_count':len(config['vias']),'layer_count':4,'ground_plane_layer':'inner1','discarded_floating_plane_area_mm2':discarded_island_area,'plane_area_mm2':plane.area,'keypad_PTH_lands_integrated':len(keypad_lands),'keypad_internal_common_pairs':len(keypad_internal),'plane_components':1,'plane_minimum_neck_screen_mm':.2,'plane_triangles_exported':len(triangles),'all_placed_supply_and_ground_joined':True,'release':False,'unverified':['via fabrication/drill tolerance','thermal relief/process','plane impedance and EMI','unplaced bottom component lands','poweroff and transient behavior']}
(root/'output/usb-layered-v66-checks.json').write_text(json.dumps(out,indent=2));(root/'output/usb-layered-v66.circuit.json').write_text(json.dumps(j,indent=2));(root/'output/usb-layered-v66-geometry.json').write_text(json.dumps([dict(name=x['name'],net=x['net'],layer=x['layer'],kind=x['kind'],geometry=mapping(x['shape'])) for x in items if x['kind'] not in ['pad','external_pad']]))
print('PASS layered geometry, actual copper connectivity, plane continuity:',{k:v for k,v in out.items() if k not in ['placed_net_islands','unverified']})
