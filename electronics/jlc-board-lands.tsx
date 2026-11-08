import React from 'react'
import { ImportedPhonePartForReview, type ImportedPhonePartId } from './jlc-review-candidates'

// Legacy MCU Y = -Y_kicad - 3 mm. JLC Y = -Y_kicad + 0.7849527 mm.
// Apply before component rotation and bottom-layer X reflection.
export const MCU_IMPORT_TO_BOARD_Y = -3.7849527
function mm(value: unknown): number {
  if (typeof value === 'number' && Number.isFinite(value)) return value
  if (typeof value === 'string' && /^-?\d+(\.\d+)?mm$/.test(value)) return Number(value.slice(0, -2))
  if (value === undefined) return 0
  throw new Error(`Unsupported imported coordinate: ${value}`)
}
/** Copper-only migration. Retain board symbols/nets, including pending modem functions.
 * Imported courtyard/model bounds must not move existing component datums. */
export function JlcBoardLands({ part, offsetY = 0, modemCourtyard = false }: {
  part: ImportedPhonePartId; offsetY?: number; modemCourtyard?: boolean
}) {
  const element = ImportedPhonePartForReview({ part, name: 'LAND_SOURCE' })
  const footprint = element.props.footprint as React.ReactElement<any>
  const pads = React.Children.toArray(footprint.props.children).filter((node): node is React.ReactElement<any> => React.isValidElement(node) && node.type === 'smtpad')
  if (!pads.length) throw new Error(`No imported copper found for ${part}`)
  return <footprint>
    {modemCourtyard && <courtyardrect width={31} height={35} />}
    {pads.map((pad, index) => React.cloneElement(pad, {
      key: `${part}-${index}`, noSolderPaste: true,
      ...(pad.props.shape === 'polygon'
        ? { points: pad.props.points.map((point: any) => ({ x: mm(point.x), y: mm(point.y) + offsetY })) }
        : { pcbX: mm(pad.props.pcbX), pcbY: mm(pad.props.pcbY) + offsetY }),
    }))}
  </footprint>
}
