import React from 'react'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import {Circuit} from '@tscircuit/core'
import {convertCircuitJsonToSchematicSvg} from 'circuit-to-svg'
import {PowerIntegratedV45} from '../electronics/power-integrated-v45'
const c=new Circuit({platform:{pcbDisabled:true}});c.add(<PowerIntegratedV45/>);await c.renderUntilSettled()
const j:any[]=c.getCircuitJson();const all=(t:string)=>j.filter(x=>x.type===t)
assert.deepEqual(j.filter(x=>/error$/.test(x.type)),[])
const comps=all('source_component');assert.equal(new Set(comps.map(x=>x.name)).size,comps.length)
assert.equal(comps.find(c=>c.name==='U_CC').manufacturer_part_number,'HUSB320-BA000-QN12R');
const nets=all('source_net');assert.equal(new Set(nets.map(x=>x.name)).size,nets.length,'shared nets must merge on one board')
function pins(net:string){const n=nets.find(x=>x.name===net);assert.ok(n,net);return [...new Set(all('source_trace').filter(t=>t.connected_source_net_ids.includes(n.source_net_id)).flatMap(t=>t.connected_source_port_ids))].map(id=>{const p=all('source_port').find(p=>p.source_port_id===id);return comps.find(c=>c.source_component_id===p.source_component_id).name+'.'+p.pin_number})}
for(const [net,required] of Object.entries({USB_AUX3V3_PENDING:['U_USB_AUX.5','U_USB_POR.6','U_USB_3A.5','U_CC_PROTECT.10','U_CC.12'],USB_3A_ENABLE_PENDING:['U_USB_POR.1','U_USB_PROTECT.1','R_USB_3A_DRIVE.2','R_USB_OFF.1'],USB_CC_FAULT_N:['U_USB_POR.3','U_CC_PROTECT.9'],USB_CC1_PROTECTED_PENDING:['U_CC_PROTECT.12','U_CC.1'],USB_CC2_PROTECTED_PENDING:['U_CC_PROTECT.11','U_CC.2']}))for(const p of required)assert.ok(pins(net).includes(p),`${net}: ${p}`)
assert.ok(pins('SYS_CANDIDATE').includes('U_LOGIC.10'));assert.ok(pins('SYS_CANDIDATE').includes('U_CHG.15'));assert.ok(!nets.some(n=>n.name==='SYS_INPUT'));assert.ok(pins('CC_SINK_CONFIG').includes('U_CC.3'));assert.ok(pins('CC_SINK_CONFIG').includes('R_CC_SINK0.1'));assert.ok(pins('USIM1_VDD_PENDING').includes('U_SIM_ESD.5'));assert.ok(pins('GND').includes('U_SIM_ESD.3'));assert.ok(pins('USIM1_DATA_SOCKET_PENDING').includes('U_SIM_ESD.4'));assert.ok(pins('CHARGE_REQUEST_MCU').includes('U_MCU.24'));assert.ok(pins('CHARGE_REQUEST_MCU').includes('U_CHARGE_AND.1'));assert.ok(pins('CHARGE_REQUEST_QUALIFIED_PENDING').includes('U_CHARGE_AND.4'));assert.ok(pins('CHARGE_REQUEST_QUALIFIED_PENDING').includes('Q_TEMP_REQUEST.1'));assert.ok(pins('CHARGE_REGN_SENSE').includes('U_CHARGE_POR.5'));assert.equal(all('pcb_component').length,0)
for(const [net,pad] of Object.entries({VLOGIC_3V15:2,MCU_EN:3,LCD_CS_N:23,LCD_RST_N:31,BACKLIGHT_PWM:35,HOST_TX:10,HOST_RX:11,HOST_RTS:8,HOST_CTS:9,BUTTON_INT_N:39,MODEM_STATUS_HOST_PENDING:38}))assert.ok(pins(net).includes('U_MCU.'+pad),net)
// Independently transcribed QuecOpen V1.0 interface pads; no land-pattern claim.
for(const [net,required] of Object.entries({MODEM_RX:['U_TX.4','U_MODEM_LOGICAL_ONLY.34'],MODEM_TX:['U_RX.4','U_MODEM_LOGICAL_ONLY.35'],MODEM_CTS:['U_CTS.4','U_MODEM_LOGICAL_ONLY.36'],MODEM_RTS:['U_RTS.4','U_MODEM_LOGICAL_ONLY.37'],USIM1_VDD_PENDING:['U_MODEM_LOGICAL_ONLY.43','C_SIM_VDD.1'],USIM1_RST_MODEM_PENDING:['U_MODEM_LOGICAL_ONLY.44'],USIM1_DATA_MODEM_PENDING:['U_MODEM_LOGICAL_ONLY.45'],USIM1_CLK_MODEM_PENDING:['U_MODEM_LOGICAL_ONLY.46'],MODEM_PWRKEY_OD:['U_MODEM_LOGICAL_ONLY.15','Q_MODEM_KEY.3'],MODEM_RESET_OD:['U_MODEM_LOGICAL_ONLY.17','Q_MODEM_RESET.3'],MODEM_STATUS:['U_MODEM_LOGICAL_ONLY.20','U_STATUS.4']})) for(const p of required)assert.ok(pins(net).includes(p),net+': '+p)
for(const name of ['U_DTR','U_RI'])assert.ok(!comps.some(c=>c.name===name),'startup-contention path must not be fitted')
assert.ok(!pins('MODEM_3V8_CANDIDATE').some(p=>p.startsWith('U_MODEM_LOGICAL_ONLY.')),'power gate must remain open')
for(const pin of [8,9,10,30,39,75,121,122]){
 const p=all('source_port').find(p=>p.source_component_id===comps.find(c=>c.name==='U_MODEM_LOGICAL_ONLY').source_component_id&&p.pin_number===pin)
 assert.ok(p);assert.ok(!all('source_trace').some(t=>t.connected_source_port_ids.includes(p.source_port_id)),`unverified modem endpoint ${pin} must stay open`)
}
for(const [net,pin] of Object.entries({USIM1_VDD_PENDING:1,USIM1_RST_SOCKET_PENDING:2,USIM1_CLK_SOCKET_PENDING:3,GND:5,USIM1_DATA_SOCKET_PENDING:7}))assert.ok(pins(net).includes('J_SIM_CANDIDATE.'+pin))
assert.equal(comps.find(c=>c.name==='J_SIM_CANDIDATE').manufacturer_part_number,'SIM8051-6-0-14-00-A')
assert.equal(comps.find(c=>c.name==='R_TEMP_HOT_INPUT').manufacturer_part_number,'RT0603BRD0710KL')
assert.equal(comps.find(c=>c.name==='R_FB_BOTTOM').manufacturer_part_number,'RT0603BRD07200KL')
assert.equal(comps.find(c=>c.name==='R_IDLE_TX').manufacturer_part_number,'RT0603BRD07100KL')
const adc=all('source_port').find(p=>p.source_component_id===comps.find(c=>c.name==='U_MCU').source_component_id&&p.pin_number===4)
assert.ok(adc);assert.ok(!all('source_trace').some(t=>t.connected_source_port_ids.includes(adc.source_port_id)),'ADC must remain disconnected pending isolation circuit')

for(const [net,required] of Object.entries({BUTTON_BRANCH_UNQUALIFIED:['SW3.1','U_BUTTON_BRANCH.2'],BUTTON_ENABLE_RAW:['U_BUTTON_BRANCH.6','U_BUTTON_EN_BUFFER.2','R_BUTTON_EN_DOWN.1'],LOGIC_ENABLE:['U_BUTTON_EN_BUFFER.4','U_LOGIC.12','R_EN_OFF.1'],BUTTON_INT_N:['U_BUTTON_BRANCH.5','U_MCU.39'],SYSTEM_OFF_REQUEST:['U_MCU.25','Q_BUTTON_KILL.1'],BUTTON_KILL_BRANCH:['U_BUTTON_BRANCH.8','Q_BUTTON_KILL.3']}))for(const pin of required)assert.ok(pins(net).includes(pin),`${net}: ${pin}`)
assert(!pins('ROW0').some(p=>p.startsWith('SW3.')));assert(!pins('COL2').some(p=>p.startsWith('SW3.')))
assert.equal(comps.find(x=>x.name==='R_BUTTON_EN_UP').resistance,10000)
assert(!pins('BUTTON_ENABLE_RAW').includes('U_LOGIC.12'),'buffer must separate raw enable from converter')
for(const [net,required] of Object.entries({MODEM_MICBIAS_PENDING:['U_MODEM_LOGICAL_ONLY.120','R_MIC_BIAS_TOP.1'],MODEM_MIC_P_PENDING:['U_MODEM_LOGICAL_ONLY.126','R_MIC_P_SERIES.1'],MODEM_MIC_N_PENDING:['U_MODEM_LOGICAL_ONLY.119','R_MIC_N_SERIES.1'],MIC_BIAS_UPPER_PENDING:['R_MIC_BIAS_TOP.2','C_MIC_BIAS.1','R_MIC_BIAS_P.1'],MIC_BIAS_LOWER_PENDING:['R_MIC_BIAS_BOTTOM.1','C_MIC_BIAS.2','R_MIC_BIAS_N.2'],MIC_P_FILTER_INPUT_PENDING:['C_MIC_P_AC.2','R_MIC_BIAS_P.2'],MIC_N_FILTER_INPUT_PENDING:['C_MIC_N_AC.2','R_MIC_BIAS_N.1']}))for(const pin of required)assert(pins(net).includes(pin),net+': '+pin)
assert(!pins('GND').includes('C_MIC_BIAS.2'),'bias bypass spans both bias rails, not ground')
assert(!pins('GND').includes('U_MODEM_LOGICAL_ONLY.119'),'differential microphone negative is not ground')
const rfManifest=JSON.parse(fs.readFileSync('sourcing/rf-population-v17.json','utf8'))
for(const [net,required] of Object.entries({ANT_MAIN_MATCH_IN_PENDING:['U_MODEM_LOGICAL_ONLY.60','R_RF_SERIES_CANDIDATE.1','RF_SHUNT_IN_DNP_RESERVE.1'],ANT_TO_RECEPTACLE_PENDING:['R_RF_SERIES_CANDIDATE.2','RF_SHUNT_OUT_DNP_RESERVE.1']}))for(const pin of required)assert(pins(net).includes(pin),net+': '+pin)
assert.equal(comps.find(x=>x.name==='R_RF_SERIES_CANDIDATE').resistance,0)
for(const name of ['RF_SHUNT_IN_DNP_RESERVE','RF_SHUNT_OUT_DNP_RESERVE']){
 assert.equal(rfManifest[name].default_population,'DO_NOT_POPULATE')
 assert.equal(rfManifest[name].MPN,null);assert.equal(rfManifest[name].capacitance,null)
 assert(!comps.find(x=>x.name===name).manufacturer_part_number)
 assert(pins('GND').includes(name+'.2'))
}
fs.writeFileSync('output/power-integrated-v45.circuit.json' ,JSON.stringify(j,null,2));fs.writeFileSync('output/power-integrated-v45-schematic.svg',convertCircuitJsonToSchematicSvg(j,{width:2400,height:1200}))
fs.writeFileSync('output/power-integration-v45-checks.json',JSON.stringify({components:comps.length,nets:nets.length,errors:[],scope:'logical connectivity; no electrical simulation or PCB release'},null,2));console.log('PASS: power shared-net integration')
