# EG912UGLAC-I05-SNNSA feature evidence

Checked 2026-11-08. Evidence checkpoint only, not production approval.

- [JLC C7472750](https://jlcpcb.com/partdetail/Quectel-EG912UGLAC_I05SNNSA/C7472750) identifies the exact selected MPN, EG912UGLAC-I05-SNNSA.
- In an [August 19, 2025 reply](https://forums.quectel.com/t/what-is-full-part-number-for-eg912u-gl-with-optional-wifi-scan/49052/2), Quectel support member mandy.wang states that this exact ordering code does not support Bluetooth, Wi-Fi scanning or GNSS. Public forum metadata identifies the author as staff, moderator and Support-team. This is specific manufacturer-support evidence, not a shipped-unit test or pad-termination instruction.
- The officially hosted, released [Series specification V1.5](https://www.quectel.com/content/uploads/2024/03/Quectel_EG912U_Series_LTE_Standard_Specification_V1.5.pdf?wpId=126964), page 2, lists VoLTE for EG912U-GL, marks those three other features optional, and describes Wi-Fi scan as receive-only. Its GL regulatory column lists FCC for America and IC for Canada. Both pages were visually checked. These are family-level statements, not exact-SKU firmware or carrier approval.

## Unresolved VoLTE report

An [October 14–16, 2026 thread](https://forums.quectel.com/t/eg912u-gl-how-to-enable-volte-ims-never-registers-cireg-0-0/61860) concerns QuecPython firmware EG912UGLAAR03A01M08_OCPU_QPY, an operator string of DIALOG, failed IMS and 2G fallback. USA is the planned destination; no complete ordering code, actual test country or US-carrier test is supplied. Staff member Felix.feng-Q asks for the exact model and gives an explicitly tentative negative VoLTE answer requiring another check. His separate US-certification assertion cites no certification type or grant. No follow-up appears.

Resolve that discrepancy for the exact SKU/firmware/network before claiming voice readiness. Neither the thread nor the family FCC listing establishes the candidate's carrier acceptance or end-product certification. Preserve optional-feature and voice qualification gates; do not infer optional functions from generic library pad names.

## Current design dependency review

At baseline `6eb8da0`, neither the logical phone nor the placed candidate depends on modem GNSS, Bluetooth or Wi-Fi scanning:

- Generic imported names appear on pin49 (ANT_GNSS), pin51 (1PPS) and pin56 (ANT_BT/WIFI_SCAN). The live logical component keeps these endpoints unreviewed and disconnected. The only connected modem RF antenna endpoint is cellular ANT_MAIN, pin60; matching and antenna performance remain unqualified.
- Host prototypes emit dialing, answering, hang-up and SMS commands. They do not implement GNSS, Bluetooth or Wi-Fi scanning. They are not flashed firmware or a working serial/modem driver, and no successful VoLTE call is claimed.
- The power policy still requires explicit LTE-only, carrier-voice and power-path evidence; the shipped study defaults all such evidence false. This is a host contract, not a physical safety interlock or radio-mode configuration.

The existing logical and placed-board tests now require optional pins49/51/56 to remain open. Three deliberately added cellular-RF connections are rejected, one per optional endpoint. The three USB wrong-VBUS checks remain intact. Complete logical and placement Circuit JSON outputs are byte-identical before/after the new assertions: no raw imports, supplier IDs, wiring, copper, part positions, firmware logic or release gates changed.

This does not prove that floating every unused pad is the correct production treatment. Exact-SKU electrical termination still needs its applicable hardware instructions. No substitute modem is selected, and the optional-feature finding does not invalidate the current voice/SMS-only feature plan.

## Qualification gates retained

Confirm the intended cellular country/carrier rather than inferring it from the shipping destination. Verify the exact delivered ordering code, hardware revision and firmware build; supported voice/IMS profile and carrier acceptance; applicable regulatory grants and integration conditions; actual incoming/outgoing voice and SMS behavior on the intended network, including permitted fallback/reset states. Emergency-service requirements need a compliant validation plan, not unrequested live emergency calls. Battery pulses, independent charging protection, audio/antenna implementation and physical tests remain separate unresolved gates.

Run `npm run typecheck`, `npm run test:placement`, `npm run test:logical-phone`, `npm run test:control`, or the wider `npm run check:current`. The evidence and design-review JSON files record the review scope. No purchase, supplier communication, modem configuration or fabrication was performed.
