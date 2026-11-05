import json,math,copy
from pathlib import Path
j=json.load(open('output/usb-placement-v45.circuit.json'));ids={x[x['type']+'_id']:x for x in j if x['type']+'_id' in x}
expected={'TP_BOOT':('MCU_BOOT_N',27),'TP_EN':('MCU_EN',3),'TP_RX':('DEBUG_RX_3V15',36),'TP_TX':('DEBUG_TX_3V15',37),'TP_GND':('GND',1),'TP_VREF':('VLOGIC_3V15',2)}
rows=[]
for ref,(net,pin) in expected.items():
 s=next(x for x in j if x['type']=='source_component' and x['name']==ref);assert not s.get('manufacturer_part_number')
 p=next(p for p in j if p['type']=='pcb_smtpad' and ids[p['pcb_component_id']]['source_component_id']==s['source_component_id']);port=ids[p['pcb_port_id']]['source_port_id']
 ns={ids[n]['name'] for t in j if t['type']=='source_trace' and port in t.get('connected_source_port_ids',[]) for n in t.get('connected_source_net_ids',[])};assert ns=={net};assert p['width']==1.5 and p['height']==1.5 and p['layer']=='bottom'
 rows.append({'reference':ref,'net':net,'MCU_pin':pin,'x_mm':p['x'],'y_mm':p['y'],'side':'bottom','land_mm':[1.5,1.5]})
logical=json.load(open('output/power-integrated-v45.circuit.json'));mcu=next(x for x in logical if x['type']=='source_component' and x['name']=='U_MCU');g46=next(x for x in logical if x['type']=='source_port' and x['source_component_id']==mcu['source_component_id'] and x.get('pin_number')==16)
assert not any(g46['source_port_id'] in t.get('connected_source_port_ids',[]) for t in logical if t['type']=='source_trace')
c=json.load(open('routing/usb-layered-v45.json'));lengths={r['name']:sum(math.dist(a,b) for a,b in zip(r['points'],r['points'][1:])) for r in c['routes'] if r['name'].startswith('MCU_DBG') or r['name']=='MCU_R_BOOT_V_AUTO'}
assert lengths['MCU_DBG_EN_SOURCE_AUTO']<5 and lengths['MCU_R_BOOT_V_AUTO']<25,'reject avoidable long detours'
Path('output/mcu-test-access-v45.json').write_text(json.dumps({'contacts':rows,'coordinates':'Board top-view datum, even for bottom contacts; fixture underside must mirror appropriately','trace_lengths_mm':lengths,'fixture_qualified':False,'release':False},indent=2));print('PASS six bare-board contacts, UART orientation, GPIO46 left open; no connector BOM invented')
