"""Conditional screens only: preserve unsupported states instead of interpolating guarantees."""
import json
from pathlib import Path
rmin=10000*.99*.99;rmax=10000*1.01*1.01
rows=[]
for rail in [0,.5,1.5,1.65,2.3,2.99,3.0,3.15,3.3,3.6]:
 buffer_operating=1.65<=rail<=5.5;mcu_operating=3<=rail<=3.6
 rows.append({'rail_V':rail,'buffer_recommended_supply':buffer_operating,'MCU_recommended_supply':mcu_operating,'full_driver_qualified':False,'reason':'VCC0 Ioff is not a positive-gate MOSFET-off guarantee' if rail==0 else 'Buffer outside operating range' if not buffer_operating else 'MCU outside operating range' if not mcu_operating else 'Loaded GPIO, threshold envelope and sequencing evidence incomplete','input_pulldown_current_upper_A':rail/rmin})
assert all(not r['full_driver_qualified'] for r in rows)
# Espressif50nA powered input leakage + TI5uA test-endpoint leakage: conditional, not reset/brownout proof.
leak_voltage=(5e-6+50e-9)*rmax
assert leak_voltage<.89
# At3V only, high-Z MCU output figures would give positive margins; actual10k load invalidates claiming them directly.
high_z_only={'rail_V':3,'hypothetical_high_margin_V':.8*3-1.92,'hypothetical_low_margin_V':.89-.1*3,'applicable_to_loaded_driver':False}
assert high_z_only['hypothetical_high_margin_V']>0 and high_z_only['hypothetical_low_margin_V']>0
# Typical630pF MOSFET Ciss is12.6 times the buffer's50pF timing load, not a guaranteed worst-case capacitance.
out={'states':rows,'powered_leakage_only_voltage_V':leak_voltage,'high_z_only':high_z_only,'typical_gate_C_to_50pF_ratio':630/50,'input_current_upper_at_3_3V_A':3.3/rmin,'qualification':False,'sources':['https://www.ti.com/lit/ds/symlink/sn74lvc1g17.pdf','https://documentation.espressif.com/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf','https://www.aosmd.com/res/data_sheets/AO3400A.pdf']}
Path('output/schmitt-envelope-v41.json').write_text(json.dumps(out,indent=2));print('PASS state envelope keeps brownout, loaded GPIO and gate-capacitance assumptions unqualified')
