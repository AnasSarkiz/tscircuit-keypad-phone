import React from 'react'
import '@tscircuit/core'
import data from '../sourcing/reviewed-lands-v24.json'
/** Isolated review candidates. No paste, no automatic assignment to the phone. */
export function ReviewedLandV24({kind}:{kind:keyof typeof data.packages}){
 const f=data.packages[kind]
 return <footprint>{f.pads.map(p=><React.Fragment key={p.pin}><smtpad portHints={[`pin${p.pin}`]} shape="rect" pcbX={p.x} pcbY={-p.y_down} width={p.width} height={p.height} cornerRadius={p.corner_radius} solderMaskMargin={f.mask_margin} noSolderPaste/></React.Fragment>)}{'polygons' in f && f.polygons.map(p=><React.Fragment key={p.pin}><smtpad portHints={[`pin${p.pin}`]} shape="polygon" points={p.points.map(q=>({x:q.x,y:-q.y_down}))} solderMaskMargin={f.mask_margin} noSolderPaste/></React.Fragment>)}</footprint>
}
