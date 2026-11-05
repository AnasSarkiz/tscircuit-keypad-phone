import React from 'react'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import {Circuit} from '@tscircuit/core'
import {convertCircuitJsonToSchematicSvg} from 'circuit-to-svg'
import {BuckBoostCandidateV21} from '../electronics/buckboost-candidate-v21'
const c=new Circuit({platform:{pcbDisabled:true}});c.add(<BuckBoostCandidateV21/>);await c.renderUntilSettled()
const j:any[]=c.getCircuitJson();const all=(t:string)=>j.filter(x=>x.type===t)
assert.deepEqual(j.filter(x=>/error$/.test(x.type)),[])
const u=all('source_component').find(x=>x.name==='U_BB_CANDIDATE')
for(const [i,net] of ['BB_ENABLE_UNQUALIFIED','BB_INPUT_UNQUALIFIED','GND','BB_FB','BB_PG_UNQUALIFIED','BB_OUTPUT_UNQUALIFIED','BB_L2','GND','BB_L1','BB_INPUT_UNQUALIFIED'].entries()){
 const p=all('source_port').find(x=>x.source_component_id===u.source_component_id&&x.pin_number===i+1)
 const names=all('source_trace').filter(t=>t.connected_source_port_ids.includes(p.source_port_id)).flatMap(t=>t.connected_source_net_ids).map(id=>all('source_net').find(n=>n.source_net_id===id).name)
 assert.deepEqual([...new Set(names)],[net])
}
assert.equal(all('pcb_component').length,0)
fs.writeFileSync('output/buckboost-candidate-v21.circuit.json',JSON.stringify(j,null,2));fs.writeFileSync('output/buckboost-candidate-v21.svg',convertCircuitJsonToSchematicSvg(j))
console.log('PASS isolated TPS63802 pin/net contract; power and physical design unqualified')
