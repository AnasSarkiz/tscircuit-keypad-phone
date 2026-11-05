import React from 'react'
import {Circuit} from '@tscircuit/core'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import {CapacitorLandCandidate,capacitorLandGeometry} from '../electronics/footprints'
import {convertCircuitJsonToPcbSvg} from 'circuit-to-svg'
for(const size of ['0603','0805','1210'] as const){
 const c=new Circuit();c.add(<board width={10} height={8} routingDisabled><capacitor name="C_GEOMETRY" capacitance="1uF" footprint={<CapacitorLandCandidate size={size}/>}/></board>);await c.renderUntilSettled()
 const j:any[]=c.getCircuitJson();const pads=j.filter(x=>x.type==='pcb_smtpad');assert.equal(pads.length,2);const g=capacitorLandGeometry[size]
 for(const n of [1,2]){const sp=j.find(p=>p.type==='source_port'&&p.pin_number===n);const pp=j.find(p=>p.type==='pcb_port'&&p.source_port_id===sp.source_port_id);const pad=pads.find(p=>p.pcb_port_id===pp.pcb_port_id);assert.equal(pad.x,(n===1?-1:1)*g.center);assert.equal(pad.y,0);assert.equal(pad.width,g.width);assert.equal(pad.height,g.height)}
 assert.deepEqual(j.filter(x=>/error$/.test(x.type)),[])
 fs.writeFileSync(`output/capacitor-${size}-v14.circuit.json`,JSON.stringify(j,null,2));fs.writeFileSync(`output/capacitor-${size}-v14.svg`,convertCircuitJsonToPcbSvg(j))
}
console.log('PASS three capacitor candidate pad mappings; assembly remains unqualified')
