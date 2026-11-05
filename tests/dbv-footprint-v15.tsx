import React from 'react'
import {Circuit} from '@tscircuit/core'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import {TiDbvCandidate} from '../electronics/footprints'
import {convertCircuitJsonToPcbSvg} from 'circuit-to-svg'
for(const pins of [5,6] as const){
 const c=new Circuit();c.add(<board width={10} height={8} routingDisabled><chip name="U_GEOMETRY" pinLabels={Object.fromEntries(Array.from({length:pins},(_,i)=>[`pin${i+1}`,`P${i+1}`]))} footprint={<TiDbvCandidate pins={pins}/>}/></board>);await c.renderUntilSettled()
 const j:any[]=c.getCircuitJson();const pads=j.filter(x=>x.type==='pcb_smtpad');assert.equal(pads.length,pins)
 const expected=pins===5?[[-1.3,.95],[-1.3,0],[-1.3,-.95],[1.3,-.95],[1.3,.95]]:[[-1.3,.95],[-1.3,0],[-1.3,-.95],[1.3,-.95],[1.3,0],[1.3,.95]]
 for(const [i,[x,y]] of expected.entries()){const sp=j.find(p=>p.type==='source_port'&&p.pin_number===i+1);const pp=j.find(p=>p.type==='pcb_port'&&p.source_port_id===sp.source_port_id);const pad=pads.find(p=>p.pcb_port_id===pp.pcb_port_id);assert.equal(pad.x,x);assert.equal(pad.y,y);assert.equal(pad.width,1.1);assert.equal(pad.height,.6)}
 assert.deepEqual(j.filter(x=>/error$/.test(x.type)),[])
 fs.writeFileSync(`output/dbv${pins}-v15.circuit.json`,JSON.stringify(j,null,2));fs.writeFileSync(`output/dbv${pins}-v15.svg`,convertCircuitJsonToPcbSvg(j))
}
console.log('PASS DBV5/6 emitted pad mapping; visual manufacturer orientation audit remains open')
