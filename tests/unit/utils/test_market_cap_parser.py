import unittest

from src.utils.market_cap_value_parser import CurrencyValueAdapter


class TestCurrencyValueAdapter(unittest.TestCase):

    def test_convert_trillions(self):
        result = CurrencyValueAdapter.convert("$3.29T")
        expected = {"currency": "USD", "value": 3.29e12}
        self.assertEqual(result, expected)

    def test_convert_billions(self):
        result = CurrencyValueAdapter.convert("€500B")
        expected = {"currency": "EUR", "value": 500e9}
        self.assertEqual(result, expected)

    def test_convert_millions(self):
        result = CurrencyValueAdapter.convert("R$1.5M")
        expected = {"currency": "BRL", "value": 1.5e6}
        self.assertEqual(result, expected)

    def test_convert_thousands(self):
        result = CurrencyValueAdapter.convert("$250K")
        expected = {"currency": "USD", "value": 250e3}
        self.assertEqual(result, expected)

    def test_convert_no_multiplier(self):
        result = CurrencyValueAdapter.convert("€100")
        expected = {"currency": "EUR", "value": 100.0}
        self.assertEqual(result, expected)

    def test_convert_unrecognized_currency(self):
        result = CurrencyValueAdapter.convert(
            "¥500M"
        )
        expected = {"currency": "USD", "value": 500e6}  # Default para 'USD'
        self.assertEqual(result, expected)

    def test_convert_invalid_format(self):
        with self.assertRaises(ValueError):
            CurrencyValueAdapter.convert("invalid_value")

    def test_convert_lower_case_multiplier(self):
        result = CurrencyValueAdapter.convert(
            "$3.29t"
        )
        expected = {"currency": "USD", "value": 3.29e12}
        self.assertEqual(result, expected)

    def test_convert_with_extra_spaces(self):
        result = CurrencyValueAdapter.convert(
            "  $3.29T  "
        )
        expected = {"currency": "USD", "value": 3.29e12}
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
