import React from 'react'
import '@tscircuit/core'
import {sourcePassives} from './sourced-passives'
const n=(s:string)=>`net.${s}`
/** Isolated TPS63802 comparison circuit. Not integrated or qualified for modem use.
 * XFL4015 is TI-listed but L(I,T), caps, fault protection and loaded startup remain open.
 * No fabricated footprint is assigned to the DLA package. */
export function BuckBoostCandidateV21(){return sourcePassives(<board width={30} height={30} routingDisabled>
 <chip name="U_BB_CANDIDATE" manufacturerPartNumber="TPS63802DLAR" pinLabels={{pin1:'EN',pin2:'MODE',pin3:'AGND',pin4:'FB',pin5:'PG',pin6:'VOUT',pin7:'L2',pin8:'GND',pin9:'L1',pin10:'VIN'}} connections={{EN:n('BB_ENABLE_UNQUALIFIED'),MODE:n('BB_INPUT_UNQUALIFIED'),AGND:n('GND'),FB:n('BB_FB'),PG:n('BB_PG_UNQUALIFIED'),VOUT:n('BB_OUTPUT_UNQUALIFIED'),L2:n('BB_L2'),GND:n('GND'),L1:n('BB_L1'),VIN:n('BB_INPUT_UNQUALIFIED')}}/>
 <inductor name="L_BB_CANDIDATE" manufacturerPartNumber="XFL4015-471MEC" inductance="0.47uH" schY={8} connections={{pin1:n('BB_L1'),pin2:n('BB_L2')}}/>
 <resistor name="R_BB_FB_TOP" manufacturerPartNumber="RT0603BRD0766K5L" resistance="66.5k" schX={8} schY={4} connections={{pin1:n('BB_OUTPUT_UNQUALIFIED'),pin2:n('BB_FB')}}/>
 <resistor name="R_BB_FB_BOTTOM" manufacturerPartNumber="RT0603BRD0710KL" resistance="10k" schX={8} schY={-4} connections={{pin1:n('BB_FB'),pin2:n('GND')}}/>
 <resistor name="R_BB_EN_OFF" resistance="100k" schX={-8} schY={-8} connections={{pin1:n('BB_ENABLE_UNQUALIFIED'),pin2:n('GND')}}/>
 <capacitor name="C_BB_INPUT" capacitance="10uF" schX={-8} connections={{pin1:n('BB_INPUT_UNQUALIFIED'),pin2:n('GND')}}/>
 {[1,2].map(i=><capacitor key={i} name={`C_BB_OUTPUT_${i}`} capacitance="22uF" schX={16+i*8} connections={{pin1:n('BB_OUTPUT_UNQUALIFIED'),pin2:n('GND')}}/>)}
 {/* PG intentionally left as an open-drain interface; no rail/controller chosen yet. */}
</board>)}
