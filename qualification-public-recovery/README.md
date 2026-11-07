# Host sequencing repair after public-source recovery

Date: 2026-11-07. This changes the host simulation contract only. It does not add physical protection, alter the V66 PCB or qualify any modem firmware, battery, power converter, enclosure or carrier.

## Reproduced faults and repairs

1. During `settle`, an unexpected STATUS-high indication was ignored. Cancelling startup immediately disabled supply without shutdown proof; keeping the request asserted eventually asserted PWRKEY on an apparently active modem. STATUS or AT-ready now causes a latched fault before cancellation or dwell logic. The previous supply request is retained and PWRKEY/reset are released. A stale AT-ready indication also inhibits a new cold startup from `off`.
2. The first sample could contain a negative timestamp and still enable modem supply or authorize system shutdown. Both contracts now reject negative timestamps using their existing latched fault behavior. A subsequent nonnegative timestamp does not clear the fault.
3. Boot readiness and shutdown confirmation arriving at 60,050 ms bypassed their existing 60,000 ms deadline because success was checked first. Expiry now takes precedence; success at exactly 60,000 ms remains allowed. Late shutdown proof does not silently clear a timed-out fault or cut supply.
4. When the 2,100 ms stable-rail dwell completed just after the 10,000 ms settle deadline, entering `key-on` reset the timer before the timeout comparison. The original deadline is now checked before any state transition. Dwell ending exactly at 10,000 ms remains allowed by the existing inclusive boundary; ending at 10,050 ms faults and preserves supply.

`tests/modem-startup-faults.ts` covers 19 cases: unexpected STATUS/AT-ready with startup retained or cancelled, fault latching, stale-ready startup inhibition, two negative initial clocks, the late/exact dwell and boot/shutdown deadline boundaries, activity exactly at dwell completion, negative time after supply enable, and clean cancellation. The first 12-case regression run failed 10 cases before the fix; the added boot/shutdown checks independently reproduced both late-success failures. The shutdown suite separately covers negative clocks and latched recovery. The existing eight-case shutdown brownout regression in `tests/modem-brownout-v44.ts` is now included in the standard control suite rather than left as a manual check.

The normal-cycle fixture now explicitly clears the old AT-ready and shutdown-confirmed indications before another startup. Drivers must provide trustworthy fresh observations. These checks still cannot react while the processor or scheduler is stopped and cannot protect a battery from a hardware fault. Fault preservation is a software sequencing policy, not a physical overvoltage/undervoltage/thermal protection design.

## Reproduce

Run `npm run test:control` and `npm run typecheck:host`. The public aggregate is `npm run check:public`; `npm test` also includes the control regressions. See `PUBLIC_CHECKS.md` for the deliberately incomplete board scope and omitted footprint inputs. No fabrication or purchase is authorized by a passing test.

## Validation result

On the final repaired source, `npm run check:public`, `npm test`, `npm run test:control`, `npm run typecheck:host`, and `npm run test:power` passed. An independent review reran the host typecheck and control suite, including all 19 new cases, with no remaining issue found in that scope. `git diff --check` passed. Full `npm run typecheck` remains failed with the same three omitted footprint inputs and cascading type errors; `npm run check:pcb-inputs` exits nonzero as intended. Complete board routing, footprint imports, physical mechanical assembly, battery pulse and hardware fault tests were not performed.
