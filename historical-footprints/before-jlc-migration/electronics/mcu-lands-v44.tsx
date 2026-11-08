import React from 'react'
import data from '../sourcing/mcu-lands-v44.json'
// Exact manufacturer KiCad copper; two identical duplicates removed. No paste released.
export function McuLandsV44(){return <footprint>{data.pads.map((p,i)=><smtpad portHints={[`pin${p.pin}`]} shape="rect" pcbX={p.x} pcbY={-(p.y_down+3)} width={p.width} height={p.height} noSolderPaste/>)}</footprint>}
