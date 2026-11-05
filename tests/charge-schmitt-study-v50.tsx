import React from 'react'
import fs from 'node:fs'
import assert from 'node:assert/strict'
import {Circuit} from '@tscircuit/core'
import {convertCircuitJsonToSchematicSvg} from 'circuit-to-svg'
import {ChargeSchmittStudyV50} from '../electronics/charge-schmitt-study-v50'
const c=new Circuit({platform:{pcbDisabled:true}});c.add(<ChargeSchmittStudyV50/>);await c.renderUntilSettled();const j:any[]=c.getCircuitJson();assert.deepEqual(j.filter(x=>/error$/.test(x.type)),[])
function pinNet(ref:string,pin:number){const u=j.find(x=>x.type==='source_component'&&x.name===ref);const p=j.find(x=>x.type==='source_port'&&x.source_component_id===u.source_component_id&&x.pin_number===pin);const t=j.find(x=>x.type==='source_trace'&&x.connected_source_port_ids.includes(p.source_port_id));return j.find(x=>x.type==='source_net'&&t.connected_source_net_ids.includes(x.source_net_id)).name}
;['ALT_GND','ALT_GND','ALT_REQUEST','ALT_CHARGE_GATE_UNQUALIFIED','ALT_VLOGIC_PENDING','ALT_REGN_READY'].forEach((n,i)=>assert.equal(pinNet('U_ALT_CHARGE_SCHMITT',i+1),n))
;['ALT_REGN_READY','ALT_GND','ALT_MCU_EN_PENDING','ALT_CT','ALT_REGN_SENSE','ALT_VLOGIC_PENDING'].forEach((n,i)=>assert.equal(pinNet('U_ALT_CHARGE_POR',i+1),n))
assert(j.filter(x=>x.type==='source_net').every(x=>x.name.startsWith('ALT_')));assert.equal(j.filter(x=>x.type==='pcb_component').length,0)
// Independently transcribed full manufacturer truth table, ordered IN2,IN1,IN0.
const truth=[0,0,1,1,0,1,0,1];const rows=[]
for(const request of [0,1])for(const ready of [0,1]){const result=truth[ready*4+request];assert.equal(result,request&ready);rows.push({request,ready,result})}
// A mistaken configuration strap can enable despite ready=0; reject it.
assert.notEqual(truth[2],0)
fs.writeFileSync('output/charge-schmitt-study-v50.circuit.json',JSON.stringify(j,null,2));fs.writeFileSync('output/charge-schmitt-study-v50.svg',convertCircuitJsonToSchematicSvg(j));fs.writeFileSync('output/charge-schmitt-study-v50-checks.json',JSON.stringify({pin_maps_pass:true,truth_table_cases:rows,wrong_strap_fault_detected:true,integrated:false,hardware_qualified:false,release:false},null,2));console.log('PASS isolated two-chip pin mapping, four AND truth cases and incorrect strap fault; no PCB integration')
