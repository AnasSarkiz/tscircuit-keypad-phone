import React from 'react'
import '@tscircuit/core'
export const debugPadsV45=[['TP_BOOT','MCU_BOOT_N',25.85],['TP_EN','MCU_EN',28.85],['TP_RX','DEBUG_RX_3V15',31.85],['TP_TX','DEBUG_TX_3V15',34.85],['TP_GND','GND',37.85],['TP_VREF','VLOGIC_3V15',40.85]] as const
/** Bare-board probe lands, not fitted components or qualified fixture geometry. */
export function McuTestAccessV45(){return <board width={56} height={144} routingDisabled>{debugPadsV45.map(([name,net])=><chip key={name} name={name} pinLabels={{pin1:'CONTACT'}} connections={{CONTACT:`net.${net}`}} footprint={<footprint><smtpad portHints={['pin1']} shape="rect" width={1.5} height={1.5} noSolderPaste/></footprint>}/>)}</board>}
