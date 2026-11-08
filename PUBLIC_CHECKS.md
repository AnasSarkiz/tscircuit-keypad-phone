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

## Recovered routing checks

The separate C93151 keypad-switch review runs with `npm run test:keypad-import` and is included in `check:current`. It checks the unmodified import hashes, eight isolated placements, explicit common contacts, absence of unqualified model/paste, 48 deliberate geometry/contact/model mutations, and the factory-versus-manufacturer hole tolerance interval. The candidate remains quarantined and is not substituted into the live board. See [the keypad import review](qualification-keypad-import/README.md).

Original V66 routing and modem-clearance sources have now been recovered and verified against the saved complete-history bundle. The unmodified routing checker reproduced its original results exactly in isolation. The current checker handles explicit internal terminal groups, and17 migration-related clearance violations were repaired without moving components or deleting routes.

Install the isolated geometry dependencies with `python3 -m venv .venv` and `.venv/bin/python -m pip install -r requirements-routing.txt`. Run `npm run check:current` for the recovered aggregate, or `.venv/bin/python scripts/check-current.py --negative` to include the full routing-mutation suite. `check:board` now runs the recovered layered-copper checker. `test:modem-safety` now passes its historical boundary checks using the hardened recovered module; it still does not validate every physical body in the complete board.

The routed candidate retains539 routes,249 vias and95 historical copper islands. Coverage is freshly reproduced at133/210 electronic components placed,336/522 minimum joins completed and186 open. See [routing recovery](qualification-routing-recovery/README.md).

## Checks that remain unavailable or unqualified

Mechanical/model-fit and manufacturing acceptance are separate from recovered copper checks. `check:placement` intentionally requires an explicit verified-body placement file; no missing/unverified envelope is silently accepted. Historical Python integration tests may still require manufacturer snapshots or mechanical fixtures not restored into the public repository. `check:current` clearly defines its present scope and does not silently claim those historical mechanical/process stages passed.

Mask/stencil approval, physical body clearances, stackup/impedance/thermal validation, exact modem/carrier compatibility, battery/protection pulses, charging interlocks, RF/audio and physical assembly remain open. The remaining186 minimum joins must still be completed and reviewed. No fabrication release is implied.

## Recovery validation (2026-11-07)

The saved public-safe history was restored at `1baed9a26356d5fa335dd4993838d121b3ad1fe0` into a separate checkout, preserving the unavailable original engineering checkout. Locked installation, `check:public` and `npm test` passed here. `check:pcb-inputs` exited 1 and full `typecheck` exited 2 with the missing-input errors above. No verified GitHub remote was available and no push occurred. The local bundle remote is only a recovery source, not GitHub.
