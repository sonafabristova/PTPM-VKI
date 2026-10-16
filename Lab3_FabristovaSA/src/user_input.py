from abc import ABC, abstractmethod


class UserInput(ABC):
    """Интерфейс получения данных от пользователя."""

    @abstractmethod
    def get_sides(self):
        """Вернуть кортеж из трёх строк — стороны треугольника."""
        ...


class ConsoleUserInput(UserInput):
    """Реализация через консоль: input()."""

    def get_sides(self):
        s1 = input("Сторона A: ").strip()
        s2 = input("Сторона B: ").strip()
        s3 = input("Сторона C: ").strip()
        return s1, s2, s3