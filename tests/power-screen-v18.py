"""Necessary-power rejection and startup timing sensitivity; no hardware approval."""
import json
from pathlib import Path
# Ideal efficiency is deliberately optimistic: failure here cannot be fixed by a better converter.
required_w=3.8*2+3.3*.6
packs=[{'part':'ICP606168PRT','continuous_A':2.24,'source':'https://www.renata.com/en-us/downloads/?fileid=f82bf4bf06b0198391e517809f&product=icp606168prt'}, {'part':'ICP543759PMT','continuous_A':1.32,'source':'https://www.renata.com/en-us/downloads/?fileid=26760f2abea111a29c91240df5&product=icp543759pmt'}]
for p in packs:
 p['ideal_max_power_at_4_2V_W']=4.2*p['continuous_A'];p['can_sustain_budget_even_ideally']=p['ideal_max_power_at_4_2V_W']>=required_w
 assert not p['can_sustain_budget_even_ideally']
# CPDT formula from2954fb: capacitance[uF]=1.56e-4*(tPDT[ms]-1).
# This is a design equation, NOT a guaranteed scaling of 1500pF timing limits to2.2uF.
shutdown_ms=3100;firmware_allocation_ms=500
required_cap=(shutdown_ms+firmware_allocation_ms-1)*1.56e-4
retention=required_cap/2.2
assert .25<retention<.26
rows=[{'effective_fraction':f,'nominal_equation_delay_ms':1+2.2*f/1.56e-4,'covers_assumed_3600ms':1+2.2*f/1.56e-4>=3600} for f in [.1,.2,.3,.5,.7,1]]
assert any(x['covers_assumed_3600ms'] for x in rows) and any(not x['covers_assumed_3600ms'] for x in rows)
r={'required_output_W_no_backlight':required_w,'packs':packs,'scope':'Conservative simultaneous sustained design load; does not assert actual average phone load or unsupported pack pulse rating. Neither pack qualifies this design budget.','PDT':{'source':'https://www.analog.com/media/en/technical-documentation/data-sheets/2954fb.pdf','assumed_shutdown_ms':shutdown_ms,'unverified_firmware_latency_allocation_ms':firmware_allocation_ms,'required_capacitance_uF_from_design_equation':required_cap,'required_nominal_2_2uF_retention':retention,'sensitivity':rows,'guaranteed_large_cap_timer_bounds':False},'qualification':False}
Path('output/power-screen-v18.json').write_text(json.dumps(r,indent=2));print('PASS optimistic-power rejection of two packs and timer sensitivity checks')
