import json,itertools
from pathlib import Path
# Compare like with like: microphone terminal voltage after each circuit's load resistor.
i=.00015;ref_terminal=2-2200*i
vref=2.2-4020*i
assert abs(ref_terminal-1.67)<1e-9 and abs(vref-1.597)<1e-9
assert abs((vref-ref_terminal)-(-.073))<1e-9
# Reference source equivalent is conditional on same microphone current, not a device model.
equivalent_supply=vref+2200*i;assert abs(equivalent_supply-1.927)<1e-9
# Fixed 2.5V DBV LDO is specified ±40mV at input>=2.8 and load>=1mA.
vlo,vhi=2.46,2.54;imin=vlo/(2200*1.01);imax=vhi/(2200*.99)
assert imin>.001 and vlo>2.3 and vhi<3
assert 3.049>2.8
result={'correction':'V25 2V-terminal comparison was not a microphone qualification criterion. Test circuit has2V supply and2.2kohm load. Preserve terminal sensitivity, withdraw implied undervoltage conclusion.','test_terminal_V_at_assumed_150uA':ref_terminal,'existing_terminal_V_at_assumed_150uA':vref,'difference_V':vref-ref_terminal,'equivalent_test_supply_V':equivalent_supply,'mic_current_bound_and_IV_model_confirmed':False,'MEMS_supply_candidate':{'MPN':'TPS7A2025PDBVR','specified_output_V':[vlo,vhi],'minimum_input_for_tolerance_V':2.8,'bleeder_A_range':[imin,imax],'bleeder_worst_W':vhi*imax,'IM73_normal_supply_V':[2.3,3.0],'output_stability_requires_effective_uF':.47,'cap_ESR_max_ohm':.1,'qualified':False,'remaining':['capacitor effective value and ESR','enable sequencing/backpower and turn-on ramp','load/transient and microphone2.5V behavior','output headroom/input impedance and RF/ESD filters','footprints/acoustic port','supplier availability']}}
Path('output/audio-correction-v26.json').write_text(json.dumps(result,indent=2));print('PASS corrected reference circuit comparison and conditional2.5V MEMS supply margins')
