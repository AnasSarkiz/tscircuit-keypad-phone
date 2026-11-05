"""Conservative conditional design bounds. Unknown device maxima are never fabricated."""
import itertools,math,json
from pathlib import Path
# TPS62827A FB ±1%, bias max50nA; .1% resistors +25ppm/C over100C.
# No aging bound provided: release must add it. Includes bias with either sign.
ranges=[]
for ref,rt,rb,leak in itertools.product([.594,.606],[536000*.9965,536000*1.0035],[100000*.9965,100000*1.0035],[-50e-9,50e-9]):
 ranges.append(ref*(1+rt/rb)+leak*rt)
vlo,vhi=min(ranges),max(ranges)
assert 3.3<vlo<vhi<4.3
# These are deliberately pessimistic ASSUMPTIONS, not guaranteed efficiency floors.
# Auxiliary load includes max display/backlight scenario and host reserve.
aux=3.3*.6/.80+5.3*.131/.75
rows=[]
for mode,im in [('LTE_only',2),('GSM_enabled',3)]:
 power=vhi*im/.85+aux
 for voc,rshared in itertools.product([4.1,3.8,3.6],[.05,.10,.20]):
  # Shared resistance represents cell+PCM+harness+charger BATFET+copper upstream
  # of SYS. Solve constant-power equation on stable high-voltage branch.
  disc=voc*voc-4*rshared*power
  current=(voc-math.sqrt(disc))/(2*rshared) if disc>=0 else None
  sys=voc-current*rshared if current else None
  # 100mOhm high-side +12mOhm inductor +30mOhm downstream are ALLOCATIONS.
  # TI Rds table gives typical only, so cannot certify these bounds.
  minimum_module=sys-im*(.100+.012+.030)-.100 if sys else None
  rows.append(dict(mode=mode,cell_ocv_V=voc,shared_resistance_ohm=rshared,power_W=power,pack_A=current,SYS_V=sys,conditional_min_modem_V=minimum_module,PCM_4A_margin_A=4-current if current else None,voltage_pass=minimum_module is not None and minimum_module>=3.3,PCM_pass=current is not None and current<4))
# Stored-energy sensitivity: assume local160uF effective,20mOhm total ESR.
# Actual selected caps and loop response must meet the declared bounds.
transients=[]
for step,tus in itertools.product([2,3],[10,20,50]):
 droop=step*.020+step*tus*1e-6/160e-6
 transients.append(dict(step_A=step,unserved_us=tus,droop_V=droop,min_module_V=vlo-.060-droop,passes=vlo-.060-droop>=3.3))
assert any(not r['PCM_pass'] for r in rows if r['mode']=='LTE_only')
assert all(not r['PCM_pass'] for r in rows if r['mode']=='GSM_enabled')
assert any(not r['passes'] for r in transients)
report={'reference':'QuecOpen V1.0 section3.5.2: total capability2A LTE-only/3A GSM; per-rail ratings are not summed consumption. Exact AT SKU applicability unconfirmed.','correction':'TPS62827ADMQR is4A; earlier V10 3A statement was wrong. Minimum switch DC current limit4.8A is not a delivered-current thermal guarantee.','regulated_dc_corner_V':[vlo,vhi],'regulator_FB_bias_max_A':50e-9,'resistor_total_tolerance_assumed':.0035,'power_model':'Vout high corner; efficiencies modem85%,logic80%,backlight75%; auxiliary3.3V*.6A and5.3V*.131A. Efficiency floors and loads unverified.','DC_scenarios':rows,'transient_sensitivity':transients,'hard_rejections':['GSM operation with current Jauch PCM candidate under this conservative budget','Calling the flat pack qualified merely because the nominal2A LTE arithmetic passes','Using the typical26mOhm switch resistance as a guaranteed maximum','Treating100uF capacitor nomination or0.7ohm ESR recommendation alone as a transient guarantee','Using a4.7V standoff TVS as a4.3V overvoltage clamp','Using published10uF output capacitance minimum to prove arbitrary added200uF bulk-loop stability'],'required_evidence':['Exact module variant and persistent LTE-only configuration','Measured load/pulse envelope and brownout cutoff','Battery and PCM resistance/temperature/aging limits','Guaranteed or tested Rds/dropout and inductor temperature behavior','Effective capacitance/ESR and regulator loop response with local bulk','Overshoot and thermal tests; raw-bus and modem-rail protection coordination'],'fabrication_ready':False}
Path('output/power-integrity-v11.json').write_text(json.dumps(report,indent=2));print('DC corner',vlo,vhi,'V;',len(rows),'conditional DC cases;',len(transients),'transient cases; fabrication remains blocked')
