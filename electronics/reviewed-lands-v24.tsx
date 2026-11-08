import React from 'react'
import { JlcBoardLands } from './jlc-board-lands'
export const reviewedJlcParts = { DLA0010A: 'C2845237', RUK0020B: 'C2876380', DMQ0006A: 'C3189972', RPW0010A: 'C3662793' } as const
// Compatibility export: catalog copper, not the historical TI mask/radius construction.
// No paste is released. Manufacturing qualification remains separate.
export function ReviewedLandV24({ kind }: { kind: keyof typeof reviewedJlcParts }) { return <JlcBoardLands part={reviewedJlcParts[kind]} /> }
