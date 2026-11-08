# Physical-keypad phone study

A low-cost cellular-phone engineering study in tscircuit. **Incomplete and not fabrication-ready.** Preferred architecture: one custom four-layer rigid PCB, physical keypad, separate display ribbon, wired battery and audio. Exact modem/VoLTE compatibility, battery/protection pulses and physical assembly remain unqualified.

## Current reproducible checkpoint

Six exact JLCPCB parts have been imported through the normal tscircuit/EasyEDA workflow. Their source and downloaded models are hash-recorded. Core0.0.2302 includes the upstream multi-pad grounding fix. The MCU, modem and USB-protection footprints are migrated into the placement candidate while preserving component datums and logical nets.

Verified in the recovered checkout:

- Full TypeScript check and active footprint-input checks pass.
- 139 components render with510 mapped SMT pads, including all nine grounded MCU exposed-pad lands.
- Independent pad anchors, required ground/control/supply connections and deliberately open modem pins are tested.
- No different-net same-layer SMT-pad overlaps were found. All paste remains disabled pending manufacturing review.
- Host control, keypad, SMS, charging-policy and illustrative battery-power calculation tests pass.

Original V66 routing sources were recovered and revalidated against the migrated footprints after repairing17 clearance violations. All539 routes and249 vias remain;95 prior copper islands are preserved. Coverage is133/210 electronic components placed,336/522 minimum joins completed and186 open. This is a provisional geometry/connectivity screen, **not electrical simulation, factory acceptance or physical safety approval**.

## Reproduce

Use Node24, npm11 and Python3:

```
npm ci --ignore-scripts
npm run typecheck
npm run check:pcb-inputs
npm run test:jlc-imports
npm run test:board-imports
npm run check:public
npm test
npm run test:power
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-routing.txt
npm run check:current
# Optional full routing fault-injection suite:
.venv/bin/python scripts/check-current.py --negative
```

Generated circuit JSON/SVG and reports go under `output/`. See [PUBLIC_CHECKS.md](PUBLIC_CHECKS.md) for the exact scope and historical checks that still need recovered inputs.

The `.obj` and `.step` imports use ordinary bundler asset handling. Node-only geometry tests use the checked-in asset loader, which supplies actual local URLs but does not parse models or establish enclosure fit.

## Sources and qualification

- [JLC import checkpoint](qualification-jlc-imports/README.md): exact catalog IDs, source hashes, copper/symbol review and remaining mask/stencil concerns.
- [Datum-aware board migration](qualification-board-migration/README.md): preserved datums, net checks, pad-clearance evidence and remaining routing limitations.
- [Routing recovery](qualification-routing-recovery/README.md): recovered source lineage, clearance repairs, connectivity and negative-test scope.
- [Verified tscircuit issue list](qualification-jlc-imports/tscircuit-issues.md): old-core grounding problem already resolved upstream; current explicit paste-region omission recorded separately.
- [Preserved historical source/tests](historical-footprints/before-jlc-migration/): previous consumers are retained for comparison, not hidden by invented JSON.

Major release gates remain: country/carrier and exact modem firmware/VoLTE acceptance; real battery/connector/protection pulse impedance; independent charging interlocks under faults; capacitor bias/transient limits; mask/stencil and assembly review; display/SIM fit; RF/audio and antenna clearance; complete routing and physical enclosure testing. No fabrication, purchase or operational readiness is implied.

Earlier upstream resistor-converter work: [PR645](https://github.com/tscircuit/easyeda-converter/pull/645) and [PR646](https://github.com/tscircuit/easyeda-converter/pull/646). MCU ground-port repair: [core PR5177](https://github.com/tscircuit/core/pull/5177).
