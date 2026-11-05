import React from 'react'
import {UsbPlacementV60,placementV60} from './usb-placement-v60'
import {ChargerCandidate} from './front-end'
import {sourcePassives} from './sourced-passives'
export const placementV61={...placementV60,R_CHG_TS_TOP:{x:5,y:43,rotation:0,layer:'top' as const},R_CHG_TS_BOTTOM:{x:9,y:43,rotation:0,layer:'top' as const},R_CHG_TS_TRIM:{x:13,y:43,rotation:0,layer:'top' as const}}
export function UsbPlacementV61(){const prior:any=UsbPlacementV60(),block:any=sourcePassives(ChargerCandidate({flatPack:true}));const names=['R_CHG_TS_TOP','R_CHG_TS_BOTTOM','R_CHG_TS_TRIM'];return React.cloneElement(prior,{},<>{prior.props.children}{React.Children.toArray(block.props.children).filter((e:any)=>names.includes(e?.props?.name)).map((e:any)=>{const p=(placementV61 as any)[e.props.name];return React.cloneElement(e,{key:e.props.name,pcbX:p.x,pcbY:p.y+12,layer:p.layer,footprint:<footprint>{[1,2].map(n=><React.Fragment key={n}><smtpad portHints={['pin'+n]} shape="rect" pcbX={n===1?-.85:.85} width={1} height={1.1} noSolderPaste/></React.Fragment>)}</footprint>})})}</>)}
