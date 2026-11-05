import React from 'react'
import {UsbPlacementV45,placementV45} from './usb-placement-v45'
import {BacklightSinkCandidate} from './power-v4'
import {sourcePassives} from './sourced-passives'
export const placementV48={...placementV45,R_BACKLIGHT_OFF:{x:-25.1,y:46.5,rotation:0,layer:'bottom' as const}}
export function UsbPlacementV48(){const prior:any=UsbPlacementV45(),block:any=sourcePassives(BacklightSinkCandidate());return React.cloneElement(prior,{},<>{prior.props.children}{React.Children.toArray(block.props.children).filter((e:any)=>e?.props?.name==='R_BACKLIGHT_OFF').map((e:any)=><React.Fragment key={e.props.name}>{React.cloneElement(e,{pcbX:-25.1,pcbY:58.5,layer:'bottom',footprint:<footprint>{[1,2].map(n=><React.Fragment key={n}><smtpad portHints={['pin'+n]} shape="rect" pcbX={n===1?-.85:.85} width={1} height={1.1} noSolderPaste/></React.Fragment>)}</footprint>})}</React.Fragment>)}</>)}
