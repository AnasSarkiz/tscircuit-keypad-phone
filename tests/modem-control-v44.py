"""Schmitt pin isolation, conditional DC screens, and old-default regressions."""
import json
from pathlib import Path
j=json.load(open('output/usb-placement-v44.circuit.json'));checks=json.load(open('output/usb-layered-v44-checks.json'));comps={x['name']:x for x in j if x['type']=='source_component'}
for s in ['KEY','RESET']:
 u=comps[f'U_MODEM_{s}_BUF'];assert u['manufacturer_part_number']=='SN74LVC1G17DBVR'
 ports={p['pin_number']:p for p in j if p['type']=='source_port' and p['source_component_id']==u['source_component_id']}
 nc=ports[1]['source_port_id'];a=ports[2]['source_port_id']
 assert all(nc not in t.get('connected_source_port_ids',[]) for t in j if t['type']=='source_trace')
 assert any(a in t.get('connected_source_port_ids',[]) for t in j if t['type']=='source_trace')
 assert comps[f'R_MODEM_{s}_INPUT_OFF']['resistance']==10000
 assert comps[f'R_MODEM_{s}_GATE_OFF']['resistance']==39000
 assert comps[f'Q_MODEM_{s}']['manufacturer_part_number']=='AO3400A'
 for n in [('ON_OFF_MCU' if s=='KEY' else 'RESET_MCU'),f'MODEM_{s}_GATE']:
  assert len(checks['placed_net_islands'][n])==1,n
old_rmax=100000*1.001*1.0025
new_input_rmax=10000*1.01*1.01
gate_min=39000*.99*.99;gate_max=39000*1.01*1.01
old_input=2*5e-6*old_rmax;new_input=5e-6*new_input_rmax
assert old_input>.8 and new_input<.89
on_load=3.3/gate_min+1e-6;off_screen=11e-6*gate_max
assert on_load<100e-6 and off_screen<.5
out={'source':'https://www.ti.com/lit/ds/symlink/sn74lvc1g17.pdf RevY pp3,5,6,11','input':'Schmitt; ordinary CMOS input slew limit removed','pin1':'NC and electrically isolated','threshold_screen_at_VCC_3V_only':{'VTplus_max_V':1.92,'VTminus_min_V':.89,'new_input_leakage_screen_V':new_input},'old_1G08_tied_inputs_100k_screen_V':old_input,'input_leakage_test_A':5e-6,'additional_host_leakage_budget_at_3V_A':.89/new_input_rmax-5e-6,'gate_external_leakage_allocation_A_NOT_verified':1e-6,'gate_on_load_screen_A':on_load,'VOH_min_V_at_3V_100uA_minus40_to85C':2.9,'VCC0_gate_voltage_screen_V':off_screen,'off_screen_target_V_NOT_device_spec':.5,'limits':['Threshold values are the3V table point, not interpolated proof across3.15V regulator tolerance','No claim of full125C DC qualification from text table with ambiguous column extraction','II test endpoints do not bound arbitrary input ramps','Ioff only applies atVCC0; brownout behavior not qualified','Positive gate voltage does not guarantee AO3400A off-state','GPIO loading, rail sequencing and propagation at actual gate capacitance need qualification','MOSFET copper orientation independently reviewed; solder process and electrical validation remain open'],'hardware_qualified':False}
Path('output/modem-control-v44.json').write_text(json.dumps(out,indent=2));print('PASS Schmitt pin1 isolated, input2 routed; conditional DC screens and old default regression; full operating envelope unqualified')
