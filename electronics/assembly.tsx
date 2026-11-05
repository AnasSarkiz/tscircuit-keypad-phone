import React from 'react'
import { assembly } from '@tscircuit/core'
import KeypadFloorplan from './keypad'

// Models are authored at world origin in mm. The GLB uses metres, standard
// glTF units. This asset records the whole preliminary fit study, including a
// mechanical PCB blank; hide the blank if combining with rendered copper.
export default function PhoneAssembly() {
  return <assembly.device name="ANAS_PHONE_FIT_STUDY">
    <KeypadFloorplan />
    <assembly.part name="MECHANICAL_FIT_STUDY" cadModel={<cadmodel modelUrl="./output/retained-battery/assembly.glb" modelUnitToMmScale={1000} />} />
  </assembly.device>
}
