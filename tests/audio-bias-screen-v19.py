"""DC sensitivity only: electret I/V law and MICBIAS loaded capability are unknown."""
import json,itertools
from pathlib import Path
rows=[]
for bias,current,tolerance in itertools.product([2.2,2.6,3.0],[.1e-3,.25e-3,.5e-3],[.99,1.01]):
 resistance=(510+1500+1500+510)*tolerance
 rows.append(dict(bias_V=bias,assumed_mic_current_A=current,resistance_ohm=resistance,projected_terminal_V=bias-current*resistance))
assert min(r['projected_terminal_V'] for r in rows)<.2
assert max(r['projected_terminal_V'] for r in rows)>2.5
Path('output/audio-bias-screen-v19.json').write_text(json.dumps({'cases':rows,'scope':'DC series-resistance budget from reviewed transcription. Microphone current is a scenario, not a guaranteed constant-current load. No actual microphone connected. 2V microphone standard test supply is NOT a guaranteed minimum terminal voltage. Ferrite DCR and MICBIAS output impedance omitted; qualification remains open.','approved':False},indent=2));print('PASS 18 DC sensitivity scenarios; microphone compatibility unresolved')
