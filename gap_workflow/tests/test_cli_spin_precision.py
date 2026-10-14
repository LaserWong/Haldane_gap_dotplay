import unittest
from gapflow.workflow import load_request


class CliSpinPrecisionTests(unittest.TestCase):
    def test_unrepresentable_half_spin_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'not exactly representable'):
            load_request('{"model":{"spin":9007199254740992.5}}')

    def test_large_integral_decimal_is_kept_exact(self):
        parsed = load_request('{"model":{"spin":9007199254740993.0}}')
        self.assertEqual(parsed['model']['spin'], 9007199254740993)
        self.assertIs(type(parsed['model']['spin']), int)

    def test_nonhalf_decimal_is_not_rounded(self):
        with self.assertRaisesRegex(ValueError, 'exact positive integer or half-integer'):
            load_request('{"model":{"spin":0.500000000000000000000000000001}}')


if __name__ == '__main__':
    unittest.main()
