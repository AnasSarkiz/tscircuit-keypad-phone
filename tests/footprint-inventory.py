"""Status inventory, not CAD qualification. Keep explicit audited-part allowlists."""
import json,csv,collections
from pathlib import Path
j=json.loads(Path('output/power-integrated.circuit.json').read_text());caps=json.loads(Path('sourcing/capacitor-dimensions-v18.json').read_text());dbv={'TPS70933DBVR':5,'SN74LVC1G02DBVR':5,'SN74LVC1G08DBVR':5,'SN74LVC1G17DBVR':5,'TPS3808G01DBVR':6,'SN74AXC1T45DBVR':6};counts=collections.Counter()
with Path('sourcing/footprint-status-v20.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['reference','MPN','land_pattern_status','release'])
 for c in j:
  if c['type']!='source_component':continue
  m=c.get('manufacturer_part_number','');status='unassigned exact land pattern'
  if m in caps:status='capacitor engineering proposal; dimensional overlap screened'
  elif m in ('TLV9032DR','LTC2954ITS8-1#TRMPBF'):status='dual-row8 text-derived proposal; visual audit pending'
  elif m=='CAT4104V-GT3':status='SOIC8 engineering proposal; not onsemi recommended lands; visual audit pending'
  elif m=='TPD3E001DRLR':status='TI DRL5 text-derived proposal; visual audit pending'
  elif c['name']=='U_MODEM_LOGICAL_ONLY':status='126-pad reviewer transcription; independent visual overlay and variant pending'
  elif m in ('XGL4020-102MEC','XGL4020-222MEC','XFL4015-471MEC'):status='Coilcraft4mm engineering proposal; terminal orientation and positional tolerance unverified'
  elif m=='AO3400A':status='AOS SOT23 engineering proposal; orientation and solder contact unverified'
  elif c['name'] in ('RF_SHUNT_IN_DNP_RESERVE','RF_SHUNT_OUT_DNP_RESERVE'):status='intentional DNP tuning reserve; lands unassigned'
  elif m.startswith(('RT0603','RC0603')):status='resistor engineering proposal; dimensional overlap screened'
  elif m in dbv:status=f'TI DBV{dbv[m]} dimensions transcribed; visual orientation audit pending'
  elif m=='B3F-1050':status='existing B3F fit-study lands; real contact continuity unverified'
  elif c['name']=='U_BL_BOOST':status='TI DDC land dimensions; assembly process unqualified'
  counts[status]+=1;w.writerow([c['name'],m,status,'BLOCKED'])
Path('output/footprint-status-v20.json').write_text(json.dumps(dict(counts),indent=2));print(dict(counts))
