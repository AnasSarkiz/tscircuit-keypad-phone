import json
from pathlib import Path
old=json.load(open('output/via-in-pad-v40.json'));new=json.load(open('output/manufacturing-v41.json'))
assert old['count']==46 and len(old['entries'])==46
assert new['drill_in_land_intersections']==[] and new['violations']==[]
assert not new['filled_capped_vias_assumed'] and not new['factory_rules_approved']
a={v['name']:v for v in json.load(open('routing/usb-layered-v40.json'))['vias']};b={v['name']:v for v in json.load(open('routing/usb-layered-v41.json'))['vias']}
assert set(a)<=set(b) and set(b)-set(a)=={'MOD_UART_RXD_ESCAPE','MOD_UART_RXD_TRANSLATOR','MOD_UART_TXD_ESCAPE','MOD_UART_TXD_TRANSLATOR'} and all(v['outer']==.45 and v['drill']==.2 for v in b.values())
changed=[n for n in a if a[n]['xy']!=b[n]['xy']]
assert all(v['via'] in changed for v in old['entries'])
Path('output/fanout-final-v41.json').write_text(json.dumps({'original_drill_in_land_cases':46,'final_drill_in_land_cases':0,'relocated_vias':len(changed),'relocated_names':changed,'final_total_vias':len(b),'additional_UART_vias':4,'automatic_first_pass_unresolved':['EFUSE_OVLO_via26','EFUSE_OV_SUPPLY_via33'],'manual_resolution':'Both rerouted; OVLO via27 adjusted to clear retainer spacer','residual_manufacturing_geometry_violations':new['violations'],'factory_process_approval':False,'release':False},indent=2))
print('PASS46 former drill/land overlaps eliminated;',len(changed),'vias relocated; four ordinary UART vias added; no filled/capped process')
