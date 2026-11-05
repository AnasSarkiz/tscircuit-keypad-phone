import json,math
from pathlib import Path
j=json.loads(Path('output/power-integrated.circuit.json').read_text());parts={c['name']:c for c in j if c['type']=='source_component'}
expected={'R_MIC_BIAS_TOP':('resistance',510,'RC0603FR-07510RL'),'R_MIC_BIAS_BOTTOM':('resistance',510,'RC0603FR-07510RL'),'R_MIC_BIAS_P':('resistance',1500,'RC0603FR-071K5L'),'R_MIC_BIAS_N':('resistance',1500,'RC0603FR-071K5L'),'R_MIC_P_SERIES':('resistance',1000,'RC0603FR-071KL'),'R_MIC_N_SERIES':('resistance',1000,'RC0603FR-071KL'),'C_MIC_BIAS':('capacitance',2.2e-6,'C0805C225K5RACTU'),'C_MIC_P_AC':('capacitance',100e-9,'C0603C104K5RACTU'),'C_MIC_N_AC':('capacitance',100e-9,'C0603C104K5RACTU')}
for name,(field,value,mpn) in expected.items():
 assert math.isclose(parts[name][field],value,rel_tol=1e-9),(name,field)
 assert parts[name]['manufacturer_part_number']==mpn,name
print('PASS nine audio nominal values and sourcing assignments; electrical qualification open')
