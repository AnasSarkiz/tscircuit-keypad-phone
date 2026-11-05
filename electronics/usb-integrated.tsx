import React from 'react'
import {UsbStartup,UsbCCProtection} from './usb-startup'
import {UsbCCCandidate,UsbInputProtectionCandidate} from './usb-c'
/** One board, shared nets; logical integration only, no placement or routing. */
export function UsbIntegrated(){
 const blocks=[UsbStartup(),UsbCCProtection(),UsbCCCandidate({highVoltage:true}),UsbInputProtectionCandidate()]
 return <board name="USB_INTEGRATED" width={56} height={144} routingDisabled>{blocks.flatMap((block,index)=>React.Children.toArray(block.props.children).map((child:any)=>React.isValidElement(child)?React.cloneElement(child as React.ReactElement<any>,{key:`${index}:${child.key}`,schX:((child.props as any).schX??0)+index*45}):child))}</board>
}
