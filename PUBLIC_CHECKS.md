# Reproducing the public-safe source

This checkout is a deliberately incomplete phone study, not a full hardware release. No footprint, board, battery or protection system is approved by these software checks.

Use Node.js 24, npm 11 and Python 3. Install the locked dependencies with `npm ci --ignore-scripts`. The November7 recovery did not change dependencies. The November8 JLCPCB checkpoint updates core to0.0.2302 to include the already-merged multi-pad connection fix. The install currently reports pre-existing peer-version warnings from `jscad-electronics`; they remain unresolved. If npm's normal cache is not writable, select a writable directory with `--cache /absolute/path/to/cache`.

## Checks supported by the included sources

Run `npm run check:public` from the repository root. It runs:

- `npm run typecheck:host`: strict TypeScript checks of all host firmware plus the ten included host/contract test files. This separate configuration does not modify or weaken the full-project TypeScript check.
- `npm run test:host`: dialing/keypad, invalid-clock recovery, SMS, GPIO contracts, power policy, charge freshness, modem sequencing, startup fault, shutdown brownout and system-shutdown host tests. These are executable contracts, not MCU firmware or hardware safety validation. The shutdown suite is now part of `test:control` and therefore the existing `npm test` command too.
- `npm run test:battery`: eight tests of the V113 necessary-power calculation. The 50 cases are illustrative sustained simultaneous allocations, not measured modem waveforms, pack qualification or transient validation.
- `npm run build:keypad`: emitted keypad geometry and net assertions plus an assembly API smoke test. It creates its output directory on a clean checkout. Copper routing is disabled. The referenced assembly mesh is intentionally absent; this command does not load it or validate physical fit. `npm run build` remains the same keypad-only study for compatibility.

The commands load TypeScript using the supported `node --import tsx` hook. They do not require the `tsx` CLI's optional local IPC server. No simulation assertion has been removed.

## JLC imports and migrated placement (2026-11-08)

The six exact JLCPCB imports are verified with `npm run typecheck:jlc-imports` and `npm run test:jlc-imports`. Their raw source/model files remain hash-checked and untouched. See [the import checkpoint](qualification-jlc-imports/README.md).

The three active footprint consumers now use these imports. `npm run typecheck` and `npm run check:pcb-inputs` both pass. No placeholder JSON or fabricated source data was added. Historical code and tests are retained under `historical-footprints/before-jlc-migration/`.

Run `npm run test:board-imports` for the migrated modem/TI footprints, preserved modem courtyard, 139-component placement, mapped MCU ground lands, numbered-pin net contracts, and SMT-pad copper overlap/bounds checks. These checks produce circuit JSON/SVG and reports under `output/`. They do not run copper routing or inspect models. See [migration scope](qualification-board-migration/README.md).

## Checks that remain unavailable

The complete routed-board and mechanical release are not recovered. The existing `check:board`, `check:current` and `check:placement` commands reference absent `engineering/` or historical scripts and are not a passing validation path. Historical Python integration tests also require absent manufacturer snapshots or routed outputs. Their assertions were not weakened or supplied fake inputs.

The last routed acceptance figures were V66: 133/210 components placed and186 open minimum joins. Those are historical results, not revalidated results of the new footprints. Component placement maps and logical nets are preserved, but catalog copper differs from the former manufacturer-derived lands, so any old route endpoints and clearance assumptions must be rechecked before reuse. Mask/stencil, exact modem/carrier compatibility, battery/protection pulses, charging interlocks, RF/audio and physical assembly remain open.

## Recovery validation (2026-11-07)

The saved public-safe history was restored at `1baed9a26356d5fa335dd4993838d121b3ad1fe0` into a separate checkout, preserving the unavailable original engineering checkout. Locked installation, `check:public` and `npm test` passed here. `check:pcb-inputs` exited 1 and full `typecheck` exited 2 with the missing-input errors above. No verified GitHub remote was available and no push occurred. The local bundle remote is only a recovery source, not GitHub.
