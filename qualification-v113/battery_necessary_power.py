"""Optimistic necessary-condition screen, not battery or converter qualification.

Battery terminal voltage is a loaded, measured value, not open-circuit voltage.
The assumed loads are simultaneous and sustained for the interval being assessed;
they do not claim that an LTE transmit burst lasts for that interval.
"""
from __future__ import annotations
import json
import math
from pathlib import Path

# Earlier phone sensitivity allocation; NOT a measured modem waveform.
MODEM_W = 3.8 * 2.0
HOST_INPUT_W = 3.3 * 0.1 / 0.8
LIGHT_INPUT_W = 5.3 * 0.131 / 0.75

# Manufacturer-listed discharge limits, not guaranteed cold/aged limits. For
# 246524 use a separate 3.6 A engineering budget below the low end of the
# stated PCM detection range; this is not a guarantee of no trip.
PACKS = {
    "Jauch 246524 conservative PCM budget": 3.6,
    "USE-18650-2600PCBJST pack-only optimistic ceiling": 2.6,
    "USE-18650-2600PCBJST hypothetical JST PH rated path": 2.0,
    "Adafruit 2011 linked cell sheet": 2.0,
    "US Electronics USE-104060-3K-PCBJST": 1.5,
}


def required_efficiency(voltage_v: float, current_a: float, aux_w: float) -> float | None:
    """Necessary modem conversion efficiency; None means even ideal fails.

    Zero interconnect loss and steady converter input/output power are assumed.
    Exactly 100% is returned as a boundary, not a practical pass.
    """
    if not all(math.isfinite(x) for x in (voltage_v, current_a, aux_w)):
        raise ValueError("Inputs must be finite")
    if voltage_v <= 0 or current_a <= 0 or aux_w < 0:
        raise ValueError("Voltage/current must be positive and load nonnegative")
    remaining_w = voltage_v * current_a - aux_w
    if remaining_w < MODEM_W:
        return None
    return MODEM_W / remaining_w


def run() -> dict:
    rows = []
    for name, limit in PACKS.items():
        for v in (4.2, 3.8, 3.6, 3.3, 3.0):
            for light in (False, True):
                aux = HOST_INPUT_W + (LIGHT_INPUT_W if light else 0)
                eta = required_efficiency(v, limit, aux)
                rows.append({"pack": name, "current_limit_A": limit,
                             "loaded_terminal_V": v, "backlight": light,
                             "allocated_aux_input_W": round(aux, 6),
                             "minimum_modem_conversion_efficiency": round(eta, 6) if eta is not None else None,
                             "necessary_condition": "not_met_even_ideally" if eta is None else ("ideal_only" if eta >= 1 else "not_ruled_out_only")})
    # Negative controls: should reject a real power deficit, the 100% boundary,
    # non-finite measurements, and preserve monotonic efficiency requirements.
    assert required_efficiency(3.3, 2.6, HOST_INPUT_W + LIGHT_INPUT_W) is None
    assert required_efficiency(3.0, 2.6, HOST_INPUT_W) is None
    assert math.isclose(required_efficiency(MODEM_W + HOST_INPUT_W, 1, HOST_INPUT_W), 1.0)
    assert required_efficiency(4.2, 3.6, HOST_INPUT_W) < required_efficiency(3.6, 3.6, HOST_INPUT_W)
    for values in ((float("nan"), 2, 0), (3.6, float("inf"), 0), (0, 1, 0), (3.6, 1, -1)):
        try:
            required_efficiency(*values)
        except ValueError:
            pass
        else:
            raise AssertionError(f"invalid inputs accepted: {values}")
    return {"scope": "necessary sustained-power condition under stated simultaneous design allocation; no waveform, impedance or converter qualification",
            "modem_output_W": MODEM_W, "host_input_W": HOST_INPUT_W,
            "backlight_input_W": LIGHT_INPUT_W, "rows": rows,
            "pack_or_hardware_approved": False}


if __name__ == "__main__":
    result = run()
    path = Path(__file__).with_name("necessary-power-results.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(f"PASS: {len(result['rows'])} necessary-condition cases and boundary/invalid-input controls; no pack qualified")
