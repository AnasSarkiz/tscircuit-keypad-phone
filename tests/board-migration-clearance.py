"""Placement-only same-layer pad-copper checks, not a routed-board DRC.

Uses conservative rectangle envelopes and exact orthogonal-polygon cells.
Rejects unsupported geometry instead of silently approximating it.
"""
import json, math
from pathlib import Path
j=json.loads(Path('output/usb-placement-v66.circuit.json').read_text())
source={x['source_component_id']:x for x in j if x['type']=='source_component'}
comp={x['pcb_component_id']:x for x in j if x['type']=='pcb_component'}
ports={x['pcb_port_id']:x for x in j if x['type']=='pcb_port'}
nets={x['source_net_id']:x['name'] for x in j if x['type']=='source_net'}
traces=[x for x in j if x['type']=='source_trace']
def pad_nets(p):
    port=ports.get(p.get('pcb_port_id'))
    assert port,('unmapped pad',p['pcb_smtpad_id'])
    ids={port['source_port_id']}
    for g in source[comp[p['pcb_component_id']]['source_component_id']].get('internally_connected_source_port_ids',[]):
        if port['source_port_id'] in g:ids.update(g)
    return {nets[n] for t in traces if ids.intersection(t['connected_source_port_ids']) for n in t['connected_source_net_ids']}
def inside(x,y,points):
    result=False
    for a,b in zip(points,points[1:]+points[:1]):
        if (a[1]>y)!=(b[1]>y) and x < (b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:result=not result
    return result

def cells(p):
    if p['shape']=='rect':return [(p['x']-p['width']/2,p['y']-p['height']/2,p['x']+p['width']/2,p['y']+p['height']/2)]
    assert p['shape']=='polygon',p['shape']
    points=[(q['x'],q['y']) for q in p['points']]
    assert all(abs(a[0]-b[0])<1e-9 or abs(a[1]-b[1])<1e-9 for a,b in zip(points,points[1:]+points[:1])), 'nonorthogonal polygon unsupported'
    xs=sorted({q[0] for q in points});ys=sorted({q[1] for q in points})
    result=[(a,c,b,d) for a,b in zip(xs,xs[1:]) for c,d in zip(ys,ys[1:]) if inside((a+b)/2,(c+d)/2,points)]
    assert result,'empty polygon';return result

def separation(a,b):
    return math.hypot(max(a[0]-b[2],b[0]-a[2],0),max(a[1]-b[3],b[1]-a[3],0))
def overlap(a,b):return min(a[2],b[2])-max(a[0],b[0])>1e-9 and min(a[3],b[3])-max(a[1],b[1])>1e-9
# Prove we do not fill an L-pad's empty notch with its bounding rectangle.
l={'shape':'polygon','points':[{'x':x,'y':y}for x,y in [(0,0),(2,0),(2,1),(1,1),(1,2),(0,2)]]}
assert abs(sum((b-a)*(d-c)for a,c,b,d in cells(l))-3)<1e-9
assert not any(overlap(c,(1.1,1.1,1.9,1.9))for c in cells(l))
pads=[x for x in j if x['type']=='pcb_smtpad'];geometry=[cells(p)for p in pads];pn=[pad_nets(p)for p in pads]
assert all(len(ns)<=1 for ns in pn),'conflicting net assignments'
for p,cs in zip(pads,geometry):
    for a,c,b,d in cs:assert a>=-28 and b<=28 and c>=-84 and d<=60,('pad outside board',p['pcb_smtpad_id'])
shorts=[];minimum=None
for i,p in enumerate(pads):
    for k in range(i+1,len(pads)):
        q=pads[k]
        if p['layer']!=q['layer'] or (pn[i] and pn[i]==pn[k]):continue
        distance=min(separation(a,b)for a in geometry[i]for b in geometry[k])
        if minimum is None or distance<minimum['mm']:minimum={'mm':distance,'pads':[p['pcb_smtpad_id'],q['pcb_smtpad_id']]}
        if any(overlap(a,b)for a in geometry[i]for b in geometry[k]):
            shorts.append({'pads':[p['pcb_smtpad_id'],q['pcb_smtpad_id']], 'components':[source[comp[z['pcb_component_id']]['source_component_id']]['name']for z in [p,q]],'nets':[sorted(pn[i]),sorted(pn[k])]})
report={'smt_pads':len(pads),'polygons':sum(p['shape']=='polygon'for p in pads),'different_net_overlaps':shorts,'minimum_different_net_pad_spacing':minimum,'scope':'SMT pad copper and rectangular board bounds only; no traces, vias, holes, solder mask, body/courtyard or routed-board DRC'}
Path('output/board-migration-clearance.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2));assert not shorts,'different-net pad overlaps'
assert minimum and minimum['mm']>1e-6,'different-net pad copper touching'
