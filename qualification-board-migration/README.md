# Datum-aware JLC footprint migration, 2026-11-08

The three active missing-JSON consumers now use exact JLCPCB copper through `electronics/jlc-board-lands.tsx`. Full-project TypeScript and active PCB-input checks pass. Original providers and TypeScript tests are preserved under `historical-footprints/before-jlc-migration/` and in prior Git history.

## What is preserved

- Existing placement maps, component sides/rotations, board outline, logical chips and their pin labels/net connections remain in place.
- The imported MCU local datum is corrected by **−3.7849527 mm Y before bottom reflection/rotation**. Physical manufacturer pad anchors, not the generated component bounding-box center, establish placement.
- The old explicit `pin41_internal_1`…`_8` workaround is removed. Core0.0.2302 creates nine distinct EP physical ports internally linked to the primary ground terminal. All nine resolve to GND in the full board render.
- Modem body-center coordinates and the explicit31×35 mm clearance courtyard are retained. Unverified headphone pins123–125 remain open. Unqualified modem supply net names remain separate from a power-source approval.
- Raw imports and their hashes are unchanged. No catalog model or courtyard geometry is allowed to silently shift placed copper. The adapter selects copper only and suppresses paste.

## What changes

MCU, modem, USB protector and USB eFuse footprints now come from catalog geometry. The copper is not claimed identical to historical manufacturer-derived lands. Small catalog offsets, USB-protector longer toes, sharp corners and the eFuse polygon differences are documented in the import checkpoint. Two additional TI land providers are also migrated and tested in isolation, without inventing placements for them.

Generated PCB bounding-box centers can change while physical datums stay fixed. For example, MCU bbox center is now(-13,28.2150473) and modem bbox center(11.999873,5.979934), even though their placement datums remain(-13,32) and(12,6). Moving components to force the former bbox centers would be incorrect.

## Validation

- `npm run typecheck`: entire active source tree passes.
- `npm run check:pcb-inputs`: active providers and all16 imported files readable/hash-verified.
- `npm run test:board-imports`: isolated copper/port checks, independent modem anchors and no pad overlap, four preserved eFuse L-polygons, modem courtyard, then full placement checks.
- Full placement:139 emitted components; unchanged non-migrated component centers; independent asymmetric MCU/modem pad anchors; nine distinct grounded MCU EP pads; numbered-pin control, supply, keypad, full eFuse and USB ground contracts; unverified modem headphone pins stay open; zero paste; no emitted error records.
- SMT-pad-only copper check:510 pads, including four exact orthogonal polygons and conservative rectangular pad envelopes, inside the rectangular board. No different-net same-layer overlaps. Minimum observed different-net pad spacing is **0.1900809 mm**. This is an observation, not a chosen fabrication rule.
- The polygon checker includes a negative notch test so an L-pad is not replaced by its filled bounding box.

`output/usb-placement-v66.circuit.json`, its SVG, `board-migration-report.json` and `board-migration-clearance.json` contain generated evidence. The compatibility V66 export name remains; this output is the migrated candidate, not a reproduction of historical routedV66.

## Original routing blocker, subsequently resolved

At this migration checkpoint, original routing scripts/artifacts were absent. They were subsequently recovered and revalidated, with17 clearance repairs and explicit internal-terminal resolution. See [the routing recovery checkpoint](../qualification-routing-recovery/README.md). The original limitation is preserved in this checkpoint's validation record; it is no longer the current routing blocker.

The new copper checks exclude traces, vias, drilled holes, solder mask, component bodies and mechanical fit. Model orientation, mask/stencil, RF/antenna keepouts, battery/protection pulse capability, exact modem firmware/carrier and fabrication approval remain separate. A pre-existing React missing-key warning in the inherited placement tree is informational and is not hidden as an electrical result.
