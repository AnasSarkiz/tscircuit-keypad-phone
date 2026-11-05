"""Conditional DC screens and physical-net regression; not a MOSFET-off guarantee."""
import json
from pathlib import Path
j=json.load(open('output/usb-placement-v37.circuit.json'));checks=json.load(open('output/usb-layered-v37-checks.json'));comps={x['name']:x for x in j if x['type']=='source_component'}
for s in ['KEY','RESET']:
 assert comps[f'R_MODEM_{s}_INPUT_OFF']['resistance']==10000
 assert comps[f'R_MODEM_{s}_GATE_OFF']['resistance']==39000
 assert comps[f'R_MODEM_{s}_GATE_OFF']['manufacturer_part_number']=='RC0603FR-0739KL'
 assert f'Q_MODEM_{s}' not in comps
 for n in [('ON_OFF_MCU' if s=='KEY' else 'RESET_MCU'),f'MODEM_{s}_GATE']:
  assert len(checks['placed_net_islands'][n])==1,n
# -40..125C screen: maximum100C displacement from25C. New RC tolerance1%, TCR100ppm/C.
old_rmax=100000*1.001*1.0025
new_input_rmax=10000*1.01*1.01
gate_min=39000*.99*.99;gate_max=39000*1.01*1.01
old_input=2*5e-6*old_rmax;new_input=2*5e-6*new_input_rmax
assert old_input>.8 and new_input<.8
extra_input_budget=.8/new_input_rmax-10e-6
# Gate external leakage is an engineering allocation, not verified MOSFET data.
gate_leak_allocation=1e-6
on_load=3.3/gate_min+gate_leak_allocation
off_screen=(10e-6+gate_leak_allocation)*gate_max
assert on_load<100e-6 and off_screen<.5
assert (10e-6+gate_leak_allocation)*old_rmax>.5
out={'source':'https://www.ti.com/lit/ds/symlink/sn74lvc1g08.pdf RevAA electrical table p6','rail_screen_V':[3.0,3.3],'input_leakage_per_gate_A':5e-6,'Ioff_at_VCC0_A':10e-6,'old_tied_input_voltage_screen_V':old_input,'new_tied_input_voltage_screen_V':new_input,'additional_host_leakage_budget_A':extra_input_budget,'gate_external_leakage_allocation_A_NOT_verified':gate_leak_allocation,'new_gate_on_load_screen_A':on_load,'VOH_min_V_at_3V_125C_100uA':3-.15,'new_VCC0_gate_voltage_screen_V':off_screen,'off_screen_target_V_NOT_device_spec':.5,'limits':['II is specified atVI=0 or5.5V; intermediate/ramp behavior not qualified','Ioff applies atVCC=0, not arbitrary brownout voltage','MOSFET off drain leakage at positive gate voltage not guaranteed by threshold','GPIO leakage, dynamic gate charging and power sequencing unqualified','MOSFET footprint and physical orientation not accepted','SN74LVC1G08 input transition limit10ns/V at3.0..3.6V not established during GPIO release; Schmitt alternative requires redesign'],'hardware_qualified':False}
Path('output/modem-control-v37.json').write_text(json.dumps(out,indent=2));print('PASS old100k defaults fail conditional screens;10k input/39k gate satisfy stated budgets; MOSFET and ramp gates remain')
