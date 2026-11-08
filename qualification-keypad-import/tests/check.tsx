import React from 'react'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { createHash } from 'node:crypto'
import { Circuit } from '@tscircuit/core'
import { B3F_1050 } from '../imports/B3F_1050/B3F_1050'
import { B3F1050Review } from '../review-candidate'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const evidence = JSON.parse(fs.readFileSync(path.join(root, 'source-evidence.json'), 'utf8'))
const hash = (b: Buffer) => createHash('sha256').update(b).digest('hex')
const verifyHash = (b: Buffer, expected: string) => assert.equal(hash(b), expected)
for (const [name, expected] of Object.entries(evidence.sha256)) {
  const bytes = fs.readFileSync(path.join(root, name))
  verifyHash(bytes, expected as string)
  assert.throws(() => verifyHash(Buffer.concat([bytes, Buffer.from('\nmutation')]), expected as string))
}
// Interval containment only: this is not a physical-fit or factory approval test.
const nominalUm = 1000
const factory = evidence.factory_reference
assert.equal(factory.url, 'https://jlcpcb.com/capabilities/Capabilities')
const minusUm = Math.round(factory.ordinary_through_hole_tolerance_mm.minus * 1000)
const plusUm = Math.round(factory.ordinary_through_hole_tolerance_mm.plus * 1000)
assert.deepEqual([minusUm,plusUm], [80,130])
const referenceUm = evidence.manufacturer_reference.reference_hole_range_mm.map((v:number)=>Math.round(v*1000))
assert.deepEqual(referenceUm, [950,1050])
assert.deepEqual([nominalUm-minusUm,nominalUm+plusUm], [920,1130])
const requiredNominalMinimumUm = referenceUm[0]+minusUm
const allowedNominalMaximumUm = referenceUm[1]-plusUm
assert.deepEqual([requiredNominalMinimumUm,allowedNominalMaximumUm], [1030,920])
assert.ok(requiredNominalMinimumUm > allowedNominalMaximumUm,
  'no nominal ordinary-order hole guarantees containment in the Omron reference interval')
assert.equal(factory.hole_position_tolerance_mm, 0.075)
assert.equal(factory.tighter_offering.label, 'press-fit')
assert.equal(factory.tighter_offering.tolerance_mm, 0.05)

// JSON records are deliberately inspected at runtime, including optional fields.
type RecordJson = Record<string, any>
const select = (j: RecordJson[], type: string) => j.filter(x => x.type === type)
const holes = (j: RecordJson[]) => select(j, 'pcb_plated_hole').map(h => {
  const pp = select(j, 'pcb_port').find(p => p.pcb_port_id === h.pcb_port_id)
  assert.ok(pp, 'every physical hole maps to a PCB port')
  const sp = select(j, 'source_port').find(p => p.source_port_id === pp.source_port_id)
  assert.ok(sp)
  return {pin: sp.pin_number, x: h.x, y: h.y, outer: h.outer_diameter, hole: h.hole_diameter}
}).sort((a,b) => a.pin-b.pin)
const groupPins = (j: RecordJson[]) => select(j, 'source_component_internal_connection').map(g =>
  g.source_port_ids.map((id: string) => select(j, 'source_port').find(p => p.source_port_id === id)!.pin_number).sort()).sort()
function checkCandidate(j: RecordJson[], raw: RecordJson[]) {
  assert.equal(select(j, 'pcb_plated_hole').length, 4)
  assert.equal(select(j, 'pcb_port').length, 4)
  assert.equal(select(j, 'source_port').length, 4)
  const actual = holes(j), baseline = holes(raw)
  assert.deepEqual(actual.map(({hole, ...p})=>p), baseline.map(({hole, ...p})=>p), 'copper centers/outer diameters unchanged')
  assert.ok(actual.every(h => h.hole === 1))
  assert.deepEqual(groupPins(j), [[1,2],[3,4]])
  const ports = select(j, 'source_port')
  const net = (pin: number) => ports.find(p => p.pin_number === pin)!.subcircuit_connectivity_map_key
  assert.ok(net(1)); assert.ok(net(3))
  assert.equal(net(1),net(2)); assert.equal(net(3),net(4)); assert.notEqual(net(1),net(3))
  const cad = select(j, 'cad_component')
  assert.equal(cad.length, 1)
  assert.equal(cad[0].show_as_bounding_box, true)
  assert.ok(!Object.entries(cad[0]).some(([k,v]) => /url|model.*path/i.test(k) && v))
  assert.equal(select(j, 'pcb_solder_paste').length, 0)
  assert.equal(j.filter(x=>x.type.includes('error')).length, 0)
}
let cases=0, mutations=0
for (const layer of ['top','bottom'] as const) for (const rotation of [0,90,180,270]) {
  const results: RecordJson[][]=[]
  for (const Component of [B3F_1050,B3F1050Review]) {
    const c=new Circuit(); c.schematicDisabled=true
    c.add(<board width={30} height={30} routingDisabled>
      <Component name="SW1" layer={layer} pcbRotation={rotation} pcbX={2} pcbY={-3}
        connections={{pin1:'net.A',pin2:'net.A',pin3:'net.B',pin4:'net.B'}} />
    </board>)
    await c.renderUntilSettled(); results.push(c.getCircuitJson() as RecordJson[])
  }
  const [raw, review]=results
  assert.equal(holes(raw).length,4)
  assert.ok(holes(raw).every(h=>Math.abs(h.hole-1.1999976)<1e-9 && Math.abs(h.outer-1.7999964)<1e-9))
  assert.deepEqual(groupPins(raw), [])
  if (layer === 'top' && rotation === 0) for (const h of holes(raw)) {
    const source = evidence.pads.find((p: {pin:string})=>Number(p.pin)===h.pin).source_mm
    assert.ok(Math.abs(h.x-(source.x+2))<1e-8)
    assert.ok(Math.abs(h.y-(source.y-3))<1e-8)
    assert.ok(Math.abs(h.outer-source.outer)<1e-8)
    assert.ok(Math.abs(h.hole-source.hole)<1e-8)
  }
  assert.equal(select(raw,'pcb_solder_paste').length,0)
  // Each physical common pair stays on the long 6.5 mm axis through flips/rotations.
  for (const j of [raw,review]) for (const [a,b] of [[1,2],[3,4]]) {
    const hs=holes(j); const p=hs.find(h=>h.pin===a)!,q=hs.find(h=>h.pin===b)!
    assert.ok(Math.abs(Math.hypot(p.x-q.x,p.y-q.y)-6.49986)<1e-8)
  }
  checkCandidate(review,raw)
  const change = (fn:(j:RecordJson[])=>void) => {
    const bad=structuredClone(review); fn(bad)
    assert.throws(()=>checkCandidate(bad,raw)); mutations++
  }
  change(j=>select(j,'pcb_plated_hole')[0].x+=0.1)
  change(j=>select(j,'pcb_plated_hole')[0].outer_diameter+=0.1)
  change(j=>select(j,'pcb_plated_hole')[0].hole_diameter=1.2)
  change(j=>select(j,'source_component_internal_connection')[0].source_port_ids[1]=select(j,'source_port')[2].source_port_id)
  change(j=>j.splice(j.findIndex(x=>x.type==='cad_component'),1))
  change(j=>j.push({type:'pcb_solder_paste'}))
  cases++
}
console.log(`PASS ${cases} placements (top/bottom × 4 rotations), ${mutations} rejected mutations; raw import hashes immutable; geometry/common groups/model quarantine/paste checks`)
