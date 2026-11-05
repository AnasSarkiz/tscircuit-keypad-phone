import React from 'react'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import {Circuit} from '@tscircuit/core'
import {sourcePassives} from '../electronics/sourced-passives'
import {convertCircuitJsonToPcbSvg} from 'circuit-to-svg'
for(const [mpn,count,w,h] of [['TPD3E001DRLR',5,.67,.3],['CAT4104V-GT3',8,1.55,.6]] as const){const c=new Circuit();c.add(sourcePassives(<board width={12} height={10} routingDisabled><chip name="U_AUDIT" manufacturerPartNumber={mpn} pinLabels={Object.fromEntries(Array.from({length:count},(_,i)=>['pin'+(i+1),'P'+(i+1)]))}/></board>));await c.renderUntilSettled();const j:any[]=c.getCircuitJson();const pads=j.filter(x=>x.type==='pcb_smtpad');assert.equal(pads.length,count);for(let n=1;n<=count;n++){const sp=j.find(x=>x.type==='source_port'&&x.pin_number===n);const pp=j.find(x=>x.type==='pcb_port'&&x.source_port_id===sp.source_port_id);const p=pads.find(x=>x.pcb_port_id===pp.pcb_port_id);assert.equal(p.width,w);assert.equal(p.height,h);if(count===5){const expected=[[-.74,.5],[-.74,0],[-.74,-.5],[.74,-.5],[.74,.5]][n-1];assert.equal(p.x,expected[0]);assert.equal(p.y,expected[1])}}
for(let i=0;i<pads.length;i++)for(let k=i+1;k<pads.length;k++)assert(Math.abs(pads[i].x-pads[k].x)>=w||Math.abs(pads[i].y-pads[k].y)>=h)
assert.deepEqual(j.filter(x=>/error$/.test(x.type)),[]);fs.writeFileSync(`output/${mpn}-v19.svg`,convertCircuitJsonToPcbSvg(j));fs.writeFileSync(`output/${mpn}-v19.circuit.json`,JSON.stringify(j,null,2))}
console.log('PASS DRL5 and SOIC8 candidate pad mapping and nonoverlap; independent drawing audit pending')
