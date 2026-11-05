import React from 'react'
import '@tscircuit/core'
const n=(s:string)=>`net.${s}`
/** SIM conditioning from V1.0 text, pp44-45; GCT candidate logical connector added.
 * SOCKET_PENDING nets now reach GCT C-contact numbers; parent-reviewed physical land candidate added inV39.
 * No modem variant/land-pattern applicability claimed.
 */
export function SimConditioning(){return <board name="SIM_CONDITIONING" width={56} height={144} routingDisabled>
 {['RST','CLK','DATA'].map((signal,i)=><group name={`SIM_${signal}`} key={signal} schX={i*12}>
  <resistor name={`R_SIM_${signal}`} resistance="0" connections={{pin1:n(`USIM1_${signal}_MODEM_PENDING`),pin2:n(`USIM1_${signal}_SOCKET_PENDING`)}}/>
  <capacitor name={`C_SIM_${signal}`} capacitance="33pF" schY={-6} connections={{pin1:n(`USIM1_${signal}_SOCKET_PENDING`),pin2:n('GND')}}/>
 </group>)}
 <capacitor name="C_SIM_VDD" manufacturerPartNumber="C0603C104K5RACTU" capacitance="100nF" schX={-12} connections={{pin1:n('USIM1_VDD_PENDING'),pin2:n('GND')}}/>
 <chip name="U_SIM_ESD" manufacturerPartNumber="TPD3E001DRLR" schX={12} schY={12} pinLabels={{pin1:'IO1',pin2:'IO2',pin3:'GND',pin4:'IO3',pin5:'VCC'}} connections={{IO1:n('USIM1_RST_SOCKET_PENDING'),IO2:n('USIM1_CLK_SOCKET_PENDING'),GND:n('GND'),IO3:n('USIM1_DATA_SOCKET_PENDING'),VCC:n('USIM1_VDD_PENDING')}}/>
 <chip name="J_SIM_CANDIDATE" manufacturerPartNumber="SIM8051-6-0-14-00-A" schX={32} schY={12}
  pinLabels={{pin1:'C1_VCC',pin2:'C2_RST',pin3:'C3_CLK',pin5:'C5_GND',pin6:'C6_VPP_NC',pin7:'C7_IO',pin8:'MOUNT_L_NC',pin9:'MOUNT_R_NC'}}
  connections={{C1_VCC:n('USIM1_VDD_PENDING'),C2_RST:n('USIM1_RST_SOCKET_PENDING'),C3_CLK:n('USIM1_CLK_SOCKET_PENDING'),C5_GND:n('GND'),C7_IO:n('USIM1_DATA_SOCKET_PENDING')}}/>
 {/* Contact functions from GCT SIM8051 drawing D5 sheet2; pin indices are C numbers.
     VPP unused; no hot plug. Shell mounting tabs have separate unconnected pads; shell grounding/process not qualified. */}
 {/* Shared C_SIM_VDD supplies local VCC bypass; exact physical proximity required. */}
 {/* DET left absent; no hot swap until configuration and connector are verified. */}
</board>}
