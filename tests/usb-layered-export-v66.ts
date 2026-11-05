import fs from 'node:fs'
import {pcb_trace,pcb_via,pcb_copper_pour,pcb_smtpad,pcb_plated_hole} from 'circuit-json'
import {convertCircuitJsonToPcbSvg} from 'circuit-to-svg'
const j=JSON.parse(fs.readFileSync('output/usb-layered-v66.circuit.json','utf8'))
for(const x of j){if(x.type==='pcb_plated_hole')pcb_plated_hole.parse(x);if(x.type==='pcb_smtpad'){pcb_smtpad.parse(x);if(typeof x.soldermask_margin!=='number')throw new Error('Unspecified mask expansion')} if(x.type==='pcb_trace')pcb_trace.parse(x);if(x.type==='pcb_via')pcb_via.parse(x);if(x.type==='pcb_copper_pour')pcb_copper_pour.parse(x)}
fs.writeFileSync('output/usb-layered-v66.svg',convertCircuitJsonToPcbSvg(j));console.log('PASS layered traces, vias and exact triangulated pour schemas; SVG exported')
