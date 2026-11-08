import React from 'react'
import data from '../sourcing/modem-pad-transcription-v19.json'
/** Copper geometry/numbering independently overlaid against V1.0; variant/process still blocked. */
export function ModemLandCandidate(){return <footprint><courtyardrect width={31} height={35}/>{data.pads.map(p=><React.Fragment key={p.pin}><smtpad portHints={[`pin${p.pin}`]} shape="rect" noSolderPaste pcbX={p.x} pcbY={-p.y_down} width={p.width} height={p.height}/></React.Fragment>)}</footprint>}
