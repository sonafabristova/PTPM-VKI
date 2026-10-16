import math


class TriangleCalculator:
    """Класс вычислений: определяет вид треугольника и координаты вершин."""

    def calculate(self, s1, s2, s3):
        """
        Возвращает (тип: str, координаты: list[(int, int)], сообщение_об_ошибке: str).
        Если ошибок нет — сообщение пустое.
        """
        try:
            a, b, c = float(s1), float(s2), float(s3)
        except (ValueError, TypeError):
            return "", [(-2, -2), (-2, -2), (-2, -2)], "Нечисловые данные"

        if a <= 0 or b <= 0 or c <= 0 or a + b <= c or a + c <= b or b + c <= a:
            return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)], "Нарушено неравенство треугольника"

        if math.isclose(a, b) and math.isclose(b, c):
            kind = "равносторонний"
        elif math.isclose(a, b) or math.isclose(b, c) or math.isclose(a, c):
            kind = "равнобедренный"
        else:
            kind = "разносторонний"

        coords = self._calculate_coordinates(a, b, c)
        return kind, coords, ""

    @staticmethod
    def _calculate_coordinates(a, b, c):
        AB, AC, BC = c, b, a
        xC = (AC ** 2 + AB ** 2 - BC ** 2) / (2 * AB)
        yC = math.sqrt(max(AC ** 2 - xC ** 2, 0.0))

        pts = [(0.0, 0.0), (AB, 0.0), (xC, yC)]

        pad, size = 10, 80
        max_x = max(x for x, _ in pts)
        max_y = max(y for _, y in pts)
        scale = min(size / max_x, size / max_y) if max_x and max_y else 1

        return [(int(pad + x * scale), int(100 - pad - y * scale)) for x, y in pts]