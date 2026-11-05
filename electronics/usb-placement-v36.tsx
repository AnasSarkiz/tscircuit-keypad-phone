import React from 'react'
import '@tscircuit/core'
import {UsbPlacementV35,placementV35} from './usb-placement-v35'
import {ModemLogic,channels} from './interfaces'
import {sourcePassives} from './sourced-passives'
import {SupervisorLandV29} from './usb-placement-v29'
export const placementV36:Record<string,{x:number,y:number,rotation:number,layer?:'top'|'bottom'}>={...placementV35}
for(const [i,ch] of channels.entries()){
 const y=[-12,-18,-27,-39,-51][i]
 for(const [name,x,dy] of [[`U_${ch.name}`,-14,0],[`C_A_${ch.name}`,-9.5,1.05],[`C_B_${ch.name}`,-18.5,1.05],[`R_IDLE_${ch.name}`,-14,-2.8]] as [string,number,number][])placementV36[name]={x,y:y+dy,rotation:name.startsWith('C_A_')?180:0,layer:'bottom'}
}
function leaves(el:any):any[]{if(!React.isValidElement(el))return [];const e:any=el;return ['group','board',React.Fragment].includes(e.type)?React.Children.toArray(e.props.children).flatMap(leaves):[e]}
export function UsbPlacementV36(){const prior:any=UsbPlacementV35();return React.cloneElement(prior,{},<>{prior.props.children}{leaves(sourcePassives(ModemLogic())).map((el:any)=>{const p=placementV36[el.props.name];return React.cloneElement(el,{key:el.props.name,pcbX:p.x,pcbY:p.y+12,pcbRotation:p.rotation,layer:'bottom',pcbLayer:'bottom',footprint:el.props.name.startsWith('U_')?<SupervisorLandV29/>:<footprint>{[1,2].map(n=><React.Fragment key={n}><smtpad portHints={[`pin${n}`]} shape="rect" pcbX={n===1?-.85:.85} width={1} height={1.15} noSolderPaste/></React.Fragment>)}</footprint>})})}</>)}
