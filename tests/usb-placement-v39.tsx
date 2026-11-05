import React from 'react'
import fs from 'node:fs'
import assert from 'node:assert/strict'
import {Circuit} from '@tscircuit/core'
import {convertCircuitJsonToPcbSvg} from 'circuit-to-svg'
import {UsbPlacementV39,placementV39} from '../electronics/usb-placement-v39'
const c=new Circuit();c.schematicDisabled=true;c.add(<UsbPlacementV39/>);await c.renderUntilSettled();const j:any[]=c.getCircuitJson()
assert.equal(j.filter(x=>x.type==='source_component').length,66)
for(const [name,a]of Object.entries(placementV39)){const s=j.find(x=>x.type==='source_component'&&x.name===name),p=j.find(x=>x.type==='pcb_component'&&x.source_component_id===s.source_component_id);assert(Math.abs(p.center.x-a.x)<1e-8);assert(Math.abs(p.center.y-a.y)<1e-8)}
assert.equal(j.filter(x=>x.type==='pcb_solder_paste').length,0);assert.deepEqual(j.filter(x=>/error$/.test(x.type)),[])
fs.writeFileSync('output/usb-placement-v39.circuit.json',JSON.stringify(j,null,2));fs.writeFileSync('output/usb-placement-v39.svg',convertCircuitJsonToPcbSvg(j));console.log('PASS 66 mapped components; no paste; routing performed separately from explicit route manifest')
