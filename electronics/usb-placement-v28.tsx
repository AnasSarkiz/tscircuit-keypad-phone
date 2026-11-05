import React from 'react'
import '@tscircuit/core'
import {UsbPlacementV27,ccPlacementV27} from './usb-placement-v27'
import {UsbStartup} from './usb-startup'
import {sourcePassives} from './sourced-passives'
export const placementV28={...ccPlacementV27,R_USB_SENSE_TOP:{x:-18,y:-76,rotation:0},R_USB_SENSE_BOTTOM:{x:-14,y:-76,rotation:0},C_USB_SENSE:{x:-14,y:-78,rotation:0}}
export function UsbPlacementV28(){const prior:any=UsbPlacementV27(),startup:any=sourcePassives(UsbStartup());const names=['R_USB_SENSE_TOP','R_USB_SENSE_BOTTOM','C_USB_SENSE'];return React.cloneElement(prior,{},<>{prior.props.children}{React.Children.toArray(startup.props.children).filter((el:any)=>names.includes(el.props?.name)).map((el:any)=>{const p=placementV28[el.props.name as keyof typeof placementV28];return React.cloneElement(el,{pcbX:p.x,pcbY:p.y+12,pcbRotation:p.rotation,footprint:<footprint>{[1,2].map(n=><React.Fragment key={n}><smtpad portHints={[`pin${n}`]} shape="rect" pcbX={n===1?-.85:.85} width={1} height={1.15} noSolderPaste/></React.Fragment>)}</footprint>})})}</>)}
