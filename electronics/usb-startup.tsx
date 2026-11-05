import React from 'react'
import '@tscircuit/core'
const n=(s:string)=>`net.${s}`
/** Independent raw-VBUS auxiliary supply and supervisor-clamped 3 A qualifier.
 * No MCU or battery required to qualify the main input. Bench validation pending.
 */
export function UsbStartup(){return <board name="USB_STARTUP" width={56} height={144} routingDisabled>
 <chip name="U_USB_AUX" manufacturerPartNumber="TPS70933DBVR" pinLabels={{pin1:'IN',pin2:'GND',pin3:'EN_NC',pin4:'NC',pin5:'OUT'}} connections={{IN:n('USB_VBUS_RAW'),GND:n('GND'),OUT:n('USB_AUX3V3_PENDING')}}/>
 <chip name="U_USB_POR" manufacturerPartNumber="TPS3808G01DBVR" schX={-12} pinLabels={{pin1:'RESET_N',pin2:'GND',pin3:'MR_N',pin4:'CT',pin5:'SENSE',pin6:'VDD'}} connections={{RESET_N:n('USB_3A_ENABLE_PENDING'),GND:n('GND'),MR_N:n('USB_CC_FAULT_N'),CT:n('USB_POR_CT'),SENSE:n('USB_POR_SENSE'),VDD:n('USB_AUX3V3_PENDING')}}/>
 <chip name="U_USB_3A" manufacturerPartNumber="SN74LVC1G02DBVR" schX={12} pinLabels={{pin1:'A',pin2:'B',pin3:'GND',pin4:'Y',pin5:'VCC'}} connections={{A:n('CC_OUT1'),B:n('CC_OUT2'),GND:n('GND'),Y:n('USB_3A_LOGIC'),VCC:n('USB_AUX3V3_PENDING')}}/>
 {[
 ['C_USB_AUX_IN','1uF','USB_VBUS_RAW'],['C_USB_AUX_OUT','4.7uF','USB_AUX3V3_PENDING'],['C_USB_POR','100nF','USB_AUX3V3_PENDING'],['C_USB_3A','100nF','USB_AUX3V3_PENDING']
 ].map(([name,v,rail],i)=><capacitor key={name} name={name} capacitance={v} schX={-15+i*10} schY={12} connections={{pin1:n(rail),pin2:n('GND')}}/>)}
 <resistor name="R_USB_POR_CT" resistance="100k" schY={-12} connections={{pin1:n('USB_AUX3V3_PENDING'),pin2:n('USB_POR_CT')}}/>
 <resistor name="R_USB_3A_DRIVE" resistance="100k" schX={12} schY={-12} connections={{pin1:n('USB_3A_LOGIC'),pin2:n('USB_3A_ENABLE_PENDING')}}/>
 <resistor name="R_USB_SENSE_TOP" manufacturerPartNumber="RT0603BRD07634KL" resistance="634k" schX={-12} schY={-20} connections={{pin1:n('USB_AUX3V3_PENDING'),pin2:n('USB_POR_SENSE')}}/>
 <resistor name="R_USB_SENSE_BOTTOM" manufacturerPartNumber="RT0603BRD07100KL" resistance="100k" schX={-12} schY={-25} connections={{pin1:n('USB_POR_SENSE'),pin2:n('GND')}}/>
 <capacitor name="C_USB_SENSE" capacitance="1nF" schX={-20} schY={-25} connections={{pin1:n('USB_POR_SENSE'),pin2:n('GND')}}/>
 {/* Deliberately no reset pullup to VDD: NOR through 100k supplies it only for 3A. */}
</board>}
export function UsbCCProtection(){
 const pins=['C_SBU1_NC','C_SBU2_NC','VBIAS','C_CC1','C_CC2','RPD_G2','RPD_G1','GND8','FAULT_N','VPWR','CC2','CC1','GND13','SBU2_NC','SBU1_NC','NC16_GND','NC17_GND','GND18','D2_GND','D1_GND','EP_GND']
 const con:Record<string,string>={VBIAS:'USB_CC_VBIAS',C_CC1:'USB_CC1_RAW',C_CC2:'USB_CC2_RAW',RPD_G2:'USB_CC2_RAW',RPD_G1:'USB_CC1_RAW',GND8:'GND',FAULT_N:'USB_CC_FAULT_N',VPWR:'USB_AUX3V3_PENDING',CC2:'USB_CC2_PROTECTED_PENDING',CC1:'USB_CC1_PROTECTED_PENDING',GND13:'GND',NC16_GND:'GND',NC17_GND:'GND',GND18:'GND',D2_GND:'GND',D1_GND:'GND',EP_GND:'GND'}
 return <board name="USB_CC_PROTECTION" width={56} height={144} routingDisabled>
 <chip name="U_CC_PROTECT" manufacturerPartNumber="TPD6S300ARUKR" pinLabels={Object.fromEntries(pins.map((p,i)=>[`pin${i+1}`,p]))} connections={Object.fromEntries(Object.entries(con).map(([p,v])=>[p,n(v)]))}/>
 <capacitor name="C_CC_VBIAS" manufacturerPartNumber="C0603C104K5RACTU" capacitance="100nF" schX={12} connections={{pin1:n('USB_CC_VBIAS'),pin2:n('GND')}}/>
 <capacitor name="C_CC_PROTECT" capacitance="1uF" schX={-12} connections={{pin1:n('USB_AUX3V3_PENDING'),pin2:n('GND')}}/>
 <resistor name="R_CC_FAULT" resistance="100k" schY={12} connections={{pin1:n('USB_AUX3V3_PENDING'),pin2:n('USB_CC_FAULT_N')}}/>
 </board>
}
