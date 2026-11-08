import React from 'react'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import {Circuit} from '@tscircuit/core'
import {convertCircuitJsonToPcbSvg} from 'circuit-to-svg'
import {ReviewedLandV24} from '../electronics/reviewed-lands-v24'
import data from '../sourcing/reviewed-lands-v24.json'
for(const kind of Object.keys(data.packages) as (keyof typeof data.packages)[]){
 const d=data.packages[kind],c=new Circuit()
 c.add(<board width={8} height={8} routingDisabled><chip name="U_REVIEW" pinLabels={Object.fromEntries([...d.pads,...('polygons' in d?d.polygons:[])].map(p=>[`pin${p.pin}`,`P${p.pin}`]))} footprint={<ReviewedLandV24 kind={kind}/>}/></board>)
 await c.renderUntilSettled();const j:any[]=c.getCircuitJson(),pads=j.filter(x=>x.type==='pcb_smtpad')
 assert.equal(pads.length,d.pads.length+('polygons' in d?d.polygons.length:0));assert.equal(j.filter(x=>x.type==='pcb_solder_paste').length,0)
 for(const expected of d.pads){const a=pads.find(x=>x.port_hints.includes(`pin${expected.pin}`));assert(a)
 for(const [key,v] of Object.entries({x:expected.x,y:-expected.y_down,width:expected.width,height:expected.height,corner_radius:expected.corner_radius,soldermask_margin:d.mask_margin}))assert(Math.abs(a[key]-v)<1e-9,`${kind} pin${expected.pin} ${key}`)
 }
 // Independent asymmetric anchors catch a mirrored top/bottom or invented exposed pad.
 const at=(n:number)=>pads.find(x=>x.port_hints.includes(`pin${n}`))
 if(kind==='DLA0010A'){assert.equal(at(1).y,1);assert.equal(at(8).x,.55);assert.equal(at(8).width,1.3);assert.equal(pads.length,10)}
 if(kind==='RUK0020B'){assert.equal(at(1).x,-1.4);assert.equal(at(6).y,-1.4);assert.equal(at(16).y,1.4);assert.equal(at(21).width,1.7)}
 if(kind==='DMQ0006A'){assert.equal(at(1).y,.5);assert.equal(at(4).y,-.5);assert(Math.abs(at(1).width+2*at(1).soldermask_margin-.6)<1e-9);assert.equal(at(1).corner_radius,.1)}
 assert.deepEqual(j.filter(x=>/error$/.test(x.type)),[])
 fs.writeFileSync(`output/${kind}-v24.circuit.json`,JSON.stringify(j,null,2));fs.writeFileSync(`output/${kind}-v24.svg`,convertCircuitJsonToPcbSvg(j))
 console.log(`PASS ${kind}: ${pads.length} copper pads, preserved radii and mask margin, no paste; export/process/courtyard unqualified`)
}
