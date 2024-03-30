import unittest

from payload_validator.comparisons import PayloadComparison
from payload_validator.validators import PayloadValidator


class TestPayloadComparison(unittest.TestCase):
    def test_payload_comparison_with_payload_and_skip_validate_keys_exists(self):
        # Given: Create a PayloadValidator with payload
        payload = {"key": "value"}
        validator = PayloadValidator(payload)
        # And: Add skip_validate_keys
        validator.skip_validate_keys.add("key")

        # When: Create a PayloadComparison existing key
        comparison = PayloadComparison(validator, "key")

        # Then: Perform various comparisons as False
        self.assertEqual(comparison > 5, False)
        self.assertEqual(comparison < 15, False)
        self.assertEqual(comparison >= 10, False)
        self.assertEqual(comparison <= 10, False)
        self.assertEqual(comparison == 10, False)
        self.assertEqual(comparison != 5, False)
        self.assertEqual(len(comparison), 0)
        self.assertEqual(bool(comparison), False)
        self.assertEqual("value" in comparison, False)
        self.assertEqual(str(comparison), f"PayloadComparison({payload['key']})")
        self.assertEqual(repr(comparison), f"PayloadComparison({payload['key']})")
        self.assertEqual(comparison.value, payload["key"])

    def test_payload_comparison_with_payload_and_skip_validate_keys_not_exists_and_value_is_int(self):
        # Given: Create a PayloadValidator with payload
        payload = {"key": 10}
        validator = PayloadValidator(payload)

        # When: Create a PayloadComparison existing key
        comparison = PayloadComparison(validator, "key")

        # Then: Perform various comparisons as False
        self.assertEqual(comparison > 5, True)
        self.assertEqual(comparison < 15, True)
        self.assertEqual(comparison >= 10, True)
        self.assertEqual(comparison <= 10, True)
        self.assertEqual(comparison == 10, True)
        self.assertEqual(comparison != 5, True)
        self.assertEqual(bool(comparison), True)
        self.assertEqual(str(comparison), f"PayloadComparison({payload['key']})")
        self.assertEqual(repr(comparison), f"PayloadComparison({payload['key']})")

    def test_payload_comparison_with_payload_and_skip_validate_keys_not_exists_and_value_is_iter(self):
        # Given: Create a PayloadValidator with payload
        payload = {"key": [1, 2, 3]}
        validator = PayloadValidator(payload)

        # When: Create a PayloadComparison existing key
        comparison = PayloadComparison(validator, "key")

        # Then: Perform various comparisons as False
        self.assertEqual(bool(comparison), True)
        self.assertEqual(len(comparison), 3)
        self.assertEqual(1 in comparison, True)
        self.assertEqual(4 in comparison, False)
        self.assertEqual(str(comparison), f"PayloadComparison({payload['key']})")
        self.assertEqual(repr(comparison), f"PayloadComparison({payload['key']})")
