import React from 'react'
import '@tscircuit/core'
const n=(s:string)=>`net.${s}`
/** REGN-qualified host request. Independent analog temperature MOSFETs remain
 * in series with CE. Candidate only: power sequencing and watchdog not validated.
 */
export function ChargeEnableCandidate(){return <board name="CHARGE_ENABLE" width={56} height={144} routingDisabled>
 <chip name="U_CHARGE_POR" manufacturerPartNumber="TPS3808G01DBVR" pinLabels={{pin1:'RESET_N',pin2:'GND',pin3:'MR_N',pin4:'CT',pin5:'SENSE',pin6:'VDD'}} connections={{RESET_N:n('CHARGE_REGN_READY'),GND:n('GND'),MR_N:n('MCU_EN'),CT:n('CHARGE_POR_CT'),SENSE:n('CHARGE_REGN_SENSE'),VDD:n('VLOGIC_3V15')}}/>
 <chip name="U_CHARGE_AND" manufacturerPartNumber="SN74LVC1G08DBVR" schX={18} pinLabels={{pin1:'A',pin2:'B',pin3:'GND',pin4:'Y',pin5:'VCC'}} connections={{A:n('CHARGE_REQUEST_MCU'),B:n('CHARGE_REGN_READY'),GND:n('GND'),Y:n('CHARGE_REQUEST_QUALIFIED_PENDING'),VCC:n('VLOGIC_3V15')}}/>
 {[
 ['SENSE_TOP','845k','CHG_REGN','CHARGE_REGN_SENSE'],['SENSE_BOTTOM','100k','CHARGE_REGN_SENSE','GND'],['READY_PULLUP','10k','VLOGIC_3V15','CHARGE_REGN_READY'],['CT','100k','VLOGIC_3V15','CHARGE_POR_CT'],['REQUEST_OFF','100k','CHARGE_REQUEST_MCU','GND']
 ].map(([k,v,a,b],i)=><resistor key={k} name={`R_CHARGE_${k}`} resistance={v} schX={-20+i*10} schY={-12} connections={{pin1:n(a),pin2:n(b)}}/>)}
 <capacitor name="C_CHARGE_SENSE" capacitance="1nF" schX={-12} schY={12} connections={{pin1:n('CHARGE_REGN_SENSE'),pin2:n('GND')}}/>
 {['POR','AND'].map((k,i)=><capacitor key={k} name={`C_CHARGE_${k}`} manufacturerPartNumber="C0603C104K5RACTU" capacitance="100nF" schX={i*12} schY={12} connections={{pin1:n('VLOGIC_3V15'),pin2:n('GND')}}/>)}
</board>}
