import React from 'react'
import {Circuit} from '@tscircuit/core'
import {DDC0006A} from '../electronics/footprints'
import {convertCircuitJsonToPcbSvg} from 'circuit-to-svg'
import fs from 'node:fs'
import assert from 'node:assert/strict'
const c=new Circuit();c.add(<board width={10} height={10} routingDisabled><chip name="U_DDC_AUDIT" pinLabels={{pin1:'SW',pin2:'GND',pin3:'EN',pin4:'FB',pin5:'VOUT',pin6:'VBAT'}} footprint={<DDC0006A/>}/></board>);await c.renderUntilSettled();const j:any[]=c.getCircuitJson()
const pads=j.filter(x=>x.type==='pcb_smtpad');assert.equal(pads.length,6)
const expected=[[-1.35,.95],[-1.35,0],[-1.35,-.95],[1.35,-.95],[1.35,0],[1.35,.95]]
for(const [i,[x,y]] of expected.entries()){
 const sp=j.find(q=>q.type==='source_port'&&q.pin_number===i+1)
 const pp=j.find(q=>q.type==='pcb_port'&&q.source_port_id===sp.source_port_id)
 const p=pads.find(q=>q.pcb_port_id===pp.pcb_port_id);assert.ok(p)
 assert.ok(Math.abs(p.x-x)<1e-6&&Math.abs(p.y-y)<1e-6,`pin${i+1}`);assert.equal(p.width,1.1);assert.equal(p.height,.6)
}
const errs=j.filter(x=>/error$/.test(x.type));assert.deepEqual(errs,[])
fs.writeFileSync('output/ddc-footprint-audit.svg',convertCircuitJsonToPcbSvg(j))
fs.writeFileSync('output/ddc-footprint-checks.json',JSON.stringify({pads:6,dimensions:'1.1 x 0.6 mm, 2.7 mm row spacing, .95 mm pitch',pinMapping:'passed emitted-source-port to pad-center checks',limitations:'top side unrotated only; rectangle approximation; not assembler-approved'},null,2))
console.log('DDC land-pattern pad dimensions and pin orientation passed.')
