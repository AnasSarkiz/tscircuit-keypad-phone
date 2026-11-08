# Verified tscircuit issues from these imports

## Resolved locally: missing MCU exposed-pad port associations

Core0.0.2272 loses PCB-port association for the nine pin41 lands. Already fixed by [core#5177](https://github.com/tscircuit/core/pull/5177). Update to released core0.0.2302 repairs the same import without modifying its geometry or pin labels. `npm run test:jlc-imports` is the phone regression. No duplicate report was filed.

## Open observation: explicit EasyEDA paste regions are omitted

Normal import of TPD6S300ARUKR/C2876380 with tscircuit0.0.3120 / CLI0.1.2446 produces no explicit paste geometry, although the exact EasyEDA source has21 SOLIDREGION shapes on layer5, declared `TopPasteMaskLayer`. The exposed-pad aperture `gge214` is approximately1.36000744 mm square, smaller than the1.70 mm copper pad. See `paste-source-evidence.json` for the exact source layer/shape excerpt, component/package IDs and response hash.

The bundled converter's SOLIDREGION conversion path handles board cutouts/documentation but does not preserve these paste-layer regions. This is source manufacturing intent lost during import, separate from the catalog's own differences from TI. The catalog aperture is one square; TI's example uses four windows. Neither should be described as the other.

Reproduce by importing C2876380 with the manifest command, comparing its raw package layer5 SOLIDREGION entries with the generated TSX, and inspecting eventual paste-layer fabrication output. A full Gerber/stencil export comparison has not been performed, so this observation does not claim a particular manufactured stencil result.

Local mitigation: all review adapters explicitly suppress paste. Do not remove this guard until mask/stencil geometry is independently reviewed and represented correctly. No upstream issue or PR was opened during this checkpoint.

## Not converter defects

Exact-source comparison across all47 TI copper pads confirms the generated geometry is faithful:43 rectangles and four polygons preserve the catalog coordinates/dimensions under one translation and Y inversion per part. The TPS25947 polygon vertices match to floating-point tolerance below1.1e-13 mm. Catalog SBU typos and cross-variant aliases are also already present in the source symbols. They are corrected in the local review adapters without changing downloaded imports. The MCU's approximately0.03 mm bottom-row asymmetry is similarly present in catalog data.

## Existing upstream stack verified against this phone part (2026-11-08)

Do not open a duplicate report. User-authored [easyeda-converter PR612](https://github.com/tscircuit/easyeda-converter/pull/612) is an open draft stacked on [reproduction PR611](https://github.com/tscircuit/easyeda-converter/pull/611), which currently reports conflicts. Focused C2876380 reproduction against current converter main9d377ea2 produces0 paste apertures and21 copper pads. PR612 heada70bb8f3 produces all21 paste polygons and21 copper pads, with all84 vertices matching the supplier transform within2.28e-13 mm; EP aperture remains1.36000744 mm square.

[props PR955](https://github.com/tscircuit/props/pull/955) and [core PR4865](https://github.com/tscircuit/core/pull/4865) were closed unmerged by stale bots. Their functionality is not superseded in current main: solderpaste still supports rect/circle rather than polygon, and footprint-level paste suppression is absent. Installed props0.0.718 rejects the polygon output. Therefore converter-only publication is insufficient. The appropriate general fix is to refresh and test the existing dependency stack, not add another PR.

This is source-conversion evidence only. Native rendering and Gerber/stencil export of the complete stack remain unverified. The phone's no-paste guards stay in place. No upstream branches, PR statuses or merges were changed during this investigation.


## Focused downstream Gerber check (2026-11-08)

Current `circuit-json-to-gerber` main `35583a5c5fea6fba05bf5b56c62427d800e97876` (version 0.0.122) already supports polygon paste. Feeding the 21 C2876380 polygons from the PR612 conversion into that exporter preserves all 84 unique vertices, with 21 closed regions per face. Top/bottom and Y-reflection combinations pass; maximum serialized coordinate error is 0.00000036 mm. An independent `gerber-to-svg` 4.2.8 parser reports no geometry warnings. Other Gerber/drill files remain unchanged against a board-only control. Exact versions and results are in `paste-gerber-geometry.json`.

This check starts at converted Circuit JSON and does not validate the released generated-TSX/Core pipeline. The existing props/Core/converter refresh is separate and still requires its own verification and publication. No new exporter PR is needed for these apertures. The supplier's single-square EP aperture remains distinct from TI's example stencil pattern, and the phone's no-paste guards remain unchanged.
