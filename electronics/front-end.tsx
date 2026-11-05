import React from 'react'
import '@tscircuit/core'
const net=(s:string)=>`net.${s}`
// Logical connector numbering only. No released footprint or FPC fold claim.
export function DisplayInterface(){
 const labels=['GND1','IOVDD','VDD','CS_N','RST_N','SDIO','GND7','DC','SCL','GND10','SPI4W','TE','NC13','NC14','NC15','NC16','LEDA','LEDK1','LEDK2','GND20','NC21','NC22','NC23','NC24']
 return <board name="DISPLAY_SCHEMATIC_ONLY" width={56} height={144} routingDisabled>
  <chip name="J_LCD" manufacturerPartNumber="0524352471" pinLabels={Object.fromEntries(labels.map((l,i)=>[`pin${i+1}`,l]))}
   connections={{GND1:net('GND'),IOVDD:net('VLOGIC_3V15'),VDD:net('VLOGIC_3V15'),CS_N:net('LCD_CS_N'),RST_N:net('LCD_RST_N'),SDIO:net('LCD_SDIO'),GND7:net('GND'),DC:net('LCD_DC'),SCL:net('LCD_SCL'),GND10:net('GND'),SPI4W:net('VLOGIC_3V15'),LEDA:net('BACKLIGHT_ANODE_PENDING'),LEDK1:net('BACKLIGHT_SINK1_PENDING'),LEDK2:net('BACKLIGHT_SINK2_PENDING'),GND20:net('GND')}}/>
  <capacitor name="C_LCD_IO" manufacturerPartNumber="C0603C104K5RACTU" capacitance="100nF" schX={-12} schY={6} connections={{pin1:net('VLOGIC_3V15'),pin2:net('GND')}}/>
  <capacitor name="C_LCD_VDD" capacitance="1uF" schX={-12} schY={2} connections={{pin1:net('VLOGIC_3V15'),pin2:net('GND')}}/>
  <resistor name="R_LCD_CS" resistance="100k" schX={12} schY={6} connections={{pin1:net('VLOGIC_3V15'),pin2:net('LCD_CS_N')}}/>
  <resistor name="R_LCD_RST" resistance="100k" schX={12} schY={2} connections={{pin1:net('GND'),pin2:net('LCD_RST_N')}}/>
 </board>
}
// BQ25616 (NOT J, NOT BQ25606): 10k VSET selects 4.1 V.
// Deliberately isolated SYS_CANDIDATE: modem connection needs transient evidence.
// CE is held disabled; enable controller and temperature qualification unresolved.
// V4 flat pack permits charging only 10..45 C. This nominal 0..45 C TS network
// is INCOMPATIBLE with that pack. Do not enable it; use a separately reviewed window.
export function ChargerCandidate({flatPack=false}:{flatPack?:boolean}={}){
 const pins=['VAC','ACDRV','DP','DM','STAT','OTG','PG','ILIM','CE_N','ICHG','TS','VSET','BAT1','BAT2','SYS1','SYS2','GND17','GND18','SW19','SW20','BTST','REGN','PMID','VBUS','EP_GND']
 const nets:Record<string,string>={VAC:'USB_5V_QUALIFIED',STAT:'CHARGE_STATUS_N',OTG:'GND',PG:'USB_GOOD_N',ILIM:'CHARGER_ILIM',CE_N:'CHARGE_DISABLE',ICHG:'CHARGER_ICHG',TS:'BAT_NTC',VSET:'CHARGER_VSET',BAT1:'PACK_POS',BAT2:'PACK_POS',SYS1:'SYS_CANDIDATE',SYS2:'SYS_CANDIDATE',GND17:'GND',GND18:'GND',SW19:'CHG_SW',SW20:'CHG_SW',BTST:'CHG_BOOT',REGN:'CHG_REGN',PMID:'CHG_PMID',VBUS:'USB_5V_QUALIFIED',EP_GND:'GND'}
 return <board name="CHARGER_CANDIDATE_NOT_RELEASED" width={56} height={144} routingDisabled>
  <chip name="U_CHG" manufacturerPartNumber="BQ25616RTWR" pinLabels={Object.fromEntries(pins.map((p,i)=>[`pin${i+1}`,p]))} connections={Object.fromEntries(Object.entries(nets).map(([p,n])=>[p,net(n)]))}/>
  <inductor name="L_CHG" inductance="1uH" manufacturerPartNumber="XGL4020-102MEC" schY={12} connections={{pin1:net('CHG_SW'),pin2:net('SYS_CANDIDATE')}}/>
  {[
   ['C_CHG_IN','1uF','USB_5V_QUALIFIED','GND'],['C_CHG_PMID','10uF','CHG_PMID','GND'],['C_CHG_REGN','4.7uF','CHG_REGN','GND'],['C_CHG_BOOT','47nF','CHG_BOOT','CHG_SW'],['C_CHG_BAT','10uF','PACK_POS','GND'],['C_CHG_SYS1','10uF','SYS_CANDIDATE','GND'],['C_CHG_SYS2','10uF','SYS_CANDIDATE','GND']
  ].map(([name,value,a,b],i)=><capacitor key={name} name={name} capacitance={value} schX={-20+(i%4)*7} schY={18+Math.floor(i/4)*5} connections={{pin1:net(a),pin2:net(b)}}/>)}
  {[
   ['R_CHG_VSET','10k','CHARGER_VSET','GND'],['R_CHG_ICHG',flatPack?'698':'2.21k','CHARGER_ICHG','GND'],['R_CHG_ILIM',flatPack?'383':'1k','CHARGER_ILIM','GND'],['R_CHG_DISABLE','100k','SYS_CANDIDATE','CHARGE_DISABLE'],['R_CHG_TS_TOP','5.3k','CHG_REGN','BAT_NTC'],['R_CHG_TS_BOTTOM','30.9k','BAT_NTC','TS_SERIES'],['R_CHG_TS_TRIM','240','TS_SERIES','GND'],['R_CHG_STAT','10k','VLOGIC_3V15','CHARGE_STATUS_N'],['R_CHG_PG','10k','VLOGIC_3V15','USB_GOOD_N']
  ].map(([name,value,a,b],i)=><resistor key={name} name={name} resistance={value} schX={-20+(i%4)*7} schY={-18-Math.floor(i/4)*5} connections={{pin1:net(a),pin2:net(b)}}/>)}
  <chip name="NTC_EXTERNAL" manufacturerPartNumber="103AT-2" schX={18} schY={0} pinLabels={{pin1:'NTC',pin2:'RETURN'}} connections={{NTC:net('BAT_NTC'),RETURN:net('GND')}}/>
 </board>
}
