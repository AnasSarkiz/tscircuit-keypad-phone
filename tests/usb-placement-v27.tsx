import React from 'react'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import {Circuit} from '@tscircuit/core'
import {convertCircuitJsonToPcbSvg} from 'circuit-to-svg'
import {UsbPlacementV27,ccPlacementV27} from '../electronics/usb-placement-v27'
const c=new Circuit();c.add(<UsbPlacementV27/>);await c.renderUntilSettled();const j:any[]=c.getCircuitJson(),all=(t:string)=>j.filter(x=>x.type===t)
assert.equal(all('pcb_solder_paste').length,0)
for(const [name,a] of Object.entries(ccPlacementV27)){const s=all('source_component').find(x=>x.name===name),p=all('pcb_component').find(x=>x.source_component_id===s.source_component_id);assert.equal(p.center.x,a.x);assert.equal(p.center.y,a.y)}
const pads=all('pcb_smtpad');let minGap=Infinity
for(let i=0;i<pads.length;i++)for(let k=i+1;k<pads.length;k++){const a=pads[i],b=pads[k];if(a.pcb_component_id===b.pcb_component_id)continue;const dx=Math.max(Math.abs(a.x-b.x)-(a.width+b.width)/2,0),dy=Math.max(Math.abs(a.y-b.y)-(a.height+b.height)/2,0);const gap=Math.hypot(dx,dy);assert(gap>=.2,`inter-component copper gap ${gap}: ${JSON.stringify(a)} vs ${JSON.stringify(b)}`);minGap=Math.min(minGap,gap)}
function pad(ref:string,n:number){const s=all('source_component').find(x=>x.name===ref),p=all('pcb_component').find(x=>x.source_component_id===s.source_component_id);return pads.find(x=>x.pcb_component_id===p.pcb_component_id&&x.port_hints.includes(`pin${n}`))}
const u=pad('U_CC_PROTECT',10),v=pad('C_CC_PROTECT',1),length=Math.hypot(u.x-v.x,u.y-v.y);assert(length<=1.5,'VPWR bypass too far')
assert.deepEqual(j.filter(x=>/error$/.test(x.type)),[])
fs.writeFileSync('output/usb-placement-v27.circuit.json',JSON.stringify(j,null,2));fs.writeFileSync('output/usb-placement-v27.svg',convertCircuitJsonToPcbSvg(j));fs.writeFileSync('output/usb-placement-v27-checks.json',JSON.stringify({minimum_intercomponent_copper_gap_mm:minGap,VPWR_to_bypass_pad_center_mm:length,routed:false,geometry_independent_overlay:false,release:false},null,2));console.log('PASS four fixed placements, copper gaps and local bypass distance; routing and return loop pending')
