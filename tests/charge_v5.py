import json
from pathlib import Path
ichg=[639/(698*1.01),677/698,715/(698*.99)]
iusb=[459/(383*1.01),478/383,500/(383*.99)]
assert ichg[2]<2.4 and iusb[2]<1.5
j={'charge_A_min_nom_max':ichg,'input_A_min_nom_max_unknown_adapter_only':iusb,'ideal_CC_hours_at_nominal':4.8/ichg[1],'status':'candidate values only; CE stays off until guarded temperature and source path qualified','conditions':['Flat 246524 pack only; not old 18650 cold-temperature branch','Only connect main USB load after proven 3A CC advertisement for current eFuse branch','BQ25616 D+/D- unknown-adapter detection must be confirmed; ILIM does not override every detected source type','Input limit covers charger SYS loads too; CE off alone does not stop SYS drawing current','Thermal throttling and CV taper can extend charge time; do not defeat safety timer']}
Path('output/charge-v5-checks.json').write_text(json.dumps(j,indent=2));print(json.dumps(j,indent=2))
