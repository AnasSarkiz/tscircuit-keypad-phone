import React from 'react'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import {Circuit} from '@tscircuit/core'
import {convertCircuitJsonToSchematicSvg} from 'circuit-to-svg'
import {MemsAudioCandidateV26} from '../electronics/mems-audio-candidate-v26'
const c=new Circuit({platform:{pcbDisabled:true}});c.add(<MemsAudioCandidateV26/>);await c.renderUntilSettled()
const j:any[]=c.getCircuitJson(),all=(t:string)=>j.filter(x=>x.type===t)
function nets(ref:string,pin:number){const u=all('source_component').find(x=>x.name===ref),p=all('source_port').find(x=>x.source_component_id===u.source_component_id&&x.pin_number===pin);return [...new Set(all('source_trace').filter(t=>t.connected_source_port_ids.includes(p.source_port_id)).flatMap(t=>t.connected_source_net_ids).map(id=>all('source_net').find(n=>n.source_net_id===id).name))]}
for(const [i,net] of ['MIC_LOGIC_INPUT_PENDING','GND','MIC_ENABLE_PENDING',null,'MIC_2V5'].entries())assert.deepEqual(nets('U_MIC_LDO',i+1),net?[net]:[])
for(const [i,net] of ['MEMS_OUT_P_AFE_PENDING','MIC_2V5','MEMS_OUT_N_AFE_PENDING','GND','GND'].entries())assert.deepEqual(nets('MIC_MEMS_CANDIDATE',i+1),[net])
assert(!all('source_net').some(n=>n.name.includes('MICBIAS')))
assert.deepEqual(j.filter(x=>/error$/.test(x.type)),[]);assert.equal(all('source_component').length,7)
fs.writeFileSync('output/mems-audio-v26.circuit.json',JSON.stringify(j,null,2));fs.writeFileSync('output/mems-audio-v26.svg',convertCircuitJsonToSchematicSvg(j))
console.log('PASS MEMS/LDO pin nets, NC and isolation from electret bias; AFE/enable integration remains pending')
