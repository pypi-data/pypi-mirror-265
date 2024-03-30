class PayloadComparison(object):
    def __init__(self, _validator: 'PayloadValidator', key):  # noqa: F821
        self._validator = _validator
        self.key = key

    def __gt__(self, value):
        if self.key in self._validator.skip_validate_keys:
            return False
        return self._validator.payload.get(self.key) > value

    def __lt__(self, value):
        if self.key in self._validator.skip_validate_keys:
            return False
        return self._validator.payload.get(self.key) < value

    def __ge__(self, value):
        if self.key in self._validator.skip_validate_keys:
            return False
        return self._validator.payload.get(self.key) >= value

    def __le__(self, value):
        if self.key in self._validator.skip_validate_keys:
            return False
        return self._validator.payload.get(self.key) <= value

    def __eq__(self, value):
        if self.key in self._validator.skip_validate_keys:
            return False
        return self._validator.payload.get(self.key) == value

    def __ne__(self, value):
        if self.key in self._validator.skip_validate_keys:
            return False
        return self._validator.payload.get(self.key) != value

    def __contains__(self, value):
        if self.key in self._validator.skip_validate_keys:
            return False
        return value in self._validator.payload.get(self.key)

    def __bool__(self):
        if self.key in self._validator.skip_validate_keys:
            return False
        return bool(self._validator.payload.get(self.key))

    def __len__(self):
        if self.key in self._validator.skip_validate_keys:
            return 0
        return len(self._validator.payload.get(self.key))

    def __str__(self):
        return f'{self.__class__.__name__}({self._validator.payload.get(self.key)})'

    def __repr__(self):
        return f'{self.__class__.__name__}({self._validator.payload.get(self.key)})'

    @property
    def value(self):
        return self._validator.payload.get(self.key)
