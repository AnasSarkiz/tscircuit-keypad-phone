import json,itertools
from pathlib import Path
rows=[]
for bias,imax,tol in itertools.product([2.2,3.0],[.00015],[.99,1.01]):
 r=(510*2+1500*2)*tol
 rows.append({'MICBIAS_V':bias,'assumed_mic_A':imax,'resistor_scale':tol,'series_ohm':r,'mic_terminal_V':bias-imax*r})
assert min(x['mic_terminal_V'] for x in rows)<2
rmax=4020*1.01
out={'superseded_interpretation':'2V is test supply through2.2kohm, NOT terminal minimum; see audio-correction-v26.json','scope':'DC sensitivity using reviewed electret topology; no complete microphone model. 150uA taken as candidate consumption, not proven worst-case over temperature. 2V is published test/operating condition, not an established minimum.','cases':rows,'audio_qualified':False,'remaining':['microphone minimum bias and maximum current over operating conditions','MICBIAS source current and transient limits','AFE input impedance and allowable levels','RF filter exact topology and part ratings','ESD clamp behavior','receiver differential output level and acoustic calibration']}
Path('output/audio-bias-margin-v25.json').write_text(json.dumps(out,indent=2));print('PASS bias sensitivity retains historical terminal-voltage sensitivity (not a microphone pass/fail criterion); audio NOT qualified')
