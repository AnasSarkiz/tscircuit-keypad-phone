import React from 'react'
import {ModemLandCandidate} from './modem-footprint'
import '@tscircuit/core'
const n=(v:string)=>`net.${v}`
// Historical logical subset retained; additional physical pads remain explicitly
// UNREVIEWED, not NC. Exact candidate identity matches the imported catalog part.
// This does not approve its firmware/VoLTE profile, optional interfaces or power path;
// see qualification-modem-supply/. Do not infer QuecOpen from the former placeholder MPN.
const grounds=[3,31,48,50,54,55,58,59,61,62,67,68,69,70,71,72,73,74,79,80,81,82,89,90,91,100,101,102]
export const modemPins:Record<number,string>={...Object.fromEntries(Array.from({length:126},(_,i)=>[i+1,`UNREVIEWED_${i+1}`])),8:'USB_VBUS',9:'USB_DP',10:'USB_DM',15:'PWRKEY',17:'RESET_N',20:'STATUS',21:'NET_STATUS',22:'DBG_RXD',23:'DBG_TXD',29:'VDD_EXT',30:'DTR_UNVERIFIED',32:'VBAT_BB1',33:'VBAT_BB2',34:'RXD',35:'TXD',36:'CTS',37:'RTS',39:'RI_UNVERIFIED',42:'SIM_DET',43:'SIM_VDD',44:'SIM_RST',45:'SIM_DATA',46:'SIM_CLK',47:'SIM_GND',52:'VBAT_RF1',53:'VBAT_RF2',60:'ANT_MAIN',75:'USB_BOOT',119:'MIC_N',120:'MICBIAS',121:'SPK_P',122:'SPK_N',126:'MIC_P',...Object.fromEntries(grounds.map(p=>[p,`GND${p}`]))}
const connections:Record<string,string>={MIC_P:'MODEM_MIC_P_PENDING',MIC_N:'MODEM_MIC_N_PENDING',MICBIAS:'MODEM_MICBIAS_PENDING',ANT_MAIN:'ANT_MAIN_MATCH_IN_PENDING',PWRKEY:'MODEM_PWRKEY_OD',RESET_N:'MODEM_RESET_OD',STATUS:'MODEM_STATUS',VDD_EXT:'MODEM_VDD_EXT_1V8',RXD:'MODEM_RX',TXD:'MODEM_TX',CTS:'MODEM_CTS',RTS:'MODEM_RTS',SIM_VDD:'USIM1_VDD_PENDING',SIM_RST:'USIM1_RST_MODEM_PENDING',SIM_DATA:'USIM1_DATA_MODEM_PENDING',SIM_CLK:'USIM1_CLK_MODEM_PENDING',SIM_GND:'GND',VBAT_BB1:'MODEM_BB_SUPPLY_UNQUALIFIED',VBAT_BB2:'MODEM_BB_SUPPLY_UNQUALIFIED',VBAT_RF1:'MODEM_RF_SUPPLY_UNQUALIFIED',VBAT_RF2:'MODEM_RF_SUPPLY_UNQUALIFIED',...Object.fromEntries(grounds.map(p=>[`GND${p}`,'GND']))}
export function ModemSupportCandidate(){return <board name="MODEM_SUPPORT_UNRELEASED" width={56} height={144} routingDisabled>
 <chip name="U_MODEM_LOGICAL_ONLY" manufacturerPartNumber="EG912UGLAC-I05-SNNSA" supplierPartNumbers={{jlcpcb:["C7472750"]}} footprint={<ModemLandCandidate/>} pinLabels={Object.fromEntries(Object.entries(modemPins).map(([p,l])=>['pin'+p,l]))} connections={Object.fromEntries(Object.entries(connections).map(([p,v])=>[p,n(v)]))}/>
 <capacitor name="C_MODEM_VDD_EXT" capacitance="2.2uF" schX={-24} schY={20} connections={{pin1:n('MODEM_VDD_EXT_1V8'),pin2:n('GND')}}/>
 {(['KEY','RESET'] as const).map((s,i)=><group key={s} name={`MODEM_${s}_DRIVER`} schX={i*40} schY={-40}>
  {/* Gate load must remain within100uA for the near-rail VOH bound; ramp/off-state and MOSFET leakage remain qualification gates. */}
  <chip name={`U_MODEM_${s}_BUF`} manufacturerPartNumber="SN74LVC1G17DBVR" pinLabels={{pin1:'NC',pin2:'A',pin3:'GND',pin4:'Y',pin5:'VCC'}} connections={{A:n(s==='KEY'?'ON_OFF_MCU':'RESET_MCU'),GND:n('GND'),Y:n(`MODEM_${s}_GATE`),VCC:n('VLOGIC_3V15')}}/>
  <chip name={`Q_MODEM_${s}`} manufacturerPartNumber="AO3400A" schX={12} pinLabels={{pin1:'G',pin2:'S',pin3:'D'}} connections={{G:n(`MODEM_${s}_GATE`),S:n('GND'),D:n(s==='KEY'?'MODEM_PWRKEY_OD':'MODEM_RESET_OD')}}/>
  <resistor name={`R_MODEM_${s}_INPUT_OFF`} resistance="10k" schX={-12} connections={{pin1:n(s==='KEY'?'ON_OFF_MCU':'RESET_MCU'),pin2:n('GND')}}/>
  <resistor name={`R_MODEM_${s}_GATE_OFF`} resistance="39k" manufacturerPartNumber="RC0603FR-0739KL" schX={12} schY={-8} connections={{pin1:n(`MODEM_${s}_GATE`),pin2:n('GND')}}/>
  <capacitor name={`C_MODEM_${s}_BUF`} manufacturerPartNumber="C0603C104K5RACTU" capacitance="100nF" schX={-12} schY={8} connections={{pin1:n('VLOGIC_3V15'),pin2:n('GND')}}/>
 </group>)}
 {/* Supply rails intentionally not connected to buck: overall supply capability
     is2A LTE-only /3A GSM perV1.0; selected battery/power path is unqualified.
     USB/earpiece/debug/recovery remain open. Microphone bias/AC coupling added; microphone RF filtering and load unresolved. RF matching added but antenna routing incomplete. */}
</board>}
