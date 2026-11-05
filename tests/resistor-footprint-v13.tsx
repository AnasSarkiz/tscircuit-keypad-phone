import React from 'react'
import {Circuit} from '@tscircuit/core'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import {convertCircuitJsonToPcbSvg} from 'circuit-to-svg'
import {Yageo0603ResistorCandidate} from '../electronics/footprints'
const c=new Circuit();c.add(<board width={8} height={6} routingDisabled><resistor name="R_GEOMETRY" resistance="100k" manufacturerPartNumber="RT0603BRD07100KL" footprint={<Yageo0603ResistorCandidate/>}/></board>);await c.renderUntilSettled()
const j:any[]=c.getCircuitJson();const pads=j.filter(x=>x.type==='pcb_smtpad');assert.equal(pads.length,2)
for(const [i,x] of [-.85,.85].entries()){
 const sp=j.find(p=>p.type==='source_port'&&p.pin_number===i+1);const pp=j.find(p=>p.type==='pcb_port'&&p.source_port_id===sp.source_port_id);const pad=pads.find(p=>p.pcb_port_id===pp.pcb_port_id)
 assert.equal(pad.x,x);assert.equal(pad.y,0);assert.equal(pad.width,1);assert.equal(pad.height,1.1)
}
assert.deepEqual(j.filter(x=>/error$/.test(x.type)),[])
fs.writeFileSync('output/resistor-footprint-v13.circuit.json',JSON.stringify(j,null,2));fs.writeFileSync('output/resistor-footprint-v13.svg',convertCircuitJsonToPcbSvg(j))
console.log('PASS two-pad candidate emitted geometry/pin mapping; assembly process unqualified')
