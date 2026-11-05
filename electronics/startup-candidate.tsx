import React from 'react'
import '@tscircuit/core'
import {sourcePassives} from './sourced-passives'
/** LTC2954-1 candidate: isolated by default; integrated variant has explicit rail/GPIO mapping.
 * Requires qualified supply >=2.7V, logic rise <400ms, minimum PDT timing,
 * complete modem power dependency, and physical button/ESD design. */
export function StartupCandidate({integrated=false}:{integrated?:boolean}={}){
 const mapped:Record<string,string>={SYS_BRANCH_UNQUALIFIED:'SYS_CANDIDATE',VLOGIC_BRANCH_UNQUALIFIED:'VLOGIC_3V15',LOGIC_EN_BRANCH_UNQUALIFIED:'BUTTON_ENABLE_RAW',BUTTON_INT_BRANCH_UNQUALIFIED:'BUTTON_INT_N',SYSTEM_OFF_REQUEST_BRANCH_UNQUALIFIED:'SYSTEM_OFF_REQUEST'}
 const n=(x:string)=>`net.${integrated?(mapped[x]??x):x}`
 return sourcePassives(<board name="STARTUP_BRANCH_UNQUALIFIED" width={56} height={144} routingDisabled>
 <chip name="U_BUTTON_BRANCH" schX={0} schY={0} manufacturerPartNumber="LTC2954ITS8-1#TRMPBF" pinLabels={{pin1:'VIN',pin2:'PB',pin3:'ONT',pin4:'GND',pin5:'INT_N',pin6:'EN',pin7:'PDT',pin8:'KILL'}} connections={{VIN:n('SYS_BRANCH_UNQUALIFIED'),PB:n('BUTTON_BRANCH_UNQUALIFIED'),GND:n('GND'),INT_N:n('BUTTON_INT_BRANCH_UNQUALIFIED'),EN:n('LOGIC_EN_BRANCH_UNQUALIFIED'),PDT:n('BUTTON_PDT_BRANCH'),KILL:n('BUTTON_KILL_BRANCH')}}/>
 <capacitor name="C_BUTTON_BYPASS" schX={-12} schY={8} capacitance="100nF" connections={{pin1:n('SYS_BRANCH_UNQUALIFIED'),pin2:n('GND')}}/>
 <capacitor name="C_BUTTON_PDT" schX={8} schY={-10} capacitance="2.2uF" connections={{pin1:n('BUTTON_PDT_BRANCH'),pin2:n('GND')}}/>
 <resistor name="R_BUTTON_EN_UP" schX={-12} schY={-8} resistance={integrated?"10k":"100k"} connections={{pin1:n('SYS_BRANCH_UNQUALIFIED'),pin2:n('LOGIC_EN_BRANCH_UNQUALIFIED')}}/>
 <resistor name="R_BUTTON_EN_DOWN" schX={-6} schY={-8} resistance={integrated?"100k":"1M"} connections={{pin1:n('LOGIC_EN_BRANCH_UNQUALIFIED'),pin2:n('GND')}}/>
 <resistor name="R_BUTTON_INT_UP" schX={12} schY={8} resistance="100k" connections={{pin1:n('VLOGIC_BRANCH_UNQUALIFIED'),pin2:n('BUTTON_INT_BRANCH_UNQUALIFIED')}}/>
 <resistor name="R_BUTTON_KILL_UP" schX={20} schY={0} resistance="100k" connections={{pin1:n('VLOGIC_BRANCH_UNQUALIFIED'),pin2:n('BUTTON_KILL_BRANCH')}}/>
 <chip name="Q_BUTTON_KILL" schX={20} schY={-8} manufacturerPartNumber="AO3400A" pinLabels={{pin1:'G',pin2:'S',pin3:'D'}} connections={{G:n('SYSTEM_OFF_REQUEST_BRANCH_UNQUALIFIED'),S:n('GND'),D:n('BUTTON_KILL_BRANCH')}}/>
 <resistor name="R_BUTTON_KILL_OFF" schX={20} schY={-16} resistance="100k" connections={{pin1:n('SYSTEM_OFF_REQUEST_BRANCH_UNQUALIFIED'),pin2:n('GND')}}/>
 {integrated&&<chip name="U_BUTTON_EN_BUFFER" schX={28} schY={0} manufacturerPartNumber="SN74LVC1G17DBVR" pinLabels={{pin1:'NC',pin2:'A',pin3:'GND',pin4:'Y',pin5:'VCC'}} connections={{A:n('BUTTON_ENABLE_RAW'),GND:n('GND'),Y:n('LOGIC_ENABLE'),VCC:n('SYS_CANDIDATE')}}/>}
 {integrated&&<capacitor name="C_BUTTON_BUFFER" schX={32} schY={8} capacitance="100nF" connections={{pin1:n('SYS_CANDIDATE'),pin2:n('GND')}}/>}
</board>)}
