import React from 'react'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import {Circuit} from '@tscircuit/core'
import {sourcePassives} from '../electronics/sourced-passives'
import {convertCircuitJsonToPcbSvg} from 'circuit-to-svg'
for(const mpn of ['XGL4020-102MEC','XGL4020-222MEC','XFL4015-471MEC']){const c=new Circuit();c.add(sourcePassives(<board width={8} height={8} routingDisabled><inductor name="L_TEST" manufacturerPartNumber={mpn} inductance="1uH"/></board>));await c.renderUntilSettled();const j:any[]=c.getCircuitJson();const pads=j.filter(x=>x.type==='pcb_smtpad');assert.equal(pads.length,2);for(const n of [1,2]){const sp=j.find(x=>x.type==='source_port'&&x.pin_number===n);const pp=j.find(x=>x.type==='pcb_port'&&x.source_port_id===sp.source_port_id);const p=pads.find(x=>x.pcb_port_id===pp.pcb_port_id);assert.equal(p.x,n===1?-1.625:1.625);assert.equal(p.width,1.3);assert.equal(p.height,2.5)}assert.deepEqual(j.filter(x=>/error$/.test(x.type)),[]);fs.writeFileSync(`output/${mpn}-v20.svg`,convertCircuitJsonToPcbSvg(j));fs.writeFileSync(`output/${mpn}-v20.circuit.json`,JSON.stringify(j,null,2))}
console.log('PASS three Coilcraft proposal pad mappings; no manufacturer land/orientation qualification')
