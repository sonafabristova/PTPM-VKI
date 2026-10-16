import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.calculator import TriangleCalculator


class TestTriangleCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = TriangleCalculator()

    def test_calculate_returns_three_values_for_valid_triangle(self):
        """calculate возвращает (kind, coords, error) — три значения."""
        result = self.calc.calculate("3", "4", "5")
        self.assertEqual(len(result), 3)

        kind, coords, error = result
        self.assertEqual(kind, "разносторонний")
        self.assertEqual(len(coords), 3)
        self.assertEqual(error, "")

    def test_calculate_returns_error_message_for_non_numeric(self):
        """При нечисловых данных error заполнен, kind пустой."""
        kind, coords, error = self.calc.calculate("abc", "4", "5")
        self.assertEqual(kind, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])
        self.assertEqual(error, "Нечисловые данные")


if __name__ == "__main__":
    unittest.main()