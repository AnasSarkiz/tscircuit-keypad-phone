import React from 'react'
import {UsbPlacementV62,placementV62} from './usb-placement-v62'
import {KeypadCandidateV64} from './keypad-v64'
export const placementV65={...placementV62,...Object.fromEntries(Array.from({length:15},(_,i)=>['SW'+(i+1),{x:[-14,0,14][i%3],y:[-21,-33,-45,-57,-69][Math.floor(i/3)],rotation:0,layer:'top' as const}]))}
export function UsbPlacementV65(){const old:any=UsbPlacementV62(),keys:any=KeypadCandidateV64();return React.cloneElement(old,{},<>{old.props.children}{keys.props.children}</>)}
