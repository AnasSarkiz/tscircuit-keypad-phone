import React from 'react'
import { B3F_1050 } from './imports/B3F_1050/B3F_1050'

type ImportedProps = Parameters<typeof B3F_1050>[0]
// Callers may place this isolated review candidate, not override its reviewed geometry.
export type KeypadReviewProps = Omit<ImportedProps,
  'footprint' | 'cadModel' | 'internallyConnectedPins'>

/** Quarantined review only. 1.00 mm is the manufacturer nominal PCB-hole target,
 * not a validated raw drill tool size. Copper/mask/process and physical fit remain open.
 * Catalog labels are rotated 180 degrees from Omron's printed top view.
 */
export const B3F1050Review = (props: KeypadReviewProps) => {
  const raw = B3F_1050(props)
  const footprint = raw.props.footprint as React.ReactElement<{children: React.ReactNode}>
  const reviewedFootprint = React.cloneElement(footprint, {},
    React.Children.map(footprint.props.children, child => {
      if (!React.isValidElement(child) || child.type !== 'platedhole') return child
      return React.cloneElement(child as React.ReactElement<{holeDiameter: number}>, {holeDiameter: 1})
    }))
  return React.cloneElement(raw, {
    footprint: reviewedFootprint,
    cadModel: undefined,
    internallyConnectedPins: [['pin1', 'pin2'], ['pin3', 'pin4']],
  })
}
