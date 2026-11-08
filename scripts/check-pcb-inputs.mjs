import { access, constants, readFile } from 'node:fs/promises'
import './check-jlc-imports.mjs'
// Active placement dependencies, not historical missing JSON snapshots.
for (const input of ['electronics/jlc-board-lands.tsx','electronics/mcu-lands-v44.tsx','electronics/modem-footprint.tsx','electronics/reviewed-lands-v24.tsx']) {
  const url=new URL(`../${input}`,import.meta.url)
  await access(url,constants.R_OK)
  if (/sourcing\/(mcu-lands-v44|modem-pad-transcription-v19|reviewed-lands-v24)\.json/.test(await readFile(url,'utf8'))) throw new Error(`${input}: legacy missing-data dependency remains`)
}
console.log('PASS active placement sources and imported assets are readable and hash-verified. Historical routed-board/CAD assets remain separate; this is not fabrication approval.')
