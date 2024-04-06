# encoding: utf-8
import pytest
from randomgen.histogram import Histogram
from randomgen.errors import *

versions = [Histogram, ]


# #############################################################################
@pytest.fixture(scope="class")
def histogram(request):
    if hasattr(request, 'param'):
        return request.param()
    return Histogram()  # Default version if none specified


###############################################################################

@pytest.mark.parametrize("histogram", versions, indirect=True)
class TestHistogramParamNumbers(object):
    """ Test the `numbers` parameter. """

    def test_none(self, histogram):
        """ Test the `numbers` parameter with None."""

        with pytest.raises(RandomGenTypeError):
            histogram.set_numbers(None)
            histogram.validate_numbers()

    def test_empty(self, histogram):
        """ Test the `numbers` parameter with an empty list."""

        with pytest.raises(RandomGenEmptyError):
            histogram.set_numbers([])
            histogram.validate_numbers()

    def test_int(self, histogram):
        """ Test the `numbers` parameter with an integer."""

        with pytest.raises(RandomGenTypeError):
            histogram.set_numbers(123)
            histogram.validate_numbers()

    def test_int_list(self, histogram):
        """ Test the `numbers` parameter with an integer list."""

        histogram.set_numbers([-1, 0, 1, 2, 3])
        histogram.validate_numbers()
        assert histogram._numbers == [-1, 0, 1, 2, 3]

    def test_int_tuple(self, histogram):
        """ Test the `numbers` parameter with an integer tuple."""

        histogram.set_numbers((-1, 0, 1, 2, 3))
        histogram.validate_numbers()
        assert histogram._numbers == (-1, 0, 1, 2, 3)

    def test_int_set(self, histogram):
        """ Test the `numbers` parameter with an integer set."""

        histogram.set_numbers({-1, 0, 1, 2, 3})
        histogram.validate_numbers()
        assert histogram._numbers == {-1, 0, 1, 2, 3}

    def test_float(self, histogram):
        """ Test the `numbers` parameter with a float."""

        with pytest.raises(RandomGenTypeError):
            histogram.set_numbers(123.45)
            histogram.validate_numbers()

    def test_float_list(self, histogram):
        """ Test the `numbers` parameter with a float list."""

        histogram.set_numbers([-1.0, 0.0, 1.0, 2.0, 3.0])
        histogram.validate_numbers()
        assert histogram._numbers == [-1.0, 0.0, 1.0, 2.0, 3.0]

    def test_float_tuple(self, histogram):
        """ Test the `numbers` parameter with a float tuple."""

        histogram.set_numbers((-1.0, 0.0, 1.0, 2.0, 3.0))
        histogram.validate_numbers()
        assert histogram._numbers == (-1.0, 0.0, 1.0, 2.0, 3.0)

    def test_float_set(self, histogram):
        """ Test the `numbers` parameter with a float set."""

        histogram.set_numbers({-1.0, 0.0, 1.0, 2.0, 3.0})
        histogram.validate_numbers()
        assert histogram._numbers == {-1.0, 0.0, 1.0, 2.0, 3.0}

    def test_string(self, histogram):
        """ Test the `numbers` parameter with a string."""

        with pytest.raises(RandomGenTypeError):
            histogram.set_numbers("123")
            histogram.validate_numbers()

    def test_string_list(self, histogram):
        """ Test the `numbers` parameter with a string list."""

        with pytest.raises(RandomGenTypeError):
            histogram.set_numbers(["-1", "0", "1", "2", "3"])
            histogram.validate_numbers()

    def test_dict(self, histogram):
        """ Test the `numbers` parameter with a dictionary."""

        with pytest.raises(RandomGenTypeError):
            histogram.set_numbers({-1: 1, 0: 1, 1: 1, 2: 1, 3: 1})
            histogram.validate_numbers()

    def test__mixed_types(self, histogram):
        """ Test the `numbers` parameter with mixed types."""

        with pytest.raises(RandomGenTypeError):
            histogram.set_numbers([-1, 0.0, "1", 2.0, 3])
            histogram.validate_numbers()

    def test__mixed_numbers(self, histogram):
        """ Test the `numbers` parameter with mixed numbers."""

        histogram.set_numbers([-1, 0, 1, 2.0, 3])
        histogram.validate_numbers()
        assert histogram._numbers == [-1, 0, 1, 2.0, 3]


@pytest.mark.parametrize("histogram", versions, indirect=True)
class TestHistogramFunctional(object):
    """ Test the functional aspects of the `Histogram` class. """

    def test_from_dict(self, histogram):
        """ Test the `from_dict` method. """

        histogram.from_dict({-1: 0.01, 0: 0.3, 1: 0.58, 2: 0.1, 3: 0.01})
        assert list(histogram.keys()) == [-1, 0, 1, 2, 3]
        assert list(histogram.values()) == [0.01, 0.3, 0.58, 0.1, 0.01]

    def test_calc(self, histogram):
        """ Test the `calc` method. """

        histogram.set_numbers([-1, -1, 0, 0, 1, 1,  2, 2, 3, 3])
        histogram.calc()
        assert list(histogram.keys()) == [-1, 0, 1, 2, 3]
        assert list(histogram.values()) == [0.2, 0.2, 0.2, 0.2, 0.2]


if __name__ == "__main__":
    pytest.main()
