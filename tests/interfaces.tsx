import React from 'react'
import fs from 'node:fs'
import assert from 'node:assert/strict'
import {Circuit} from '@tscircuit/core'
import {convertCircuitJsonToSchematicSvg} from 'circuit-to-svg'
import {ModemLogic,LogicSupply,channels} from '../electronics/interfaces'
import {DisplayInterface,ChargerCandidate} from '../electronics/front-end'
import {ModemBuckCandidate,BacklightSinkCandidate} from '../electronics/power-v4'
import {BacklightBoost,ChargeTemperatureGuard} from '../electronics/power-v5'
import {UsbCCCandidate,UsbInputProtectionCandidate} from '../electronics/usb-c'
import {UsbStartup,UsbCCProtection} from '../electronics/usb-startup'
const reports=[]
for(const [name,element] of [['modem-logic',<ModemLogic/>],['logic-supply',<LogicSupply/>],['display-interface',<DisplayInterface/>],['charger-candidate',<ChargerCandidate/>],['modem-buck-candidate',<ModemBuckCandidate/>],['backlight-sink-candidate',<BacklightSinkCandidate/>],['backlight-boost',<BacklightBoost/>],['charge-temperature-guard',<ChargeTemperatureGuard/>],['usb-cc-candidate',<UsbCCCandidate/>],['flat-pack-charger',<ChargerCandidate flatPack/>],['usb-input-protection',<UsbInputProtectionCandidate/>],['usb-startup',<UsbStartup/>],['usb-cc-protection',<UsbCCProtection/>]] as const){
 const c=new Circuit({platform:{pcbDisabled:true}})
 c.add(element);await c.renderUntilSettled();const j:any[]=c.getCircuitJson()
 const all=(t:string)=>j.filter(x=>x.type===t)
 const pinNet=(component:string,pin:number)=>{
  const comp=all('source_component').find(x=>x.name===component);assert.ok(comp,component)
  const p=all('source_port').find(x=>x.source_component_id===comp.source_component_id&&x.pin_number===pin);assert.ok(p,`${component}.${pin}`)
  const traces=all('source_trace').filter(x=>x.connected_source_port_ids.includes(p.source_port_id))
  return [...new Set(traces.flatMap(t=>t.connected_source_net_ids.map((id:string)=>all('source_net').find(x=>x.source_net_id===id).name)))].sort()
 }
 const check=(c:string,p:number,n:string)=>assert.deepEqual(pinNet(c,p),[n],`${c}.${p}`)
 if(name==='modem-logic')for(const ch of channels){
  check(`U_${ch.name}`,1,'VLOGIC_3V15');check(`U_${ch.name}`,2,'GND');check(`U_${ch.name}`,3,ch.host);check(`U_${ch.name}`,4,ch.modem);check(`U_${ch.name}`,5,ch.toModem?'VLOGIC_3V15':'GND');check(`U_${ch.name}`,6,'MODEM_VDD_EXT_1V8')
 }
 else if(name==='logic-supply') {
  const expected=['SYS_INPUT','GND','LOGIC_FB','VLOGIC_3V15','VLOGIC_3V15','SW_L2','SW_L2','SW_L1','SW_L1','SYS_INPUT','SYS_INPUT','LOGIC_ENABLE','SYS_INPUT','LOGIC_POWER_GOOD','GND']
  expected.forEach((n,i)=>check('U_LOGIC',i+1,n))
  check('L_LOGIC',1,'SW_L1');check('L_LOGIC',2,'SW_L2');check('R_FB_TOP',1,'VLOGIC_3V15');check('R_FB_TOP',2,'LOGIC_FB_SERIES');check('R_FB_TRIM',1,'LOGIC_FB_SERIES');check('R_FB_TRIM',2,'LOGIC_FB');check('R_FB_BOTTOM',1,'LOGIC_FB');check('R_FB_BOTTOM',2,'GND')
 }
 if(name==='display-interface'){
  const expected:Record<number,string>={1:'GND',2:'VLOGIC_3V15',3:'VLOGIC_3V15',4:'LCD_CS_N',5:'LCD_RST_N',6:'LCD_SDIO',7:'GND',8:'LCD_DC',9:'LCD_SCL',10:'GND',11:'VLOGIC_3V15',17:'BACKLIGHT_ANODE_PENDING',18:'BACKLIGHT_SINK1_PENDING',19:'BACKLIGHT_SINK2_PENDING',20:'GND'}
  for(const [p,n] of Object.entries(expected))check('J_LCD',Number(p),n)
  for(const p of [12,13,14,15,16,21,22,23,24])assert.deepEqual(pinNet('J_LCD',p),[],`LCD NC ${p}`)
 }
 if(name==='charger-candidate'||name==='flat-pack-charger'){
  const expected:Record<number,string>={1:'USB_5V_QUALIFIED',5:'CHARGE_STATUS_N',6:'GND',7:'USB_GOOD_N',8:'CHARGER_ILIM',9:'CHARGE_DISABLE',10:'CHARGER_ICHG',11:'BAT_NTC',12:'CHARGER_VSET',13:'PACK_POS',14:'PACK_POS',15:'SYS_CANDIDATE',16:'SYS_CANDIDATE',17:'GND',18:'GND',19:'CHG_SW',20:'CHG_SW',21:'CHG_BOOT',22:'CHG_REGN',23:'CHG_PMID',24:'USB_5V_QUALIFIED',25:'GND'}
  for(const [p,n] of Object.entries(expected))check('U_CHG',Number(p),n)
  for(const p of [2,3,4])assert.deepEqual(pinNet('U_CHG',p),[],`charger unused ${p}`)
  check('R_CHG_DISABLE',1,'SYS_CANDIDATE');check('R_CHG_DISABLE',2,'CHARGE_DISABLE')
  check('R_CHG_VSET',1,'CHARGER_VSET');check('R_CHG_VSET',2,'GND')
  check('R_CHG_TS_BOTTOM',1,'BAT_NTC');check('R_CHG_TS_BOTTOM',2,'TS_SERIES');check('R_CHG_TS_TRIM',1,'TS_SERIES');check('R_CHG_TS_TRIM',2,'GND')
  check('NTC_EXTERNAL',1,'BAT_NTC');check('NTC_EXTERNAL',2,'GND')
  assert.ok(!all('source_net').some(n=>n.name==='MODEM_VBAT'),'unqualified SYS must not feed modem')
 }
 if(name==='modem-buck-candidate'){
  ['MODEM_SUPPLY_ENABLE_PENDING','MODEM_SUPPLY_GOOD','MODEM_FB','GND','MODEM_SW','SYS_CANDIDATE'].forEach((n,i)=>check('U_MODEM_BUCK',i+1,n))
  check('L_MODEM',1,'MODEM_SW');check('L_MODEM',2,'MODEM_3V8_CANDIDATE');check('R_MODEM_ENABLE',2,'GND')
  check('C_MODEM_FF',1,'MODEM_3V8_CANDIDATE');check('C_MODEM_FF',2,'MODEM_FB')
 }
 if(name==='backlight-sink-candidate'){
  check('U_BACKLIGHT',1,'BACKLIGHT_SINK1_PENDING');check('U_BACKLIGHT',2,'BACKLIGHT_SINK2_PENDING')
  for(const p of [3,4])assert.deepEqual(pinNet('U_BACKLIGHT',p),[])
  check('U_BACKLIGHT',5,'GND');check('U_BACKLIGHT',6,'BACKLIGHT_PWM');check('U_BACKLIGHT',7,'BACKLIGHT_5V_PENDING');check('U_BACKLIGHT',8,'BACKLIGHT_RSET')
 }
 if(name==='backlight-boost'){
 ['BL_SW','GND','BL_BOOST_ENABLE_PENDING','BL_FB','BACKLIGHT_5V_PENDING','SYS_CANDIDATE'].forEach((n,i)=>check('U_BL_BOOST',i+1,n))
 check('L_BL',1,'SYS_CANDIDATE');check('L_BL',2,'BL_SW')
 }
 if(name==='charge-temperature-guard'){
 ['TEMP_COLD_OK','BAT_NTC','TEMP_COLD_REF','GND','TEMP_HOT_SENSE','TEMP_HOT_REF','TEMP_HOT_OK','CHG_REGN'].forEach((n,i)=>check('U_TEMP',i+1,n))
 check('Q_TEMP_COLD',3,'CHARGE_DISABLE');check('Q_TEMP_COLD',2,'CE_MID1');check('Q_TEMP_HOT',3,'CE_MID1');check('Q_TEMP_HOT',2,'CE_MID2');check('Q_TEMP_REQUEST',3,'CE_MID2');check('Q_TEMP_REQUEST',2,'GND');check('Q_TEMP_REQUEST',1,'CHARGE_REQUEST_QUALIFIED_PENDING')
 }
 if(name==='usb-cc-candidate'){
 const expected:Record<number,string>={1:'USB_CC1_PROTECTED_PENDING',2:'USB_CC2_PROTECTED_PENDING',3:'GND',4:'CC_VBUS_SENSE',6:'CC_NO_AUDIO_ACCESSORY',7:'CC_OUT1',8:'CC_OUT2',10:'GND',11:'GND',12:'USB_AUX3V3_PENDING'}
 for(const [p,n] of Object.entries(expected))check('U_CC',+p,n)
 for(const p of [5,9])assert.deepEqual(pinNet('U_CC',p),[])
 check('R_CC_VBUS',1,'USB_VBUS_RAW');check('R_CC_VBUS',2,'CC_VBUS_SENSE')
 }
 if(name==='usb-input-protection'){
 const expected:Record<number,string>={1:'USB_3A_ENABLE_PENDING',2:'USB_OVLO',4:'USB_FAULT_N',5:'USB_VBUS_RAW',6:'USB_5V_QUALIFIED',7:'USB_DVDT',8:'GND',9:'USB_ILM'}
 for(const [p,n] of Object.entries(expected))check('U_USB_PROTECT',+p,n)
 for(const p of [3,10])assert.deepEqual(pinNet('U_USB_PROTECT',p),[])
 check('R_USB_OFF',1,'USB_3A_ENABLE_PENDING');check('R_USB_OFF',2,'GND')
 }
 if(name==='usb-startup'){
 check('U_USB_AUX',1,'USB_VBUS_RAW');check('U_USB_AUX',2,'GND');check('U_USB_AUX',5,'USB_AUX3V3_PENDING')
 for(const p of [3,4])assert.deepEqual(pinNet('U_USB_AUX',p),[])
 ;['USB_3A_ENABLE_PENDING','GND','USB_CC_FAULT_N','USB_POR_CT','USB_POR_SENSE','USB_AUX3V3_PENDING'].forEach((n,i)=>check('U_USB_POR',i+1,n))
 ;['CC_OUT1','CC_OUT2','GND','USB_3A_LOGIC','USB_AUX3V3_PENDING'].forEach((n,i)=>check('U_USB_3A',i+1,n))
 check('R_USB_3A_DRIVE',1,'USB_3A_LOGIC');check('R_USB_3A_DRIVE',2,'USB_3A_ENABLE_PENDING')
 }
 if(name==='usb-cc-protection'){
 const m:Record<number,string>={3:'USB_CC_VBIAS',4:'USB_CC1_RAW',5:'USB_CC2_RAW',6:'USB_CC2_RAW',7:'USB_CC1_RAW',8:'GND',9:'USB_CC_FAULT_N',10:'USB_AUX3V3_PENDING',11:'USB_CC2_PROTECTED_PENDING',12:'USB_CC1_PROTECTED_PENDING',13:'GND',16:'GND',17:'GND',18:'GND',19:'GND',20:'GND',21:'GND'}
 for(const [p,n] of Object.entries(m))check('U_CC_PROTECT',+p,n)
 for(const p of [1,2,14,15])assert.deepEqual(pinNet('U_CC_PROTECT',p),[])
 }
 const errors=j.filter(x=>/error$/.test(x.type));assert.deepEqual(errors,[])
 assert.equal(all('pcb_component').length,0)
 fs.writeFileSync(`output/${name}.circuit.json`,JSON.stringify(j,null,2))
 fs.writeFileSync(`output/${name}-schematic.svg`,convertCircuitJsonToSchematicSvg(j,{width:1800,height:1600}))
 reports.push({sheet:name,components:all('source_component').length,errors,scope:'pin/net contract only; no PCB, electrical simulation or hardware validation'})
}
fs.writeFileSync('output/interface-checks.json',JSON.stringify(reports,null,2));console.log(reports)
