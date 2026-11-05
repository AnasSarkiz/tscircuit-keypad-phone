import React from 'react'
import {UsbPlacementV50,placementV50} from './usb-placement-v50'
import {StartupCandidate} from './startup-candidate'
import {sourcePassives} from './sourced-passives'
export const placementV52={...placementV50,R_BUTTON_KILL_OFF:{x:-9,y:17,rotation:0,layer:'top' as const}}
export function UsbPlacementV52(){const prior:any=UsbPlacementV50(),block:any=sourcePassives(StartupCandidate({integrated:true}));return React.cloneElement(prior,{},<>{prior.props.children}{React.Children.toArray(block.props.children).filter((e:any)=>e?.props?.name==='R_BUTTON_KILL_OFF').map((e:any)=>React.cloneElement(e,{key:e.props.name,pcbX:-9,pcbY:29,layer:'top',footprint:<footprint>{[1,2].map(n=><React.Fragment key={n}><smtpad portHints={['pin'+n]} shape="rect" pcbX={n===1?-.85:.85} width={1} height={1.1} noSolderPaste/></React.Fragment>)}</footprint>}))}</>)}
