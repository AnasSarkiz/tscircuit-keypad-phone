import { access, constants } from 'node:fs/promises'

// Availability check only. No substitute geometry or qualification is inferred.
const requiredInputs = [
  'sourcing/mcu-lands-v44.json',
  'sourcing/modem-pad-transcription-v19.json',
  'sourcing/reviewed-lands-v24.json',
]
const missing = []
for (const input of requiredInputs) {
  try {
    await access(new URL(`../${input}`, import.meta.url), constants.R_OK)
  } catch {
    missing.push(input)
  }
}
if (missing.length) {
  console.error('BLOCKED: full PCB source inputs are missing or unreadable:')
  for (const input of missing) console.error(`  ${input}`)
  console.error('Do not create placeholder footprints. Obtain rights-cleared imports, review pad mapping and geometry, and update their consuming sources and tests.')
  console.error('Host/keypad checks do not establish full-board or fabrication readiness. See PUBLIC_CHECKS.md.')
  process.exitCode = 1
} else {
  console.log('Inputs exist and are readable only; provenance, dimensions, mappings, import rights and hardware qualification remain separate checks.')
}
