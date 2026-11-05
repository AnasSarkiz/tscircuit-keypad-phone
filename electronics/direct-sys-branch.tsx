import React from 'react'
import '@tscircuit/core'
import {sourcePassives} from './sourced-passives'
const n=(s:string)=>`net.${s}`
/** Isolated comparison branch, not integrated. NO OVP/UVLO or short protection.
 * BIAS=VIN avoids the invalid 3.15V bias / 4.1V input arrangement.
 * Do not connect output to modem until protection, inrush and power qualify.
 */
export function DirectSysBranch(){return sourcePassives(<board width={20} height={20} routingDisabled>
 <chip name="U_MODEM_SWITCH_BRANCH" manufacturerPartNumber="TPS22992RXPR" pinLabels={{pin1:'BIAS',pin2:'VIN',pin3:'PG',pin4:'GND',pin5:'QOD',pin6:'VOUT',pin7:'CT',pin8:'ON'}} connections={{BIAS:n('SYS_BRANCH_UNQUALIFIED'),VIN:n('SYS_BRANCH_UNQUALIFIED'),PG:n('SWITCH_PG_UNQUALIFIED'),GND:n('GND'),QOD:n('SWITCH_QOD'),VOUT:n('MODEM_SWITCH_OUT_UNQUALIFIED'),CT:n('SWITCH_CT'),ON:n('SWITCH_ENABLE_UNQUALIFIED')}}/>
 <capacitor name="C_SWITCH_IN" capacitance="1uF" schX={-8} connections={{pin1:n('SYS_BRANCH_UNQUALIFIED'),pin2:n('GND')}}/>
 <capacitor name="C_SWITCH_CT" capacitance="1nF" schY={-8} connections={{pin1:n('SWITCH_CT'),pin2:n('GND')}}/>
 <resistor name="R_SWITCH_OFF" resistance="100k" schX={8} connections={{pin1:n('SWITCH_ENABLE_UNQUALIFIED'),pin2:n('GND')}}/>
 <resistor name="R_SWITCH_QOD" resistance="1k" manufacturerPartNumber="RC0603FR-071KL" schY={8} connections={{pin1:n('MODEM_SWITCH_OUT_UNQUALIFIED'),pin2:n('SWITCH_QOD')}}/>
 {/* Output bulk and PG pullup intentionally absent: selected rail/control pending. */}
</board>)}
