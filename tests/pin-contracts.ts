import fs from 'node:fs'
import assert from 'node:assert/strict'
// Independent transcription of module pad->GPIO mapping from Espressif Table3-1.
const padGPIO:Record<number,number>={4:4,5:5,6:6,7:7,8:15,9:16,10:17,11:18,12:8,13:19,14:20,15:3,16:46,17:9,18:10,19:11,20:12,21:13,22:14,23:21,24:47,25:48,26:45,27:0,28:35,29:36,30:37,31:38,32:39,33:40,34:41,35:42,36:44,37:43,38:2,39:1}
const lines=fs.readFileSync('electronics/gpio-proposal.csv','utf8').trim().split('\n').slice(1).map(l=>l.split(','))
const reserved=new Set([0,3,45,46,19,20,43,44,40,41])
// GPIO35/36 are usable only for the exact N16 Quad-SPI/no-PSRAM variant.
// Espressif module datasheet Table 1-1 and pin-table note restrict them on Octal variants.
const moduleSource=fs.readFileSync('electronics/mcu.tsx','utf8')
const selected=moduleSource.match(/manufacturerPartNumber="([^"]+)"/)?.[1]
const qualifyVariant=(part:string|undefined)=>assert.equal(part,'ESP32-S3-WROOM-1-N16','Requalify GPIO35/36 for any MCU substitution')
qualifyVariant(selected)
assert.throws(()=>qualifyVariant('ESP32-S3-WROOM-1-N16R8'))
const seen=new Set<number>()
for(const [name,g,p] of lines){assert.equal(padGPIO[+p],+g,name);assert.ok(!reserved.has(+g),name);assert.ok(!seen.has(+g),name);seen.add(+g)}
assert.equal(lines.length,25)
console.log('PASS: 25 proposed GPIO assignments match module pads; no duplicates, straps, native USB, UART0 or reserved flash pins used; exact N16 variant enforced and Octal substitution rejected')
