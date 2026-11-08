# C93151 import review checkpoint, 2026-11-08

**Quarantined review only. No live board, routing, enclosure or fabrication release change.**

The normal exact JLCPCB import succeeds using tscircuit 0.0.3120 / CLI 0.1.2446:

```
tsci import C93151 --jlcpcb --download --use-exact-footprint
```

`imports/B3F_1050/` contains the unmodified TSX, OBJ and STEP outputs. `source-evidence.json` records hashes, minimal extracted source dimensions, source identities and the hash of the locally retained full response. The full supplier response and manufacturer PDFs are intentionally not redistributed. Import success is not component, model or manufacturing qualification.

## Confirmed source issues and conservative correction

- The EasyEDA package itself uses 1.1999976 mm holes and 1.7999964 mm copper diameters, at 6.49986 × 4.499864 mm pitch. Direct source-unit conversion matches all four imported holes/centers/copper diameters within 1e-8 mm. This is not a converter geometry defect.
- Omron's page5 reference pattern specifies a nominal **1.00 mm PCB hole, ±0.05 mm**, for a 1.6 mm PCB. This does not specify uncompensated drill-tool diameter, plating compensation or a full land/mask pattern. Catalog copper sizes are not manufacturer approval.
- The downloaded OBJ has Z bounds -3.5 to +4.9 mm with approximately zero model offset and only a Z rotation. It cannot establish the specified B3F-1050 actuator height of 7.3±0.2 mm. STEP is preserved but not geometrically qualified. Do not stretch either model to invent missing geometry.
- The raw four-pin component omits internal common-pair annotations. Source symbol graphics and the manufacturer drawing show {1,2}/{3,4}. Connecting raw pins1/2 as opposite sides of a switch would put both nets on permanently common contacts. The package's labels correspond to a 180-degree rotation from Omron's printed top view; commoning is equivalent for this nonpolar switch. Exact numbering and assembly orientation still need explicit review.

`review-candidate.tsx` is an isolated, typed adapter. It retains source copper centers/diameters and changes only the hole target to 1.00 mm, explicitly declares both internal groups, and removes the unqualified supplier model. Core emits a fallback bounding box, which is **not** a mechanical substitute. Tests explicitly connect all four physical terminals to their two appropriate nets. Internal groups alone need not populate every source-port connectivity-map key.

## Relationship to earlier V106–V108 findings

This confirms earlier quarantine findings, rather than claiming a new general converter fix. V106 distinguished round B32-2010 (6 mm) from square B32-1010 (4×4 mm) keycaps: the existing 6.5 mm round panel openings do not establish square-cap fit. The quoted 0.35 mm minimum protrusion was conditional, excluded case/PCB/seating tolerances, and depended on an unverified datum. V107 verified explicit common-pair annotation and rejected automatic inference from arbitrary graphical lines. V108 prepared a conservative CLI warning candidate, not guessed geometry or topology. Its saved bundle is presently unrecovered; current upstream disposition was not verified here, and no duplicate warning PR was opened. This current CLI import emitted no warning.

## Regression coverage

From the repository root with its installed core0.0.2302 dependencies:

```
node node_modules/typescript/bin/tsc -p tsconfig.keypad-import.json
TSX_TSCONFIG_PATH=tsconfig.keypad-import.json node --import ./qualification-keypad-import/tests/register-cad-assets.mjs --import tsx qualification-keypad-import/tests/check.tsx
```

Eight isolated placements cover both board sides and 0/90/180/270-degree rotations. Checks cover immutable raw hashes, source-derived raw geometry, raw group absence, all four mapped physical holes, unchanged candidate copper, 1.00 mm nominal hole target, correct two groups and two nets, exactly one fallback CAD record, zero solder-paste records, and zero emitted error records. Forty-eight deliberate mutations to centers, copper, holes, groups, fallback presence and paste are rejected; mutated raw bytes also fail hash checks. Schematic and routing are disabled; these are not full-board DRC, schematic, mask, stencil or mechanical tests.

## Factory tolerance gate

[JLCPCB capabilities](https://jlcpcb.com/capabilities/Capabilities), drilling section checked 2026-11-08, lists ordinary through-hole tolerance **+0.13/-0.08 mm** and a finished-hole example. A nominal 1.00 mm ordinary-order hole therefore permits **0.92–1.13 mm**, wider than Omron's reference **0.95–1.05 mm**. Under these stated intervals, no nominal diameter guarantees containment: the lower bound requires nominal ≥1.03 mm while the upper bound requires nominal ≤0.92 mm. The regression uses integer micrometers to check this bounded calculation without floating-point ambiguity.

This is a tolerance incompatibility, not proof that a switch cannot physically assemble or function. Nominal adapter correction alone does not satisfy factory acceptance. JLCPCB's tighter ±0.05 mm offering is labeled **press-fit**, for circular 0.55–2.0 mm holes on multilayer ENIG with specific PCB remarks. It is not automatically an approved process for this soldered switch. Actual finished-hole acceptance or a justified engineering deviation remains pending. The listed hole-position tolerance is ±0.075 mm; this audit records it without treating it as an approved complete pattern/assembly tolerance stack. No order or supplier outreach is authorized by this checkpoint.

## Remaining release gates

Keep the board unchanged until finished-hole versus tool/plating interpretation, copper annular ring, solder mask, solder process, insertion/retention and assembly tolerances are reviewed. Review manufacturer numbering against the actual mounting orientation. Verify keycap type, socket geometry, engagement/seating depth, assembled datum, retention, off-axis movement, force/travel/overtravel and enclosure tolerance with appropriate physical evidence. Existing envelope translations and panel checks do not prove switch/cap mating. No sample purchase, manufacturing order or readiness approval is implied.

## Sources

- [Omron B3F manufacturer drawing](https://omronfs.omron.com/en_US/ecb/products/pdf/en-b3f.pdf), page5.
- [JLCPCB C93151 identity](https://jlcpcb.com/partdetail/OmronElectronics-B3F1050/C93151).
- [EasyEDA source response](https://easyeda.com/api/products/C93151/components?version=6.4.19.5), symbol `e1d43d7addfb4a7496e83af283c8a57c`, package `153ed004b0794cb6b8a2ebde7a1aabdf`.
