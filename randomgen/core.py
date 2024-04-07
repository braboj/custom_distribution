# encoding: utf-8

from randomgen.errors import (
    RandomGenMismatchError,
    RandomGenProbabilitySumError,
    RandomGenEmptyError,
    RandomGenTypeError,
)

import random
from abc import ABCMeta, abstractmethod


class RandomGenABC(metaclass=ABCMeta):
    """Abstract base class for random number generators.

    Attributes:
        _numbers: A list of numbers.
        _probabilities: A list of probabilities.
        _cumulative_probabilities: A list of cumulative probabilities.

    """

    def __init__(self):
        self._numbers = ()
        self._probabilities = ()
        self._cumulative_probabilities = []

    def __str__(self):
        return f"Numbers: {self._numbers}, Probabilities: {self._probabilities}"

    def from_dict(self, dict_obj):
        """Set the numbers and probabilities from a dictionary.

        Args:
            dict_obj: A dictionary of numbers and probabilities.

        Returns:
            self: The instance of the class.

        """

        self._numbers = dict_obj.keys
        self._probabilities = dict_obj.values

        return self

    def to_dict(self):
        """Return the numbers and probabilities as a dictionary.

        Returns:
            A dictionary of numbers and respective probabilities.

        """

        return dict(zip(self._numbers, self._probabilities))

    def set_numbers(self, values):
        """Set the numbers (similar to the categories in a histogram).

        Args:
            values: A list of numbers.

        Returns:
            self: The instance of the class.

        """

        self._numbers = values
        return self

    def validate_numbers(self):
        """Validate the numbers.

        Returns:
            self: The instance of the class.

        """

        # Check if the numbers is None
        if self._numbers is None:
            raise RandomGenTypeError()

        # Check if the numbers are iterable
        elif not hasattr(self._numbers, '__iter__'):
            raise RandomGenTypeError()

        # Check if dictionary
        elif isinstance(self._numbers, dict):
            raise RandomGenTypeError()

        # Check if any member is not a number
        elif not all(isinstance(num, (int, float)) for num in self._numbers):
            raise RandomGenTypeError()

        # Check if the number list is empty
        elif not self._numbers:
            raise RandomGenEmptyError()

        return self

    def set_probabilities(self, values):
        """ Set the probabilities.

        Args:
            values: A list of probabilities.

        Returns:
            self: The instance of the class.

        """

        self._probabilities = values
        return self

    def validate_probabilities(self):
        """ Validate the probabilities.

        Returns:
            self: The instance of the class.

        """

        # Check if the probabilities is None
        if self._probabilities is None:
            raise RandomGenTypeError()

        # Check if the numbers are iterable
        elif not hasattr(self._probabilities, '__iter__'):
            raise RandomGenTypeError()

        # Check if empty
        elif not self._probabilities:
            raise RandomGenEmptyError()

        # Check if set
        elif isinstance(self._probabilities, set):
            raise RandomGenTypeError()

        # Check if dictionary
        elif isinstance(self._probabilities, dict):
            raise RandomGenTypeError()

        # Check if any member is not a number
        elif not all(
                isinstance(prob, (int, float)) for prob in self._probabilities):
            raise RandomGenTypeError()

        # Check if the probabilities are non-negative
        elif any(probability < 0 for probability in self._probabilities):
            raise RandomGenTypeError()

        # Check if the probabilities sum to 1
        elif round(sum(self._probabilities), 3) != 1:
            raise RandomGenProbabilitySumError()

        return self

    def calc_cdf(self):
        """ Calculate the cumulative probabilities.

        Returns:
            self: The instance of the class.

        """

        self._cumulative_probabilities = [
            sum(self._probabilities[:i + 1])
            for i in
            range(len(self._probabilities))
        ]

    def validate(self):
        """ Validate all the attributes of the class.

        Returns:
            self: The instance of the class.

        """

        # Validate the numbers and probabilities
        self.validate_numbers()
        self.validate_probabilities()

        # Check if the numbers and probabilities' lists have the same length
        if len(self._numbers) != len(self._probabilities):
            raise RandomGenMismatchError()

        # After the validation calculate the cumulative probabilities
        self.calc_cdf()

        return self

    def generate(self, amount):
        """ Generate random numbers based on the probabilities.

        Args:
            amount: The number of random numbers to generate.

        Returns:
            A list of random numbers.

        """

        return [self.next_num() for _ in range(amount)]

    @abstractmethod
    def next_num(self):
        """ Abstract method to generate the next random number.

        Returns:
            A random number.

        """
        raise NotImplementedError


class RandomGenV1(RandomGenABC):

    def next_num(self):
        rand = random.random()
        for i, cum_prob in enumerate(self._cumulative_probabilities):
            if rand <= cum_prob:
                return self._numbers[i]


class RandomGenV2(RandomGenABC):

    def next_num(self):
        # Use random.choices to select a number based on the probabilities
        return random.choices(self._numbers, self._probabilities, k=1)[0]


################################################################################
# Example
################################################################################

if __name__ == "__main__":

    from randomgen.histogram import Histogram

    rg = (
        RandomGenV1()
        .set_numbers([1, 2, 3])
        .set_probabilities([0.2, 0.2, 0.6])
        .validate()
    )

    random_numbers = rg.generate(10000)

    observed = (
        Histogram()
        .set_numbers(random_numbers)
        .calc()
    )

    # Expected distribution
    expected = rg.to_dict()
    print("Expected distribution:", expected)

    # Observed distribution
    print("Observed distribution:", observed)
