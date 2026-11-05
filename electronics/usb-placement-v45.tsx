import React from 'react'
import {McuCandidate} from './mcu'
import {sourcePassives} from './sourced-passives'
import {UsbPlacementV44,placementV44} from './usb-placement-v44'
import {McuTestAccessV45,debugPadsV45} from './mcu-test-access-v45'
export const biasPlacementV45=Object.fromEntries(['COL0','COL1','COL2','LCD_CS_N'].map((n,i)=>['R_MCU_'+n,{x:-8-i*4,y:16.5,rotation:0,layer:'bottom' as const}]))
export const placementV45={...placementV44,...biasPlacementV45,...Object.fromEntries(debugPadsV45.map(([name,net,y])=>[name,{x:-25.1,y,rotation:0,layer:'bottom' as const}]))}
export function UsbPlacementV45(){const prior:any=UsbPlacementV44();const debug:any=McuTestAccessV45(),mcu:any=sourcePassives(McuCandidate());return React.cloneElement(prior,{},<>{prior.props.children}{React.Children.map(debug.props.children,(e:any)=>{const p=placementV45[e.props.name];return React.cloneElement(e,{pcbX:p.x,pcbY:p.y+12,layer:'bottom'})})}{React.Children.toArray(mcu.props.children).filter((e:any)=>e?.props?.name in biasPlacementV45).map((e:any)=>{const p=biasPlacementV45[e.props.name];return React.cloneElement(e,{key:e.props.name,pcbX:p.x,pcbY:p.y+12,layer:'bottom',footprint:<footprint>{[1,2].map(n=><React.Fragment key={n}><smtpad portHints={['pin'+n]} shape="rect" pcbX={n===1?-.85:.85} width={1} height={1.1} noSolderPaste/></React.Fragment>)}</footprint>})})}</>)}
