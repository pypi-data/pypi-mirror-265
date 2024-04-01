import unittest
from calculator import add, subtract, multiply, divide, gcd, decimal_to_percent, calculate_percentage, round_up, bmi, rounded_bmi

class TestMathFunctions(unittest.TestCase):

    def test_add(self):
        self.assertEqual(add(1, 2), 3)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(0, 0), 0)

    def test_subtract(self):
        self.assertEqual(subtract(3, 2), 1)
        self.assertEqual(subtract(5, -2), 7)
        self.assertEqual(subtract(0, 0), 0)

    def test_multiply(self):
        self.assertEqual(multiply(3, 2), 6)
        self.assertEqual(multiply(-1, 1), -1)
        self.assertEqual(multiply(0, 5), 0)

    def test_divide(self):
        self.assertAlmostEqual(divide(5, 2), 2.5)
        self.assertAlmostEqual(divide(-6, 2), -3)
        self.assertRaises(ValueError, divide, 5, 0)

    def test_gcd(self):
        self.assertEqual(gcd([12, 18, 24]), 6)
        self.assertEqual(gcd([5, 10, 15]), 5)

    def test_decimal_to_percent(self):
        self.assertEqual(decimal_to_percent(0.5), 50)
        self.assertEqual(decimal_to_percent(0.25), 25)

    def test_calculate_percentage(self):
        self.assertEqual(calculate_percentage(2, 4), 50)
        self.assertEqual(calculate_percentage(75, 100), 75)

    def test_round_up(self):
        self.assertEqual(round_up(3.4), 3)
        self.assertEqual(round_up(6.7), 7)

    def test_bmi(self):
        self.assertAlmostEqual(bmi(70, 180), 21.6, places=1)
        self.assertAlmostEqual(bmi(90, 170), 31.1, places=1)

    def test_rounded_bmi(self):
        self.assertEqual(rounded_bmi(70, 180), 22)
        self.assertEqual(rounded_bmi(90, 170), 31)

if __name__ == '__main__':
    unittest.main()
