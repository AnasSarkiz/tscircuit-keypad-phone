import React from 'react'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import { Circuit } from '@tscircuit/core'
import { convertCircuitJsonToPcbSvg } from 'circuit-to-svg'
import { ESP32_S3_WROOM_1_N16 } from '../imports/ESP32_S3_WROOM_1_N16/ESP32_S3_WROOM_1_N16'
import { EG912UGLAC_I05_SNNSA } from '../imports/EG912UGLAC_I05_SNNSA/EG912UGLAC_I05_SNNSA'
import { TPS63802DLAR } from '../imports/TPS63802DLAR/TPS63802DLAR'
import { TPD6S300ARUKR } from '../imports/TPD6S300ARUKR/TPD6S300ARUKR'
import { TPS62827ADMQR } from '../imports/TPS62827ADMQR/TPS62827ADMQR'
import { TPS259470LRPWR } from '../imports/TPS259470LRPWR/TPS259470LRPWR'
import { ImportedPhonePartForReview, type ImportedPhonePartId } from '../electronics/jlc-review-candidates'

// Imported parts are isolated review candidates, not substitutions into V66.
// The checks below exercise actual tscircuit output and terminal connectivity.
// They do not approve solder mask, paste, component placement or model fit.
const cases = [
  { component: ESP32_S3_WROOM_1_N16, mpn: 'ESP32-S3-WROOM-1-N16', id: 'C2913199', terminals: 41, pads: 49, ground: [1, 40, 41], power: [2] },
  { component: EG912UGLAC_I05_SNNSA, mpn: 'EG912UGLAC-I05-SNNSA', id: 'C7472750', terminals: 126, pads: 126, ground: [3, 31, 47, 48, 50, 54, 55, 58, 59, 61, 62], power: [32, 33, 52, 53] },
  { component: TPS63802DLAR, mpn: 'TPS63802DLAR', id: 'C2845237', terminals: 10, pads: 10, ground: [3, 8], power: [10], extra: { pin1: 'net.VTEST', pin2: 'net.GND' } },
  { component: TPD6S300ARUKR, mpn: 'TPD6S300ARUKR', id: 'C2876380', terminals: 21, pads: 21, ground: [8, 13, 16, 17, 18, 21], power: [3, 10] },
  { component: TPS62827ADMQR, mpn: 'TPS62827ADMQR', id: 'C3189972', terminals: 6, pads: 6, ground: [4], power: [6] },
  { component: TPS259470LRPWR, mpn: 'TPS259470LRPWR', id: 'C3662793', terminals: 10, pads: 10, ground: [8], power: [5] },
]

fs.mkdirSync('output/jlc-imports', { recursive: true })
const report: unknown[] = []
const selectedIds = process.argv.slice(2)
assert.ok(selectedIds.every(id => cases.some(item => item.id === id)), 'unknown part selector')
const catalogPads = new Map<string, unknown[]>()
for (const mode of ['catalog', 'review'] as const) {
for (const item of cases.filter(item => selectedIds.length === 0 || selectedIds.includes(item.id))) {
  const Component = (mode === 'catalog' ? item.component : (props: any) => ImportedPhonePartForReview({ ...props, part: item.id as ImportedPhonePartId })) as React.ComponentType<any>
  const connections: Record<string, string> = { ...item.extra }
  const importedProps = (Component as Function)({ name: 'U_IMPORT' }).props
  // Honor additional generated ground requirements as well as explicit
  // manufacturer-required grounds (including the USB protector's NC and EP).
  const grounds = new Set(item.ground)
  for (const [pin, attributes] of Object.entries(importedProps.pinAttributes ?? {}) as [string, any][]) {
    if (attributes.requiresGround) grounds.add(Number(pin.replace('pin', '')))
    if (attributes.requiresPower) connections[pin] = 'net.VTEST'
  }
  for (const pin of grounds) connections[`pin${pin}`] = 'net.GND'
  for (const pin of item.power) connections[`pin${pin}`] = 'net.VTEST'
  const circuit = new Circuit()
  circuit.schematicDisabled = true
  circuit.add(<board width={60} height={60} routingDisabled>
    <Component name="U_IMPORT" connections={connections} />
  </board>)
  await circuit.renderUntilSettled()
  const json: any[] = circuit.getCircuitJson()
  // Preserve failing output too: absent PCB ports must remain inspectable.
  fs.writeFileSync(`output/jlc-imports/${item.id}-${mode}.circuit.json`, JSON.stringify(json, null, 2))
  fs.writeFileSync(`output/jlc-imports/${item.id}-${mode}.svg`, convertCircuitJsonToPcbSvg(json))
  const pads = json.filter(x => x.type === 'pcb_smtpad')
  const sources = json.filter(x => x.type === 'source_component')
  assert.equal(sources.length, 1)
  assert.equal(sources[0].manufacturer_part_number, item.mpn)
  assert.deepEqual(sources[0].supplier_part_numbers.jlcpcb, [item.id])
  assert.equal(pads.length, item.pads)
  const geometry = pads.map(p => ({ pin: p.port_hints[0], shape: p.shape, x: p.x, y: p.y, width: p.width, height: p.height, points: p.points }))
  if (mode === 'catalog') catalogPads.set(item.id, geometry)
  else {
    assert.deepEqual(geometry, catalogPads.get(item.id), 'review adapter must not silently change copper')
    assert.equal(json.filter(x => x.type === 'pcb_solder_paste').length, 0)
    if (item.id === 'C2876380') {
      assert.deepEqual(importedProps.pinLabels.pin1, ['C_SBU1'])
      assert.deepEqual(importedProps.pinLabels.pin2, ['C_SBU2'])
      assert.deepEqual(importedProps.pinLabels.pin15, ['SBU1'])
      for (const pin of [16, 17, 21]) assert.equal(importedProps.pinAttributes[`pin${pin}`].requiresGround, true)
    }
    if (item.id === 'C3662793') {
      assert.deepEqual(importedProps.pinLabels.pin2, ['OVLO'])
      assert.deepEqual(importedProps.pinLabels.pin3, ['AUXOFF'])
      assert.deepEqual(importedProps.pinLabels.pin4, ['N_FLT'])
    }
  }
  assert.equal(json.filter(x => x.type === 'pcb_plated_hole').length, 0)
  const actualPins = [...new Set(pads.map(p => Number(p.port_hints[0].replace('pin', ''))))].sort((a, b) => a - b)
  assert.deepEqual(actualPins, Array.from({ length: item.terminals }, (_, i) => i + 1))
  for (const pad of pads) {
    assert.ok(pad.pcb_port_id, `${item.id} ${pad.port_hints}: missing PCB port`)
    const pcbPort = json.find(x => x.type === 'pcb_port' && x.pcb_port_id === pad.pcb_port_id)
    const sourcePort = json.find(x => x.type === 'source_port' && x.source_port_id === pcbPort.source_port_id)
    assert.ok(sourcePort.port_hints.includes(pad.port_hints[0]), `${item.id}: pad mapped to wrong logical port`)
    const pin = Number(pad.port_hints[0].replace('pin', ''))
    if (grounds.has(pin)) {
      const connectedIds = new Set([sourcePort.source_port_id])
      for (const group of sources[0].internally_connected_source_port_ids ?? []) {
        if (group.includes(sourcePort.source_port_id)) for (const id of group) connectedIds.add(id)
      }
      const traces = json.filter(x => x.type === 'source_trace' && x.connected_source_port_ids.some((id: string) => connectedIds.has(id)))
      const netNames = new Set(traces.flatMap(t => t.connected_source_net_ids).map(id => json.find(x => x.type === 'source_net' && x.source_net_id === id)?.name))
      assert.deepEqual([...netNames], ['GND'], `${item.id} pin${pin}: required ground not explicit`)
    }
  }
  if (item.id === 'C2913199') assert.equal(pads.filter(p => p.port_hints.includes('pin41')).length, 9)
  if (item.id === 'C3662793') assert.deepEqual(pads.filter(p => p.shape === 'polygon').map(p => p.port_hints[0]).sort(), ['pin1', 'pin10', 'pin4', 'pin7'])
  const errors = json.filter(x => /error$/.test(x.type))
  assert.deepEqual(errors, [], `${item.id}: emitted diagnostics`)
  report.push({ mode, mpn: item.mpn, id: item.id, terminals: actualPins.length, copperPrimitives: pads.length,
    explicitGroundTerminals: [...grounds].sort((a, b) => a - b), diagnostics: errors,
    status: 'isolated import connectivity only; copper routing disabled; geometry and manufacturing review separate' })
  console.log(`PASS ${item.id} ${item.mpn} (${mode}): ${actualPins.length} terminals, ${pads.length} copper primitives`)
}
}
fs.writeFileSync('output/jlc-imports/connectivity-report.json', JSON.stringify(report, null, 2))
