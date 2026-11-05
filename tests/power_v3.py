"""Independent arithmetic checks. These do not simulate charger or modem transients."""
from pathlib import Path
import json,math,itertools
out=Path(__file__).resolve().parents[1]/'output'
logic_w=.6*3.15
backlight_w=.1*3.4
aux_a=(logic_w+backlight_w)/(3.5*.85)
loads={'LTE':2+aux_a,'GSM':3+aux_a}
assert loads['GSM']<4<5<6
# BQ25616 selected resistor 2.21 kohm +/-1%, datasheet KICHG range.
i_min=639/(2210*1.01);i_nom=677/2210;i_max=715/(2210*.99)
assert .3<=i_nom and i_max<.335
# Distinguish maximum battery voltage from the SYS transient voltage.
vbat_max=4.1*1.004
sys_typ_from_max_battery=vbat_max+.05
headroom=4.3-sys_typ_from_max_battery
assert headroom>0
# 32 ohm receiver, -15% impedance: protect rated 20 mW even at lowest impedance.
r_min=32*.85;v_rated=math.sqrt(.02*r_min);chosen_v=.7
assert chosen_v**2/r_min<.02
report={'scope':'document arithmetic only; no electrical or thermal validation','load_assumptions_A':loads,'5A_protected_18650_current_margin_A':5-loads['GSM'],'5A_rating_temperature_C':[20,40],'6A_wired_21700_current_margin_A':6-loads['GSM'],'charger':'BQ25616RTWR at VSET=10k; NOT BQ25606','charge_current_A':[i_min,i_nom,i_max],'battery_4V1_regulation_max_V':vbat_max,'SYS_estimate_V':sys_typ_from_max_battery,'SYS_estimate_uses_typical_offset_not_guaranteed_bound':True,'modem_headroom_from_estimate_V':headroom,'SYS_OVP_typical_V':4.1+.3,'modem_max_V':4.3,'SYS_OVP_exceeds_modem_max':True,'charge_timer_min_h':8,'charge_3250mAh_ideal_CC_h':3.25/i_nom,'timer_may_expire_before_full_charge':True,'earpiece_impedance_min_ohm':r_min,'earpiece_20mW_voltage_limit_Vrms':v_rated,'proposed_bench_ceiling_Vrms':chosen_v,'ceiling_power_mW':1000*chosen_v**2/r_min,'open_gates':['SYS overshoot with plug/unplug, pack removed, load steps and termination','NTC tolerance guard bands and sensor attachment','USB source qualification before enabling input load','pack PCM pulse response and resistance at low SOC/temperature/aging','cell purchase or quote and matching connector','receiver acoustic exposure and pop transient calibration']}
(out/'power-v3-checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
