import React from 'react'
import '@tscircuit/core'
const n=(v:string)=>`net.${v}`
/** Parent reviewer transcription of EG912U-GL QuecOpenV1.0Figure25.
 * Only bias and AC coupling; NO inferred ferrite/TVS/filter topology or microphone load.
 * Actual component variants, bias current and microphone match remain unqualified. */
export function AudioBiasCandidate(){return <board name="AUDIO_BIAS_UNQUALIFIED" width={56} height={144} routingDisabled>
 <resistor name="R_MIC_BIAS_TOP" resistance="510" schX={0} schY={16} connections={{pin1:n('MODEM_MICBIAS_PENDING'),pin2:n('MIC_BIAS_UPPER_PENDING')}}/>
 <resistor name="R_MIC_BIAS_BOTTOM" resistance="510" schX={0} schY={-16} connections={{pin1:n('MIC_BIAS_LOWER_PENDING'),pin2:n('GND')}}/>
 <capacitor name="C_MIC_BIAS" capacitance="2.2uF" schX={12} schY={0} connections={{pin1:n('MIC_BIAS_UPPER_PENDING'),pin2:n('MIC_BIAS_LOWER_PENDING')}}/>
 <resistor name="R_MIC_BIAS_P" resistance="1.5k" schX={24} schY={12} connections={{pin1:n('MIC_BIAS_UPPER_PENDING'),pin2:n('MIC_P_FILTER_INPUT_PENDING')}}/>
 <resistor name="R_MIC_BIAS_N" resistance="1.5k" schX={24} schY={-12} connections={{pin1:n('MIC_N_FILTER_INPUT_PENDING'),pin2:n('MIC_BIAS_LOWER_PENDING')}}/>
 {(['P','N'] as const).map((s,i)=><group key={s} schY={i===0?4:-4}>
  <resistor name={`R_MIC_${s}_SERIES`} resistance="1k" schX={-12} connections={{pin1:n(`MODEM_MIC_${s}_PENDING`),pin2:n(`MIC_${s}_AC_NODE`)}}/>
  <capacitor name={`C_MIC_${s}_AC`} capacitance="100nF" schX={0} connections={{pin1:n(`MIC_${s}_AC_NODE`),pin2:n(`MIC_${s}_FILTER_INPUT_PENDING`)}}/>
 </group>)}
</board>}
