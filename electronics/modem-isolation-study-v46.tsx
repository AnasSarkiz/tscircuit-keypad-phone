import React from 'react'
import '@tscircuit/core'
/** Isolated topology study. No main-board substitution or footprint; guard remains unimplemented. */
export function ModemIsolationStudyV46(){return <board name="ISOLATION_STUDY_NOT_INTEGRATED" width={56} height={144} routingDisabled>
 <chip name="U_ALT_SWITCH" manufacturerPartNumber="TMUX1511PWR" pinLabels={{pin1:'SEL1',pin2:'S1',pin3:'D1',pin4:'SEL2',pin5:'S2',pin6:'D2',pin7:'GND',pin8:'D3',pin9:'S3',pin10:'SEL3',pin11:'D4',pin12:'S4',pin13:'SEL4',pin14:'VDD'}} connections={{SEL1:'net.ALT_KEY_CMD',S1:'net.ALT_MODEM_KEY',D1:'net.ALT_KEY_MID',SEL2:'net.ALT_HARDWARE_VALID_PENDING',S2:'net.ALT_KEY_MID',D2:'net.ALT_GND',GND:'net.ALT_GND',D3:'net.ALT_RESET_MID',S3:'net.ALT_MODEM_RESET',SEL3:'net.ALT_RESET_CMD',D4:'net.ALT_GND',S4:'net.ALT_RESET_MID',SEL4:'net.ALT_HARDWARE_VALID_PENDING',VDD:'net.ALT_RETAINED_MODEM_SUPPLY_PENDING'}}/>
 <capacitor name="C_ALT_BYPASS" capacitance="100nF" manufacturerPartNumber="C0603C104K5RACTU" connections={{pin1:'net.ALT_RETAINED_MODEM_SUPPLY_PENDING',pin2:'net.ALT_GND'}}/>
 {['KEY_CMD','RESET_CMD','HARDWARE_VALID_PENDING'].map((n,i)=><resistor key={n} name={'R_ALT_OFF_'+i} resistance="100k" manufacturerPartNumber="RT0603BRD07100KL" connections={{pin1:'net.ALT_'+n,pin2:'net.ALT_GND'}}/>)}
</board>}
