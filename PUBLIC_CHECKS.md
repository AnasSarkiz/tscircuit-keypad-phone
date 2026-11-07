# Reproducing the public-safe source

This checkout is a deliberately incomplete phone study, not a full hardware release. No footprint, board, battery or protection system is approved by these software checks.

Use Node.js 24, npm 11 and Python 3. Install the locked dependencies with `npm ci --ignore-scripts`. No dependency versions were changed for this recovery. The install currently reports pre-existing peer-version warnings from `jscad-electronics`; they remain unresolved. If npm's normal cache is not writable, select a writable directory with `--cache /absolute/path/to/cache`.

## Checks supported by the included sources

Run `npm run check:public` from the repository root. It runs:

- `npm run typecheck:host`: strict TypeScript checks of all host firmware plus the ten included host/contract test files. This separate configuration does not modify or weaken the full-project TypeScript check.
- `npm run test:host`: dialing/keypad, invalid-clock recovery, SMS, GPIO contracts, power policy, charge freshness, modem sequencing, startup fault, shutdown brownout and system-shutdown host tests. These are executable contracts, not MCU firmware or hardware safety validation. The shutdown suite is now part of `test:control` and therefore the existing `npm test` command too.
- `npm run test:battery`: eight tests of the V113 necessary-power calculation. The 50 cases are illustrative sustained simultaneous allocations, not measured modem waveforms, pack qualification or transient validation.
- `npm run build:keypad`: emitted keypad geometry and net assertions plus an assembly API smoke test. It creates its output directory on a clean checkout. Copper routing is disabled. The referenced assembly mesh is intentionally absent; this command does not load it or validate physical fit. `npm run build` remains the same keypad-only study for compatibility.

The commands load TypeScript using the supported `node --import tsx` hook. They do not require the `tsx` CLI's optional local IPC server. No simulation assertion has been removed.

## Checks that remain blocked

`npm run check:pcb-inputs` exits nonzero while three omitted footprint-data files are unavailable, naming each path and the required action. File existence, if restored, is not proof of geometry, provenance or import rights. Do not add fake JSON, guessed pads, empty geometry or ambient module declarations to hide the missing sources.

`npm run typecheck` still checks the entire original source tree and fails on these missing JSON imports and consequent type errors. `npm test` was also run independently and passed: it covers keypad generation, schematic interface contracts, GPIO and host behavior, not the complete PCB. The wider board, footprint, placement and mechanical checks were not run in this recovery; their missing assets and wider requirements remain. Never infer their success from either passing command.

To close the PCB gap, obtain appropriately licensed parts using the project's standard `tsci import <LCSC-ID> --jlcpcb --download` workflow; check the exact part and package, pad numbering, dimensions, model orientation and stock/assembly constraints. Update the consuming components and independent tests together. Preserve the previous studies for comparison. An imported part or successful build alone is not fabrication approval.

The last accepted engineering candidate remains V66: 133/210 components placed and 186 open minimum joins. This recovery does not modify that layout or the enclosure. Exact modem/carrier compatibility, battery/protection pulse behavior, independent charging interlocks, RF/audio and physical assembly remain open.

## Recovery validation (2026-11-07)

The saved public-safe history was restored at `1baed9a26356d5fa335dd4993838d121b3ad1fe0` into a separate checkout, preserving the unavailable original engineering checkout. Locked installation, `check:public` and `npm test` passed here. `check:pcb-inputs` exited 1 and full `typecheck` exited 2 with the missing-input errors above. No verified GitHub remote was available and no push occurred. The local bundle remote is only a recovery source, not GitHub.
