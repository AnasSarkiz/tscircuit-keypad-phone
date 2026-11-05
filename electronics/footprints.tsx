import React from 'react'
import '@tscircuit/core'
// TI DDC0006A land-pattern dimensions, drawing 4214841/E (08/2024).
// Top view, circuit coordinate Y up. Rectangular pad approximation omits R0.05 corners.
// Stencil, solder-mask expansion, courtyard and assembler approval still pending.
export function DDC0006A(){return <footprint>
 {[[1,-1.35,.95],[2,-1.35,0],[3,-1.35,-.95],[4,1.35,-.95],[5,1.35,0],[6,1.35,.95]].map(([p,x,y])=><React.Fragment key={p}><smtpad portHints={[`pin${p}`]} shape="rect" pcbX={x} pcbY={y} width={1.1} height={.6}/></React.Fragment>)}
 <silkscreenpath route={[{x:-.65,y:1.6},{x:.65,y:1.6}]} strokeWidth={.12}/>
 <silkscreencircle pcbX={-2.1} pcbY={.95} radius={.15} strokeWidth={.12}/>
</footprint>}

// Engineering proposal, NOT Yageo's recommended land pattern or IPC certification.
// 0603 RT/RC body/terminal bounds from manufacturer sheets; assembly process pending.
export function Yageo0603ResistorCandidate(){return <footprint>
 <smtpad portHints={['pin1']} shape="rect" pcbX={-.85} pcbY={0} width={1} height={1.1}/>
 <smtpad portHints={['pin2']} shape="rect" pcbX={.85} pcbY={0} width={1} height={1.1}/>
</footprint>}

// Engineering candidates from dimensional bounds only; not manufacturer land recommendations.
export const capacitorLandGeometry={
 '0603':{center:.85,width:1,height:1.15},
 '0805':{center:1.05,width:1.2,height:1.65},
 '1210':{center:1.65,width:1.3,height:3.0},
}
export function CapacitorLandCandidate({size}:{size:keyof typeof capacitorLandGeometry}){
 const g=capacitorLandGeometry[size];return <footprint>
 {[1,2].map(p=><React.Fragment key={p}><smtpad portHints={[`pin${p}`]} shape="rect" pcbX={(p===1?-1:1)*g.center} pcbY={0} width={g.width} height={g.height}/></React.Fragment>)}
 </footprint>
}

// TI DBV0005A/DBV0006A dimensional transcription; visual orientation audit pending.
// Rectangles omit 0.05mm corner radius; no mask/paste/courtyard release.
export function TiDbvCandidate({pins}:{pins:5|6}){
 const coords=pins===5?[[1,-1.3,.95],[2,-1.3,0],[3,-1.3,-.95],[4,1.3,-.95],[5,1.3,.95]]:[[1,-1.3,.95],[2,-1.3,0],[3,-1.3,-.95],[4,1.3,-.95],[5,1.3,0],[6,1.3,.95]]
 return <footprint>{coords.map(([p,x,y])=><React.Fragment key={p}><smtpad portHints={[`pin${p}`]} shape="rect" pcbX={x} pcbY={y} width={1.1} height={.6}/></React.Fragment>)}</footprint>
}

// AO3400A PO-00001 version N: parent independently reviewed top-view copper orientation.
// CAD Y up: G lower-left, S lower-right, D upper. Mask/paste/process remain unreleased.
export function Ao3400LandCandidate(){return <footprint>
 {[[1,-.95,-1.2],[2,.95,-1.2],[3,0,1.2]].map(([p,x,y])=><React.Fragment key={p}><smtpad portHints={[`pin${p}`]} shape="rect" pcbX={x} pcbY={y} width={.8} height={.8}/></React.Fragment>)}
</footprint>}

// Text-derived proposals. Not visually verified; do not export for fabrication.
// TI D0008A 4214825/C: 5.4 row spacing,1.27 pitch,1.55x0.6 lands.
// ADI2954fb TS8:2.62 REF row spacing,.65 pitch,1.22 REF x .40 MAX lands.
export function DualRow8Candidate({kind}:{kind:'TI_D8'|'ADI_TS8'}){
 const [row,pitch,w,h]=kind==='TI_D8'?[2.7,1.27,1.55,.6]:[1.31,.65,1.22,.4]
 return <footprint>{Array.from({length:8},(_,i)=>{const p=i+1;return <React.Fragment key={p}><smtpad portHints={[`pin${p}`]} shape="rect" pcbX={p<=4?-row:row} pcbY={(p<=4?2.5-p:p-6.5)*pitch} width={w} height={h}/></React.Fragment>})}</footprint>
}

// TI DRL0005A4220753/E11/2024; text-derived dimensions, pending drawing audit.
export function TiDrl5Candidate(){return <footprint>{[[1,-.74,.5],[2,-.74,0],[3,-.74,-.5],[4,.74,-.5],[5,.74,.5]].map(([p,x,y])=><React.Fragment key={p}><smtpad portHints={[`pin${p}`]} shape="rect" pcbX={x} pcbY={y} width={.67} height={.3}/></React.Fragment>)}</footprint>}

// Engineering proposal for Coilcraft XGL4020/XFL4015, NOT copied recommended lands.
// Nominal terminal centers3.25mm; termination bounds require independent drawing audit.
export function Coilcraft4mmCandidate(){return <footprint>{[1,2].map(p=><React.Fragment key={p}><smtpad portHints={[`pin${p}`]} shape="rect" pcbX={p===1?-1.625:1.625} pcbY={0} width={1.3} height={2.5}/></React.Fragment>)}</footprint>}
