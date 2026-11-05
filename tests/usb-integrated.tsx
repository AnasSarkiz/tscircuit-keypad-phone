import React from 'react'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import {Circuit} from '@tscircuit/core'
import {convertCircuitJsonToSchematicSvg} from 'circuit-to-svg'
import {UsbIntegrated} from '../electronics/usb-integrated'
const c=new Circuit({platform:{pcbDisabled:true}});c.add(<UsbIntegrated/>);await c.renderUntilSettled()
const j:any[]=c.getCircuitJson();const all=(t:string)=>j.filter(x=>x.type===t)
assert.deepEqual(j.filter(x=>/error$/.test(x.type)),[])
const comps=all('source_component');assert.equal(new Set(comps.map(x=>x.name)).size,comps.length)
assert.equal(comps.find(c=>c.name==='U_CC').manufacturer_part_number,'HUSB320-BA000-QN12R');
const nets=all('source_net');assert.equal(new Set(nets.map(x=>x.name)).size,nets.length,'shared nets must merge on one board')
function pins(net:string){const n=nets.find(x=>x.name===net);assert.ok(n,net);return [...new Set(all('source_trace').filter(t=>t.connected_source_net_ids.includes(n.source_net_id)).flatMap(t=>t.connected_source_port_ids))].map(id=>{const p=all('source_port').find(p=>p.source_port_id===id);return comps.find(c=>c.source_component_id===p.source_component_id).name+'.'+p.pin_number})}
for(const [net,required] of Object.entries({USB_AUX3V3_PENDING:['U_USB_AUX.5','U_USB_POR.6','U_USB_3A.5','U_CC_PROTECT.10','U_CC.12'],USB_3A_ENABLE_PENDING:['U_USB_POR.1','U_USB_PROTECT.1','R_USB_3A_DRIVE.2','R_USB_OFF.1'],USB_CC_FAULT_N:['U_USB_POR.3','U_CC_PROTECT.9'],USB_CC1_PROTECTED_PENDING:['U_CC_PROTECT.12','U_CC.1'],USB_CC2_PROTECTED_PENDING:['U_CC_PROTECT.11','U_CC.2']}))for(const p of required)assert.ok(pins(net).includes(p),`${net}: ${p}`)
assert.ok(pins('CC_SINK_CONFIG').includes('U_CC.3'));assert.ok(pins('CC_SINK_CONFIG').includes('R_CC_SINK0.1'));assert.equal(all('pcb_component').length,0)
fs.writeFileSync('output/usb-integrated.circuit.json',JSON.stringify(j,null,2));fs.writeFileSync('output/usb-integrated-schematic.svg',convertCircuitJsonToSchematicSvg(j,{width:2400,height:1200}))
fs.writeFileSync('output/usb-integration-checks.json',JSON.stringify({components:comps.length,nets:nets.length,errors:[],scope:'logical connectivity; no electrical simulation or PCB release'},null,2));console.log('PASS: USB shared-net integration')
