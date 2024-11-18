import unittest
from calculator import Calculator


class TestCalculator(unittest.TestCase):

    def test_add(self):
        self.assertEqual(Calculator.add(3, 2), 5)
        self.assertEqual(Calculator.add(-1, 1), 0)

    def test_subtract(self):
        self.assertEqual(Calculator.subtract(10, 5), 5)
        self.assertEqual(Calculator.subtract(-1, -1), 0)

    def test_multiply(self):
        self.assertEqual(Calculator.multiply(2, 5), 10)
        self.assertEqual(Calculator.multiply(0, 5), 0)

    def test_divide(self):
        self.assertEqual(Calculator.divide(10, 2), 5)
        self.assertEqual(Calculator.divide(9, 3), 3)


        with self.assertRaises(ValueError):
            Calculator.divide(10, 0)


if __name__ == '__main__':
    unittest.main()
