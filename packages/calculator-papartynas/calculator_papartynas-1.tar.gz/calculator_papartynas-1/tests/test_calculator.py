import unittest

from src.calculator_papartynas.calculator import Calculator


class CalculatorTestCase(unittest.TestCase):

    def setUp(self):
        self.calculator = Calculator()

    def test_add(self):
        for first_addend, second_addend, expected_result in [(0, 0, 0), (2, -1, 1), (-1, -1, -2), (.5, .5, 1)]:
            with self.subTest(equation=f"{first_addend} + {second_addend} = {expected_result}"):
                self.assertAlmostEqual(
                    expected_result,
                    self.calculator.reset_memory().add(first_addend).add(second_addend).result
                )

    def test_subtract(self):
        for minuend, subtrahend, expected_result in [(0, 0, 0), (1, -1, 2), (-9, -6, -3), (.7, .6, .1)]:
            with self.subTest(equation=f"{minuend} - {subtrahend} = {expected_result}"):
                self.assertAlmostEqual(
                    expected_result,
                    self.calculator.reset_memory().add(minuend).subtract(subtrahend).result
                )

    def test_multiply_by(self):
        for first_factor, second_factor, expected_result in [(0, 0, 0), (4, -1, -4), (-2, -4, 8), (10, .3, 3)]:
            with self.subTest(equation=f"{first_factor} × {second_factor} = {expected_result}"):
                self.assertAlmostEqual(
                    expected_result,
                    self.calculator.reset_memory().add(first_factor).multiply_by(second_factor).result
                )

    def test_divide_by_raises_exception_when_divisor_is_0(self):
        with self.assertRaises(ValueError) as context_manager:
            self.calculator.divide_by(0)
        self.assertEqual("Division by 0 is undefined", str(context_manager.exception))

    def test_divide_by(self):
        for dividend, divisor, expected_result in [(0, 1, 0), (5, -5, -1), (-12, -4, 3), (.8, .2, 4)]:
            with self.subTest(equation=f"{dividend} / {divisor} = {expected_result}"):
                self.assertAlmostEqual(
                    expected_result,
                    self.calculator.reset_memory().add(dividend).divide_by(divisor).result
                )

    def test_take_nth_root_raises_exception_when_index_is_0(self):
        with self.assertRaises(ValueError) as context_manager:
            self.calculator.take_nth_root(0)
        self.assertEqual("0th root is undefined", str(context_manager.exception))

    def test_take_nth_root(self):
        for radicand, index, expected_result in [(0, 2, 0), (4, -2, .5), (-8, 3, -2), (.5, .5, .25)]:
            with self.subTest(equation=f"{radicand} ^ {1.0 / index} = {expected_result}"):
                self.assertAlmostEqual(
                    expected_result,
                    self.calculator.reset_memory().add(radicand).take_nth_root(index).result
                )

    def test_reset_memory(self):
        self.assertAlmostEqual(
            2.0,
            self.calculator.add(3).subtract(1).multiply_by(4).divide_by(2).take_nth_root(2).result
        )
        self.assertAlmostEqual(0.0, self.calculator.reset_memory().result)

    def test___str__(self):
        self.assertEqual(
            str(self.calculator.add(1).multiply_by(4).divide_by(2).subtract(1).take_nth_root(.5).take_nth_root(.25)),
            "((0 + 1) × 4 / 2 - 1) ^ 2.0 ^ 4.0 = 1.0"
        )


if __name__ == '__main__':
    unittest.main()
