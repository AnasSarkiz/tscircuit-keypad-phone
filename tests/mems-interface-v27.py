import math,json,itertools
from pathlib import Path
rows=[]
for rin,c in itertools.product([1000,2000,10000,25000,50000],[60e-9,100e-9,220e-9]):
 rout=250;rs=1000;rt=rin+rs+rout;fc=1/(2*math.pi*rt*c)
 gain300=(rin/rt)/math.sqrt(1+(fc/300)**2)
 rows.append({'assumed_AFE_per_leg_R_ohm':rin,'assumed_effective_series_C_F':c,'assumed_mic_Rout_ohm':rout,'proposed_series_R_ohm':rs,'first_order_fc_Hz':fc,'gain_at300Hz_dB':20*math.log10(gain300),'meets_25kohm_load_screen':rin+rs>=25000})
assert all(not r['meets_25kohm_load_screen'] for r in rows if r['assumed_AFE_per_leg_R_ohm']<=10000)
assert all(r['meets_25kohm_load_screen'] for r in rows if r['assumed_AFE_per_leg_R_ohm']>=25000)
out={'scope':'Interface sensitivity only, not a proposed final netlist.250ohm Rout is typical; actual AFE impedance and load-capacitance bounds require applicable documentation/measurement. No coupling caps or series resistors added to main design.','reference':'Infineon IM73A135V01 V1.20 Tables6/7 Figures11/13; column placement/footprint still needs visual audit','requirements_pending':{'AFE_input_impedance_per_leg':'must satisfy minimum load condition over audio band; unknown for modem','AFE_common_mode':'direct-coupled normal-mode table1.17..1.43V; AC coupling changes transient/DC analysis','capacitive_load':'100pF entries Ca/Cb/Cd need exact column/connection verification; include cable,TVS andPCB','startup':'5ms ramp entry and30ms startup entry require table condition/column confirmation and actual2.5V test','ESD':'no approved clamp path or powered-off injection limits','mic_footprint':'mask-defined Figure13,0.8mm acoustic port, exact pads not locally inspectable'},'cases':rows,'AFE_approved':False}
Path('output/mems-interface-v27.json').write_text(json.dumps(out,indent=2));print('PASS15 interface sensitivity cases retain low-impedance load failures; AFE remains unqualified')
