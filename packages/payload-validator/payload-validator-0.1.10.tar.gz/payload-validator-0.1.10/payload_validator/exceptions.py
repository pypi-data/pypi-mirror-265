from typing import (
    Dict,
    Iterable,
    Union,
)


class ValidationException(Exception):
    def __init__(self):
        super().__init__(self, "Validation failed")


class ValidationNotRunException(Exception):
    pass


class MismatchedErrorKeysException(Exception):
    pass


class InvalidValueError(Exception):
    def __init__(self, error_value_by_key: Dict[str, Union[str, Iterable]], ignore_existing_error_keys: set = None):
        if ignore_existing_error_keys is None:
            ignore_existing_error_keys = set()
        result = [key for key in ignore_existing_error_keys if key not in error_value_by_key.keys()]
        if result:
            raise MismatchedErrorKeysException(
                "In ignore_existing_error_keys {} not in error_value_by_key".format(', '.join(result))
            )
        self.error_value_by_key = error_value_by_key
        self.ignore_existing_error_keys = ignore_existing_error_keys
