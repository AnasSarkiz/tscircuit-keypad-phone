import json
from pathlib import Path
j=json.load(open('engineering/drive-alternatives-v44.json'))
lo,hi=j['operating_screen_V'];load=hi/(j['input_pulldown_nominal_ohm']*(1-j['tolerance_fraction'])*(1-j['drift_allocation_fraction']))+j['buffer_input_leakage_test_endpoint_A']
high_margin=lo-j['MCU_VOH_drop_V']-j['buffer_VIH_min_V'];low_margin=j['buffer_VIL_max_V']-j['MCU_VOL_max_V']
assert high_margin>.59 and low_margin>=.4 and load<j['MCU_test_load_A']
# Enabling does not become qualified solely because static margins pass.
assert j['supervisor_delay_guaranteed_max_s'] is None and not j['release']
out={'candidate_static_high_margin_V':high_margin,'candidate_static_low_margin_V':low_margin,'input_load_screen_A':load,'MCU_test_load_A':j['MCU_test_load_A'],'scope':'Conditional static screen for normal non-FT_c pin; exact pin, rail and firmware not implemented. Leakage endpoint is a screen, not arbitrary-input bound.','brownout_qualified':False,'integrated':False,'release':False}
Path('output/drive-alternatives-v44.json').write_text(json.dumps(out,indent=2));print(out)
