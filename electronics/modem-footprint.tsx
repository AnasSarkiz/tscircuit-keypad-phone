import React from 'react'
import { JlcBoardLands } from './jlc-board-lands'
// Exact C7472750 copper. Body-center datum and 3 mm neighbor clearance retained.
// Geometry does not establish QuecOpen firmware or carrier compatibility.
export function ModemLandCandidate() { return <JlcBoardLands part="C7472750" modemCourtyard /> }
