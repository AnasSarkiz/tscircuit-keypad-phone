import React from 'react'
import '@tscircuit/core'
const n=(s:string)=>`net.${s}`
// Candidate steady-state regulation, NOT independent fault overvoltage protection.
// EN remains pulled down until low-cell supervisor/startup sequencing is designed.
export function ModemBuckCandidate(){
 return <board name="MODEM_BUCK_CANDIDATE" width={56} height={144} routingDisabled>
 <chip name="U_MODEM_BUCK" manufacturerPartNumber="TPS62827ADMQR" pinLabels={{pin1:'EN',pin2:'PG',pin3:'FB',pin4:'GND',pin5:'SW',pin6:'VIN'}} connections={{EN:n('MODEM_SUPPLY_ENABLE_PENDING'),PG:n('MODEM_SUPPLY_GOOD'),FB:n('MODEM_FB'),GND:n('GND'),SW:n('MODEM_SW'),VIN:n('SYS_CANDIDATE')}}/>
 <inductor name="L_MODEM" inductance="470nH" manufacturerPartNumber="XFL4015-471MEC" schY={10} connections={{pin1:n('MODEM_SW'),pin2:n('MODEM_3V8_CANDIDATE')}}/>
 {[
 ['C_MODEM_IN','4.7uF','SYS_CANDIDATE','GND'],['C_MODEM_OUT1','10uF','MODEM_3V8_CANDIDATE','GND'],['C_MODEM_OUT2','10uF','MODEM_3V8_CANDIDATE','GND'],['C_MODEM_FF','120pF','MODEM_3V8_CANDIDATE','MODEM_FB']
 ].map(([name,value,a,b],i)=><capacitor key={name} name={name} capacitance={value} schX={-14+i*8} schY={15} connections={{pin1:n(a),pin2:n(b)}}/>)}
 {[
 ['R_MODEM_TOP','536k','MODEM_3V8_CANDIDATE','MODEM_FB'],['R_MODEM_BOTTOM','100k','MODEM_FB','GND'],['R_MODEM_ENABLE','100k','MODEM_SUPPLY_ENABLE_PENDING','GND'],['R_MODEM_PG','100k','VLOGIC_3V15','MODEM_SUPPLY_GOOD']
 ].map(([name,value,a,b],i)=><resistor key={name} name={name} resistance={value} schX={-14+i*8} schY={-12} connections={{pin1:n(a),pin2:n(b)}}/>)}
 </board>
}
// Needs an independently designed 5 V boost source. Two separate sinks prevent
// unbalanced parallel cathodes. LCD branch current ratings remain a supplier gate.
export function BacklightSinkCandidate(){
 return <board name="BACKLIGHT_SINK_CANDIDATE" width={56} height={144} routingDisabled>
 <chip name="U_BACKLIGHT" manufacturerPartNumber="CAT4104V-GT3" pinLabels={{pin1:'LED1',pin2:'LED2',pin3:'LED3_UNUSED',pin4:'LED4_UNUSED',pin5:'GND',pin6:'PWM',pin7:'VIN',pin8:'RSET'}} connections={{LED1:n('BACKLIGHT_SINK1_PENDING'),LED2:n('BACKLIGHT_SINK2_PENDING'),GND:n('GND'),PWM:n('BACKLIGHT_PWM'),VIN:n('BACKLIGHT_5V_PENDING'),RSET:n('BACKLIGHT_RSET')}}/>
 <resistor name="R_BACKLIGHT_SET" resistance="3.16k" schY={9} connections={{pin1:n('BACKLIGHT_RSET'),pin2:n('GND')}}/>
 <resistor name="R_BACKLIGHT_OFF" resistance="100k" schY={-9} connections={{pin1:n('BACKLIGHT_PWM'),pin2:n('GND')}}/>
 <capacitor name="C_BACKLIGHT" manufacturerPartNumber="C0603C104K5RACTU" capacitance="100nF" schX={12} connections={{pin1:n('BACKLIGHT_5V_PENDING'),pin2:n('GND')}}/>
 </board>
}
