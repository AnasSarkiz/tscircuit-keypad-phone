import assert from 'node:assert/strict'
import test from 'node:test'
import { ModemSequencer, type Sample } from '../firmware/modem-sequencer'

const base: Sample = {
  now: 0, requestOn: true, releaseApproved: true, vbatt: 0,
  status: false, atReady: false, shutdownConfirmed: false, railsValid: false,
}

for (const activity of [{ status: true }, { atReady: true }, { status: true, atReady: true }]) {
  for (const requestOn of [false, true]) {
    test(`unexpected settle activity ${JSON.stringify(activity)}, requestOn=${requestOn}`, () => {
      const q = new ModemSequencer()
      assert.equal(q.step(base).stage, 'settle')
      const active = { ...base, now: 50, vbatt: 3.8, railsValid: true, requestOn, ...activity }
      assert.deepEqual(q.step(active), {
        stage: 'fault', supplyEnable: true, pwrkeyLow: false, resetLow: false,
      }, 'unexpected activity must neither cut an operating supply nor assert PWRKEY')
      for (let now = 100; now <= 2500; now += 50) {
        assert.deepEqual(q.step({ ...base, now, vbatt: 3.8, railsValid: true }), {
          stage: 'fault', supplyEnable: true, pwrkeyLow: false, resetLow: false,
        }, 'fault must remain latched after activity disappears')
      }
    })
  }
}

test('an already asserted AT-ready indication inhibits cold startup', () => {
  const out = new ModemSequencer().step({ ...base, atReady: true })
  assert.equal(out.stage, 'off')
  assert.equal(out.supplyEnable, false)
  assert.equal(out.pwrkeyLow, false)
})

for (const now of [-1, -1000]) {
  test(`negative initial clock ${now} cannot enable supply`, () => {
    const q = new ModemSequencer()
    assert.deepEqual(q.step({ ...base, now }), {
      stage: 'fault', supplyEnable: false, pwrkeyLow: false, resetLow: false,
    })
    assert.equal(q.step(base).stage, 'fault')
    assert.equal(q.step({ ...base, now: 50 }).supplyEnable, false)
  })
}

function atSettleBoundary(railsValidAt: number, until: number) {
  const q = new ModemSequencer()
  let out = q.step(base)
  for (let now = 50; now <= until; now += 50) {
    out = q.step({ ...base, now, vbatt: 3.8, railsValid: now >= railsValidAt })
  }
  return { q, out }
}

test('dwell finishing after the settle deadline cannot reset the timeout', () => {
  const { q, out } = atSettleBoundary(7950, 10050)
  assert.deepEqual(out, { stage: 'fault', supplyEnable: true, pwrkeyLow: false, resetLow: false })
  assert.equal(q.step({ ...base, now: 10100, vbatt: 3.8, railsValid: true }).stage, 'fault')
})

test('dwell completed exactly at the inclusive settle deadline remains allowed', () => {
  const { out } = atSettleBoundary(7900, 10000)
  assert.equal(out.stage, 'key-on')
  assert.equal(out.pwrkeyLow, true)
})

test('settle cancellation without modem activity retains the safe pre-start path', () => {
  const q = new ModemSequencer()
  q.step(base)
  const out = q.step({ ...base, now: 50, requestOn: false, vbatt: 3.8, railsValid: true })
  assert.deepEqual(out, { stage: 'discharge', supplyEnable: false, pwrkeyLow: false, resetLow: false })
})

for (const activity of [{ status: true }, { atReady: true }]) {
  test(`unexpected activity on the final dwell sample ${JSON.stringify(activity)}`, () => {
    const q = new ModemSequencer()
    q.step(base)
    for (let now = 50; now < 2150; now += 50) {
      assert.equal(q.step({ ...base, now, vbatt: 3.8, railsValid: true }).stage, 'settle')
    }
    assert.deepEqual(q.step({ ...base, now: 2150, vbatt: 3.8, railsValid: true, ...activity }), {
      stage: 'fault', supplyEnable: true, pwrkeyLow: false, resetLow: false,
    })
  })
}

test('a negative clock after supply enable preserves supply and releases key', () => {
  const q = new ModemSequencer()
  assert.equal(q.step(base).supplyEnable, true)
  assert.deepEqual(q.step({ ...base, now: -1 }), {
    stage: 'fault', supplyEnable: true, pwrkeyLow: false, resetLow: false,
  })
})

function reachTimedStage(target: 'boot' | 'shutdown') {
  const q = new ModemSequencer()
  let now = 0
  let sample = { ...base }
  let out = q.step(sample)
  const tick = (patch: Partial<Sample> = {}) => {
    sample = { ...sample, ...patch, now: now += 50 }
    out = q.step(sample)
    return out
  }
  tick({ vbatt: 3.8, railsValid: true })
  for (let i = 0; i < 100 && out.stage !== 'boot'; i++) tick()
  assert.equal(out.stage, 'boot')
  if (target === 'shutdown') {
    assert.equal(tick({ status: true, atReady: true }).stage, 'on')
    assert.equal(tick({ requestOn: false }).stage, 'key-off')
    for (let i = 0; i < 100; i++) {
      const next = tick()
      if (next.stage === 'shutdown') return { tick }
      assert.equal(next.stage, 'key-off')
    }
    assert.fail('normal shutdown key dwell did not reach shutdown')
  }
  return { tick }
}

for (const phase of ['boot', 'shutdown'] as const) {
  for (const late of [false, true]) {
    test(`${phase} success ${late ? 'after' : 'at'} its inclusive 60 second deadline`, () => {
      const { tick } = reachTimedStage(phase)
      // Every sample is fresh; only the stage's total deadline is in question.
      for (let elapsed = 50; elapsed <= (late ? 60000 : 59950); elapsed += 50) {
        assert.equal(tick().stage, phase)
      }
      const success = phase === 'boot'
        ? { status: true, atReady: true }
        : { status: false, atReady: false, shutdownConfirmed: true }
      const out = tick(success)
      if (late) {
        assert.deepEqual(out, { stage: 'fault', supplyEnable: true, pwrkeyLow: false, resetLow: false })
        assert.equal(tick(success).stage, 'fault')
      } else {
        assert.equal(out.stage, phase === 'boot' ? 'on' : 'discharge')
        assert.equal(out.supplyEnable, phase === 'boot')
      }
    })
  }
}
