import React from 'react'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import {Circuit} from '@tscircuit/core'
import {sourcePassives} from '../electronics/sourced-passives'
import {convertCircuitJsonToPcbSvg} from 'circuit-to-svg'
for(const [mpn,row,pitch,w,h] of [['TLV9032DR',2.7,1.27,1.55,.6],['LTC2954ITS8-1#TRMPBF',1.31,.65,1.22,.4]] as const){
 const c=new Circuit();c.add(sourcePassives(<board width={12} height={10} routingDisabled><chip name="U_TEST" manufacturerPartNumber={mpn} pinLabels={{pin1:'P1',pin2:'P2',pin3:'P3',pin4:'P4',pin5:'P5',pin6:'P6',pin7:'P7',pin8:'P8'}}/></board>));await c.renderUntilSettled();const j:any[]=c.getCircuitJson();const pads=j.filter(x=>x.type==='pcb_smtpad');assert.equal(pads.length,8)
 for(let n=1;n<=8;n++){const s=j.find(x=>x.type==='source_port'&&x.pin_number===n);const p=j.find(x=>x.type==='pcb_port'&&x.source_port_id===s.source_port_id);const pad=pads.find(x=>x.pcb_port_id===p.pcb_port_id);assert.equal(pad.width,w);assert.equal(pad.height,h);assert.equal(pad.x,n<5?-row:row)}
 const left=pads.filter(x=>x.x<0).sort((a,b)=>a.y-b.y);for(let i=1;i<4;i++)assert(Math.abs(left[i].y-left[i-1].y-pitch)<1e-8)
 for(let i=0;i<pads.length;i++)for(let k=i+1;k<pads.length;k++)assert(Math.abs(pads[i].x-pads[k].x)>=w||Math.abs(pads[i].y-pads[k].y)>=h)
 assert.deepEqual(j.filter(x=>/error$/.test(x.type)),[])
 const slug=mpn.split('#')[0];fs.writeFileSync(`output/${slug}-v18.circuit.json`,JSON.stringify(j,null,2));fs.writeFileSync(`output/${slug}-v18.svg`,convertCircuitJsonToPcbSvg(j))
}
console.log('PASS two text-derived eight-pad candidates; no fabrication approval')
