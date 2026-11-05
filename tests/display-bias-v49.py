from pathlib import Path
import hashlib,json
from shapely.geometry import LineString
j=json.load(open('output/usb-placement-v49.circuit.json'));c=json.load(open('routing/usb-layered-v49.json'));prior=json.load(open('routing/usb-layered-v48.json'));ids={x[x['type']+'_id']:x for x in j if x['type']+'_id' in x}
assert [r for r in c['routes'] if not r['name'].startswith('MCU_DBG_LCD49_')]==prior['routes']
assert [v for v in c['vias'] if not v['name'].startswith('MCU_DBG_LCD49_')]==prior['vias']
for ref,want in [('R_LCD_CS',['VLOGIC_3V15','LCD_CS_N']),('R_LCD_RST',['GND','LCD_RST_N'])]:
 u=next(x for x in j if x['type']=='source_component' and x['name']==ref);assert u['manufacturer_part_number']=='RT0603BRD07100KL'
 for pin,net in enumerate(want,1):
  port=next(x for x in j if x['type']=='source_port' and x['source_component_id']==u['source_component_id'] and x['pin_number']==pin)
  nets={ids[n]['name'] for t in j if t['type']=='source_trace' and port['source_port_id'] in t.get('connected_source_port_ids',[]) for n in t.get('connected_source_net_ids',[])}
  assert nets=={net}
lengths={r['name']:LineString(r['points']).length for r in c['routes'] if r['name'].startswith('MCU_DBG_LCD49_')}
assert max(lengths.values())<30,'Reject long detours'
assert hashlib.sha256(Path('/workspace/anas-phone-study-v48.zip').read_bytes()).hexdigest()=='c68989f7c87c1ceaaacd232e9fc70909e93b99b609dd38953afe83d0ed152d5f'
out={'new_parts':['R_LCD_CS','R_LCD_RST'],'prior_routes_and_vias_unchanged':True,'route_lengths_mm':lengths,'V48_archive_intact':True,'CS_parallel_nominal_ohm':1/(1/10000+1/100000),'scope':'Existing schematic bias only; no guaranteed MCU/display logic state, leakage or power-sequencing validation. Connector remains unplaced.','release':False}
Path('output/display-bias-v49.json').write_text(json.dumps(out,indent=2));print('PASS pin/net mapping; original V48 routes unchanged; detour limit; V48 archive intact',lengths)
