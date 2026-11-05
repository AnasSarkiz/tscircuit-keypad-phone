import itertools,json
from pathlib import Path
# Include OVLO reference min/max, .1% divider, +/-100 nA leakage.
v=[ref*(1+402000*(1+a)/(100000*(1+b)))+leak*402000*(1+a) for ref,a,b,leak in itertools.product([1.183,1.223],[-.001,.001],[-.001,.001],[-1e-7,1e-7])]
assert min(v)>5.5 and max(v)<6.5
report={'OVLO_trip_V':[min(v),max(v)],'source_requirement':'3 A CC advertisement; 1.5 A and default sources rejected by policy','current_limit_A_datasheet_at_1p65k':[1.8,2.028,2.2],'current_limit_resistor':'Use precision resistor; nominal datasheet range excludes external resistor tolerance; margin to 3A remains large','protection_scope':'candidate steady thresholds only; response time typical, no tested surge clamp or complete connector ESD path','enable':'held low; CC qualification/auxiliary supply/supervisor incomplete','voltage_rating_requirement':'raw USB and dVdt capacitors at least 35V; protected input capacitors at least 25V pending surge review; BQ25616 accepts higher input than nominal 5V','warning':'OVLO is not a 5.5V clamp. Never power low-voltage CC controller directly from protected output; independent regulated auxiliary rail required.'}
Path('output/input-v5-checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
