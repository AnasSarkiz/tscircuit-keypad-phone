import React from 'react'
import '@tscircuit/core'
import {UsbPlacementV43,placementV43} from './usb-placement-v43'
import {McuCandidate} from './mcu'
import {McuLandsV44} from './mcu-lands-v44'
import {sourcePassives} from './sourced-passives'
export const placementV44:Record<string,{x:number,y:number,rotation:number,layer?:'top'|'bottom'}>={...placementV43,
 U_MCU:{x:-13,y:32,rotation:0,layer:'bottom'},
 C_MCU_HF:{x:-1.75,y:39.5,rotation:0,layer:'bottom'},
 C_MCU_BULK:{x:.5,y:29,rotation:0,layer:'bottom'},
 C_MCU_EN:{x:.5,y:32,rotation:0,layer:'bottom'},
 R_MCU_MCU_EN:{x:.5,y:35,rotation:0,layer:'bottom'},
 R_MCU_MCU_BOOT_N:{x:-25,y:20,rotation:0,layer:'bottom'}}
function noPaste(e:any):any {if(!React.isValidElement(e))return e;const x:any=e;if(typeof x.type==='function')return noPaste(x.type(x.props));return React.cloneElement(x,{...(x.type==='smtpad'?{noSolderPaste:true}:{}),children:React.Children.map(x.props.children,noPaste)})}
export function UsbPlacementV44(){const prior:any=UsbPlacementV43();const tree:any=sourcePassives(McuCandidate());return React.cloneElement(prior,{},<>{prior.props.children}{React.Children.toArray(tree.props.children).flat().filter((e:any)=>e?.props?.name in placementV44).map((e:any)=>{const p=placementV44[e.props.name];return React.cloneElement(e,{key:e.props.name,pcbX:p.x,pcbY:p.y+12,pcbRotation:p.rotation,layer:'bottom',...(e.props.name==='U_MCU'?{footprint:<McuLandsV44/>,connections:e.props.connections}:{footprint:noPaste(e.props.footprint)})})})}</>)}
