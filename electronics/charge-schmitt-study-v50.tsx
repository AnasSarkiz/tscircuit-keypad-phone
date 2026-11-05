import React from 'react'
import '@tscircuit/core'
/** Isolated candidate. Valid-rail Schmitt AND only; startup and charge-disable not qualified. */
export function ChargeSchmittStudyV50(){return <board name="CHARGE_SCHMITT_NOT_INTEGRATED" width={56} height={144} routingDisabled>
 <chip name="U_ALT_CHARGE_SCHMITT" manufacturerPartNumber="SN74LVC1G97DBVR" pinLabels={{pin1:'IN1',pin2:'GND',pin3:'IN0',pin4:'Y',pin5:'VCC',pin6:'IN2'}} connections={{IN1:'net.ALT_GND',GND:'net.ALT_GND',IN0:'net.ALT_REQUEST',Y:'net.ALT_CHARGE_GATE_UNQUALIFIED',VCC:'net.ALT_VLOGIC_PENDING',IN2:'net.ALT_REGN_READY'}}/>
 <chip name="U_ALT_CHARGE_POR" manufacturerPartNumber="TPS3808G01DBVR" pinLabels={{pin1:'RESET_N',pin2:'GND',pin3:'MR_N',pin4:'CT',pin5:'SENSE',pin6:'VDD'}} connections={{RESET_N:'net.ALT_REGN_READY',GND:'net.ALT_GND',MR_N:'net.ALT_MCU_EN_PENDING',CT:'net.ALT_CT',SENSE:'net.ALT_REGN_SENSE',VDD:'net.ALT_VLOGIC_PENDING'}}/>
 {[
 ['READY','10k','ALT_VLOGIC_PENDING','ALT_REGN_READY','RC0603FR-0710KL'],
 ['REQUEST_OFF','100k','ALT_REQUEST','ALT_GND','RT0603BRD07100KL'],
 ['OUTPUT_OFF','100k','ALT_CHARGE_GATE_UNQUALIFIED','ALT_GND','RT0603BRD07100KL'],
 ['SENSE_TOP','845k','ALT_CHG_REGN_PENDING','ALT_REGN_SENSE','RT0603BRD07845KL'],
 ['SENSE_BOTTOM','100k','ALT_REGN_SENSE','ALT_GND','RT0603BRD07100KL'],
 ['CT','100k','ALT_VLOGIC_PENDING','ALT_CT','RT0603BRD07100KL']
 ].map(([name,value,a,b,mpn])=><resistor key={name} name={'R_ALT_'+name} resistance={value} manufacturerPartNumber={mpn} connections={{pin1:'net.'+a,pin2:'net.'+b}}/>)}
 {['SCHMITT','POR'].map(name=><capacitor key={name} name={'C_ALT_'+name} capacitance="100nF" manufacturerPartNumber="C0603C104K5RACTU" connections={{pin1:'net.ALT_VLOGIC_PENDING',pin2:'net.ALT_GND'}}/>)}
 <capacitor name="C_ALT_SENSE" capacitance="1nF" manufacturerPartNumber="C0603C102J5GACTU" connections={{pin1:'net.ALT_REGN_SENSE',pin2:'net.ALT_GND'}}/>
</board>}
