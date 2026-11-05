import React from 'react'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import {Circuit} from '@tscircuit/core'
import {convertCircuitJsonToSchematicSvg} from 'circuit-to-svg'
import {DirectSysBranch} from '../electronics/direct-sys-branch'
const c=new Circuit({platform:{pcbDisabled:true}});c.add(<DirectSysBranch/>);await c.renderUntilSettled()
const j:any[]=c.getCircuitJson();const all=(t:string)=>j.filter(x=>x.type===t)
assert.deepEqual(j.filter(x=>/error$/.test(x.type)),[])
const u=all('source_component').find(x=>x.name==='U_MODEM_SWITCH_BRANCH')
for(const [i,net] of ['SYS_BRANCH_UNQUALIFIED','SYS_BRANCH_UNQUALIFIED','SWITCH_PG_UNQUALIFIED','GND','SWITCH_QOD','MODEM_SWITCH_OUT_UNQUALIFIED','SWITCH_CT','SWITCH_ENABLE_UNQUALIFIED'].entries()){
 const p=all('source_port').find(x=>x.source_component_id===u.source_component_id&&x.pin_number===i+1)
 const names=all('source_trace').filter(t=>t.connected_source_port_ids.includes(p.source_port_id)).flatMap(t=>t.connected_source_net_ids).map(id=>all('source_net').find(n=>n.source_net_id===id).name)
 assert.deepEqual([...new Set(names)],[net])
}
assert.equal(all('pcb_component').length,0)
fs.writeFileSync('output/direct-sys-branch.circuit.json',JSON.stringify(j,null,2));fs.writeFileSync('output/direct-sys-branch.svg',convertCircuitJsonToSchematicSvg(j))
console.log('PASS isolated switch branch pin/net contract; not protected or integrated')
