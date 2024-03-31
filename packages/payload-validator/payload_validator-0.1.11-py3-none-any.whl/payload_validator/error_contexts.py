from abc import (
    ABC,
    abstractmethod,
)


class ValidatorErrorContext(ABC, dict):
    @abstractmethod
    def add_error(self, field: str, error: str):
        pass


class NormalValidatorErrorContext(ValidatorErrorContext):
    def add_error(self, field: str, error: str):
        value = self.setdefault(field, [])
        value.append(error)
