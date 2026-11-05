import React from 'react'
import '@tscircuit/core'

export const keyRows = [-21,-33,-45,-57,-69]
export const keyCols = [-14,0,14]
export const keyNames = [['CALL','OK','END'],['1','2','3'],['4','5','6'],['7','8','9'],['*','0','#']]

// Layout constants are world mm. Board children use Y+12 to compensate
// the board origin at Y=-12, checked against emitted pad centres.
// mm, PCB world frame: +X right, +Y toward earpiece, +Z toward user.
// B3F 6.5 x 4.5 hole centres; 1.1 drill / 2.0 pads from KiCad SW_PUSH_6mm.
// Physical top pair are internally common, bottom pair internally common.
// Pin numbers here are library aliases: switch plastic is not numbered.
// Datasheet/real-part continuity must be checked before manufacturing.
export function B3FFootprint() {
  return <footprint>
    {[[1,-3.25,2.25],[1,3.25,2.25],[2,-3.25,-2.25],[2,3.25,-2.25]].map(([n,x,y],i)=>
      <React.Fragment key={i}><platedhole portHints={[`pin${n}`]} pcbX={x} pcbY={y} shape="circle" holeDiameter={1.1} outerDiameter={2}/></React.Fragment>
    )}
    <silkscreenrect width={6} height={6} strokeWidth={0.12}/>
  </footprint>
}

export default function KeypadFloorplan() {
  return <board name="MAIN_FIT_STUDY" width={56} height={144} thickness={1.6} pcbY={-12} layers={4} routingDisabled>
    {[-24,24].flatMap((x)=>[-79,54].map((y)=><React.Fragment key={`${x}:${y}`}><hole name={`H_${x}_${y}`} diameter={2.3} pcbX={x} pcbY={y+12}/></React.Fragment>))}
    {keyRows.flatMap((y,r)=>keyCols.map((x,c)=><pushbutton key={`${r}:${c}`} name={`SW${r*3+c+1}`} footprint={B3FFootprint()} pcbX={x} pcbY={y+12} schX={c*5} schY={-r*3}
      connections={{pin1:`net.ROW${r}`,pin2:`net.COL${c}`}}/>))}
    <pcbnotetext text="FIT STUDY ONLY - NO MODEM / POWER / ROUTING" pcbX={0} pcbY={47} fontSize={1}/>
    <pcbnotetext text="NHD DISPLAY / FRONT" pcbX={0} pcbY={36} fontSize={1.2}/>
    <pcbnotetext text="FPC MATING TO VERIFY" pcbX={0} pcbY={5} fontSize={1}/>
  </board>
}

/** Electrical V16 variant: END key is dedicated to always-on pushbutton control.
 * The other14 keys remain scanned. Preserves existing switch positions/assembly.
 * Historical keypad routing output describes the original15-key matrix only. */
export function KeypadElectrical(){return <board name="KEYPAD_ELECTRICAL" width={56} height={144} routingDisabled>
 {keyRows.flatMap((y,r)=>keyCols.map((x,c)=><pushbutton key={`${r}:${c}`} name={`SW${r*3+c+1}`} manufacturerPartNumber="B3F-1050" footprint={B3FFootprint()} pcbX={x} pcbY={y+12} schX={c*5} schY={-r*3} connections={r===0&&c===2?{pin1:'net.BUTTON_BRANCH_UNQUALIFIED',pin2:'net.GND'}:{pin1:`net.ROW${r}`,pin2:`net.COL${c}`}}/>))}
</board>}
