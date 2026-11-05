import json
from pathlib import Path
j=json.load(open('engineering/mcu-drive-review-v42.json'))
i=j['rail_max_V']/(j['pulldown_nominal_ohms']*(1-j['pulldown_tolerance_fraction'])*(1-j['additional_resistance_drift_allocation_fraction']))
assert .00036<i<.000368
assert not j['loaded_drive_guaranteed'] and not j['brownout_output_state_guaranteed']
j['pulldown_current_max_A']=i
j['conclusion']='0.3673 mA finite load; no loaded VOH or brownout margin claimed. Typical current is excluded as a guarantee.'
Path('output/mcu-drive-review-v42.json').write_text(json.dumps(j,indent=2));print(j['conclusion'])
