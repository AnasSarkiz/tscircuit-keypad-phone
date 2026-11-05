import React from 'react'
import '@tscircuit/core'

// Main-board schematic blocks, not a separate PCB. PCB rendering is disabled
// by tests/interfaces.tsx until mechanical and power release gates are closed.
export const channels = [
  {name:'TX',host:'HOST_TX',modem:'MODEM_RX',toModem:true},
  {name:'RX',host:'HOST_RX',modem:'MODEM_TX',toModem:false},
  {name:'RTS',host:'HOST_RTS',modem:'MODEM_RTS',toModem:true},
  {name:'CTS',host:'HOST_CTS',modem:'MODEM_CTS',toModem:false},
  // DTR/RI omitted: QuecOpen V1.0 startup drives 3 V, then low;
  // these pins default to GPIO, not the named modem functions.
  {name:'STATUS',host:'MODEM_STATUS_HOST_PENDING',modem:'MODEM_STATUS',toModem:false},
]
const net=(n:string)=>`net.${n}`
export function ModemLogic(){
 return <board name="MODEM_LOGIC_SCHEMATIC_ONLY" width={56} height={144} routingDisabled>
  {channels.map((ch,i)=> <group key={ch.name} name={`G_${ch.name}`} schX={(i%2)*22} schY={-Math.floor(i/2)*18}>
   <chip name={`U_${ch.name}`} manufacturerPartNumber="SN74AXC1T45DBVR"
    pinLabels={{pin1:'VCCA',pin2:'GND',pin3:'A',pin4:'B',pin5:'DIR',pin6:'VCCB'}}
    schPinArrangement={{leftSide:['VCCA','A','GND'],rightSide:['VCCB','B','DIR']}}
    connections={{VCCA:net('VLOGIC_3V15'),GND:net('GND'),A:net(ch.host),B:net(ch.modem),DIR:net(ch.toModem?'VLOGIC_3V15':'GND'),VCCB:net('MODEM_VDD_EXT_1V8')}}/>
   <capacitor name={`C_A_${ch.name}`} manufacturerPartNumber="C0603C104K5RACTU" capacitance="100nF" schX={-6} schY={4} connections={{pin1:net('VLOGIC_3V15'),pin2:net('GND')}}/>
   <capacitor name={`C_B_${ch.name}`} manufacturerPartNumber="C0603C104K5RACTU" capacitance="100nF" schX={6} schY={4} connections={{pin1:net('MODEM_VDD_EXT_1V8'),pin2:net('GND')}}/>
   <resistor name={`R_IDLE_${ch.name}`} resistance="100k" schY={-5} connections={{pin1:net(ch.toModem?'VLOGIC_3V15':'MODEM_VDD_EXT_1V8'),pin2:net(ch.toModem?ch.host:ch.modem)}}/>
  </group>)}
 </board>
}

// Candidate 3.15-V shared MCU/display supply. Fixed forced PWM is essential:
// power-save voltage positioning can exceed the display's 3.3-V maximum.
// PGND is synthetic logical pin15 for the unnumbered thermal pad, not a
// released land-pattern number. Physical star point belongs at the IC.
export function LogicSupply(){
 return <board name="LOGIC_SUPPLY_SCHEMATIC_ONLY" width={56} height={144} routingDisabled>
  <chip name="U_LOGIC" manufacturerPartNumber="TPS63020QDSJRQ1" schX={0} schY={0}
   pinLabels={{pin1:'VINA',pin2:'GND',pin3:'FB',pin4:'VOUT1',pin5:'VOUT2',pin6:'L2A',pin7:'L2B',pin8:'L1A',pin9:'L1B',pin10:'VIN1',pin11:'VIN2',pin12:'EN',pin13:'PS_SYNC',pin14:'PG',pin15:'EP_PGND'}}
   connections={{VINA:net('SYS_INPUT'),GND:net('GND'),FB:net('LOGIC_FB'),VOUT1:net('VLOGIC_3V15'),VOUT2:net('VLOGIC_3V15'),L2A:net('SW_L2'),L2B:net('SW_L2'),L1A:net('SW_L1'),L1B:net('SW_L1'),VIN1:net('SYS_INPUT'),VIN2:net('SYS_INPUT'),EN:net('LOGIC_ENABLE'),PS_SYNC:net('SYS_INPUT'),PG:net('LOGIC_POWER_GOOD'),EP_PGND:net('GND')}}/>
  <inductor name="L_LOGIC" inductance="2.2uH" manufacturerPartNumber="XGL4020-222MEC" schX={0} schY={9} connections={{pin1:net('SW_L1'),pin2:net('SW_L2')}}/>
  <resistor name="R_FB_TOP" resistance="1M" manufacturerPartNumber="RT0603BRD071ML" schX={8} schY={4} connections={{pin1:net('VLOGIC_3V15'),pin2:net('LOGIC_FB_SERIES')}}/>
  <resistor name="R_FB_TRIM" resistance="60k" manufacturerPartNumber="RT0603BRD0760KL" schX={8} schY={7} connections={{pin1:net('LOGIC_FB_SERIES'),pin2:net('LOGIC_FB')}}/>
  <resistor name="R_FB_BOTTOM" resistance="200k" schX={8} schY={0} connections={{pin1:net('LOGIC_FB'),pin2:net('GND')}}/>
  <resistor name="R_PG" resistance="1M" schX={8} schY={-5} connections={{pin1:net('VLOGIC_3V15'),pin2:net('LOGIC_POWER_GOOD')}}/>
  <resistor name="R_EN_OFF" resistance="100k" schX={-8} schY={-5} connections={{pin1:net('LOGIC_ENABLE'),pin2:net('GND')}}/>
  {[0,1].map(i=><capacitor key={i} name={`C_IN_${i}`} capacitance="10uF" schX={-8-i*4} schY={4} connections={{pin1:net('SYS_INPUT'),pin2:net('GND')}}/>)}
  <capacitor name="C_VINA" manufacturerPartNumber="C0603C104K5RACTU" capacitance="100nF" schX={-8} schY={0} connections={{pin1:net('SYS_INPUT'),pin2:net('GND')}}/>
  {[0,1,2,3].map(i=><capacitor key={i} name={`C_OUT_${i}`} capacitance="22uF" schX={14+i*4} schY={4} connections={{pin1:net('VLOGIC_3V15'),pin2:net('GND')}}/>)}
 </board>
}
