import React from 'react'
import '@tscircuit/core'
import {UsbPlacementV28,placementV28} from './usb-placement-v28'
import {UsbStartup} from './usb-startup'
import {sourcePassives} from './sourced-passives'
export const placementV29={...placementV28,U_USB_POR:{x:-21,y:-63,rotation:0},C_USB_POR:{x:-17.5,y:-62.05,rotation:0},R_USB_POR_CT:{x:-21,y:-65.8,rotation:0}}
/** TI TPS3808 RevN PDF37 DBV0006A4214840/G textual audit; visual overlay/process unqualified. */
export function SupervisorLandV29(){return <footprint>{[[1,-1.3,.95],[2,-1.3,0],[3,-1.3,-.95],[4,1.3,-.95],[5,1.3,0],[6,1.3,.95]].map(([p,x,y])=><React.Fragment key={p}><smtpad portHints={[`pin${p}`]} shape="rect" pcbX={x} pcbY={y} width={1.1} height={.6} cornerRadius={.05} solderMaskMargin={.05} noSolderPaste/></React.Fragment>)}</footprint>}
export function UsbPlacementV29(){const prior:any=UsbPlacementV28(),startup:any=sourcePassives(UsbStartup());const names=['U_USB_POR','C_USB_POR','R_USB_POR_CT'];return React.cloneElement(prior,{},<>{prior.props.children}{React.Children.toArray(startup.props.children).filter((el:any)=>names.includes(el.props?.name)).map((el:any)=>{const p=placementV29[el.props.name as keyof typeof placementV29];return React.cloneElement(el,{pcbX:p.x,pcbY:p.y+12,pcbRotation:p.rotation,footprint:el.props.name==='U_USB_POR'?<SupervisorLandV29/>:<footprint>{[1,2].map(n=><React.Fragment key={n}><smtpad portHints={[`pin${n}`]} shape="rect" pcbX={n===1?-.85:.85} width={1} height={1.15} noSolderPaste/></React.Fragment>)}</footprint>})})}</>)}
