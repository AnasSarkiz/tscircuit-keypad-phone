import React from 'react'
import {UsbPlacementV49,placementV49} from './usb-placement-v49'
import {ChargeEnableCandidate} from './charge-enable'
import {sourcePassives} from './sourced-passives'
export const placementV50={...placementV49,R_CHARGE_REQUEST_OFF:{x:-14,y:17,rotation:0,layer:'top' as const}}
export function UsbPlacementV50(){const prior:any=UsbPlacementV49(),block:any=sourcePassives(ChargeEnableCandidate());return React.cloneElement(prior,{},<>{prior.props.children}{React.Children.toArray(block.props.children).filter((e:any)=>e?.props?.name==='R_CHARGE_REQUEST_OFF').map((e:any)=>React.cloneElement(e,{key:e.props.name,pcbX:-14,pcbY:29,layer:'top',footprint:<footprint>{[1,2].map(n=><React.Fragment key={n}><smtpad portHints={['pin'+n]} shape="rect" pcbX={n===1?-.85:.85} width={1} height={1.1} noSolderPaste/></React.Fragment>)}</footprint>}))}</>)}
