import React from 'react'
import '@tscircuit/core'
import {UsbPlacementV36,placementV36} from './usb-placement-v36'
import {ModemLandCandidate} from './modem-footprint'
import {SimConditioning} from './sim'
import {ModemSupportCandidate} from './modem-support'
import {sourcePassives} from './sourced-passives'
export const placementV42:Record<string,{x:number,y:number,rotation:number,layer?:'top'|'bottom'}>={...placementV36}
for(const [i,s] of ['KEY','RESET'].entries()){
 const y=-14-i*12.3
 placementV42[`U_MODEM_${s}_BUF`]={x:4,y,rotation:0,layer:'bottom'}
 placementV42[`C_MODEM_${s}_BUF`]={x:-.5,y:y+.95,rotation:0,layer:'bottom'}
 placementV42[`R_MODEM_${s}_INPUT_OFF`]={x:8.5,y:y+.95,rotation:180,layer:'bottom'}
 placementV42[`R_MODEM_${s}_GATE_OFF`]={x:4,y:y-2.7,rotation:180,layer:'bottom'}
}
Object.assign(placementV42,{U_MODEM_LOGICAL_ONLY:{x:12,y:6,rotation:0,layer:'bottom'},J_SIM_CANDIDATE:{x:12,y:47,rotation:0,layer:'bottom'},Q_MODEM_KEY:{x:0,y:-18,rotation:0,layer:'bottom'},Q_MODEM_RESET:{x:0,y:-30.3,rotation:0,layer:'bottom'},C_MODEM_VDD_EXT:{x:-23,y:-14,rotation:0,layer:'bottom'},U_SIM_ESD:{x:10,y:28,rotation:0,layer:'bottom'},R_SIM_RST:{x:14.5,y:31,rotation:0,layer:'bottom'},R_SIM_CLK:{x:14.5,y:28,rotation:0,layer:'bottom'},R_SIM_DATA:{x:6,y:28,rotation:180,layer:'bottom'},C_SIM_RST:{x:11.5,y:33,rotation:0,layer:'bottom'},C_SIM_CLK:{x:14.5,y:24.9,rotation:0,layer:'bottom'},C_SIM_DATA:{x:8,y:24.9,rotation:0,layer:'bottom'},C_SIM_VDD:{x:6.5,y:29.5,rotation:0,layer:'bottom'}})
function leaves(el:any):any[]{if(!React.isValidElement(el))return [];const e:any=el;return ['group','board',React.Fragment].includes(e.type)?React.Children.toArray(e.props.children).flatMap(leaves):[e]}
function Dbv5(){return <footprint>{[[1,-1.3,.95],[2,-1.3,0],[3,-1.3,-.95],[4,1.3,-.95],[5,1.3,.95]].map(([p,x,y])=><React.Fragment key={p}><smtpad portHints={[`pin${p}`]} shape="rect" pcbX={x} pcbY={y} width={1.1} height={.6} cornerRadius={.05} solderMaskMargin={.05} noSolderPaste/></React.Fragment>)}</footprint>}
export function UsbPlacementV42(){const prior:any=UsbPlacementV36();return React.cloneElement(prior,{},<>{prior.props.children}{[...leaves(sourcePassives(ModemSupportCandidate())),...leaves(sourcePassives(SimConditioning()))].filter((el:any)=>el.props.name in placementV42&&!(el.props.name in placementV36)).map((el:any)=>{const p=placementV42[el.props.name];return React.cloneElement(el,{key:el.props.name,pcbX:p.x,pcbY:p.y+12,pcbRotation:p.rotation,layer:'bottom',footprint:el.props.name==='U_MODEM_LOGICAL_ONLY'?<ModemLandCandidate/>:el.props.name==='J_SIM_CANDIDATE'?<Sim8051Lands/>:el.props.name.startsWith('Q_MODEM_')?<footprint>{[[1,-.95,-1.2],[2,.95,-1.2],[3,0,1.2]].map(([pin,x,y])=><React.Fragment key={pin}><smtpad portHints={[`pin${pin}`]} shape="rect" pcbX={x} pcbY={y} width={.8} height={.8} noSolderPaste/></React.Fragment>)}</footprint>:el.props.name==='C_MODEM_VDD_EXT'?<footprint>{[1,2].map(n=><React.Fragment key={n}><smtpad portHints={[`pin${n}`]} shape="rect" pcbX={n===1?-1.05:1.05} width={1.2} height={1.65} noSolderPaste/></React.Fragment>)}</footprint>:el.props.name==='U_SIM_ESD'?<Drl5/>:el.props.name.startsWith('U_')?<Dbv5/>:<footprint>{[1,2].map(n=><React.Fragment key={n}><smtpad portHints={[`pin${n}`]} shape="rect" pcbX={n===1?-.85:.85} width={1} height={1.15} noSolderPaste/></React.Fragment>)}</footprint>})})}</>)}

function Drl5(){return <footprint>{[[1,-.74,.5],[2,-.74,0],[3,-.74,-.5],[4,.74,-.5],[5,.74,.5]].map(([p,x,y])=><React.Fragment key={p}><smtpad portHints={[`pin${p}`]} shape="rect" pcbX={x} pcbY={y} width={.67} height={.3} solderMaskMargin={.05} noSolderPaste/></React.Fragment>)}</footprint>}

function Sim8051Lands(){return <footprint>{[[7,-2.54,5.9],[6,0,5.9],[5,2.54,5.9],[3,-2.54,-5.9],[2,0,-5.9],[1,2.54,-5.9],[8,-5.3,0],[9,5.3,0]].map(([p,x,y])=><React.Fragment key={p}><smtpad portHints={[`pin${p}`]} shape="rect" pcbX={x} pcbY={y} width={1} height={p>=8?3:1.1} noSolderPaste/></React.Fragment>)}</footprint>}
