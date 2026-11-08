import { registerHooks } from 'node:module'

// Match the bundler's static-asset imports during Node-only geometry tests.
// This supplies the real local asset URL; it does not parse or approve the model.
registerHooks({
  load(url, context, nextLoad) {
    if (/\.(obj|step)$/.test(new URL(url).pathname)) {
      return { format: 'module', shortCircuit: true,
        source: `export default ${JSON.stringify(url)}` }
    }
    return nextLoad(url, context)
  },
})
