import fs from 'node:fs'
import assert from 'node:assert/strict'
import {pcb_trace} from 'circuit-json'
import {convertCircuitJsonToPcbSvg} from 'circuit-to-svg'
const j=JSON.parse(fs.readFileSync('output/usb-routed-v29.circuit.json','utf8'))
const traces=j.filter((x:any)=>x.type==='pcb_trace');assert.equal(traces.length,9)
for(const t of traces)pcb_trace.parse(t)
fs.writeFileSync('output/usb-routed-v29.svg',convertCircuitJsonToPcbSvg(j));console.log('PASS nine manual routes conform to Circuit JSON trace schema; SVG exported')
