import React from 'react'
import {AudioBiasCandidate} from './audio-bias-candidate'
import {RfMatchingCandidate} from './rf-interface'
import {KeypadElectrical} from './keypad'
import {StartupCandidate} from './startup-candidate'
import {sourcePassives} from './sourced-passives'
import {ModemSupportCandidate} from './modem-support'
import {ChargeEnableCandidate} from './charge-enable'
import {SimConditioning} from './sim'
import {McuCandidate} from './mcu'
import {UsbIntegrated} from './usb-integrated'
import {ChargerCandidate,DisplayInterface} from './front-end'
import {LogicSupply,ModemLogic} from './interfaces'
import {ModemBuckCandidate,BacklightSinkCandidate} from './power-v4'
import {BacklightBoost,ChargeTemperatureGuard} from './power-v5'
/** Candidate power/interface netlist. Modem, MCU, SIM, audio, antenna and control
 * connections remain deliberately incomplete. No claim of a whole-phone netlist.
 */
export function PowerIntegrated(){
 const blocks=[UsbIntegrated(),ChargerCandidate({flatPack:true}),LogicSupply(),ModemLogic(),ModemBuckCandidate(),BacklightBoost(),BacklightSinkCandidate(),ChargeTemperatureGuard(),DisplayInterface(),McuCandidate(),SimConditioning(),ChargeEnableCandidate(),ModemSupportCandidate(),StartupCandidate({integrated:true}),KeypadElectrical(),RfMatchingCandidate(),AudioBiasCandidate()]
 function remap(v:any):any{
  if(typeof v==='string')return v==='net.SYS_INPUT'?'net.SYS_CANDIDATE':v
  if(Array.isArray(v))return v.map(remap)
  if(v&&typeof v==='object'&&!React.isValidElement(v))return Object.fromEntries(Object.entries(v).map(([k,val])=>[k,remap(val)]))
  return v
 }
 return sourcePassives(<board name="POWER_INTEGRATED" width={56} height={144} routingDisabled>{blocks.flatMap((block,index)=>React.Children.toArray(block.props.children).map((child:any)=>React.isValidElement(child)?React.cloneElement(child as React.ReactElement<any>,{...remap(child.props),key:`${index}:${child.key}`,schX:((child.props as any).schX??0)+(index%3)*180,schY:((child.props as any).schY??0)+Math.floor(index/3)*80}):child))}</board>)
}
