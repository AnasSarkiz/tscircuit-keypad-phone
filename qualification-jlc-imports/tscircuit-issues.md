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
