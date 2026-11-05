import React from 'react'
import '@tscircuit/core'
import {KeypadElectrical} from './keypad'
/** Reviewed Omron page5 component-side drawing. Project +Y points toward earpiece.
 * Logical pin1 = upper physical4/3; logical pin2 = lower physical2/1.
 * 1.00mm is a proposed FINISHED hole, not a drill-tool selection. Fabricator must
 * achieve0.95..1.05mm after plating.2mm copper remains engineering proposal.
 * Independent candidate only; V62 routing and reservations remain unchanged.
 */
export const keypadTerminalsV64=[
 {physical:4,logical:1,x:-3.25,y:2.25},
 {physical:3,logical:1,x:3.25,y:2.25},
 {physical:2,logical:2,x:-3.25,y:-2.25},
 {physical:1,logical:2,x:3.25,y:-2.25},
] as const
export function KeypadFootprintV64(){return <footprint>{keypadTerminalsV64.map(p=><React.Fragment key={p.physical}><platedhole portHints={['pin'+p.logical]} pcbX={p.x} pcbY={p.y} shape="circle" holeDiameter={1} outerDiameter={2}/></React.Fragment>)}<silkscreenrect width={6} height={6} strokeWidth={.12}/></footprint>}
export function KeypadCandidateV64(){const b:any=KeypadElectrical();return React.cloneElement(b,{pcbY:-12,layers:4,thickness:1.6},React.Children.toArray(b.props.children).map((e:any)=>React.cloneElement(e,{footprint:<KeypadFootprintV64/>,connections:{...e.props.connections,pin1_internal_1:e.props.connections.pin1,pin2_internal_1:e.props.connections.pin2}})))}
