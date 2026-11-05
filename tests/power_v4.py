"""Conservative power scenarios, not simulation or measured efficiencies."""
import json,itertools
from pathlib import Path
values=[.6*(1+r)*(1+536*(1+t)/(100*(1+b))) for r,t,b in itertools.product([-.01,.01],[-.001,.001],[-.001,.001])]
assert min(values)>3.3 and max(values)<4.3
# 3.16k current is estimated from CAT4104 empirical R(k)=117*I(mA)^-.978 + .05.
led_ma=((3.16-.05)/117)**(-1/.978)
assert 2*led_ma<100
rows=[]
for v in [3.3,3.5,3.8]:
 for mode,im in [('LTE',2),('GSM',3)]:
  # In dropout this overestimates modem output power. Includes conversion losses.
  modem=3.816*im/(v*.90)
  logic=3.15*.6/(v*.85)
  backlight=(5*2*led_ma/1000+5*.006)/(v*.80)
  total=modem+logic+backlight
  rows.append(dict(cell_loaded_V=v,mode=mode,estimated_A=total,under_4p8A_continuous=total<4.8,under_4A_min_PCM_trip=total<4))
assert all(r['under_4A_min_PCM_trip'] for r in rows if r['mode']=='LTE')
assert any(not r['under_4A_min_PCM_trip'] for r in rows if r['mode']=='GSM')
report={'status':'analytical assumptions; efficiency and transient validation required','buck_DC_range_V':[min(values),max(values)],'divider_tolerance':'.1% required','sink_estimate_each_mA':led_ma,'scenarios':rows,'decision':'Flat pack is an LTE-only candidate under this budget; GSM branch fails minimum PCM trip margin. No pulse rating used.','charge_gate':'Pack requires 10..45 C. Existing v3 TS network nominal 0..45 C is INCOMPATIBLE. CE must remain disabled.','warning':'3.3 V battery is a power calculation point, not a valid modem cutoff: buck dropout and harness drop require earlier shutdown.'}
Path('output/power-v4-checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
