import React from 'react'
import fs from 'node:fs'
import assert from 'node:assert/strict'
import { Circuit } from '@tscircuit/core'
import { convertCircuitJsonToPcbSvg } from 'circuit-to-svg'
import { UsbPlacementV66, placementV66 } from '../electronics/usb-placement-v66'
// The placement map is preserved; footprint geometry is the JLC migration candidate.
const c=new Circuit();c.schematicDisabled=true;c.add(<UsbPlacementV66/>);await c.renderUntilSettled();const j:any[]=c.getCircuitJson()
fs.mkdirSync('output',{recursive:true});fs.writeFileSync('output/usb-placement-v66.circuit.json',JSON.stringify(j,null,2));fs.writeFileSync('output/usb-placement-v66.svg',convertCircuitJsonToPcbSvg(j))
const sources=j.filter(x=>x.type==='source_component'),components=j.filter(x=>x.type==='pcb_component')
assert.equal(sources.length,139)
const modemIdentity=sources.find(x=>x.name==='U_MODEM_LOGICAL_ONLY');assert(modemIdentity)
assert.equal(modemIdentity.manufacturer_part_number,'EG912UGLAC-I05-SNNSA','placed candidate must retain the exact imported modem identity')
assert.deepEqual(modemIdentity.supplier_part_numbers?.jlcpcb,['C7472750'])
const migrated=new Set(['U_MCU','U_MODEM_LOGICAL_ONLY','U_CC_PROTECT','U_USB_PROTECT'])
for(const [name,a]of Object.entries(placementV66) as [string,any][]){
 const s=sources.find(x=>x.name===name);assert(s,name);const p=components.find(x=>x.source_component_id===s.source_component_id);assert(p,name)
 if(!migrated.has(name)){assert(Math.abs(p.center.x-a.x)<1e-8,`${name}:X moved`);assert(Math.abs(p.center.y-a.y)<1e-8,`${name}:Y moved`)}
}
const padsFor=(name:string)=>{const s=sources.find(x=>x.name===name);const p=components.find(x=>x.source_component_id===s.source_component_id);return j.filter(x=>x.type==='pcb_smtpad'&&x.pcb_component_id===p.pcb_component_id)}
const netNames=(pad:any)=>{const pp=j.find(x=>x.type==='pcb_port'&&x.pcb_port_id===pad.pcb_port_id);assert(pp,`unmapped ${pad.port_hints}`);const ids=new Set([pp.source_port_id]);const sp=j.find(x=>x.type==='source_port'&&x.source_port_id===pp.source_port_id);const sc=sources.find(x=>x.source_component_id===sp.source_component_id);for(const g of sc.internally_connected_source_port_ids??[])if(g.includes(pp.source_port_id))for(const id of g)ids.add(id);return [...new Set(j.filter(x=>x.type==='source_trace'&&x.connected_source_port_ids.some((id:string)=>ids.has(id))).flatMap(x=>x.connected_source_net_ids).map(id=>j.find(x=>x.type==='source_net'&&x.source_net_id===id)?.name))].sort()}
const anchor=(name:string,pin:number,x:number,y:number,tolerance:number)=>{const p=padsFor(name).find(p=>p.port_hints.includes(`pin${pin}`));assert(p);assert(Math.abs(p.x-x)<tolerance&&Math.abs(p.y-y)<tolerance,`${name} pin${pin}: actual ${p.x},${p.y}; expected ${x},${y}`)}
// Independent manufacturer anchors with legacy bottom-layer reflection and datum.
anchor('U_MCU',1,-4.25,37.26,.05)
anchor('U_MCU',14,-4.25,20.75,.05)
anchor('U_MCU',15,-6.015,19.5,.05)
anchor('U_MCU',40,-21.75,37.26,.05)
const mcu=padsFor('U_MCU');assert.equal(mcu.length,49)
const ep=mcu.filter(p=>p.port_hints.includes('pin41'));assert.equal(ep.length,9);assert.equal(new Set(ep.map(p=>p.pcb_port_id)).size,9)
for(const p of ep)assert.deepEqual(netNames(p),['GND'])
// Numbered-pin contracts prevent alias changes from silently altering real nets.
for(const [pin,net]of [[1,'GND'],[2,'VLOGIC_3V15'],[3,'MCU_EN'],[5,'ROW0'],[10,'HOST_TX'],[19,'LCD_SDIO'],[28,'ON_OFF_MCU'],[29,'RESET_MCU'],[40,'GND']] as const)assert.deepEqual(netNames(mcu.find(p=>p.port_hints.includes(`pin${pin}`))),[net])
const modem=padsFor('U_MODEM_LOGICAL_ONLY');assert.equal(modem.length,126)
const modemPlacement=(placementV66 as any).U_MODEM_LOGICAL_ONLY
for(const [pin,x,y]of [[1,-9.175,9.7],[19,-7.45,-11.025],[49,9.175,9.7],[119,-.85,2.55],[126,.85,2.55]])anchor('U_MODEM_LOGICAL_ONLY',pin,modemPlacement.x-x,modemPlacement.y+y,.05)
for(const [pin,net]of [[15,'MODEM_PWRKEY_OD'],[17,'MODEM_RESET_OD'],[20,'MODEM_STATUS'],[32,'MODEM_BB_SUPPLY_UNQUALIFIED'],[33,'MODEM_BB_SUPPLY_UNQUALIFIED'],[47,'GND'],[52,'MODEM_RF_SUPPLY_UNQUALIFIED'],[53,'MODEM_RF_SUPPLY_UNQUALIFIED']] as const)assert.deepEqual(netNames(modem.find(p=>p.port_hints.includes(`pin${pin}`))),[net])
// Modem USB is deliberately disconnected in this candidate. Charging USB VBUS
// does not qualify modem USB timing, termination or service access. See the
// Standard Hardware Design review under qualification-modem-supply/.
const assertOpenModemPin=(pin:number)=>assert.deepEqual(netNames(modem.find(p=>p.port_hints.includes(`pin${pin}`))),[],`unverified modem pin${pin} must stay open`)
for(const pin of [8,9,10,123,124,125])assertOpenModemPin(pin)
// Negative controls prove these guards reject an accidental charging-VBUS tie.
const rawVbus=j.find(x=>x.type==='source_net'&&x.name==='USB_VBUS_RAW');assert(rawVbus)
for(const pin of [8,9,10]){
 const pad=modem.find(p=>p.port_hints.includes(`pin${pin}`))
 const port=j.find(x=>x.type==='pcb_port'&&x.pcb_port_id===pad.pcb_port_id);assert(port)
 const mutation={type:'source_trace',source_trace_id:`usb-scope-mutation-${pin}`,connected_source_port_ids:[port.source_port_id],connected_source_net_ids:[rawVbus.source_net_id]}
 j.push(mutation)
 try {assert.throws(()=>assertOpenModemPin(pin),new RegExp(`unverified modem pin${pin} must stay open`))}
 finally {assert.equal(j.pop(),mutation)}
}
const cc=padsFor('U_CC_PROTECT');assert.equal(cc.length,21);for(const pin of [8,13,16,17,18,21])assert.deepEqual(netNames(cc.find(p=>p.port_hints.includes(`pin${pin}`))),['GND'])
const efuse=padsFor('U_USB_PROTECT');assert.equal(efuse.length,10);assert.equal(efuse.filter(p=>p.shape==='polygon').length,4);assert.deepEqual(netNames(efuse.find(p=>p.port_hints.includes('pin8'))),['GND'])
anchor('U_CC_PROTECT',1,5.500003,-74.199773,1e-6)
anchor('U_CC_PROTECT',6,6.199773,-76.499997,1e-6)
anchor('U_USB_PROTECT',5,19.7650627,-75,1e-6)
anchor('U_USB_PROTECT',6,20.2649347,-75,1e-6)
const corner=efuse.find(p=>p.port_hints.includes('pin1'))
assert(Math.abs(Math.min(...corner.points.map((p:any)=>p.x))-18.7850037)<1e-6)
assert(Math.abs(Math.max(...corner.points.map((p:any)=>p.y))+73.8000024)<1e-6)
for(const [name,layer]of [['U_MCU','bottom'],['U_MODEM_LOGICAL_ONLY','bottom'],['U_CC_PROTECT','top'],['U_USB_PROTECT','top']])assert(padsFor(name).every(p=>p.layer===layer),`${name}:wrong board side`)
for(const [pin,net]of [[1,'USB_3A_ENABLE_PENDING'],[2,'USB_OVLO'],[4,'USB_FAULT_N'],[5,'USB_VBUS_RAW'],[6,'USB_5V_QUALIFIED'],[7,'USB_DVDT'],[8,'GND'],[9,'USB_ILM']] as const)assert.deepEqual(netNames(efuse.find(p=>p.port_hints.includes(`pin${pin}`))),[net])
for(const pin of [3,10])assert.deepEqual(netNames(efuse.find(p=>p.port_hints.includes(`pin${pin}`))),[])
for(const pad of j.filter(x=>x.type==='pcb_smtpad')) {
 const pp=j.find(x=>x.type==='pcb_port'&&x.pcb_port_id===pad.pcb_port_id);assert(pp,'unmapped copper')
 const sp=j.find(x=>x.type==='source_port'&&x.source_port_id===pp.source_port_id)
 assert(pad.port_hints.some((hint:string)=>sp.port_hints.includes(hint)),'wrong logical terminal for copper')
 assert(netNames(pad).length<=1,'conflicting net assignments')
}
assert.equal(j.filter(x=>x.type==='pcb_solder_paste').length,0);assert.deepEqual(j.filter(x=>/error$/.test(x.type)),[])
const board=j.find(x=>x.type==='pcb_board');assert.equal(board.width,56);assert.equal(board.height,144);assert.equal(board.center.y,-12)
fs.writeFileSync('output/board-migration-report.json',JSON.stringify({components:sources.length,placementMapEntries:Object.keys(placementV66).length,migrated:[...migrated],mcuGroundPads:ep.length,pasteApertures:0,modemUsbPinsHeldOpen:[8,9,10],modemUsbConnectionMutationsRejected:3,scope:'Placement, physical pad anchors and source-net contracts only. No routed-board/ERC/DRC or manufacturing approval.'},null,2))
console.log('PASS139 components, preserved unmigrated placements, manufacturer anchors, mapped MCU EP, modem safety nets and open pins, zero paste; modem USB remains open. Routed copper is checked separately.')
