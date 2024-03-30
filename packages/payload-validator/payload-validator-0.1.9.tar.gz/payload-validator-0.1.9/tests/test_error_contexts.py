import unittest

from payload_validator.error_contexts import (
    NormalValidatorErrorContext,
    ValidatorErrorContext,
)


class TestValidatorErrorContext(unittest.TestCase):
    def test_validator_error_context(self):
        # Given: Create a concrete subclass of ValidatorErrorContext
        class ConcreteValidatorErrorContext(ValidatorErrorContext):
            def add_error(self, field: str, error: str):
                self[field] = error

        # And: Create an instance of the concrete subclass
        context = ConcreteValidatorErrorContext()

        # When: Use the add_error method
        context.add_error("field1", "error1")

        # Then: Check that the error was added correctly
        self.assertEqual(context["field1"], "error1")


class TestNormalValidatorErrorContext(unittest.TestCase):
    def test_normal_validator_error_context(self):
        # Given: Create an instance of NormalValidatorErrorContext
        context = NormalValidatorErrorContext()

        # When: Add an error
        context.add_error("field1", "error1")

        # Then: Check that the error was added correctly
        self.assertEqual(context["field1"], ["error1"])

        # When: Add another error to the same field
        context.add_error("field1", "error2")

        # Then: Check that the new error was appended correctly
        self.assertEqual(context["field1"], ["error1", "error2"])
