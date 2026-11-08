import React from 'react'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import {Circuit} from '@tscircuit/core'
import {ModemLandCandidate} from '../electronics/modem-footprint'
import {modemPins} from '../electronics/modem-support'
import data from '../sourcing/modem-pad-transcription-v19.json'
import {convertCircuitJsonToPcbSvg} from 'circuit-to-svg'
const c=new Circuit();c.add(<board width={33} height={37} routingDisabled><chip name="U_PAD_AUDIT" pinLabels={Object.fromEntries(Object.entries(modemPins).map(([p,l])=>['pin'+p,l]))} footprint={<ModemLandCandidate/>}/></board>);await c.renderUntilSettled();const j:any[]=c.getCircuitJson();const pads=j.filter(x=>x.type==='pcb_smtpad');assert.equal(pads.length,126);assert.equal(new Set(data.pads.map(p=>p.pin)).size,126)
for(const d of data.pads){const sp=j.find(p=>p.type==='source_port'&&p.pin_number===d.pin);assert(sp);const pp=j.find(p=>p.type==='pcb_port'&&p.source_port_id===sp.source_port_id);const pad=pads.find(p=>p.pcb_port_id===pp.pcb_port_id);assert.equal(pad.x,d.x);assert.equal(pad.y,-d.y_down);assert.equal(pad.width,d.width);assert.equal(pad.height,d.height);assert(Math.abs(pad.x)+pad.width/2<=12.5);assert(Math.abs(pad.y)+pad.height/2<=14.5)}
// Independently keyed asymmetric anchors detect Y inversion and perimeter order mistakes.
for(const [pin,x,y] of [[1,-9.175,9.7],[18,-9.175,-9.6],[19,-7.45,-11.025],[31,7.15,-11.025],[49,9.175,9.7],[50,7.15,11.025],[62,-7.45,11.025],[119,-.85,2.55],[126,.85,2.55],[122,-.85,-2.55]]){const d=data.pads.find(p=>p.pin===pin)!;assert.equal(d.x,x);assert.equal(-d.y_down,y)}
for(let i=0;i<pads.length;i++)for(let k=i+1;k<pads.length;k++)assert(Math.abs(pads[i].x-pads[k].x)>=(pads[i].width+pads[k].width)/2||Math.abs(pads[i].y-pads[k].y)>=(pads[i].height+pads[k].height)/2,'copper overlap')
assert.deepEqual(j.filter(x=>/error$/.test(x.type)),[])
fs.writeFileSync('output/modem-footprint-v19.circuit.json',JSON.stringify(j,null,2));fs.writeFileSync('output/modem-footprint-v19.svg',convertCircuitJsonToPcbSvg(j));console.log('PASS 126-pad transcription, polarity conversion, anchors, body bounds and pairwise overlap; V1.0 overlay received; variant/process release still blocked')
