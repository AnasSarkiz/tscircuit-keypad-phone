import React from 'react'
import fs from 'node:fs'
import assert from 'node:assert/strict'
import {Circuit} from '@tscircuit/core'
import {convertCircuitJsonToPcbSvg} from 'circuit-to-svg'
import {KeypadCandidateV64,keypadTerminalsV64} from '../electronics/keypad-v64'
const c=new Circuit();c.schematicDisabled=true;c.add(<KeypadCandidateV64/>);await c.renderUntilSettled();const j:any[]=c.getCircuitJson()
fs.writeFileSync('output/keypad-candidate-v64.circuit.json',JSON.stringify(j,null,2))

assert.equal(j.filter(x=>x.type==='pcb_plated_hole').length,60)
assert.equal(j.filter(x=>x.type==='source_component').length,15)
assert.equal(j.filter(x=>x.type==='pcb_trace').length,0)
assert.deepEqual(keypadTerminalsV64.map(p=>[p.physical,p.logical]),[[4,1],[3,1],[2,2],[1,2]])

const ids=new Map(j.filter(x=>x[x.type+'_id']).map(x=>[x[x.type+'_id'],x]))
function verify(data:any[]){
 const holes=data.filter(x=>x.type==='pcb_plated_hole');assert.equal(holes.length,60)
 for(let i=1;i<=15;i++){
  const source=data.find(x=>x.type==='source_component'&&x.name==='SW'+i)
  const pcb=data.find(x=>x.type==='pcb_component'&&x.source_component_id===source.source_component_id)
  const row=Math.floor((i-1)/3),col=(i-1)%3,x=[-14,0,14][col],y=[-21,-33,-45,-57,-69][row]
  const ph=holes.filter(h=>h.pcb_component_id===pcb.pcb_component_id);assert.equal(ph.length,4)
  for(const terminal of keypadTerminalsV64){
   const h=ph.find(h=>Math.abs(h.x-x-terminal.x)<1e-9&&Math.abs(h.y-y-terminal.y)<1e-9);assert(h)
   assert.equal(h.hole_diameter,1);assert.equal(h.outer_diameter,2);assert(h.port_hints.includes('pin'+terminal.logical))
   assert.deepEqual([...h.layers].sort(),['bottom','inner1','inner2','top'])
   const port=ids.get(h.pcb_port_id).source_port_id
   const nets=new Set(data.filter(t=>t.type==='source_trace'&&t.connected_source_port_ids.includes(port)).flatMap(t=>t.connected_source_net_ids.map((n:string)=>ids.get(n).name)))
   const expected=i===3?(terminal.logical===1?'BUTTON_BRANCH_UNQUALIFIED':'GND'):(terminal.logical===1?'ROW'+row:'COL'+col)
   assert.deepEqual([...nets],[expected])
  }
 }
}
verify(j)
for(const fault of ['old_hole','column_commoning','rotation90','missing_hole']){
 const bad=structuredClone(j),h=bad.find(x=>x.type==='pcb_plated_hole')
 if(fault==='old_hole')h.hole_diameter=1.1
 if(fault==='column_commoning')h.port_hints=['pin2']
 if(fault==='rotation90'){const x=h.x;h.x=h.y;h.y=x}
 if(fault==='missing_hole')bad.splice(bad.indexOf(h),1)
 assert.throws(()=>verify(bad),fault)
}
fs.writeFileSync('output/keypad-v64-checks.json',JSON.stringify({holes:60,switches:15,all_pin_nets_match:true,negative_tests:['old_hole','column_commoning','rotation90','missing_hole'],review:'Parent independent visual transcription,Omron page5;no local overlay claimed',hole_convention:'Proposed finished diameter1.00mm;factory must confirm0.95..1.05mm after plating;not drill-tool sizing',release:false},null,2))
console.log('PASS all60 keypad hole coordinates,commoning,net mapping;four injected defects rejected;not factory qualified')

fs.writeFileSync('output/keypad-candidate-v64.svg',convertCircuitJsonToPcbSvg(j,{width:600,height:1200}))
