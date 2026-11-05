import itertools,json
from pathlib import Path
# Conservative allocations: resistor +/-1%; total EN-node sinking leakage 1.2uA.
rows=[]
for sys,up,down in itertools.product([2.7,4.4],[9900,10100],[99000,101000]):
 v=(sys/up-1.2e-6)/(1/up+1/down)
 rows.append({'SYS_V':sys,'Rup_ohm':up,'Rdown_ohm':down,'EN_on_V':v,'high_margin_to_1_2V':v-1.2,'off_sink_current_upper_A':sys/up})
assert min(x['high_margin_to_1_2V'] for x in rows)>1.2
assert max(x['off_sink_current_upper_A'] for x in rows)<.0005
r={'cases':rows,'minimum_on_margin_V':min(x['high_margin_to_1_2V'] for x in rows),'off_voltage_guarantee_V':.4,'converter_VIL_limit_V':.4,'off_noise_margin_V':0,'scope':'Static screening using published test-point leakage as allocations. Does not prove untested intermediate-voltage leakage, noise, rise time or shutdown behavior. Zero guaranteed low-level margin is unresolved.','qualified':False}
Path('output/startup-margins-v16.json').write_text(json.dumps(r,indent=2));print(r['minimum_on_margin_V'])

# Buffer output bounds are continuous across1.65..5.5V at100uA;
# Schmitt thresholds below are guaranteed only at listed supply test points.
points=[]
for supply,vplus,vminus in [(3,1.92,.89),(4.5,2.74,1.51)]:
 vin=(supply/10100-6e-6)/(1/10100+1/99000)
 points.append({'supply_V':supply,'input_high_min_V':vin,'high_margin_V':vin-vplus,'low_margin_V':vminus-.4})
assert all(x['high_margin_V']>0 and x['low_margin_V']>0 for x in points)
r['buffered_candidate']={'test_points':points,'converter_low_margin_V':.4-.1,'load_bound_uA':4.4/99000*1e6+.2,'continuous_supply_threshold_guarantee_confirmed':False,'rail_ramp_validated':False}
Path('output/startup-margins-v16.json').write_text(json.dumps(r,indent=2))
