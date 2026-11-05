import {Circuit} from '@tscircuit/core'
import {StartupCandidate} from '../electronics/startup-candidate'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import {convertCircuitJsonToSchematicSvg} from 'circuit-to-svg'
const c=new Circuit({platform:{pcbDisabled:true}});c.add(StartupCandidate());await c.renderUntilSettled();const j:any[]=c.getCircuitJson()
const u=j.find(x=>x.type==='source_component'&&x.name==='U_BUTTON_BRANCH');assert(u)
for(const [pin,net] of [[1,'SYS_BRANCH_UNQUALIFIED'],[2,'BUTTON_BRANCH_UNQUALIFIED'],[4,'GND'],[5,'BUTTON_INT_BRANCH_UNQUALIFIED'],[6,'LOGIC_EN_BRANCH_UNQUALIFIED'],[7,'BUTTON_PDT_BRANCH'],[8,'BUTTON_KILL_BRANCH']] as const){
 const p=j.find(x=>x.type==='source_port'&&x.source_component_id===u.source_component_id&&x.pin_number===pin);const n=j.find(x=>x.type==='source_net'&&x.name===net);assert(j.some(x=>x.type==='source_trace'&&x.connected_source_port_ids.includes(p.source_port_id)&&x.connected_source_net_ids.includes(n.source_net_id)))
}
assert.deepEqual(j.filter(x=>/error$/.test(x.type)),[])
fs.writeFileSync('output/startup-candidate-v15.circuit.json',JSON.stringify(j,null,2));fs.writeFileSync('output/startup-candidate-v15.svg',convertCircuitJsonToSchematicSvg(j));console.log('PASS isolated startup branch pin/net contract; no integration or hardware qualification')
