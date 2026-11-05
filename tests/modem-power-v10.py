"""Sensitivity only: per-rail capability requirements are NOT measured simultaneous current."""
import json
from pathlib import Path
led=((3.16-.05)/117)**(-1/.978)/1000
rows=[]
for v in [3.3,3.5,3.8]:
 for im in [2,2.5,3,3.5]:
  total=3.816*im/(v*.9)+3.15*.6/(v*.85)+(5*2*led+5*.006)/(v*.8)
  rows.append(dict(loaded_cell_V=v,assumed_modem_A=im,pack_A=total,margin_to_PCM_min_A=4-total,within_4A_buck_rating=im<=4))
assert all(r['margin_to_PCM_min_A']<0 for r in rows if r['assumed_modem_A']==3.5)
assert any(r['margin_to_PCM_min_A']<0 for r in rows if r['assumed_modem_A']==2.5)
out={'status':'Superseded sensitivity: QuecOpen V1.0 section3.5.2 explicitly specifies total supply capability >=2A LTE-only and >=3A GSM. Separate rail capabilities are not additive consumption.','rows':rows,'decision':'At hypothetical simultaneous 3.5A modem demand the flat pack branch fails; TPS62827A is a 4A part (V10 text erroneously called it 3A). Even 2.5A has insufficient PCM margin at low cell voltage. Resolve exact SKU demand, dropout and pulse traces before connecting supply.','limits':'Same assumed efficiencies as V4. No cell impedance, temperature, aging, transient or converter thermal model. Low cell rows do not imply buck regulation at 3.816V.'}
Path('output/modem-power-v10.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
