# Standard modem supply evidence

**Checked 2026-11-08. Evidence checkpoint only; fabrication and power-path qualification remain blocked.**

The public [EG912U-GL Hardware Design V1.1](https://quectel.com/content/uploads/2024/02/Quectel_EG912U-GL_Hardware_Design_V1.1.pdf) is a released **standard, non-QuecOpen** document dated 2023-08-17. Its relevant pages were rendered and visually checked. This closes the earlier QuecOpen-only source and unverified-table-transcription gaps at **module-family** level. It does not qualify the exact shipped hardware/firmware revision.

[JLC's C7472750 listing](https://jlcpcb.com/partdetail/Quectel-EG912UGLAC_I05SNNSA/C7472750) identifies EG912UGLAC-I05-SNNSA and a 3.3–4.3 V supply. [Quectel's 2026-04-23 PCN](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/8921/Quectel_PCN202603310001EN01.pdf), page 1, independently places that ordering code in EG912U-GL. Neither source assigns a hardware-design revision to a delivered lot. The [current official product page](https://www.quectel.com/product/lte-cat-1-bis-eg912u-gl/) lists Series Hardware Design V1.4 behind login; its contents were not retrieved. V1.1 must not be called the latest document.

## Visually verified supply facts

Page numbers below are printed / one-based PDF.

- V1.1 pp32–34 / 33–35: VBAT_BB pins 32/33 and VBAT_RF pins 52/53; 3.3 V minimum, 3.8 V typical, 4.3 V maximum. Section 3.5.2 specifies module-source capability of at least 2 A for LTE-only, or 3 A when GSM is available.
- Table 39, pp69–70 / 70–71, caption **Power Supply Ratings**: burst-drop maximum 400 mV; IVBAT typical 1.7 A, maximum 2.5 A. The current row says **Peak power consumption**, unit A, condition **At maximum power control level**. Mode, pulse duration, duty cycle and measurement setup are unspecified.
- Figure 9, p33 / 34, caption **Power Supply Limits during Burst Transmission**, is conceptual: no numeric time axis or current amplitude. Section 3.5.3 independently requires the input not to fall below 3.3 V. Its star-fed BB/RF branches and local-capacitor guidance are reference design recommendations, not a validated transient response.

The [QuecOpen V1.0 document](https://developer.quectel.com/en/wp-content/uploads/sites/2/2024/11/Quectel_EG912U-GL_QuecOpen_Hardware_Design_V1.0.pdf), also released 2023-08-17, was visually checked: Table 41 pp72–73 / 73–74 confirms the same numbers, but calls IVBAT **Peak supply current**. Its figure 7 and section 3.5.2 agree with the standard document's qualitative limits and source-capability guidance.

## Interpretation and remaining gates

Do not turn the 2 A capability recommendation into continuous consumption, a pulse waveform, or a battery-duration calculation. The IVBAT row does not identify its radio mode or BB/RF split. Do not add the separate BB/RF pin-current comments to claim simultaneous 3.5 A consumption, or use the unqualified 2.5 A row to override GSM's 3 A source recommendation. Both module-pin floor and burst droop must pass; one does not substitute for the other. No pack, converter or capacitor is approved by this checkpoint.

Obtain the current applicable hardware guide and exact SKU/lot/firmware scope, permitted radio modes including fallback/reset, simultaneous BB/RF current traces and measurement conditions. Then qualify the complete path over temperature, battery age/state of charge and component tolerances.

## Firmware and USB scope

V1.1 pp34–38 corroborates the existing sequencer's underlying startup/shutdown pulse minimums and discharged-rail prerequisite; precise values and references are in `evidence.json`. The 2.1 s / 3.1 s margins and 60 s timeouts remain design choices, not manufacturer-guaranteed timing.

If modem USB is connected later, the p37 late-USB startup requirement needs an explicit timing gate. The present sequencer has no USB-VBUS input. This is **not a current connected-board timing defect**: `electronics/modem-support.tsx` leaves pins 8/9/10 unmapped. Charging `USB_VBUS_RAW` is a different net. Table 12 confirms their USB functions and requests service test points; an explicit unused-pin-8 termination instruction was not found in the reviewed pin/USB sections. Leaving the logical pins open is not proof of a fully qualified production service interface.

`evidence.json` records source hashes, exact page locations, scope and limitations. Source PDFs/page pixels are retained separately for review and are not redistributed here. No firmware logic, schematic wiring, PCB geometry, supplier settings or radio modes were changed. The sequencer comment now records the standard-document evidence and its disconnected-USB scope.

## Regression checks

The integrated logical-net test already requires modem USB pins 8/9/10 to stay open. The placed-board test now checks the same physical-pad scope and rejects three injected ties to charging VBUS, one per USB pin. These tests preserve an unresolved interface; they do not approve leaving the pins open in production. Run `npm run typecheck`, `npm run test:placement` and `npm run test:logical-phone`. The wider `npm run check:current` also includes these checks.
