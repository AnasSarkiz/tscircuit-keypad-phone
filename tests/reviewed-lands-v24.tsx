import React from 'react'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import { Circuit } from '@tscircuit/core'
import { ReviewedLandV24 } from '../electronics/reviewed-lands-v24'
const cases = [
  {kind:'DLA0010A',count:10,anchors:[[1,-.90004265,.999998,.5999988,.2999994],[8,.55004335,0,1.2999974,.2999994]]},
  {kind:'RUK0020B',count:21,anchors:[[1,-1.499997,.800227,.7999984,.1999996],[6,-.800227,-1.499997,.1999996,.7999984],[21,-.000127,.000127,1.6999966,1.6999966]]},
  {kind:'DMQ0006A',count:6,anchors:[[1,-.6750558,.499999,.5999988,.2500122],[4,.4750562,-.499999,.999998,.2500122]]},
  {kind:'RPW0010A',count:10,anchors:[[5,-.2349373,0,.2999994,2.3999952],[6,.2649347,0,.2999994,2.3999952]]},
] as const
for(const item of cases){
 const c=new Circuit();c.add(<board width={8} height={8} routingDisabled><chip name="U_REVIEW" pinLabels={Object.fromEntries(Array.from({length:item.count},(_,i)=>[`pin${i+1}`,`P${i+1}`]))} footprint={<ReviewedLandV24 kind={item.kind}/>}/></board>);await c.renderUntilSettled()
 const j:any[]=c.getCircuitJson(),pads=j.filter(x=>x.type==='pcb_smtpad')
 assert.equal(pads.length,item.count); assert(pads.every(p=>p.pcb_port_id));assert.equal(j.filter(x=>x.type==='pcb_solder_paste').length,0)
 for(const [pin,x,y,w,h] of item.anchors){const p=pads.find(p=>p.port_hints.includes(`pin${pin}`));assert(p);for(const [a,b]of[[p.x,x],[p.y,y],[p.width,w],[p.height,h]])assert(Math.abs(a-b)<1e-7)}
 if(item.kind==='RPW0010A'){assert.deepEqual(pads.filter(p=>p.shape==='polygon').map(p=>p.port_hints[0]).sort(),['pin1','pin10','pin4','pin7']);for(const p of pads.filter(p=>p.shape==='polygon'))assert(p.points.length>=6)}
 assert.deepEqual(j.filter(x=>/error$/.test(x.type)),[]);fs.mkdirSync('output',{recursive:true});fs.writeFileSync(`output/${item.kind}-v24.circuit.json`,JSON.stringify(j,null,2))
 console.log(`PASS ${item.kind}:catalog copper and numbered ports; zero paste; historical TI mask/radius assertions superseded, not claimed`)
}
