import React from 'react'
import { JlcBoardLands, MCU_IMPORT_TO_BOARD_Y } from './jlc-board-lands'
// Compatibility export: exact JLC C2913199 copper at the legacy board datum.
// This is no longer the absent historical manufacturer KiCad JSON.
export function McuLandsV44() { return <JlcBoardLands part="C2913199" offsetY={MCU_IMPORT_TO_BOARD_Y} /> }
