import json,math
from pathlib import Path
old=json.loads(Path('output/host-budget-v24.json').read_text());rows=[r for r in old['scenarios'] if r['logic_allocation_A']==.1];failed=[]
for r in rows:
 if r['conditional_pass']:continue
 p=r['power_W'];voc=r['OCV_V'];required_v=max(3.2,p/3.6);rmax=required_v*(voc-required_v)/p
 failed.append({**r,'voltage_failure':r['SYS_V']<3.2,'current_failure':r['pack_A']>3.6,'maximum_shared_resistance_ohm':rmax,'resistance_reduction_required_ohm':r['assumed_shared_R_ohm']-rmax})
assert len(failed)==10 and all(r['voltage_failure'] for r in failed) and sum(r['current_failure'] for r in failed)==1
assert all(r['assumed_shared_R_ohm']==.2 for r in failed)
worst=max(rows,key=lambda x:x['power_W']);p=worst['power_W'];voc=3.6
rmax=3.2*(voc-3.2)/p
# No efficiency increase can preserve 3.2V at 0.2ohm and3.6OCV: 6.4W at SYS boundary is less than modem output alone.
assert 3.2*(3.6-3.2)/.2<7.6
swaps=[]
for name,new in [('BQ25895RTWR',.019),('BQ25628RYKR',.025)]:
 # Pure sensitivity substitution: assumes the old30mohm was actually included in200mohm aggregate.
 r=.2-.030+new;v=(voc+math.sqrt(voc*voc-4*r*p))/2
 swaps.append(dict(candidate=name,assumed_old_BATFET_ohm=.030,new_table_max_BATFET_ohm=new,resulting_shared_R_ohm=r,SYS_V=v,pack_A=p/v,passes=bool(v>=3.2 and p/v<=3.6)))
assert not any(x['passes'] for x in swaps)
# An explicit acceptance allocation, not guaranteed component parameters.
allocation={'cell_and_PCM':.050,'two_mated_power_contacts':.020,'leads_and_crimps':.010,'BQ25616_BATFET_table_max':.030,'PCB_and_vias':.005}
r=sum(allocation.values());assert r<rmax
v=(voc+math.sqrt(voc*voc-4*r*p))/2
env_r=r+.040
env_v=(voc+math.sqrt(voc*voc-4*env_r*p))/2
assert env_v<3.2
out={'microfit_environment_screen':{'initial_plus_environment_contact_pair_ohm':.060,'total_with_50mohm_cell_PCM_assumption':env_r,'SYS_V':env_v,'passes':False},'failed_cases':failed,'worst_case_Rmax_ohm':rmax,'cannot_fix_with_efficiency_alone':True,'charger_sensitivity':swaps,'acceptance_allocation_ohm_NOT_qualified':allocation,'allocation_total_ohm':r,'conditional_worst_SYS_V':v,'conditional_worst_pack_A':p/v,'acceptance_scope':'Required load-dependent DC/pulse bounds over agreed SOC/temperature/age. Not 1kHz impedance or a vendor typical. User operating temperature, lifespan and SOC floor remain unspecified. 3.6V OCV floor is sensitivity assumption, not full usable pack discharge envelope.','unknowns':['cell/PCM combined DC and pulse impedance','connector environmental contact bounds and crimp','converter efficiency/minimum switching frequency/inductance','peak/load-step and source-sharing dynamics','physical temperature and aging envelope','LTE-only persistence and carrier acceptance'],'approved':False}
Path('output/power-root-causes-v25.json').write_text(json.dumps(out,indent=2));print('PASS ten failures classified; worst Rmax',rmax,'allocation result',v,p/v,'charger swaps fail')
