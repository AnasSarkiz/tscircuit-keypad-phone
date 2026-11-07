import math
import unittest
from battery_necessary_power import HOST_INPUT_W, LIGHT_INPUT_W, MODEM_W, required_efficiency, run


class NecessaryPowerTests(unittest.TestCase):
    def test_cylindrical_pack_3v3_rejects_sustained_allocation_even_ideally(self):
        self.assertIsNone(required_efficiency(3.3, 2.6, HOST_INPUT_W + LIGHT_INPUT_W))

    def test_cylindrical_pack_3v6_needs_over_94_percent_efficiency(self):
        required = required_efficiency(3.6, 2.6, HOST_INPUT_W + LIGHT_INPUT_W)
        self.assertIsNotNone(required)
        self.assertGreater(required, 0.94)
        self.assertLess(required, 1.0)
        self.assertAlmostEqual(required * (3.6 * 2.6 - HOST_INPUT_W - LIGHT_INPUT_W), MODEM_W)

    def test_ph_2a_path_fails_illuminated_allocation_at_4v2_even_ideally(self):
        self.assertIsNone(required_efficiency(4.2, 2.0, HOST_INPUT_W + LIGHT_INPUT_W))

    def test_ph_2a_path_needs_over_95_percent_without_light_at_4v2(self):
        self.assertGreater(required_efficiency(4.2, 2.0, HOST_INPUT_W), 0.95)

    def test_no_loss_boundary_is_not_rejected_as_impossible(self):
        self.assertTrue(math.isclose(required_efficiency(MODEM_W + HOST_INPUT_W, 1, HOST_INPUT_W), 1.0))

    def test_voltage_and_current_only_make_required_efficiency_less(self):
        self.assertLess(required_efficiency(3.8, 3.6, HOST_INPUT_W), required_efficiency(3.6, 3.6, HOST_INPUT_W))
        self.assertLess(required_efficiency(3.6, 4.0, HOST_INPUT_W), required_efficiency(3.6, 3.6, HOST_INPUT_W))

    def test_invalid_input_is_rejected(self):
        for args in ((math.nan, 1, 0), (3.6, math.inf, 0), (0, 1, 0), (3.6, 1, -1)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                required_efficiency(*args)

    def test_never_qualifies_a_pack(self):
        report = run()
        self.assertEqual(len(report['rows']), 50)
        self.assertFalse(report['pack_or_hardware_approved'])
        self.assertTrue(all(row['necessary_condition'] != 'pass' for row in report['rows']))


if __name__ == '__main__':
    unittest.main()
