import unittest
from LeetCodeTools import sum_two_integers


class TestSumTwoIntegers(unittest.TestCase):

    def test_positive_numbers(self):
        self.assertEqual(sum_two_integers(5, 7), 12)

    def test_negative_numbers(self):
        self.assertEqual(sum_two_integers(-3, -8), -11)

    def test_mixed_numbers(self):
        self.assertEqual(sum_two_integers(-10, 5), -5)

    def test_zero(self):
        self.assertEqual(sum_two_integers(0, 0), 0)

    def test_large_numbers(self):
        self.assertEqual(sum_two_integers(1000000, 9999999), 10999999)


if __name__ == "__main__":
    unittest.main()
