import React from 'react'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import {Circuit} from '@tscircuit/core'
import {Ao3400LandCandidate} from '../electronics/footprints'
import {convertCircuitJsonToPcbSvg} from 'circuit-to-svg'
const c=new Circuit();c.add(<board width={8} height={7} routingDisabled><chip name="Q_AUDIT" pinLabels={{pin1:'G',pin2:'S',pin3:'D'}} footprint={<Ao3400LandCandidate/>}/></board>);await c.renderUntilSettled();const j:any[]=c.getCircuitJson()
assert.equal(j.filter(x=>x.type==='pcb_smtpad').length,3)
for(const [i,[x,y]] of [[-1.2,.95],[-1.2,-.95],[1.2,0]].entries()){
 const sp=j.find(p=>p.type==='source_port'&&p.pin_number===i+1);const pp=j.find(p=>p.type==='pcb_port'&&p.source_port_id===sp.source_port_id);const pad=j.find(p=>p.type==='pcb_smtpad'&&p.pcb_port_id===pp.pcb_port_id);assert.equal(pad.x,x);assert.equal(pad.y,y);assert.equal(pad.width,.8);assert.equal(pad.height,.8)
}
assert.deepEqual(j.filter(x=>/error$/.test(x.type)),[])
fs.writeFileSync('output/ao-footprint-v17.circuit.json',JSON.stringify(j,null,2));fs.writeFileSync('output/ao-footprint-v17.svg',convertCircuitJsonToPcbSvg(j));console.log('PASS AO proposal emitted pad mapping; physical orientation and solder contact unverified')
