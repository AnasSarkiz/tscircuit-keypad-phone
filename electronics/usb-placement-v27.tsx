import React from 'react'
import '@tscircuit/core'
import {UsbCCProtection} from './usb-startup'
import {sourcePassives} from './sourced-passives'
import {ReviewedLandV24} from './reviewed-lands-v24'
/** Partial placement candidate: existing electrical nets; routing/process not released. */
export const ccPlacementV27:Record<string,{x:number,y:number,rotation:number}>={U_CC_PROTECT:{x:7,y:-75,rotation:0},C_CC_PROTECT:{x:7.8,y:-78.7,rotation:-90},C_CC_VBIAS:{x:3.2,y:-75,rotation:180},R_CC_FAULT:{x:10.8,y:-73.7,rotation:0}}
function Passive({size}:{size:'0603'|'0805'}){const g=size==='0805'?[1.05,1.2,1.65]:[.85,1,1.15];return <footprint>{[1,2].map(n=><React.Fragment key={n}><smtpad portHints={[`pin${n}`]} shape="rect" pcbX={(n===1?-1:1)*g[0]} width={g[1]} height={g[2]} noSolderPaste/></React.Fragment>)}</footprint>}
export function UsbPlacementV27(){const old:any=sourcePassives(UsbCCProtection());return <board width={56} height={144} pcbY={-12} routingDisabled>{React.Children.map(old.props.children,(el:any)=>{if(!React.isValidElement(el))return el;const p:any=el.props,a=ccPlacementV27[p.name];if(!a)throw Error('unmapped '+p.name);return React.cloneElement(el as any,{pcbX:a.x,pcbY:a.y+12,pcbRotation:a.rotation,footprint:p.name==='U_CC_PROTECT'?<ReviewedLandV24 kind="RUK0020B"/>:<Passive size={p.name==='C_CC_PROTECT'?'0805':'0603'}/>})})}</board>}
