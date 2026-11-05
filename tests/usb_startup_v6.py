"""DC corner checks; NOT a transient simulation or ramp guarantee."""
import json,itertools
aux_min=3.3*.98-.050-.010
trip_max=.405*1.02*(1+634000*1.0035/(100000*.9965))*1.03+25e-9*634000*1.0035
trip_min=.405*.98*(1+634000*.9965/(100000*1.0035))-25e-9*634000*1.0035
assert trip_min>2.85
assert aux_min>trip_max
# Conservative 2.2 V gate VOH, 1% resistors, 0.2 uA total sink leakage.
drive=100000*1.01; pulldown=1000000*.99
ven=(2.2/drive-.4e-6)/(1/drive+1/pulldown)
assert ven>1.223
# POR's low-voltage guarantee supports 15 uA; drive resistor limits the
# unknown NOR output, conservatively treated as the entire auxiliary voltage.
assert 1.3/(100000*.99)<15e-6
assert 3.366/(100000*.99)<.4e-3
truth=[]
for out1,out2,reset in itertools.product([False,True],repeat=3):
    enable=not(out1 or out2 or reset)
    truth.append(dict(out1=out1,out2=out2,reset_asserted=reset,enable=enable))
    assert enable==((out1,out2,reset)==(False,False,False))
r={'aux_min_V':aux_min,'supervisor_max_release_bound_V':trip_max,'release_margin_V':aux_min-trip_max,'enable_min_DC_V':ven,'enable_max_threshold_V':1.223,'truth_table':truth,'scope':'specified DC bounds only; ramp, detector transition, ESD, thermal and source downgrade remain physical tests','limitations':['0.4 uA combines supervisor 300nA and eFuse 100nA maximum; resistor 0.35% includes a provisional temperature allowance','TPS709 EN-startup specification is not a guarantee for arbitrary VBUS ramps','no auxiliary thermal/load qualification yet']}
open('output/usb-startup-checks.json','w').write(json.dumps(r,indent=2))
print(json.dumps(r,indent=2))
