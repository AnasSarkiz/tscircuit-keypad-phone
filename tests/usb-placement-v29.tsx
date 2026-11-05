import React from 'react'
import fs from 'node:fs'
import assert from 'node:assert/strict'
import {Circuit} from '@tscircuit/core'
import {convertCircuitJsonToPcbSvg} from 'circuit-to-svg'
import {UsbPlacementV29,placementV29} from '../electronics/usb-placement-v29'
const c=new Circuit();c.add(<UsbPlacementV29/>);await c.renderUntilSettled();const j:any[]=c.getCircuitJson()
assert.equal(j.filter(x=>x.type==='source_component').length,10)
for(const [name,a]of Object.entries(placementV29)){const s=j.find(x=>x.type==='source_component'&&x.name===name),p=j.find(x=>x.type==='pcb_component'&&x.source_component_id===s.source_component_id);assert.equal(p.center.x,a.x);assert.equal(p.center.y,a.y)}
assert.equal(j.filter(x=>x.type==='pcb_solder_paste').length,0);assert.deepEqual(j.filter(x=>/error$/.test(x.type)),[])
fs.writeFileSync('output/usb-placement-v29.circuit.json',JSON.stringify(j,null,2));fs.writeFileSync('output/usb-placement-v29.svg',convertCircuitJsonToPcbSvg(j));console.log('PASS ten mapped components; no paste; routing performed separately from explicit route manifest')
