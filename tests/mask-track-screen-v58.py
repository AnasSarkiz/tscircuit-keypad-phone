import json
from pathlib import Path
from shapely.geometry import shape
j=json.load(open('output/usb-placement-v58.circuit.json'));ids={x[x['type']+'_id']:x for x in j if x['type']+'_id' in x};nets={}
for p in j:
 if p['type']!='pcb_smtpad':continue
 port=ids[p['pcb_port_id']]['source_port_id'];ns={ids[n]['name'] for t in j if t['type']=='source_trace' and port in t.get('connected_source_port_ids',[]) for n in t.get('connected_source_net_ids',[])}
 nets[p['pcb_smtpad_id']]=next(iter(ns)) if ns else 'NC_'+p['pcb_smtpad_id']
nets.update({v['name']:v['net'] for v in json.load(open('routing/usb-layered-v58.json'))['vias']});nets['KEYPAD_RESERVED']='KEYPAD_RESERVED'
tracks=[(t,shape(t['geometry'])) for t in json.load(open('output/usb-layered-v58-geometry.json')) if t['kind']=='trace' and t['layer'] in ['top','bottom']]
minimum=100;viol=[]
for o in json.load(open('output/solder-mask-proposal-v58.json'))['openings']:
 g=shape(o['geometry'])
 for t,tg in tracks:
  if t['layer']!=o['layer'] or t['net']==nets[o['name']]:continue
  d=g.distance(tg);minimum=min(minimum,d)
  if d<.09-1e-8:viol.append([o['name'],t['name'],d])
out={'minimum_opening_to_foreign_surface_trace_mm':minimum,'limit_mm':.09,'violations':viol,'scope':'Foreign nets only; same-net trace exits intentionally intersect their own opening','source':'https://jlcpcb.com/capabilities/pcb-capabilities','factory_approved':False,'release':False}
Path('output/mask-track-screen-v58.json').write_text(json.dumps(out,indent=2));print(out);assert not viol
