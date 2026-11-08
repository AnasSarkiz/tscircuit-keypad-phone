import fs from 'node:fs'
import assert from 'node:assert/strict'
import { createHash } from 'node:crypto'

const manifest = JSON.parse(fs.readFileSync('qualification-jlc-imports/import-manifest.json', 'utf8'))
let count = 0
for (const part of manifest.parts) for (const item of part.files) {
  const bytes = fs.readFileSync(item.path)
  assert.equal(bytes.length, item.bytes, `${item.path}: size changed`)
  assert.equal(createHash('sha256').update(bytes).digest('hex'), item.sha256, `${item.path}: imported source changed`)
  count++
}
console.log(`PASS ${manifest.parts.length} exact catalog parts, ${count} unchanged imported source/model files`)
