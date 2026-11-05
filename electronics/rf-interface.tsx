import React from 'react'
import '@tscircuit/core'
import {sourcePassives} from './sourced-passives'
const n=(x:string)=>`net.${x}`
/** QuecOpen V1.0 p64 Figure31 text specifies series0R and two shunts not mounted.
 * Matching reserves are deliberate UNPOPULATED generic two-terminal symbols:
 * no invented capacitance, footprint, MPN or default population. */
export function RfMatchingCandidate(){return sourcePassives(<board name="RF_MATCHING_UNQUALIFIED" width={56} height={144} routingDisabled>
 <resistor name="R_RF_SERIES_CANDIDATE" resistance="0" schX={0} connections={{pin1:n('ANT_MAIN_MATCH_IN_PENDING'),pin2:n('ANT_TO_RECEPTACLE_PENDING')}}/>
 <chip name="RF_SHUNT_IN_DNP_RESERVE" schX={-8} schY={-8} pinLabels={{pin1:'RF',pin2:'GND'}} connections={{RF:n('ANT_MAIN_MATCH_IN_PENDING'),GND:n('GND')}}/>
 <chip name="RF_SHUNT_OUT_DNP_RESERVE" schX={8} schY={-8} pinLabels={{pin1:'RF',pin2:'GND'}} connections={{RF:n('ANT_TO_RECEPTACLE_PENDING'),GND:n('GND')}}/>
</board>)}
