# Phone checkpoint: charge request freshness

Baseline: engineering checkout at `97036c8` (later qualification notes through V111); the saved V66 layout remains the last accepted hardware candidate. V93 is a routing ledger analysis, not a new completed board. The 133/210 placed component and 336/522 minimum-join counts describe that candidate, with 186 joins still open. The layout and geometry were not changed here.

## What changed

`firmware/charge-qualification.ts` requires a distinct acquisition timestamp for each new sample, rejects repeated, out-of-order, future and stale acquisitions, and now offers `checkFresh(nowMs)` for a running scheduler to clear its host charge request once the last input sample is more than 100 ms old. Invalid, backward, and duplicate sample clocks latch a host fault until reset; watchdog observations must also move monotonically. Recovery from stale input requires fresh qualification samples and a complete 250 ms dwell. `tests/charge-qualification.ts` exercises the boundary, missed sample, recovery, invalid clocks and fault latch. `npm test` now includes the existing control suite so these checks run in the standard project test command.

This is a preliminary host logic contract, not firmware flashed on hardware and not a safety-rated watchdog. It depends on a trustworthy driver timestamping actual new acquisitions; relabeling cached data as new defeats this check. If the CPU, scheduler, output driver, or GPIO fails, this method cannot run or remove a hardware charge enable. Sensor freshness, charging interlock, switch-off time, thermal coupling, and fault response must be implemented and verified independently in hardware. The unreleased evidence flags remain false by default; no power architecture, battery, or board was qualified by this change.

## Hardware status

Preferred architecture remains one custom rigid board, with a separate display ribbon and wired battery/antenna/audio connections, subject to actual routing and physical assembly. The current enclosure and assembled-part studies are preliminary; switch/cap engagement and the B3F-1050 JLC C93151 import remain quarantined (V106–V108). The V105 wired receiver is only an alternative concept. The EastRising 1.8-inch display and cylindrical battery pair previously priced at $11.67 is not an approved bill of materials: the display has poor outdoor readability and the cell requires a case redesign. Flat protected battery candidates in `sourcing-v102` are not qualified for the modem's cold/aged pulse conditions. Prices and availability in old studies require fresh verification.

Before circuit or PCB release, establish the intended cellular country and carrier, exact supported modem/SKU and VoLTE; documented battery/PCM voltage droop under the actual worst-case waveform and cold/aged conditions; independent fail-safe charging and temperature sensing; display-tail connector mating and pin orientation; imported part geometry/rights and assembly process; complete RF/audio and physical assembly tests. Shipping to tscircuit Inc. does not determine cellular use country. No components or fabrication ordered.

## Reproduce

Run `npm run test:control`, `npm run test:power`, `npm run typecheck`, `npm test`, and `python3 qualification-v93/route-readiness.py` in the local engineering checkout. These are software, calculation, and historical ledger checks, not hardware, EMC, RF, mechanical sample, charger safety or manufacturing validation.
