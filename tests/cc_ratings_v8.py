import json
# Datasheet comparisons, not waveforms or proof of system-level ESD immunity.
# TPD6S300A test uses a 24V hot plug, 1m cable and 30ohm load on CC.
old_abs=6;new_abs=28;test_clamp=8
assert test_clamp>old_abs
assert test_clamp<new_abs
r={'rejected_pair':'TPD6S300A + TUSB320LAI','candidate_pair':'TPD6S300A + HUSB320-BA000-QN12R','old_CC_absolute_max_V':old_abs,'new_CC_absolute_max_V':new_abs,'protector_specified_test_clamp_V':test_clamp,'test_conditions':'24V hot plug; 1m Type-C cable; 30ohm load; VPWR3.3V','scope':'positive-voltage rating conflict removed in candidate; actual loading, undershoot, unpowered behavior and IEC ESD remain unverified','source_voltage_limit_V':22,'warning':'28V is an absolute maximum, not recommended continuous operating voltage'}
open('output/cc-ratings-v8.json','w').write(json.dumps(r,indent=2));print('PASS: positive CC clamp rating comparison; not transient validation')
