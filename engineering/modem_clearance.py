"""Fail-closed same-face placement gate using physical body envelopes, not copper bounds.

Recovered historical implementation, hardened with recovery regression tests.
Expanded rectangle is conservative at corners. Opposite-face parts need separate
3D review. No component may be omitted from expected_refs. Units mm; angles CCW.
Only quarter-turn rotations are supported. A pass is never a manufacturing release.
"""
import math
from collections.abc import Mapping


def _number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError('invalid geometry: expected a finite number, not bool/string')
    try:
        if not math.isfinite(value):
            raise ValueError('invalid geometry: nonfinite number')
        return float(value)
    except OverflowError as exc:
        raise ValueError('invalid geometry: number out of range') from exc


def _reference(value):
    if not isinstance(value, str) or not value or value != value.strip():
        raise ValueError('invalid reference: expected a nonempty trimmed string')
    return value


def corners(p, extra=0):
    if not isinstance(p, Mapping):
        raise ValueError('invalid envelope: expected an object')
    try:
        x, y, width, height, rotation = [_number(p[k]) for k in
                                        ('x', 'y', 'width', 'height', 'rotation')]
    except KeyError as exc:
        raise ValueError('invalid geometry: missing ' + str(exc)) from exc
    extra = _number(extra)
    if width <= 0 or height <= 0 or extra < 0:
        raise ValueError('invalid body dimensions')
    if rotation % 90 != 0:
        raise ValueError('unsupported rotation: only multiples of 90 degrees')
    if rotation % 180:
        width, height = height, width
    left, right = x - width / 2 - extra, x + width / 2 + extra
    bottom, top = y - height / 2 - extra, y + height / 2 + extra
    if not all(math.isfinite(v) for v in (left, right, bottom, top)):
        raise ValueError('invalid geometry: bounds overflow')
    if not left < right or not bottom < top:
        raise ValueError('invalid geometry: body collapses at supplied precision')
    return [(left, bottom), (right, bottom), (right, top), (left, top)]


def overlap(a, b):
    # corners() produces only axis-aligned, quarter-turn rectangles. Exact touching
    # at the expanded 3 mm boundary is allowed; no tolerance admits a smaller gap.
    return (min(x for x, _ in a) < max(x for x, _ in b)
            and min(x for x, _ in b) < max(x for x, _ in a)
            and min(y for _, y in a) < max(y for _, y in b)
            and min(y for _, y in b) < max(y for _, y in a))


def enforce(modem, others, expected_refs):
    if not isinstance(modem, Mapping):
        raise ValueError('invalid modem envelope')
    if not isinstance(others, (list, tuple)) or not isinstance(expected_refs, (list, tuple)):
        raise ValueError('others and expected_refs must be explicit lists')
    modem_ref = _reference(modem.get('ref'))
    expected = [_reference(ref) for ref in expected_refs]
    if len(set(ref.casefold() for ref in expected)) != len(expected):
        raise ValueError('duplicate or ambiguous expected references')
    refs = []
    for p in others:
        if not isinstance(p, Mapping):
            raise ValueError('invalid component envelope')
        refs.append(_reference(p.get('ref')))
    all_refs = [modem_ref] + refs
    if len(set(ref.casefold() for ref in all_refs)) != len(all_refs):
        raise ValueError('duplicate or ambiguous references (including modem)')
    errors = []
    if (modem.get('width'), modem.get('height')) != (25, 29):
        errors.append('modem physical body must be 25x29, not copper bounding box')
    if modem.get('layer') not in ('top', 'bottom'):
        errors.append('modem layer missing or invalid')
    missing, extra = set(expected) - set(refs), set(refs) - set(expected)
    if missing:
        errors.append('missing envelopes: ' + ','.join(sorted(missing)))
    if extra:
        errors.append('unexpected envelopes: ' + ','.join(sorted(extra)))
    try:
        zone = corners(modem, 3)
    except ValueError as exc:
        raise ValueError('invalid modem envelope: ' + str(exc)) from exc
    for p in others:
        if p.get('verified_body') is not True:
            errors.append(p['ref'] + ': unverified body')
        if p.get('layer') not in ('top', 'bottom'):
            errors.append(p['ref'] + ': missing or invalid layer')
        try:
            poly = corners(p)
        except ValueError as exc:
            errors.append(p['ref'] + ': invalid geometry: ' + str(exc))
            continue
        if p.get('layer') == modem.get('layer') and overlap(zone, poly):
            errors.append(p['ref'] + ': violates 3mm modem clearance')
    if errors:
        raise ValueError('\n'.join(errors))
    return {'same_face_clearance_pass': True,
            'opposite_face_3d_clearance_validated': False,
            'manufacturing_release': False}


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON field: ' + key)
        result[key] = value
    return result


if __name__ == '__main__':
    import json
    import sys
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python3 engineering/modem_clearance.py <verified-placement.json>; missing input is a BLOCK')
    try:
        with open(sys.argv[1], encoding='utf-8') as stream:
            d = json.load(stream, object_pairs_hook=_unique_object)
        if not isinstance(d, dict):
            raise ValueError('placement must be an object')
        result = enforce(d['modem'], d['others'], d['expected_refs'])
    except (ValueError, KeyError, OSError) as exc:
        raise SystemExit('PLACEMENT BLOCKED: ' + str(exc))
    print(json.dumps(result))
