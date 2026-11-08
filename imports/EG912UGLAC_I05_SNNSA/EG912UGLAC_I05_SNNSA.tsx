import type { ChipProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["PSM_IND"],
  pin2: ["ADC1"],
  pin3: ["GND1"],
  pin4: ["PCM_CLK"],
  pin5: ["PCM_SYNC"],
  pin6: ["PCM_DIN"],
  pin7: ["PCM_DOUT"],
  pin8: ["USB_VBUS"],
  pin9: ["USB_DP"],
  pin10: ["USB_DM"],
  pin11: ["RESERVED1"],
  pin12: ["RESERVED2"],
  pin13: ["RESERVED3"],
  pin14: ["RESERVED4"],
  pin15: ["PWRKEY"],
  pin16: ["RESERVED5"],
  pin17: ["RESET_N"],
  pin18: ["N_W_DISABLE"],
  pin19: ["AP_READY"],
  pin20: ["STATUS"],
  pin21: ["NET_STATUS"],
  pin22: ["DBG_RXD"],
  pin23: ["DBG_TXD"],
  pin24: ["ADC0"],
  pin25: ["SPI_CS"],
  pin26: ["SPI_CLK"],
  pin27: ["AUX_TXD"],
  pin28: ["AUX_RXD"],
  pin29: ["VDD_EXT"],
  pin30: ["MAIN_DTR"],
  pin31: ["GND2"],
  pin32: ["VBAT_BB1"],
  pin33: ["VBAT_BB2"],
  pin34: ["MAIN_RXD"],
  pin35: ["MAIN_TXD"],
  pin36: ["MAIN_CTS"],
  pin37: ["MAIN_RTS"],
  pin38: ["MAIN_DCD"],
  pin39: ["MAIN_RI"],
  pin40: ["I2C_SCL"],
  pin41: ["I2C_SDA"],
  pin42: ["USIM1_DET"],
  pin43: ["USIM1_VDD"],
  pin44: ["USIM1_RST"],
  pin45: ["USIM1_DATA"],
  pin46: ["USIM1_CLK"],
  pin47: ["USIM1_GND"],
  pin48: ["GND3"],
  pin49: ["ANT_GNSS"],
  pin50: ["GND4"],
  pin51: ["1PPS"],
  pin52: ["VBAT_RF1"],
  pin53: ["VBAT_RF2"],
  pin54: ["GND5"],
  pin55: ["GND6"],
  pin56: ["ANT_BT","WIFI_SCAN"],
  pin57: ["RESERVED6"],
  pin58: ["GND7"],
  pin59: ["GND8"],
  pin60: ["ANT_MAIN"],
  pin61: ["GND9"],
  pin62: ["GND10"],
  pin63: ["RESERVED12"],
  pin64: ["SPI_DOUT"],
  pin65: ["RESERVED13"],
  pin66: ["RESERVED14"],
  pin67: ["GND15"],
  pin68: ["GND16"],
  pin69: ["GND17"],
  pin70: ["GND18"],
  pin71: ["GND19"],
  pin72: ["GND20"],
  pin73: ["GND21"],
  pin74: ["GND22"],
  pin75: ["USB_BOOT"],
  pin76: ["GRFC1"],
  pin77: ["GRFC2"],
  pin78: ["RESERVED21"],
  pin79: ["GND11"],
  pin80: ["GND12"],
  pin81: ["GND13"],
  pin82: ["GND14"],
  pin83: ["USIM2_DET"],
  pin84: ["USIM2_CLK"],
  pin85: ["USIM2_RST"],
  pin86: ["USIM2_DATA"],
  pin87: ["USIM2_VDD"],
  pin88: ["SPI_DIN"],
  pin89: ["GND26"],
  pin90: ["GND27"],
  pin91: ["GND28"],
  pin92: ["RESERVED27"],
  pin93: ["RESERVED29"],
  pin94: ["RESERVED30"],
  pin95: ["RESERVED31"],
  pin96: ["PSM_EINT"],
  pin97: ["RESERVED32"],
  pin98: ["RESERVED33"],
  pin99: ["RESERVED24"],
  pin100: ["GND23"],
  pin101: ["GND24"],
  pin102: ["GND25"],
  pin103: ["RESERVED10"],
  pin104: ["RESERVED11"],
  pin105: ["RESERVED15"],
  pin106: ["RESERVED16"],
  pin107: ["RESERVED17"],
  pin108: ["RESERVED18"],
  pin109: ["RESERVED19"],
  pin110: ["RESERVED20"],
  pin111: ["RESERVED22"],
  pin112: ["RESERVED7"],
  pin113: ["RESERVED8"],
  pin114: ["RESERVED9"],
  pin115: ["RESERVED25"],
  pin116: ["RESERVED26"],
  pin117: ["RESERVED28"],
  pin118: ["RESERVED23"],
  pin119: ["MIC_N"],
  pin120: ["MICBIAS"],
  pin121: ["SPK_P"],
  pin122: ["SPK_N"],
  pin123: ["RESERVED36"],
  pin124: ["RESERVED35"],
  pin125: ["RESERVED34"],
  pin126: ["MIC_P"]
} as const

const pinAttributes = {
  pin3: {requiresGround: true},
  pin31: {requiresGround: true},
  pin48: {requiresGround: true},
  pin50: {requiresGround: true},
  pin54: {requiresGround: true},
  pin55: {requiresGround: true},
  pin58: {requiresGround: true},
  pin59: {requiresGround: true},
  pin61: {requiresGround: true},
  pin62: {requiresGround: true},
  pin67: {requiresGround: true},
  pin68: {requiresGround: true},
  pin69: {requiresGround: true},
  pin70: {requiresGround: true},
  pin71: {requiresGround: true},
  pin72: {requiresGround: true},
  pin73: {requiresGround: true},
  pin74: {requiresGround: true},
  pin79: {requiresGround: true},
  pin80: {requiresGround: true},
  pin81: {requiresGround: true},
  pin82: {requiresGround: true},
  pin89: {requiresGround: true},
  pin90: {requiresGround: true},
  pin91: {requiresGround: true},
  pin100: {requiresGround: true},
  pin101: {requiresGround: true},
  pin102: {requiresGround: true}
} as const

export const EG912UGLAC_I05_SNNSA = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      pinAttributes={pinAttributes}
      supplierPartNumbers={{
  "jlcpcb": [
    "C7472750"
  ]
}}
      manufacturerPartNumber="EG912UGLAC-I05-SNNSA"
      footprint={<footprint>
        <smtpad portHints={["pin1"]} pcbX="-9.174861mm" pcbY="9.6799146mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin2"]} pcbX="-9.174861mm" pcbY="8.5798406mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin3"]} pcbX="-9.174861mm" pcbY="7.4800206mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin4"]} pcbX="-9.174861mm" pcbY="6.3799466mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin5"]} pcbX="-9.174861mm" pcbY="5.2798726mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin6"]} pcbX="-9.174861mm" pcbY="4.1797986mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin7"]} pcbX="-9.174861mm" pcbY="3.0799786mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin8"]} pcbX="-9.174861mm" pcbY="1.9799046mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin9"]} pcbX="-9.174861mm" pcbY="0.8798306mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin10"]} pcbX="-9.174861mm" pcbY="-0.2199894mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin11"]} pcbX="-9.174861mm" pcbY="-1.9200114mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin12"]} pcbX="-9.174861mm" pcbY="-3.0200854mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin13"]} pcbX="-9.174861mm" pcbY="-4.1201594mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin14"]} pcbX="-9.174861mm" pcbY="-5.2199794mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin15"]} pcbX="-9.174861mm" pcbY="-6.3200534mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin16"]} pcbX="-9.174861mm" pcbY="-7.4201274mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin17"]} pcbX="-9.174861mm" pcbY="-8.5202014mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin18"]} pcbX="-9.174861mm" pcbY="-9.6200214mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin19"]} pcbX="-7.4499978mm" pcbY="-11.0450376mm" width="0.6999986mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin20"]} pcbX="-6.3499238mm" pcbY="-11.0450376mm" width="0.6999986mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin21"]} pcbX="-5.2501038mm" pcbY="-11.0450376mm" width="0.6999986mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin22"]} pcbX="-4.1500298mm" pcbY="-11.0450376mm" width="0.6999986mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin23"]} pcbX="-3.0499558mm" pcbY="-11.0450376mm" width="0.6999986mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin24"]} pcbX="-1.9501358mm" pcbY="-11.0450376mm" width="0.6999986mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin25"]} pcbX="0.5499862mm" pcbY="-11.0450376mm" width="0.6999986mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin26"]} pcbX="1.6500602mm" pcbY="-11.0450376mm" width="0.6999986mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin27"]} pcbX="2.7498802mm" pcbY="-11.0450376mm" width="0.6999986mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin28"]} pcbX="3.8499542mm" pcbY="-11.0450376mm" width="0.6999986mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin29"]} pcbX="4.9500282mm" pcbY="-11.0450376mm" width="0.6999986mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin30"]} pcbX="6.0501022mm" pcbY="-11.0450376mm" width="0.6999986mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin31"]} pcbX="7.1499222mm" pcbY="-11.0450376mm" width="0.6999986mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin32"]} pcbX="9.175115mm" pcbY="-9.6301814mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin33"]} pcbX="9.175115mm" pcbY="-8.5301074mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin34"]} pcbX="9.175115mm" pcbY="-7.4300334mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin35"]} pcbX="9.175115mm" pcbY="-6.3302134mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin36"]} pcbX="9.175115mm" pcbY="-5.2301394mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin37"]} pcbX="9.175115mm" pcbY="-4.1300654mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin38"]} pcbX="9.175115mm" pcbY="-3.0299914mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin39"]} pcbX="9.175115mm" pcbY="-1.9301714mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin40"]} pcbX="9.175115mm" pcbY="-0.2301494mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin41"]} pcbX="9.175115mm" pcbY="0.8699246mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin42"]} pcbX="9.175115mm" pcbY="1.9699986mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin43"]} pcbX="9.175115mm" pcbY="3.0698186mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin44"]} pcbX="9.175115mm" pcbY="4.1698926mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin45"]} pcbX="9.175115mm" pcbY="5.2699666mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin46"]} pcbX="9.175115mm" pcbY="6.3697866mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin47"]} pcbX="9.175115mm" pcbY="7.4698606mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin48"]} pcbX="9.175115mm" pcbY="8.5699346mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin49"]} pcbX="9.175115mm" pcbY="9.6700086mm" width="1.1500104mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin50"]} pcbX="7.1500238mm" pcbY="11.0049056mm" width="0.6999986mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin51"]} pcbX="6.0499498mm" pcbY="11.0049056mm" width="0.6999986mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin52"]} pcbX="4.9501298mm" pcbY="11.0049056mm" width="0.6999986mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin53"]} pcbX="3.8500558mm" pcbY="11.0049056mm" width="0.6999986mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin54"]} pcbX="2.7499818mm" pcbY="11.0049056mm" width="0.6999986mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin55"]} pcbX="1.6501618mm" pcbY="11.0049056mm" width="0.6999986mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin56"]} pcbX="0.5500878mm" pcbY="11.0049056mm" width="0.6999986mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin57"]} pcbX="-1.9500342mm" pcbY="11.0049056mm" width="0.6999986mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin58"]} pcbX="-3.0498542mm" pcbY="11.0049056mm" width="0.6999986mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin59"]} pcbX="-4.1499282mm" pcbY="11.0049056mm" width="0.6999986mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin60"]} pcbX="-5.2500022mm" pcbY="11.0049056mm" width="0.6999986mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin61"]} pcbX="-6.3500762mm" pcbY="11.0049056mm" width="0.6999986mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin62"]} pcbX="-7.4498962mm" pcbY="11.0049056mm" width="0.6999986mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin112"]} pcbX="5.94995mm" pcbY="7.629906mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin113"]} pcbX="4.249928mm" pcbY="7.629906mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin79"]} pcbX="2.549906mm" pcbY="7.629906mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin80"]} pcbX="0.850138mm" pcbY="7.629906mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin81"]} pcbX="-0.849884mm" pcbY="7.629906mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin82"]} pcbX="-2.549906mm" pcbY="7.629906mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin114"]} pcbX="-4.249928mm" pcbY="7.629906mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin103"]} pcbX="-5.94995mm" pcbY="7.629906mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin104"]} pcbX="-5.94995mm" pcbY="5.929884mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin63"]} pcbX="-5.94995mm" pcbY="4.229862mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin64"]} pcbX="-5.94995mm" pcbY="2.52984mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin65"]} pcbX="-5.94995mm" pcbY="0.830072mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin66"]} pcbX="-5.94995mm" pcbY="-0.86995mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin67"]} pcbX="-5.94995mm" pcbY="-2.569972mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin68"]} pcbX="-5.94995mm" pcbY="-4.269994mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin105"]} pcbX="-5.94995mm" pcbY="-5.970016mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin106"]} pcbX="-5.94995mm" pcbY="-7.670038mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin107"]} pcbX="-4.249928mm" pcbY="-7.670038mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin69"]} pcbX="-2.549906mm" pcbY="-7.670038mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin70"]} pcbX="-0.849884mm" pcbY="-7.670038mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin71"]} pcbX="0.849884mm" pcbY="-7.670038mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin72"]} pcbX="2.549906mm" pcbY="-7.670038mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin108"]} pcbX="4.249928mm" pcbY="-7.670038mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin109"]} pcbX="5.94995mm" pcbY="-7.670038mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin110"]} pcbX="5.94995mm" pcbY="-5.970016mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin73"]} pcbX="5.94995mm" pcbY="-4.269994mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin74"]} pcbX="5.94995mm" pcbY="-2.569972mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin75"]} pcbX="5.94995mm" pcbY="-0.86995mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin76"]} pcbX="5.94995mm" pcbY="0.830072mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin77"]} pcbX="5.94995mm" pcbY="2.52984mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin78"]} pcbX="5.94995mm" pcbY="4.229862mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin111"]} pcbX="5.94995mm" pcbY="5.929884mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin118"]} pcbX="4.249928mm" pcbY="5.929884mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin99"]} pcbX="2.549906mm" pcbY="5.929884mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin100"]} pcbX="0.849884mm" pcbY="5.929884mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin101"]} pcbX="-0.849884mm" pcbY="5.929884mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin102"]} pcbX="-2.549906mm" pcbY="5.929884mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin115"]} pcbX="-4.249928mm" pcbY="5.929884mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin83"]} pcbX="-4.249928mm" pcbY="4.229862mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin84"]} pcbX="-4.249928mm" pcbY="2.52984mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin85"]} pcbX="-4.249928mm" pcbY="0.830072mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin86"]} pcbX="-4.249928mm" pcbY="-0.86995mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin87"]} pcbX="-4.249928mm" pcbY="-2.569972mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin88"]} pcbX="-4.249928mm" pcbY="-4.269994mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin116"]} pcbX="-4.249928mm" pcbY="-5.970016mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin89"]} pcbX="-2.549906mm" pcbY="-5.970016mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin90"]} pcbX="-0.849884mm" pcbY="-5.970016mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin91"]} pcbX="0.849884mm" pcbY="-5.970016mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin92"]} pcbX="2.549906mm" pcbY="-5.970016mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin117"]} pcbX="4.249928mm" pcbY="-5.970016mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin93"]} pcbX="4.249928mm" pcbY="-4.269994mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin94"]} pcbX="4.249928mm" pcbY="-2.569972mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin95"]} pcbX="4.249928mm" pcbY="-0.86995mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin96"]} pcbX="4.249928mm" pcbY="0.830072mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin97"]} pcbX="4.249928mm" pcbY="2.52984mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin98"]} pcbX="4.249928mm" pcbY="4.229862mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin126"]} pcbX="0.849884mm" pcbY="2.52984mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin119"]} pcbX="-0.849884mm" pcbY="2.52984mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin125"]} pcbX="0.849884mm" pcbY="0.830072mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin120"]} pcbX="-0.849884mm" pcbY="0.830072mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin124"]} pcbX="0.849884mm" pcbY="-0.86995mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin121"]} pcbX="-0.849884mm" pcbY="-0.86995mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin123"]} pcbX="0.849884mm" pcbY="-2.569972mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin122"]} pcbX="-0.849884mm" pcbY="-2.569972mm" width="0.999998mm" height="0.999998mm" shape="rect" />
<silkscreencircle pcbX="-11.175746mm" pcbY="9.504934mm" radius="0.199898mm" />
<silkscreenrect pcbX="0mm" pcbY="0mm" width="24.960072mm" height="29.020008mm" strokeWidth="0.254mm" />
<silkscreentext text="{NAME}" pcbX="-0.0124968mm" pcbY="15.5087594mm" anchorAlignment="center" fontSize="1mm" />
<fabricationnotepath route={[{"x":-12.12837300000001,"y":12.489433999999846},{"x":-10.47737300000017,"y":14.1404339999998},{"x":-12.12837300000001,"y":14.1404339999998},{"x":-12.12837300000001,"y":12.489433999999846}]} strokeWidth="0mm" isFilled hasStroke={false} />
<courtyardoutline outline={[{"x":-12.771996800000124,"y":14.758759399999917},{"x":12.747003199999881,"y":14.758759399999917},{"x":12.747003199999881,"y":-14.773440600000185},{"x":-12.771996800000124,"y":-14.773440600000185},{"x":-12.771996800000124,"y":14.758759399999917}]} />
      </footprint>}
      
      {...props}
    />
  )
}