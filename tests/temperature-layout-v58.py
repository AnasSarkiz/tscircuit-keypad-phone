import json,hashlib
from pathlib import Path
from shapely.geometry import LineString
j=json.load(open('output/usb-placement-v58.circuit.json'));c=json.load(open('routing/usb-layered-v58.json'));old=json.load(open('routing/usb-layered-v57.json'))
assert [x for x in c['routes'] if not x['name'].startswith('TEMP58')]==old['routes']
assert [x for x in c['vias'] if not x['name'].startswith('TEMP58')]==old['vias']
expected={'R_TEMP_COLD_TOP':'RT0603BRD0760K4L','R_TEMP_COLD_BOTTOM':'RT0603BRD07100KL','R_TEMP_COLD_HYST':'RC0603FR-0710ML','R_TEMP_HOT_TOP':'RT0603BRD0793K1L','R_TEMP_HOT_BOTTOM':'RT0603BRD07100KL','R_TEMP_HOT_INPUT':'RT0603BRD0710KL','R_TEMP_HOT_HYST':'RC0603FR-0710ML'}
for n,m in expected.items():assert next(x for x in j if x['type']=='source_component' and x['name']==n)['manufacturer_part_number']==m
assert not any(x['type']=='pcb_solder_paste' for x in j)
lengths={r['name']:LineString(r['points']).length for r in c['routes'] if r['name'].startswith('TEMP58')};assert max(lengths.values())<65,lengths
assert hashlib.sha256(Path('/workspace/anas-phone-study-v57.zip').read_bytes()).hexdigest()=='c286a0139c2cfb9e4df72d21401987d37e3c23ee4f180bd835de0f2cdfc2e430'
Path('output/temperature-layout-v58-checks.json').write_text(json.dumps({'seven_MPNs_checked':True,'V57_routes_vias_archive_unchanged':True,'route_lengths_mm':lengths,'comparator_unplaced':True,'hardware_qualified':False,'release':False},indent=2));print('PASS seven MPNs, V57 preservation and route lengths',lengths)
