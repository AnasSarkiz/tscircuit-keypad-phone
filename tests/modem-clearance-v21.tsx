import React from 'react'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import {Circuit} from '@tscircuit/core'
import {ModemLandCandidate} from '../electronics/modem-footprint'
import {modemPins} from '../electronics/modem-support'
import {convertCircuitJsonToPcbSvg} from 'circuit-to-svg'
const c=new Circuit();c.add(<board width={40} height={45} routingDisabled><chip name="U_MODEM_REVIEW" pinLabels={Object.fromEntries(Object.entries(modemPins).map(([p,l])=>['pin'+p,l]))} footprint={<ModemLandCandidate/>}/></board>);await c.renderUntilSettled();const j:any[]=c.getCircuitJson()
assert.equal(j.filter(x=>x.type==='pcb_smtpad').length,126)
assert.equal(j.filter(x=>x.type==='pcb_solder_paste').length,0,'unqualified modem paste must be disabled')
const cy=j.filter(x=>x.type==='pcb_courtyard_rect');assert.equal(cy.length,1);assert.equal(cy[0].width,31);assert.equal(cy[0].height,35)
assert.equal(j.filter(x=>x.type==='pcb_component_missing_courtyard_warning').length,0)
assert.deepEqual(j.filter(x=>/error$/.test(x.type)),[])
fs.writeFileSync('output/modem-footprint-v21.circuit.json',JSON.stringify(j,null,2));fs.writeFileSync('output/modem-footprint-v21.svg',convertCircuitJsonToPcbSvg(j))
console.log('PASS 126 copper lands, zero modem paste, explicit 31x35 courtyard; not stencil-ready')
