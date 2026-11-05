import assert from 'node:assert/strict'
import {mcuNets,mcuPins,McuCandidate} from '../electronics/mcu'
assert.equal(mcuNets.IO35,'ON_OFF_MCU');assert.equal(mcuNets.IO36,'RESET_MCU')
assert.equal(mcuPins[28],'IO35');assert.equal(mcuPins[29],'IO36')
assert(!mcuNets.IO40&&!mcuNets.IO41)
const tree:any=McuCandidate();const chips=tree.props.children.flat().filter((x:any)=>x?.type==='chip')
assert(chips.some((c:any)=>c.props.manufacturerPartNumber==='ESP32-S3-WROOM-1-N16'))
assert.equal(Object.values(mcuNets).filter(v=>v==='ON_OFF_MCU').length,1)
assert.equal(Object.values(mcuNets).filter(v=>v==='RESET_MCU').length,1)
console.log('PASS exact N16 SKU and GPIO35/36 mapping; JTAG40/41 no longer drive modem; boot/loaded-drive tests still required')
const fs=await import('node:fs');const csv=fs.readFileSync('electronics/gpio-proposal.csv','utf8')
assert(csv.includes('MODEM_PWRKEY,35,28,ON_OFF_MCU'))
assert(csv.includes('MODEM_RESET,36,29,RESET_MCU'))
assert(!csv.includes('MODEM_PWRKEY,40,33'))
