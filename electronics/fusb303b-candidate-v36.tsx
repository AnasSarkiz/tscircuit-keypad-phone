import React from 'react'
import '@tscircuit/core'
import {UsbCCCandidate} from './usb-c'
/** Parent-reviewed CASE722AG copper transcription. Top view, CAD Y up.
 * +0.05mm mask margin is an unqualified process choice, not an onsemi recommendation.
 * No paste. Not assigned to the active phone until startup/protection qualification.
 */
export function Fusb303bLandCandidate(){const pads=[[1,-.65,.2,.7,.2],[2,-.65,-.2,.7,.2],[3,-.6,-.75,.2,.5],[4,-.2,-.75,.2,.5],[5,.2,-.75,.2,.5],[6,.6,-.75,.2,.5],[7,.65,-.2,.7,.2],[8,.65,.2,.7,.2],[9,.6,.75,.2,.5],[10,.2,.75,.2,.5],[11,-.2,.75,.2,.5],[12,-.6,.75,.2,.5]];return <footprint>{pads.map(([pin,x,y,w,h])=><React.Fragment key={pin}><smtpad portHints={[`pin${pin}`]} shape="rect" pcbX={x} pcbY={y} width={w} height={h} solderMaskMargin={.05} noSolderPaste/></React.Fragment>)}</footprint>}
/** Explicit alternate, not a drop-in change to UsbIntegrated or its policy. */
export function Fusb303bCandidate(){const base:any=UsbCCCandidate({highVoltage:true});return React.cloneElement(base,{name:'FUSB303B_ALTERNATE_UNQUALIFIED'},React.Children.map(base.props.children,(el:any)=>React.isValidElement(el)&&(el as any).props.name==='U_CC'?React.cloneElement(el as any,{manufacturerPartNumber:'FUSB303BTMX',footprint:<Fusb303bLandCandidate/>}):el))}
