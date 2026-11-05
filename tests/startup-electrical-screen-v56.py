"""Source-scoped conditional susceptibility model. No full-temperature qualification."""
import json,math
from pathlib import Path
vlow=json.load(open('output/power-budget.json'))['with_unverified_50mV_transient_budget_v'][0]
rmax=100100;threshold=.68
# Lower resistance is a study, not a BOM change.
rows=[]
for r in [100100,10100]:
 rows.append({'assumed_Rmax_ohm':r,'conditional_KILL_total_sink_budget_uA':(vlow-threshold)/r*1e6,'INT_3V3_25C_total_sink_budget_uA':(3.3-.75*3.3)/r*1e6,'INT_3V3_pullup_current_at_0V_uA':3.3/r*1e6,'INT_conditional_100pF_75pct_rise_us':-r*100e-12*math.log(.25)*1e6})
assert rows[1]['conditional_KILL_total_sink_budget_uA']>rows[0]['conditional_KILL_total_sink_budget_uA']
assert rows[1]['INT_conditional_100pF_75pct_rise_us']<rows[0]['INT_conditional_100pF_75pct_rise_us']
assert rows[1]['INT_3V3_pullup_current_at_0V_uA']<3000
out={'status':'UNQUALIFIED','sources':[{'url':'https://www.analog.com/media/en/technical-documentation/data-sheets/2954fb.pdf','revision':'2954fb RevB','pages':[3,4],'facts':{'KILL_falling_threshold_V':[.57,.63],'KILL_hysteresis_V':[.01,.05],'KILL_leakage_test':'+/-0.1uA at0.6V only','INT_leakage_test':'+/-1uA at3V only','INT_VOL_test':'0.4V max at3mA','INT_minimum_pulse_ms':26,'KILL_blanking_min_ms':400},'scope':'Full-temperature marked limits only at stated conditions. Minimum pulse requirement is not proof that shorter noise glitches are rejected.'},{'url':'https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf','revision':'v2.2','page':65,'facts':{'VIH_min_ratio':.75,'VIL_max_ratio':.25,'IIH_max_nA':50,'IIL_max_nA':50,'CIN_typ_pF':2},'scope':'Table5-4 heading3.3V,25C. Capacitance is typical only. Do not extend to full-temperature/local-rail guaranteed limits.'}],'conditional_rail_min_V':vlow,'conditional_studies':rows,'BOM_unchanged':True,'routing_is_not_electrical_qualification':True,'remaining':['Guaranteed endpoint leakage at actual bias/temperature and MCU reset/partial power','Guaranteed or measured total route/pin/assembly capacitance','Local rail ramp and actual response before400ms','RF/crosstalk/ground-shift injected noise and glitch susceptibility','INT low-current VOL and actual GPIO domain margins over intended envelope','KILL filter tradeoff and required shutdown response before selecting RC components'],'possible_next_steps':['Evaluate10k pullups with complete current/leakage and power budget','Prototype noise injection and startup/brownout sweeps','Add a documented Schmitt/filter interface only after partial-power and timing proof'],'release':False}
Path('output/startup-electrical-screen-v56.json').write_text(json.dumps(out,indent=2));print('PASS source-scoped conditional calculations; hardware remains UNQUALIFIED',rows)
