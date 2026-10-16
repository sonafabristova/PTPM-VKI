from .calculator import TriangleCalculator
from .database import TriangleDatabase
from .user_input import UserInput
from .notifier import Notifier


class TriangleController:
    """Бизнес-логика сквозного сценария."""

    def __init__(self, calculator: TriangleCalculator, database: TriangleDatabase,
                 user_input: UserInput, notifier: Notifier):
        self.calculator = calculator
        self.database = database
        self.user_input = user_input
        self.notifier = notifier

    def process(self):
        """
        Сценарий:
        1. Запросить стороны.
        2. Если в БД есть — взять оттуда; если нет — вычислить и сохранить.
        3. Отправить результат во внешнюю систему.
        4. Вернуть результат.
        """
        s1, s2, s3 = self.user_input.get_sides()

        cached = self.database.get(s1, s2, s3)

        if cached is not None:
            kind, error = cached
            coords = self.calculator._calculate_coordinates(
                float(s1), float(s2), float(s3)
            ) if kind not in ("", "не треугольник") else (
                [(-2, -2)] * 3 if kind == "" else [(-1, -1)] * 3
            )
        else:
            kind, coords, error = self.calculator.calculate(s1, s2, s3)
            self.database.add(s1, s2, s3, kind, error)

        self.notifier.send(f"Треугольник ({s1}, {s2}, {s3}): {kind}")

        return kind, coords, error