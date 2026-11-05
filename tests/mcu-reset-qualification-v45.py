"""Reject the two tempting passive shortcuts; analytical counterexamples only."""
import json,math
from pathlib import Path
j=json.load(open('engineering/mcu-reset-qualification-v45.json'))
# Ignore internal GPIO pull-up: it only worsens this low-level divider.
vdd=3.15;pullup=10000;pulldown=10000;v=vdd*pulldown/(pullup+pulldown)
assert v>.25*vdd
# A passive RC settles to a sustained undervoltage rather than forcing reset low.
tau=10000*1e-6;v_start=3.15;v_low=2.8;t=.1
en=v_low+(v_start-v_low)*math.exp(-t/tau)
assert abs(en-v_low)<.0001 and not j['release']
out={'equal_10k_fixture_divider_V':v,'nominal_GPIO_low_screen_V':.25*vdd,'nominal_RC_tau_s':tau,'RC_EN_after_100ms_at_2_8V_V':en,'interpretation':'Counterexample to RC enforcing reset, not a claim about MCU behavior outside its3.0V operating minimum','fixture_qualified':False,'brownout_qualified':False,'release':False}
Path('output/mcu-reset-qualification-v45.json').write_text(json.dumps(out,indent=2));print(out)
