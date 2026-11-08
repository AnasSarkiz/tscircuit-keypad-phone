"""Focused fail-closed regression tests for the recovered placement guard."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from engineering.modem_clearance import enforce


class RecoveredClearanceTests(unittest.TestCase):
    def setUp(self):
        self.modem = dict(ref='MODEM', x=0, y=0, width=25, height=29,
                          rotation=0, layer='top')
        self.part = dict(ref='R1', x=16, y=0, width=1, height=1,
                         rotation=0, layer='top', verified_body=True)

    def reject(self, modem=None, part=None, refs=None):
        with self.assertRaises(ValueError):
            enforce(self.modem if modem is None else modem,
                    [self.part if part is None else part],
                    ['R1'] if refs is None else refs)

    def test_boundary_and_scope(self):
        result = enforce(self.modem, [self.part], ['R1'])
        self.assertTrue(result['same_face_clearance_pass'])
        self.assertIs(result['opposite_face_3d_clearance_validated'], False)
        self.assertIs(result['manufacturing_release'], False)
        self.reject(part={**self.part, 'x': 16 - 1e-10})
        enforce(self.modem, [{**self.part, 'x': 16 + 1e-10}], ['R1'])
        enforce(self.modem, [{**self.part, 'x': 0, 'layer': 'bottom'}], ['R1'])

    def test_all_numeric_fields(self):
        for field in ('x', 'y', 'width', 'height', 'rotation'):
            for value in ('1', True, False, None, [], {}, float('nan'),
                          float('inf'), -float('inf'), 10**400):
                for target in ('modem', 'part'):
                    with self.subTest(field=field, value=value, target=target):
                        body = self.modem if target == 'modem' else self.part
                        self.reject(**{target: {**body, field: value}})

    def test_missing_fields(self):
        for target in ('modem', 'part'):
            body = self.modem if target == 'modem' else self.part
            for field in body:
                with self.subTest(target=target, field=field):
                    self.reject(**{target: {k: v for k, v in body.items() if k != field}})

    def test_layers_and_sizes(self):
        for target in ('modem', 'part'):
            body = self.modem if target == 'modem' else self.part
            for layer in ('TOP', 'front', '', None, True, [], {}):
                with self.subTest(target=target, layer=layer):
                    self.reject(**{target: {**body, 'layer': layer}})
            for field in ('width', 'height'):
                for value in (0, -1, -100):
                    self.reject(**{target: {**body, field: value}})
        self.reject(modem={**self.modem, 'width': 19.5})
        self.reject(modem={**self.modem, 'width': 29, 'height': 25})

    def test_rotations(self):
        for angle in (45, 89.999, -45, 90.001):
            self.reject(modem={**self.modem, 'rotation': angle})
            self.reject(part={**self.part, 'x': 100, 'rotation': angle})
            self.reject(part={**self.part, 'layer': 'bottom', 'rotation': angle})
        for angle in (90, 270, -90, 450):
            enforce({**self.modem, 'rotation': angle},
                    [{**self.part, 'x': 0, 'y': 16, 'rotation': angle}], ['R1'])
        for angle in (0, 180, -180, 360):
            enforce({**self.modem, 'rotation': angle}, [self.part], ['R1'])

    def test_verification_is_literal_true_even_on_other_face(self):
        for value in (False, 1, 'true', 'false', [], {}, None):
            for layer in ('top', 'bottom'):
                self.reject(part={**self.part, 'layer': layer, 'verified_body': value})

    def test_reference_completeness_and_ambiguity(self):
        for value in ('', ' R1', 'R1 ', None, 1, True, [], {}):
            self.reject(part={**self.part, 'ref': value})
            self.reject(modem={**self.modem, 'ref': value})
            self.reject(refs=[value])
        for refs in ([], ['R2'], ['R1', 'R2'], ['R1', 'R1'], ['R1', 'r1'], ['MODEM']):
            self.reject(refs=refs)
        for ref in ('MODEM', 'modem'):
            self.reject(part={**self.part, 'ref': ref}, refs=[ref])
        for parts in ([], [self.part, self.part], [self.part, {**self.part, 'ref': 'r1'}]):
            with self.assertRaises(ValueError):
                enforce(self.modem, parts, ['R1'])

    def test_malformed_containers(self):
        for value in (None, 3, True, 'R1', {}, {'R1'}, iter(['R1'])):
            with self.assertRaises(ValueError):
                enforce(self.modem, [self.part], value)
            with self.assertRaises(ValueError):
                enforce(self.modem, value, ['R1'])
        for value in (None, 1, [], 'R1'):
            with self.assertRaises(ValueError):
                enforce(value, [self.part], ['R1'])
            with self.assertRaises(ValueError):
                enforce(self.modem, [value], ['R1'])

    def test_extreme_bounds_fail_closed(self):
        self.reject(part={**self.part, 'x': 1e308})
        self.reject(part={**self.part, 'x': 1.7e308, 'width': 1.7e308})

    def test_cli_rejects_missing_malformed_and_duplicate_fields(self):
        script = str(ROOT / 'engineering/modem_clearance.py')
        result = subprocess.run([sys.executable, script], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'placement.json'
            for payload in ('[]', '{}', 'null', '{', '{"modem": {}, "modem": {}}'):
                path.write_text(payload)
                result = subprocess.run([sys.executable, script, str(path)], capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('PLACEMENT BLOCKED', result.stderr)
            path.write_text(json.dumps(dict(modem=self.modem, others=[self.part], expected_refs=['R1'])))
            result = subprocess.run([sys.executable, script, str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIs(json.loads(result.stdout)['manufacturing_release'], False)


if __name__ == '__main__':
    unittest.main()
