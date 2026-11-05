import React from 'react'
import '@tscircuit/core'
const n=(s:string)=>`net.${s}`
// ESP32-S3-WROOM-1-N16 only; Table 3-1 v1.8. No land pattern inferred.
export const mcuPins:Record<number,string>={1:'GND1',2:'VDD',3:'EN',4:'IO4',5:'IO5',6:'IO6',7:'IO7',8:'IO15',9:'IO16',10:'IO17',11:'IO18',12:'IO8',13:'IO19',14:'IO20',15:'IO3',16:'IO46',17:'IO9',18:'IO10',19:'IO11',20:'IO12',21:'IO13',22:'IO14',23:'IO21',24:'IO47',25:'IO48',26:'IO45',27:'IO0',28:'IO35',29:'IO36',30:'IO37',31:'IO38',32:'IO39',33:'IO40',34:'IO41',35:'IO42',36:'RXD0',37:'TXD0',38:'IO2',39:'IO1',40:'GND40',41:'EP_GND'}
export const mcuNets:Record<string,string>={GND1:'GND',GND40:'GND',EP_GND:'GND',VDD:'VLOGIC_3V15',EN:'MCU_EN',IO0:'MCU_BOOT_N',RXD0:'DEBUG_RX_3V15',TXD0:'DEBUG_TX_3V15',IO5:'ROW0',IO6:'ROW1',IO7:'ROW2',IO8:'ROW3',IO9:'ROW4',IO10:'COL0',IO13:'COL1',IO14:'COL2',IO21:'LCD_CS_N',IO38:'LCD_RST_N',IO11:'LCD_SDIO',IO39:'LCD_DC',IO12:'LCD_SCL',IO17:'HOST_TX',IO18:'HOST_RX',IO15:'HOST_RTS',IO16:'HOST_CTS',IO1:'BUTTON_INT_N',IO48:'SYSTEM_OFF_REQUEST',IO2:'MODEM_STATUS_HOST_PENDING',IO35:'ON_OFF_MCU',IO36:'RESET_MCU',IO42:'BACKLIGHT_PWM',IO47:'CHARGE_REQUEST_MCU'}
// LCD_RST_N uses the display interface pulldown; no opposing MCU pull-up.
// V40: modem controls use GPIO35/36 only for exact N16 quad-flash/no-PSRAM SKU; avoid JTAG GPIO40/41.
// IO4 intentionally open until an isolated battery measurement front end exists.
// IO47 requests charging; IO48 requests final system shutdown through an isolated NMOS.
export function McuCandidate(){return <board name="MCU_CANDIDATE" width={56} height={144} routingDisabled>
 <chip name="U_MCU" manufacturerPartNumber="ESP32-S3-WROOM-1-N16" pinLabels={Object.fromEntries(Object.entries(mcuPins).map(([p,l])=>['pin'+p,l]))} connections={Object.fromEntries(Object.entries(mcuNets).map(([p,v])=>[p,n(v)]))}/>
 {['MCU_EN','MCU_BOOT_N','LCD_CS_N',...['COL0','COL1','COL2']].map((rail,i)=><resistor key={rail} name={`R_MCU_${rail}`} resistance="10k" schX={-24+i*8} schY={16} connections={{pin1:n('VLOGIC_3V15'),pin2:n(rail)}}/>)}
 <capacitor name="C_MCU_EN" capacitance="1uF" schX={-16} schY={-16} connections={{pin1:n('MCU_EN'),pin2:n('GND')}}/>
 <capacitor name="C_MCU_BULK" capacitance="10uF" schX={0} schY={-16} connections={{pin1:n('VLOGIC_3V15'),pin2:n('GND')}}/>
 <capacitor name="C_MCU_HF" manufacturerPartNumber="C0603C104K5RACTU" capacitance="100nF" schX={16} schY={-16} connections={{pin1:n('VLOGIC_3V15'),pin2:n('GND')}}/>
 {/* Bring EN/BOOT/UART to test points at layout stage; no external 5V logic. */}
</board>}
