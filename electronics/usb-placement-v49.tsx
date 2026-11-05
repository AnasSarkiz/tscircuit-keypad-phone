import React from 'react'
import {UsbPlacementV48,placementV48} from './usb-placement-v48'
import {DisplayInterface} from './front-end'
import {sourcePassives} from './sourced-passives'
export const displayBiasV49:Record<string,{x:number,y:number,rotation:number,layer:'bottom'}>={R_LCD_RST:{x:-25.1,y:11,rotation:180,layer:'bottom'},R_LCD_CS:{x:-25.1,y:14.3,rotation:0,layer:'bottom'}}
export const placementV49={...placementV48,...displayBiasV49}
export function UsbPlacementV49(){const prior:any=UsbPlacementV48(),block:any=sourcePassives(DisplayInterface());return React.cloneElement(prior,{},<>{prior.props.children}{React.Children.toArray(block.props.children).filter((e:any)=>e?.props?.name in displayBiasV49).map((e:any)=>{const p=displayBiasV49[e.props.name];return React.cloneElement(e,{key:e.props.name,pcbX:p.x,pcbY:p.y+12,pcbRotation:p.rotation,layer:'bottom',footprint:<footprint>{[1,2].map(n=><React.Fragment key={n}><smtpad portHints={['pin'+n]} shape="rect" pcbX={n===1?-.85:.85} width={1} height={1.1} noSolderPaste/></React.Fragment>)}</footprint>})})}</>)}
