import React from 'react'
import fs from 'node:fs'
import assert from 'node:assert/strict'
import {Circuit} from '@tscircuit/core'
import {Fusb303bCandidate,Fusb303bLandCandidate} from '../electronics/fusb303b-candidate-v36'
import {decodeTypeCCurrent,qualifiedTypeCCurrent} from '../firmware/power-policy'
const c=new Circuit();c.schematicDisabled=true;c.add(<board width={8} height={8} routingDisabled><chip name="U_REVIEW" pinLabels={Object.fromEntries(Array.from({length:12},(_,i)=>['pin'+(i+1),'P'+(i+1)]))} footprint={<Fusb303bLandCandidate/>}/></board>);await c.renderUntilSettled();const j:any[]=c.getCircuitJson(),pads=j.filter(x=>x.type==='pcb_smtpad');assert.equal(pads.length,12);assert.equal(j.filter(x=>x.type==='pcb_solder_paste').length,0)
for(const [pin,x,y,w,h] of [[1,-.65,.2,.7,.2],[2,-.65,-.2,.7,.2],[3,-.6,-.75,.2,.5],[6,.6,-.75,.2,.5],[7,.65,-.2,.7,.2],[8,.65,.2,.7,.2],[9,.6,.75,.2,.5],[12,-.6,.75,.2,.5]]){const p=pads.find(p=>p.port_hints.includes('pin'+pin));assert.equal(p.x,x);assert.equal(p.y,y);assert.equal(p.width,w);assert.equal(p.height,h)}
const alt=new Circuit({platform:{pcbDisabled:true}});alt.add(<Fusb303bCandidate/>);await alt.renderUntilSettled();const a:any[]=alt.getCircuitJson();assert.equal(a.find(x=>x.type==='source_component'&&x.name==='U_CC').manufacturer_part_number,'FUSB303BTMX');assert.equal(a.filter(x=>x.type==='source_component'&&/^R_CC_SINK/.test(x.name)).reduce((n,x)=>n+x.resistance,0),900000)
for(const [o1,o2,want] of [[true,false,'none'],[true,true,'default'],[false,true,'1.5A'],[false,false,'3A']] as const){assert.equal(decodeTypeCCurrent(o1,o2,'FUSB303B'),want);assert.equal(qualifiedTypeCCurrent(o1,o2,'FUSB303B',false,true),'none');assert.equal(qualifiedTypeCCurrent(o1,o2,'FUSB303B',true,false),'none')}
assert.equal(decodeTypeCCurrent(true,true,'HUSB320-BA000'),'none');assert.equal(decodeTypeCCurrent(true,false,'HUSB320-BA000'),'default')
assert.deepEqual(j.filter(x=>/error$/.test(x.type)),[]);assert.deepEqual(a.filter(x=>/error$/.test(x.type)),[])
fs.writeFileSync('output/fusb303b-land-v36.circuit.json',JSON.stringify(j,null,2));fs.writeFileSync('output/fusb303b-alternate-v36.circuit.json',JSON.stringify(a,null,2));console.log('PASS alternate12-pad transcription,900k sink chain, detector-specific GPIO table and invalid-power/reset rejection; alternate not selected')
