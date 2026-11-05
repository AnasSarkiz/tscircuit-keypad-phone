import React from 'react'
import '@tscircuit/core'
import {DDC0006A} from './footprints'
const n=(s:string)=>`net.${s}`
export function BacklightBoost(){
return <board name="BACKLIGHT_BOOST_CANDIDATE" width={56} height={144} routingDisabled>
 <chip name="U_BL_BOOST" footprint={<DDC0006A/>} manufacturerPartNumber="TPS61073DDCR" pinLabels={{pin1:'SW',pin2:'GND',pin3:'EN',pin4:'FB',pin5:'VOUT',pin6:'VBAT'}} connections={{SW:n('BL_SW'),GND:n('GND'),EN:n('BL_BOOST_ENABLE_PENDING'),FB:n('BL_FB'),VOUT:n('BACKLIGHT_5V_PENDING'),VBAT:n('SYS_CANDIDATE')}}/>
 <inductor name="L_BL" inductance="4.7uH" manufacturerPartNumber="744031004" schY={10} connections={{pin1:n('SYS_CANDIDATE'),pin2:n('BL_SW')}}/>
 {['IN1','IN2','OUT1','OUT2','OUT3','OUT4'].map((k,i)=><capacitor key={k} name={`C_BL_${k}`} capacitance="4.7uF" schX={-15+(i%3)*8} schY={16+Math.floor(i/3)*5} connections={{pin1:n(k.startsWith('IN')?'SYS_CANDIDATE':'BACKLIGHT_5V_PENDING'),pin2:n('GND')}}/>)}
 <resistor name="R_BL_TOP" resistance="909k" schX={-8} schY={-10} connections={{pin1:n('BACKLIGHT_5V_PENDING'),pin2:n('BL_FB')}}/>
 <resistor name="R_BL_BOTTOM" resistance="100k" schY={-10} connections={{pin1:n('BL_FB'),pin2:n('GND')}}/>
 <resistor name="R_BL_DISABLE" resistance="100k" schX={8} schY={-10} connections={{pin1:n('BL_BOOST_ENABLE_PENDING'),pin2:n('GND')}}/>
</board>
}
// TLV9032 Rev H removes POR; startup/brownout outputs and fault latency are unqualified.
// Additional window on existing 103AT-2/5.3k/31.14k TS network.
// Approximate 20..35 C, intentionally narrow. Does not replace sensor attachment
// validation, reference curve qualification, POR supervision or USB qualification.
export function ChargeTemperatureGuard(){
return <board name="CHARGE_GUARD_CANDIDATE" width={56} height={144} routingDisabled>
 <chip name="U_TEMP" manufacturerPartNumber="TLV9032DR" pinLabels={{pin1:'COLD_OK',pin2:'A_MINUS',pin3:'A_PLUS',pin4:'GND',pin5:'B_PLUS',pin6:'B_MINUS',pin7:'HOT_OK',pin8:'VDD'}} connections={{COLD_OK:n('TEMP_COLD_OK'),A_MINUS:n('BAT_NTC'),A_PLUS:n('TEMP_COLD_REF'),GND:n('GND'),B_PLUS:n('TEMP_HOT_SENSE'),B_MINUS:n('TEMP_HOT_REF'),HOT_OK:n('TEMP_HOT_OK'),VDD:n('CHG_REGN')}}/>
 <capacitor name="C_TEMP" manufacturerPartNumber="C0603C104K5RACTU" capacitance="100nF" schY={10} connections={{pin1:n('CHG_REGN'),pin2:n('GND')}}/>
 {[
 ['COLD_TOP','60.4k','CHG_REGN','TEMP_COLD_REF'],['COLD_BOTTOM','100k','TEMP_COLD_REF','GND'],['COLD_HYST','10M','TEMP_COLD_OK','TEMP_COLD_REF'],
 ['HOT_TOP','93.1k','CHG_REGN','TEMP_HOT_REF'],['HOT_BOTTOM','100k','TEMP_HOT_REF','GND'],['HOT_INPUT','10k','BAT_NTC','TEMP_HOT_SENSE'],['HOT_HYST','10M','TEMP_HOT_OK','TEMP_HOT_SENSE'],
 ['COLD_GATE','100k','TEMP_COLD_OK','GND'],['HOT_GATE','100k','TEMP_HOT_OK','GND'],['REQUEST_OFF','100k','CHARGE_REQUEST_QUALIFIED_PENDING','GND']
 ].map(([name,val,a,b],i)=><resistor key={name} name={`R_TEMP_${name}`} resistance={val} schX={-20+(i%5)*9} schY={-15-Math.floor(i/5)*5} connections={{pin1:n(a),pin2:n(b)}}/>)}
 {/* Series NMOS sink of active-low CE. Explicit S/D mapping preserves body-diode blocking. */}
 {[
 ['COLD','TEMP_COLD_OK','CHARGE_DISABLE','CE_MID1'],['HOT','TEMP_HOT_OK','CE_MID1','CE_MID2'],['REQUEST','CHARGE_REQUEST_QUALIFIED_PENDING','CE_MID2','GND']
 ].map(([k,g,d,s],i)=><chip key={k} name={`Q_TEMP_${k}`} manufacturerPartNumber="AO3400A" schX={-10+i*10} schY={20} pinLabels={{pin1:'G',pin2:'S',pin3:'D'}} connections={{G:n(g),S:n(s),D:n(d)}}/>)}
</board>
}
