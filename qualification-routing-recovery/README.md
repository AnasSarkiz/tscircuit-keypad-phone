# Routing recovery and migration repair, 2026-11-08

Original V66 source and routing artifacts were recovered from saved source/full-study ZIPs and the complete-history Git bundle. All requested originals were byte-identical across those independent saved forms. Original revision: `f0bb2eea05b9f0cf50d171c38730f680fc7e4da3` (2026-11-05). Exact source hashes are in `provenance.json`.

Before modifying the checker, it was rerun in an isolated workspace against the original archived placement. Its checks JSON matched the saved historical result exactly. That establishes the recovered baseline; it does not approve the newer footprint geometry.

## Repairs for current imports

The imported footprints retain component datums but have different catalog copper. Running historical routing against current placement revealed17 clearances below the existing0.15 mm screen. Examples: USB protector's extended toes versus CC/fault routing, eFuse corner geometry versus raw-VBUS routing, and a roughly0.03 mm MCU pad-row difference versus nearby logic-supply traces.

Only13 route coordinate lists and one via position changed. All539 routes,249 vias, widths, drill sizes, nets, pad obligations, board placement and keepouts were preserved. `route-changes.json` records before/after coordinates. The tightly constrained fault via and its three fanout routes were adjusted together; neighboring supply routes moved by0.05 mm. No obligation was removed to make a test pass.

The recovered checker also now resolves source-component internal terminal groups. Current core creates distinct physical MCU EP ports sharing a logical ground terminal; requiring a direct source trace on every repeated pad would incorrectly classify eight as NC. Conflicting nets, cross-component groups and missing physical ports now fail closed, with three focused mutation tests.

Clearance failures are collected into an actionable diagnostic file rather than exposing only the first pair. The0.15 mm screen and existing1e-8 numerical comparison tolerance are unchanged. This remains an engineering screen, not a JLCPCB process acceptance or physical guarantee.

## Fresh results

-539 routes,249 vias and60 keypad plated lands revalidated across four layers.
-688,889 foreign-geometry pairs checked; minimum screened gap0.15 mm within floating-point tolerance; zero reported violations.
-One continuous ground-plane component,0.2 mm neck screen, with exact covered-triangle export.
-All95 previously verified V66 copper islands preserved; a deliberately deleted island is rejected.
-Whole-phone candidate:210 electronic components,133 placed.336 of522 minimum joins completed, **186 still open**. No new completed-join count is claimed for the repair.
-Layered Circuit JSON schemas and SVG export pass. This is not a Gerber/stencil or mechanical acceptance result.

Reports in this folder contain exact coverage and baseline/current results. `output/` contains generated full geometry and layered circuit artifacts; they are reproducible and intentionally excluded from Git.

## Modem body-clearance guard

`engineering/modem_clearance.py` was recovered and hardened. New regressions reject booleans/strings masquerading as geometry, nonfinite or overflowing values, unsupported rotations, malformed lists/fields, ambiguous/duplicate references, incomplete expected sets, truthy nonboolean body verification, and duplicate JSON fields. Exact3 mm same-face boundaries are retained without a tolerance admitting sub-3 mm spacing. Opposite-face exemptions remain explicitly2D-only. Historical boundary tests and10 focused unittest methods pass. A complete verified physical-body inventory has not yet been supplied, so this does not approve the whole assembly.

## Reproduce

```
npm ci --ignore-scripts
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-routing.txt
npm run check:current
.venv/bin/python scripts/check-current.py --negative
```

The aggregate runs current type/input/import/placement checks, integrated logical-net checks, host and power tests, modem guard tests, routed geometry, internal-group mutation tests, complete coverage and historical-island preservation, then schema/SVG export. `--negative` additionally runs the inherited22 route/via fault cases. The original broader mechanical/process command list is preserved separately under `historical-routing/`; omitted mechanical stages are not silently marked passing.

## Remaining work

The recovered routing blocker is closed, but186 minimum joins and77 electronic placements remain. Mask/stencil still requires qualification, including the known EasyEDA explicit-paste omission. Body/enclosure fit, antenna/impedance/RF performance, carrier/VoLTE approval, battery/protection pulses, charging fault behavior, assembly process and physical testing remain unqualified. Every result retains `release: false`.
