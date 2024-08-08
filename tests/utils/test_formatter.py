from datetime import datetime
from unittest import TestCase

from src.utils.formatter import Formatter, fmt


class TestFormatter(TestCase):
    def setUp(self):
        self.formatter = Formatter()

    def test_bytes_to_str(self):
        test_bytes = b'{"key": "value"}'
        expected_result = {"key": "value"}
        self.assertEqual(self.formatter.bytes_to_str(test_bytes), expected_result)

    def test_datetime_to_isoformat(self):
        test_datetime = datetime(2023, 10, 26, 12, 0, 0)
        expected_result = "2023-10-26T12:00:00Z"
        self.assertEqual(
            self.formatter.datetime_to_isoformat(test_datetime), expected_result
        )

    def test_str_to_bytes(self):
        test_dict = {"key": "value"}
        expected_result = b'{"key": "value"}'
        self.assertEqual(self.formatter.str_to_bytes(test_dict), expected_result)

    def test_camel_to_snake(self):
        test_camel_case = "camelCaseKey"
        expected_result = "camel_case_key"
        self.assertEqual(
            self.formatter.camel_to_snake(test_camel_case), expected_result
        )

    def test_snake_to_camel(self):
        test_snake_case = "snake_case_key"
        expected_result = "snakeCaseKey"
        self.assertEqual(
            self.formatter.snake_to_camel(test_snake_case), expected_result
        )

    def test_fmt_instance(self):
        self.assertIsInstance(fmt, Formatter)
