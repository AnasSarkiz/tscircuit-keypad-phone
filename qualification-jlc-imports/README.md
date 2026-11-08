# JLCPCB import checkpoint, 2026-11-08

All six exact catalog parts were imported successfully through the normal tscircuit CLI, using `tscircuit@0.0.3120` / CLI `0.1.2446`:

```
tsci import <LCSC-ID> --jlcpcb --download --use-exact-footprint
```

- C2913199: ESP32-S3-WROOM-1-N16, 41 terminals / 49 copper pads.
- C7472750: EG912UGLAC-I05-SNNSA, 126 terminals / pads.
- C2845237: TPS63802DLAR, 10 terminals / pads.
- C2876380: TPD6S300ARUKR, 21 terminals / pads including EP21.
- C3189972: TPS62827ADMQR, 6 terminals / pads.
- C3662793: TPS259470LRPWR, 10 terminals / pads, including four L-shaped polygon pads.

`import-manifest.json` records exact filenames, source IDs, CLI version and SHA-256 hashes. The downloaded TSX and models are unmodified. The modem catalog import did not supply a model. A model file's presence is not verification of its size, origin or physical fit.

## Actual tscircuit issue: old installed core, now repaired

The phone lockfile used core **0.0.2272**. With the new MCU import it emitted 49 copper pads but only 40 PCB ports: all nine GND3/pin41 pads had no PCB-port association, despite the logical GND connection. No error record warned about the missing association.

This was already fixed upstream by [core PR5177](https://github.com/tscircuit/core/pull/5177), merge `c38127f3c71616b9cde80e459f509e044d4385c9`. Released core **0.0.2302**, gitHead `ba89ccb98f8550284e5e1819b059660317fb7e02`, contains that merge. The same imported MCU now emits 49 mapped PCB ports. Nine EP ports form an explicit internal-connection group linked to the primary pin41 GND trace. The phone dependency and lockfile are updated to exactly 0.0.2302. No duplicate issue or PR was opened.

## Source and design differences, not established converter defects

- **MCU:** All 41 pin functions, pad numbering and orientation match Espressif's manufacturer reference. After aligning the origin, bottom-row pins15–25 differ by about 0.030 mm from the manufacturer KiCad geometry; pin26 has a corresponding small asymmetry. The exact 0.029972 mm pin26-versus-neighbor offset is already present in EasyEDA package `40128f2916484a71b10e367662746d66` and faithfully preserved by conversion. This is catalog geometry, not a conversion defect. The imported MCU datum differs from the legacy wrapper by approximately3.785 mm in localY; a future board swap must compensate this explicitly before applying the component rotation.
- **Modem:** All126 pads agree with the existing manufacturer-derived land map within 0.000162 mm X, 0.030214 mm Y and 0.0000104 mm size. The 25×29 mm body intentionally surrounds inset lands. The import marks23 pins RESERVED that the QuecOpen document assigns to display/camera/SD/headphone functions. Keep those RESERVED names until exact SKU/firmware support is demonstrated. Normal import success does not establish QuecOpen, VoLTE or carrier compatibility.
- **TPS63802:** The import uses 0.30 mm pad widths versus TI's 0.25 mm example. Centers and lengths agree within rounding. It does not encode the example's split ground-pad paste.
- **TPD6S300A:** Import peripheral pads have an extra0.20 mm outer toe relative to TI's example, with the same inner edge. EP21 dimensions agree. Imported symbol names misspell SBU as SUB, and attributes omit the required GND connections for NC16/17 and EP21.
- **TPS62827A:** The import does not implement TI's preferred solder-mask-defined land construction. TI's illustrated opening dimensions must not be mistaken for copper dimensions. Mask and paste need explicit review before use.
- **TPS259470L:** L-shaped corners survive conversion, but differ slightly from TI's example. Imported aliases OVCSEL, PG and PGTH belong to other variants, not TPS259470L.

Exact EasyEDA source comparison now confirms all47 TI copper pads, including the four polygons, are faithfully converted. SBU typos and cross-variant aliases are already in catalog symbols. Separately, the converter omits21 explicit paste-layer regions from C2876380, including its reduced EP aperture. See [the verified issue list](tscircuit-issues.md). This is distinct from TI's own example and does not establish a particular stencil-export result.

## Local repairs and regression coverage

`electronics/jlc-review-candidates.tsx` supplies isolated review adapters. It corrects the USB protector's SBU spelling and required-ground attributes, removes the eFuse's wrong-variant aliases, and suppresses all solder paste. Raw imports remain untouched. Adapters do not silently change copper geometry or substitute into the historical V66 board.

Run:

```
npm ci --ignore-scripts
npm run typecheck:jlc-imports
npm run test:jlc-imports
npm run check:public
npm test
npm run test:power
```

The import test checks exact identities, all terminals and222 copper primitives, correct PCB/source-port association, explicit required grounds including all nine MCU EP lands, and all four eFuse polygon pads. It tests raw imports and adapters independently, verifies adapters preserve copper and emit no paste, and saves circuit JSON/SVG under `output/jlc-imports/`. Routing is disabled. Node24's asset loader supplies actual local OBJ/STEP URLs but does not load or validate the models.

## Remaining integration work

Follow-up migration now replaces the three active JSON consumers with actual imported copper while preserving component datums and logical nets. Full-project typecheck and active PCB-input checks pass. See [the migration checkpoint](../qualification-board-migration/README.md). Original historical sources/tests are retained; they were not replaced by invented JSON or relabeled catalog records. Subsequent routing recovery revalidated the migrated geometry after 17 clearance repairs; see [the routing checkpoint](../qualification-routing-recovery/README.md).

Component placements and the enclosure remain unchanged. The subsequently repaired partial routing is screened, but the phone still has open joins. There is no complete-board sign-off, mask/stencil approval, model-fit approval or fabrication release. Battery/protection pulse capability and exact modem variant/carrier remain open.

### Manufacturer references

- [Espressif KiCad libraries](https://github.com/espressif/kicad-libraries), including manufacturer license and design-output exception.
- [Quectel EG912U-GL QuecOpen Hardware Design V1.0](https://developer.quectel.com/en/wp-content/uploads/sites/2/2024/11/Quectel_EG912U-GL_QuecOpen_Hardware_Design_V1.0.pdf), Figures2/42 and pin table. Standard catalog SKU capability remains to be confirmed.
- [TPS63802](https://www.ti.com/lit/ds/symlink/tps63802.pdf), drawing4223750/D.
- [TPD6S300A](https://www.ti.com/lit/ds/symlink/tpd6s300a.pdf), drawing4222676/A.
- [TPS62827A](https://www.ti.com/lit/ds/symlink/tps62827a.pdf), drawing4222645/E.
- [TPS25947](https://www.ti.com/lit/ds/symlink/tps25947.pdf), drawing4225183/A and variant-specific pin tables.
