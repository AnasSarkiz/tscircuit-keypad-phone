import React from 'react'
import '@tscircuit/core'
const n=(s:string)=>`net.${s}`
// CC detection ONLY. Not a complete USB power/protection circuit.
// AUX3V3 must start independently from protected VBUS, even with a dead battery.
export function UsbCCCandidate({highVoltage=false}:{highVoltage?:boolean}={}){return <board name="USB_CC_CANDIDATE" width={56} height={144} routingDisabled>
 <chip name="U_CC" manufacturerPartNumber={highVoltage?"HUSB320-BA000-QN12R":"TUSB320LAIRWBR"} pinLabels={{pin1:'CC1',pin2:'CC2',pin3:'PORT',pin4:'VBUS_DET',pin5:'ADDR_NC',pin6:'OUT3',pin7:'OUT1',pin8:'OUT2',pin9:'ID_NC',pin10:'GND',pin11:'EN_N',pin12:'VDD'}} connections={{CC1:n('USB_CC1_PROTECTED_PENDING'),CC2:n('USB_CC2_PROTECTED_PENDING'),PORT:n(highVoltage?'CC_SINK_CONFIG':'GND'),VBUS_DET:n('CC_VBUS_SENSE'),OUT3:n('CC_NO_AUDIO_ACCESSORY'),OUT1:n('CC_OUT1'),OUT2:n('CC_OUT2'),GND:n('GND'),EN_N:n('GND'),VDD:n('USB_AUX3V3_PENDING')}}/>
 <resistor name="R_CC_VBUS" resistance={highVoltage?"0":"887k"} schY={10} connections={{pin1:n('USB_VBUS_RAW'),pin2:n('CC_VBUS_SENSE')}}/>
 {highVoltage&&[0,1,2].map(i=><resistor key={`sink${i}`} name={`R_CC_SINK${i}`} manufacturerPartNumber="RC0603FR-07300KL" resistance="300k" schX={-12} schY={i*5} connections={{pin1:n(i===0?'CC_SINK_CONFIG':`CC_SINK_CHAIN${i}`),pin2:n(i===2?'GND':`CC_SINK_CHAIN${i+1}`)}}/>)}
 {['OUT1','OUT2','NO_AUDIO_ACCESSORY'].map((k,i)=><resistor key={k} name={`R_CC_${k}`} resistance="10k" schX={-10+i*10} schY={-12} connections={{pin1:n('USB_AUX3V3_PENDING'),pin2:n(`CC_${k}`)}}/>)}
 <capacitor name="C_CC" manufacturerPartNumber="C0603C104K5RACTU" capacitance="100nF" schX={12} connections={{pin1:n('USB_AUX3V3_PENDING'),pin2:n('GND')}}/>
</board>}
// 3 A advertised-source branch. This switch does not itself qualify CC current.
// EN pulled down and driven through 100k by UsbStartup, directly clamped by POR.
// Physical ramp and source-downgrade timing remain bench checks.
export function UsbInputProtectionCandidate(){return <board name="USB_INPUT_PROTECTION_CANDIDATE" width={56} height={144} routingDisabled>
 <chip name="U_USB_PROTECT" manufacturerPartNumber="TPS259470LRPWR" pinLabels={{pin1:'EN',pin2:'OVLO',pin3:'AUXOFF_NC',pin4:'FAULT',pin5:'IN',pin6:'OUT',pin7:'DVDT',pin8:'GND',pin9:'ILM',pin10:'ITIMER_NC'}} connections={{EN:n('USB_3A_ENABLE_PENDING'),OVLO:n('USB_OVLO'),FAULT:n('USB_FAULT_N'),IN:n('USB_VBUS_RAW'),OUT:n('USB_5V_QUALIFIED'),DVDT:n('USB_DVDT'),GND:n('GND'),ILM:n('USB_ILM')}}/>
 {[
 ['OFF','1M','USB_3A_ENABLE_PENDING','GND'],['OV_TOP','402k','USB_VBUS_RAW','USB_OVLO'],['OV_BOTTOM','100k','USB_OVLO','GND'],['ILM','1.65k','USB_ILM','GND'],['FAULT','100k','USB_AUX3V3_PENDING','USB_FAULT_N']
 ].map(([k,val,a,b],i)=><resistor key={k} name={`R_USB_${k}`} resistance={val} schX={-18+i*9} schY={-10} connections={{pin1:n(a),pin2:n(b)}}/>)}
 <capacitor name="C_USB_DVDT" capacitance="3.3nF" schY={12} connections={{pin1:n('USB_DVDT'),pin2:n('GND')}}/>
 <capacitor name="C_USB_RAW" capacitance="1uF" schX={12} connections={{pin1:n('USB_VBUS_RAW'),pin2:n('GND')}}/>
</board>}
