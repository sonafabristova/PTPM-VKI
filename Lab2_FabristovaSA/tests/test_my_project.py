import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.my_project import triangle_info, calculate_coordinates


class TestTriangleInfo(unittest.TestCase):

    # --- Равносторонний ---
    def test_equilateral_triangle_sides_3_3_3(self):
        kind, coords = triangle_info("3", "3", "3")
        self.assertEqual(kind, "равносторонний")

    def test_equilateral_triangle_sides_5_5_5(self):
        kind, _ = triangle_info("5", "5", "5")
        self.assertEqual(kind, "равносторонний")

    def test_equilateral_triangle_float_values(self):
        kind, _ = triangle_info("2.5", "2.5", "2.5")
        self.assertEqual(kind, "равносторонний")

    # --- Равнобедренный ---
    def test_isosceles_triangle_ab_equal(self):
        kind, _ = triangle_info("3", "3", "5")
        self.assertEqual(kind, "равнобедренный")

    def test_isosceles_triangle_bc_equal(self):
        kind, _ = triangle_info("5", "3", "3")
        self.assertEqual(kind, "равнобедренный")

    def test_isosceles_triangle_ac_equal(self):
        kind, _ = triangle_info("3", "5", "3")
        self.assertEqual(kind, "равнобедренный")

    # --- Разносторонний ---
    def test_scalene_triangle_3_4_5(self):
        kind, _ = triangle_info("3", "4", "5")
        self.assertEqual(kind, "разносторонний")

    def test_scalene_triangle_10_12_15(self):
        kind, _ = triangle_info("10", "12", "15")
        self.assertEqual(kind, "разносторонний")

    # --- Не треугольник ---
    def test_not_triangle_sum_too_small(self):
        kind, coords = triangle_info("1", "2", "10")
        self.assertEqual(kind, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_not_triangle_zero_side(self):
        kind, coords = triangle_info("0", "2", "3")
        self.assertEqual(kind, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_not_triangle_negative_side(self):
        kind, coords = triangle_info("-1", "2", "3")
        self.assertEqual(kind, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_not_triangle_equal_sum_and_side(self):
        kind, _ = triangle_info("1", "2", "3")
        self.assertEqual(kind, "не треугольник")

    # --- Нечисловые данные ---
    def test_non_numeric_first_string(self):
        kind, coords = triangle_info("abc", "4", "5")
        self.assertEqual(kind, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_non_numeric_all_strings(self):
        kind, coords = triangle_info("a", "b", "c")
        self.assertEqual(kind, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_non_numeric_empty_string(self):
        kind, coords = triangle_info("", "4", "5")
        self.assertEqual(kind, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_non_numeric_second_string(self):
        kind, coords = triangle_info("3", "xyz", "5")
        self.assertEqual(kind, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    # --- Координаты: в поле 100x100 ---
    def test_coordinates_within_field(self):
        _, coords = triangle_info("3", "4", "5")
        for x, y in coords:
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x, 100)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(y, 100)

    def test_coordinates_are_int_tuples(self):
        _, coords = triangle_info("3", "4", "5")
        self.assertEqual(len(coords), 3)
        for point in coords:
            self.assertIsInstance(point, tuple)
            self.assertEqual(len(point), 2)
            self.assertIsInstance(point[0], int)
            self.assertIsInstance(point[1], int)

    def test_equilateral_triangle_coordinates_symmetric(self):
        _, coords = triangle_info("5", "5", "5")
        # A и B на одной горизонтали
        self.assertEqual(coords[0][1], coords[1][1])

    # --- Пограничные длины ---
    def test_very_small_sides(self):
        kind, _ = triangle_info("0.1", "0.1", "0.1")
        self.assertEqual(kind, "равносторонний")

    def test_very_large_sides(self):
        kind, _ = triangle_info("1000", "1000", "1000")
        self.assertEqual(kind, "равносторонний")

    def test_large_scalene_triangle(self):
        kind, _ = triangle_info("100", "200", "250")
        self.assertEqual(kind, "разносторонний")

    # --- calculate_coordinates напрямую ---
    def test_calculate_coordinates_returns_three_points(self):
        coords = calculate_coordinates(3, 4, 5)
        self.assertEqual(len(coords), 3)

    def test_calculate_coordinates_a_at_bottom_left(self):
        coords = calculate_coordinates(3, 4, 5)
        # A всегда в (10, 90) — левый нижний угол полезной области
        self.assertEqual(coords[0], (10, 90))

    def test_calculate_coordinates_all_inside_100x100(self):
        coords = calculate_coordinates(3, 4, 5)
        for x, y in coords:
            self.assertTrue(0 <= x <= 100)
            self.assertTrue(0 <= y <= 100)


if __name__ == "__main__":
    unittest.main()