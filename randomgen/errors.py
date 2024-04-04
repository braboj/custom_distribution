class RandomGenError(Exception):

    def __init__(self, message):
        super().__init__(message)

    @classmethod
    def set_message(cls, message):
        cls.message = message


class RandomGenTypeError(RandomGenError):
    MESSAGE = "The numbers and probabilities must be a list of numbers."

    def __init__(self):
        super().__init__(message=self.MESSAGE)


class RandomGenEmptyError(RandomGenError):
    MESSAGE = "The numbers and probabilities lists must not be empty."

    def __init__(self):
        super().__init__(message=self.MESSAGE)


class RandomGenMismatchError(RandomGenError):
    MESSAGE = "The numbers and probabilities lists must have the same length."

    def __init__(self):
        super().__init__(message=self.MESSAGE)


class RandomGenSumError(RandomGenError):
    MESSAGE = "Probabilities must sum to 1."

    def __init__(self):
        super().__init__(message=self.MESSAGE)


class RandomGenNegativeError(RandomGenError):
    MESSAGE = "Probabilities must be non-negative."

    def __init__(self):
        super().__init__(message=self.MESSAGE)
