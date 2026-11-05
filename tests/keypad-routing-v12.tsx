import React from 'react'
import fs from 'node:fs'
import {Circuit} from '@tscircuit/core'
import {convertCircuitJsonToPcbSvg} from 'circuit-to-svg'
import Keypad from '../electronics/keypad'
// Standalone matrix routing experiment. Does not include MCU escape, RF, power,
// rear-side placement or mechanical keepouts; never merge blindly into main PCB.
const element=Keypad()
const c=new Circuit()
c.add(React.cloneElement(element,{routingDisabled:false,autorouter:{local:true,preset:'auto_local',traceClearance:.2}},React.Children.map(element.props.children,(child:any)=>React.isValidElement(child)&&String((child.props as any).text??'').includes('NO MODEM / POWER / ROUTING')?React.cloneElement(child as React.ReactElement<any>,{text:'KEYPAD ROUTING STUDY ONLY - INCOMPLETE PHONE'}):child),<autoroutingphase minTraceToPadEdgeClearance={.2} minTraceWidth={.2} minBoardEdgeClearance={.5}/>))
await c.renderUntilSettled()
const j:any[]=c.getCircuitJson()
fs.writeFileSync('output/keypad-routing-v12.circuit.json',JSON.stringify(j,null,2))
fs.writeFileSync('output/keypad-routing-v12.svg',convertCircuitJsonToPcbSvg(j,{width:700,height:1200}))
const report={scope:'Local autorouter isolated keypad experiment; no whole-phone placement or manufacturing validation',traces:j.filter(x=>x.type==='pcb_trace').length,vias:j.filter(x=>x.type==='pcb_via').length,diagnostics:j.filter(x=>/error$/.test(x.type)),fabrication_ready:false}
fs.writeFileSync('output/keypad-routing-v12-checks.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2))
