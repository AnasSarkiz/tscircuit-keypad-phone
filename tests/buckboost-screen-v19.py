"""TPS63802 requirements screening. No guaranteed efficiency/frequency or hardware approval."""
from pathlib import Path
import itertools,json
rows=[]
for vin,eta,L in itertools.product([2.5,2.7,3.0,3.2],[.75,.85,.9],[.37e-6,.47e-6]):
 vout=3.8;load=2;avg=vout*load/(eta*vin);duty=1-vin*eta/vout;room=4-avg
 fmin=vin*duty/(L*2*room) if room>0 else None
 if fmin:
  peak=avg+vin*duty/(L*fmin)/2
  assert abs(peak-4)<1e-10
  assert avg+vin*duty/(L*(fmin*.99))/2>4
 rows.append(dict(VIN=vin,assumed_efficiency=eta,L_effective_H=L,input_average_A=avg,peak_ripple_room_A=room,required_min_frequency_Hz=fmin,criterion='strictly above threshold frequency; boost CCM model only'))
volts=[]
for fb,top,bot,ibias in itertools.product([.495,.505],[66000*.999,66000*1.001],[10000*.999,10000*1.001],[-100e-9,100e-9]):
 volts.append(fb*(1+top/bot)+ibias*top)
assert min(volts)>3.7 and max(volts)<3.9
assert any(x['required_min_frequency_Hz'] is None for x in rows)
r={'source':'https://www.ti.com/lit/ds/symlink/tps63802.pdf','datasheet':'SLVSEU9D RevD','guaranteed_boost_peak_limit_min_A':4,'limit_condition':'VIN>=2.5V; other recommended conditions apply','cases':rows,'feedback_proposal':{'top_ohm':66000,'bottom_ohm':10000,'tolerance':.001,'PWM_reference_tolerance':.01,'bias_allocated_plus_minus_A':100e-9,'static_min_V':min(volts),'static_max_V':max(volts),'MPNs_assigned':False},'open':['switching frequency minimum absent; listed frequencies typical only','efficiency is assumed, not guaranteed','buck and transition-mode limits not bounded here','inductor saturation/ripple/thermal qualification','output capacitor effective value and transient response','battery/charger/protection current and voltage corners','fault OVP for modem','startup and control sequencing'],'fabrication_ready':False}
Path('output/buckboost-screen-v19.json').write_text(json.dumps(r,indent=2));print('PASS 24 converter-ripple requirement cases and16 feedback corners; candidate not approved')
