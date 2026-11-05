import React from 'react'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import {Circuit} from '@tscircuit/core'
import {convertCircuitJsonToSchematicSvg} from 'circuit-to-svg'
import {ModemIsolationStudyV46} from '../electronics/modem-isolation-study-v46'
const c=new Circuit({platform:{pcbDisabled:true}});c.add(<ModemIsolationStudyV46/>);await c.renderUntilSettled();const j:any[]=c.getCircuitJson();assert.deepEqual(j.filter(x=>/error$/.test(x.type)),[])
const u=j.find(x=>x.type==='source_component'&&x.name==='U_ALT_SWITCH');const pinNet=(pin:number)=>{const p=j.find(x=>x.type==='source_port'&&x.source_component_id===u.source_component_id&&x.pin_number===pin);const t=j.find(x=>x.type==='source_trace'&&x.connected_source_port_ids.includes(p.source_port_id));return j.find(x=>x.type==='source_net'&&t.connected_source_net_ids.includes(x.source_net_id)).name}
const want=['ALT_KEY_CMD','ALT_MODEM_KEY','ALT_KEY_MID','ALT_HARDWARE_VALID_PENDING','ALT_KEY_MID','ALT_GND','ALT_GND','ALT_RESET_MID','ALT_MODEM_RESET','ALT_RESET_CMD','ALT_GND','ALT_RESET_MID','ALT_HARDWARE_VALID_PENDING','ALT_RETAINED_MODEM_SUPPLY_PENDING'];want.forEach((n,i)=>assert.equal(pinNet(i+1),n));assert(j.filter(x=>x.type==='source_net').every(n=>n.name.startsWith('ALT_')))
function connected(a:string,b:string,edges:string[][]){const seen=new Set([a]);for(let i=0;i<20;i++)for(const [x,y]of edges){if(seen.has(x))seen.add(y);if(seen.has(y))seen.add(x)}return seen.has(b)}
const rows:any[]=[]
for(const key of [false,true])for(const reset of [false,true])for(const valid of [false,true]){
 const enabled=[key,valid,reset,valid],pairs=[[2,3],[5,6],[9,8],[12,11]];const edges=pairs.filter((_,i)=>enabled[i]).map(p=>p.map(pinNet));const k=connected('ALT_MODEM_KEY','ALT_GND',edges),r=connected('ALT_MODEM_RESET','ALT_GND',edges);assert.equal(k,key&&valid);assert.equal(r,reset&&valid);rows.push({key,reset,valid,key_ground_path:k,reset_ground_path:r})
}
assert.throws(()=>assert.equal(connected('ALT_MODEM_KEY','ALT_GND',[['ALT_MODEM_KEY','ALT_KEY_MID'],['ALT_KEY_MID','ALT_GND']]),false),'bypassing guard must fail isolation assertion')
assert.equal(j.filter(x=>x.type==='pcb_component').length,0)
fs.writeFileSync('output/modem-isolation-study-v46.circuit.json',JSON.stringify(j,null,2));fs.writeFileSync('output/modem-isolation-study-v46.svg',convertCircuitJsonToSchematicSvg(j));fs.writeFileSync('output/modem-isolation-study-v46-checks.json',JSON.stringify({topology_cases:rows,guard_bypass_fault_detected:true,scope:'Ideal switch connectivity only; hardware-valid source absent; leakage, transition and undervoltage behavior unqualified',integrated:false,release:false},null,2));console.log('PASS isolated 14-pin map and8 ideal topology cases; guard bypass fault exposed; NOT hardware qualification')
