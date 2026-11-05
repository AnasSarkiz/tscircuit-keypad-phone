import React from 'react'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import {Circuit} from '@tscircuit/core'
import {convertCircuitJsonToSchematicSvg} from 'circuit-to-svg'
import {ModemIsolationStudyV47} from '../electronics/modem-isolation-study-v47'
const c=new Circuit({platform:{pcbDisabled:true}});c.add(<ModemIsolationStudyV47/>);await c.renderUntilSettled();const j:any[]=c.getCircuitJson();assert.deepEqual(j.filter(x=>/error$/.test(x.type)),[])
const u=j.find(x=>x.type==='source_component'&&x.name==='U_ALT_SWITCH');const pinNet=(pin:number)=>{const p=j.find(x=>x.type==='source_port'&&x.source_component_id===u.source_component_id&&x.pin_number===pin);const t=j.find(x=>x.type==='source_trace'&&x.connected_source_port_ids.includes(p.source_port_id));return j.find(x=>x.type==='source_net'&&t.connected_source_net_ids.includes(x.source_net_id)).name}
const want=['ALT_KEY_CMD','ALT_MODEM_KEY','ALT_KEY_MID','ALT_GUARD_VALID','ALT_KEY_MID','ALT_GND','ALT_GND','ALT_RESET_MID','ALT_MODEM_RESET','ALT_RESET_CMD','ALT_GND','ALT_RESET_MID','ALT_GUARD_VALID','ALT_RETAINED_MODEM_SUPPLY_PENDING'];want.forEach((n,i)=>assert.equal(pinNet(i+1),n));assert(j.filter(x=>x.type==='source_net').every(n=>n.name.startsWith('ALT_')))
function connected(a:string,b:string,edges:string[][]){const seen=new Set([a]);for(let i=0;i<20;i++)for(const [x,y]of edges){if(seen.has(x))seen.add(y);if(seen.has(y))seen.add(x)}return seen.has(b)}
const rows:any[]=[]
for(const key of [false,true])for(const reset of [false,true])for(const valid of [false,true]){
 const enabled=[key,valid,reset,valid],pairs=[[2,3],[5,6],[9,8],[12,11]];const edges=pairs.filter((_,i)=>enabled[i]).map(p=>p.map(pinNet));const k=connected('ALT_MODEM_KEY','ALT_GND',edges),r=connected('ALT_MODEM_RESET','ALT_GND',edges);assert.equal(k,key&&valid);assert.equal(r,reset&&valid);rows.push({key,reset,valid,key_ground_path:k,reset_ground_path:r})
}
assert.throws(()=>assert.equal(connected('ALT_MODEM_KEY','ALT_GND',[['ALT_MODEM_KEY','ALT_KEY_MID'],['ALT_KEY_MID','ALT_GND']]),false),'bypassing guard must fail isolation assertion')
const supervisor=j.find(x=>x.type==='source_component'&&x.name==='U_ALT_SUPERVISOR');
const netAt=(name:string,pin:number)=>{const component=j.find(x=>x.type==='source_component'&&x.name===name);const port=j.find(x=>x.type==='source_port'&&x.source_component_id===component.source_component_id&&x.pin_number===pin);const trace=j.find(x=>x.type==='source_trace'&&x.connected_source_port_ids.includes(port.source_port_id));return j.find(x=>x.type==='source_net'&&trace.connected_source_net_ids.includes(x.source_net_id)).name};
assert(supervisor);
['ALT_GUARD_VALID','ALT_GND','ALT_RETAINED_MODEM_SUPPLY_PENDING','ALT_CT_INTENTIONALLY_OPEN','ALT_MCU_LOCAL_SUPPLY_PENDING','ALT_RETAINED_MODEM_SUPPLY_PENDING'].forEach((n,i)=>assert.equal(netAt('U_ALT_SUPERVISOR',i+1),n));
assert.equal(netAt('R_ALT_VALID_PULLUP',1),'ALT_RETAINED_MODEM_SUPPLY_PENDING');
assert.equal(netAt('R_ALT_VALID_PULLUP',2),'ALT_GUARD_VALID');
assert.equal(netAt('R_ALT_OFF_2',1),'ALT_GUARD_VALID');
assert.equal(netAt('R_ALT_OFF_2',2),'ALT_GND');
assert.equal(j.filter(x=>x.type==='pcb_component').length,0)
fs.writeFileSync('output/modem-isolation-study-v47.circuit.json',JSON.stringify(j,null,2));fs.writeFileSync('output/modem-isolation-study-v47.svg',convertCircuitJsonToSchematicSvg(j));fs.writeFileSync('output/modem-isolation-study-v47-checks.json',JSON.stringify({topology_cases:rows,guard_bypass_fault_detected:true,scope:'Ideal switch connectivity only; supervisor wired; release threshold screen fails; no hardware validation; leakage, transition and undervoltage behavior unqualified',integrated:false,release:false},null,2));console.log('PASS switch and supervisor pin maps, guard bias wiring and 8 ideal topology cases; candidate remains rejected for integration')
