import itertools,json
from pathlib import Path
# Total regulation budget 3%, resistor divider .1%. Don't double count reference.
volts=[.5*(1+r)*(1+909*(1+a)/(100*(1+b))) for r,a,b in itertools.product([-.03,.03],[-.001,.001],[-.001,.001])]
lo,hi=min(volts),max(volts)
peak=hi*.100/(3.3*.8)+3.3*(1-3.3/hi)/(2*4.7e-6*.8*960e3)
assert lo>3.4+.4 and hi<5.5 and peak<.5
r={'output_V':[lo,hi],'peak_A_estimate_at_100mA_load':peak,'assumptions':'80% efficiency, 3.3 V minimum SYS, L -20%, frequency 960 kHz; no validated efficiency floor or transient model','startup':'Minimum reduced startup switch limit 250mA may be insufficient with LEDs enabled. Keep sinks off until measured 5V rail stable.','required':'Inductor saturation/DCR and effective capacitor validation; waveform/thermal testing; separate ADC or supervisor qualification before PWM.'}
Path('output/boost-v5-checks.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
