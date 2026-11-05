import React from 'react'
import '@tscircuit/core'
import {sourcePassives} from './sourced-passives'
const n=(v:string)=>`net.${v}`
/** Isolated alternative: dedicated 2.5V MEMS supply. Output/enable interfaces are intentionally
 * pending until modem AFE impedance, sequencing, filtering and physical geometry are qualified. */
export function MemsAudioCandidateV26(){return sourcePassives(<board name="MEMS_CANDIDATE" width={25} height={25} routingDisabled>
 <chip name="U_MIC_LDO" manufacturerPartNumber="TPS7A2025PDBVR" pinLabels={{pin1:'IN',pin2:'GND',pin3:'EN',pin4:'NC',pin5:'OUT'}} connections={{IN:n('MIC_LOGIC_INPUT_PENDING'),GND:n('GND'),EN:n('MIC_ENABLE_PENDING'),OUT:n('MIC_2V5')}}/>
 <resistor name="R_MIC_LDO_DEFAULT_OFF" resistance="100k" schX={-10} connections={{pin1:n('MIC_ENABLE_PENDING'),pin2:n('GND')}}/>
 <resistor name="R_MIC_LDO_MIN_LOAD" manufacturerPartNumber="RC0603FR-072K2L" resistance="2.2k" schX={10} connections={{pin1:n('MIC_2V5'),pin2:n('GND')}}/>
 <capacitor name="C_MIC_LDO_IN" capacitance="2.2uF" schX={-10} schY={8} connections={{pin1:n('MIC_LOGIC_INPUT_PENDING'),pin2:n('GND')}}/>
 <capacitor name="C_MIC_LDO_OUT" capacitance="2.2uF" schX={10} schY={8} connections={{pin1:n('MIC_2V5'),pin2:n('GND')}}/>
 <chip name="MIC_MEMS_CANDIDATE" manufacturerPartNumber="IM73A135V01XTSA1" schX={24} pinLabels={{pin1:'OUT_P',pin2:'VDD',pin3:'OUT_N',pin4:'GND4',pin5:'GND5'}} connections={{OUT_P:n('MEMS_OUT_P_AFE_PENDING'),VDD:n('MIC_2V5'),OUT_N:n('MEMS_OUT_N_AFE_PENDING'),GND4:n('GND'),GND5:n('GND')}}/>
 <capacitor name="C_MIC_LOCAL" capacitance="100nF" schX={24} schY={8} connections={{pin1:n('MIC_2V5'),pin2:n('GND')}}/>
</board>)}
