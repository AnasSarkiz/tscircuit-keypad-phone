import React from 'react'
import fs from 'node:fs'
import assert from 'node:assert/strict'
import { Circuit } from '@tscircuit/core'
import { convertCircuitJsonToPcbSvg, convertCircuitJsonToSchematicSvg } from 'circuit-to-svg'
import Keypad, {keyRows,keyCols} from '../electronics/keypad'
import PhoneAssembly from '../electronics/assembly'

const circuit = new Circuit()
circuit.add(<Keypad />)
await circuit.renderUntilSettled()
const json=circuit.getCircuitJson()
fs.writeFileSync('output/keypad.circuit.json',JSON.stringify(json,null,2))
fs.writeFileSync('output/keypad-pcb.svg',convertCircuitJsonToPcbSvg(json,{width:700,height:1200}))
fs.writeFileSync('output/keypad-schematic.svg',convertCircuitJsonToSchematicSvg(json))
const byType=(t:string)=>json.filter((e:any)=>e.type===t) as any[]
const board=byType('pcb_board')[0]
assert.equal(board.width,56); assert.equal(board.height,144)
assert.equal(board.center.y,-12)
assert.equal(byType('pcb_hole').length,4)
assert.equal(byType('pcb_plated_hole').length,60)
const nets=byType('source_net').map((e:any)=>e.name).sort()
assert.deepEqual(nets,['COL0','COL1','COL2','ROW0','ROW1','ROW2','ROW3','ROW4'])
// Validate emitted pad geometry, not just input arrays.
const holes=byType('pcb_plated_hole')
for(const component of byType('pcb_component')){
  const pads=holes.filter((p:any)=>p.pcb_component_id===component.pcb_component_id)
  assert.equal(pads.length,4)
  const source=byType('source_component').find(s=>s.source_component_id===component.source_component_id)
  const index=Number(source.name.slice(2))-1
  assert.deepEqual(component.center,{x:keyCols[index%3],y:keyRows[Math.floor(index/3)]})
  for(const pad of pads){
    const port=byType('pcb_port').find(p=>p.pcb_port_id===pad.pcb_port_id)
    const sp=byType('source_port').find(p=>p.source_port_id===port.source_port_id)
    const top=pad.y>component.center.y
    const logicalPin=top?'pin1':'pin2'
    assert.ok(sp.port_hints.includes(logicalPin))
    const logical=byType('source_port').find(p=>p.source_component_id===source.source_component_id && p.name===logicalPin)
    assert.ok(source.internally_connected_source_port_ids.some((ids:string[])=>ids.includes(sp.source_port_id)&&ids.includes(logical.source_port_id)))
    const trace=byType('source_trace').find(t=>t.connected_source_port_ids.includes(logical.source_port_id))
    const net=byType('source_net').find(n=>trace.connected_source_net_ids.includes(n.source_net_id))
    assert.equal(net.name,top?`ROW${Math.floor(index/3)}`:`COL${index%3}`)
  }
  const xs=[...new Set(pads.map((p:any)=>p.x))].sort((a:any,b:any)=>a-b) as number[]
  const ys=[...new Set(pads.map((p:any)=>p.y))].sort((a:any,b:any)=>a-b) as number[]
  assert.equal(xs[1]-xs[0],6.5); assert.equal(ys[1]-ys[0],4.5)
  for(const p of pads) assert.equal(p.hole_diameter,1.1)
}
assert.deepEqual(byType('pcb_hole').map(h=>[h.x,h.y]),[[-24,-79],[-24,54],[24,-79],[24,54]])
const errors=json.filter((e:any)=>/error$/.test(e.type))
assert.equal(errors.length,0)
// Keep all diagnostics. Intentional missing copper cannot be presented as DRC pass.
const report={coreVersion:JSON.parse(fs.readFileSync('node_modules/@tscircuit/core/package.json','utf8')).version,boardDimensions:[board.width,board.height],holes:4,keyPads:60,nets,diagnostics:errors,status:'keypad geometry/net generation only; copper routing disabled; no full-phone ERC/DRC'}
fs.writeFileSync('output/electrical-checks.json',JSON.stringify(report,null,2))
console.log(JSON.stringify(report,null,2))
// Compile/render assembly entry point too. Local model mesh isn't loaded by
// Circuit JSON generation, so this checks API use, not CAD import scaling.
const assemblyCircuit=new Circuit(); assemblyCircuit.add(<PhoneAssembly/>);
await assemblyCircuit.renderUntilSettled()
const assemblyJson=assemblyCircuit.getCircuitJson()
assert.equal(assemblyJson.filter((e:any)=>/error$/.test(e.type)).length,0)
fs.writeFileSync('output/assembly.circuit.json',JSON.stringify(assemblyJson,null,2))
