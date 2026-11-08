import React from 'react'
import type { ChipProps } from '@tscircuit/props'
import { ESP32_S3_WROOM_1_N16 } from '../imports/ESP32_S3_WROOM_1_N16/ESP32_S3_WROOM_1_N16'
import { EG912UGLAC_I05_SNNSA } from '../imports/EG912UGLAC_I05_SNNSA/EG912UGLAC_I05_SNNSA'
import { TPS63802DLAR } from '../imports/TPS63802DLAR/TPS63802DLAR'
import { TPD6S300ARUKR } from '../imports/TPD6S300ARUKR/TPD6S300ARUKR'
import { TPS62827ADMQR } from '../imports/TPS62827ADMQR/TPS62827ADMQR'
import { TPS259470LRPWR } from '../imports/TPS259470LRPWR/TPS259470LRPWR'

const parts = {
  C2913199: ESP32_S3_WROOM_1_N16,
  C7472750: EG912UGLAC_I05_SNNSA,
  C2845237: TPS63802DLAR,
  C2876380: TPD6S300ARUKR,
  C3189972: TPS62827ADMQR,
  C3662793: TPS259470LRPWR,
}
export type ImportedPhonePartId = keyof typeof parts

function withoutPaste(node: React.ReactNode): React.ReactNode {
  if (Array.isArray(node)) return React.Children.map(node, withoutPaste)
  if (!React.isValidElement<Record<string, any>>(node)) return node
  const changes: Record<string, any> = {}
  if (node.type === 'smtpad') changes.noSolderPaste = true
  if (node.props.children) changes.children = withoutPaste(node.props.children)
  return React.cloneElement(node, changes)
}

/**
 * Isolated review adapters. Keep the downloaded imports byte-for-byte intact.
 * Correct manufacturer-specific symbol contracts and suppress unqualified paste.
 * Copper, mask defaults and model orientation still require assembly review.
 * These components are deliberately not substituted into the historical V66 PCB.
 */
export function ImportedPhonePartForReview({ part, ...props }: ChipProps & { part: ImportedPhonePartId }) {
  const imported = (parts[part] as Function)(props) as React.ReactElement<Record<string, any>>
  const pinLabels = { ...imported.props.pinLabels }
  const pinAttributes = { ...imported.props.pinAttributes }
  if (part === 'C2876380') {
    // TI TPD6S300A pin table: SBU (not SUB), NC16/17 and thermal pad21 -> GND.
    Object.assign(pinLabels, { pin1: ['C_SBU1'], pin2: ['C_SBU2'], pin15: ['SBU1'], pin16: ['NC1'], pin17: ['NC2'], pin21: ['GND_EP'] })
    for (const pin of [16, 17, 21]) pinAttributes[`pin${pin}`] = { ...pinAttributes[`pin${pin}`], requiresGround: true }
  }
  if (part === 'C3662793') {
    // TPS259470L specifically: the OVCSEL/PG/PGTH functions belong to other variants.
    Object.assign(pinLabels, { pin2: ['OVLO'], pin3: ['AUXOFF'], pin4: ['N_FLT'] })
  }
  return React.cloneElement(imported, { pinLabels, pinAttributes, footprint: withoutPaste(imported.props.footprint) })
}
