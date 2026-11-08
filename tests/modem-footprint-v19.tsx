import React from 'react'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import { Circuit } from '@tscircuit/core'
import { ModemLandCandidate } from '../electronics/modem-footprint'
import { modemPins } from '../electronics/modem-support'
// Historical export name retained. Geometry now comes from exact C7472750.
// These independent asymmetric manufacturer anchors allow <=0.05 mm catalog deviation.
const circuit = new Circuit()
circuit.add(<board width={33} height={37} routingDisabled><chip name="U_PAD_AUDIT" pinLabels={Object.fromEntries(Object.entries(modemPins).map(([p,l])=>['pin'+p,l]))} footprint={<ModemLandCandidate/>}/></board>)
await circuit.renderUntilSettled()
const json: any[] = circuit.getCircuitJson(), pads = json.filter(x=>x.type==='pcb_smtpad')
assert.equal(pads.length,126)
assert.equal(new Set(pads.map(p=>p.port_hints[0])).size,126)
const anchors = [[1,-9.175,9.7],[18,-9.175,-9.6],[19,-7.45,-11.025],[31,7.15,-11.025],[49,9.175,9.7],[50,7.15,11.025],[62,-7.45,11.025],[119,-.85,2.55],[126,.85,2.55],[122,-.85,-2.55]]
for (const [pin,x,y] of anchors) {
  const pad=pads.find(p=>p.port_hints.includes(`pin${pin}`)); assert(pad)
  assert(Math.abs(pad.x-x)<.05 && Math.abs(pad.y-y)<.05, `manufacturer anchor ${pin}`)
}
for(const p of pads){assert(p.pcb_port_id);assert(Math.abs(p.x)+p.width/2<=12.5);assert(Math.abs(p.y)+p.height/2<=14.5)}
for(let i=0;i<pads.length;i++)for(let k=i+1;k<pads.length;k++)assert(Math.abs(pads[i].x-pads[k].x)>=(pads[i].width+pads[k].width)/2||Math.abs(pads[i].y-pads[k].y)>=(pads[i].height+pads[k].height)/2,'copper overlap')
assert.equal(json.filter(x=>x.type==='pcb_solder_paste').length,0)
assert.deepEqual(json.filter(x=>/error$/.test(x.type)),[])
fs.mkdirSync('output',{recursive:true}); fs.writeFileSync('output/modem-footprint-v19.circuit.json',JSON.stringify(json,null,2))
console.log('PASS migrated modem:126 mapped terminals, independent asymmetric anchors, bounds, no overlaps/paste; no variant or process qualification')
