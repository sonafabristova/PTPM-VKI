import unittest
import sys
import os
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.calculator import TriangleCalculator
from src.database import TriangleDatabase
from src.user_input import ConsoleUserInput
from src.notifier import EmailNotifier
from src.controller import TriangleController


class TestTriangleControllerIntegration(unittest.TestCase):

    def setUp(self):
        self.db = TriangleDatabase(":memory:")
        self.notifier = EmailNotifier()

    def tearDown(self):
        self.db.close()

    @patch("builtins.input", side_effect=["3", "4", "5"])
    def test_process_full_scenario_with_mocked_input(self, mock_input):
        """
        ИНТЕГРАЦИОННЫЙ тест: input имитируется, Controller проходит
        весь сценарий — запрос, вычисление, сохранение, отправка.
        """
        controller = TriangleController(
            calculator=TriangleCalculator(),
            database=self.db,
            user_input=ConsoleUserInput(),
            notifier=self.notifier,
        )

        kind, coords, error = controller.process()

        self.assertEqual(kind, "разносторонний")
        self.assertEqual(len(coords), 3)
        self.assertEqual(error, "")
        # Запись должна оказаться в БД
        self.assertEqual(self.db.get("3", "4", "5"), ("разносторонний", ""))
        # input вызван 3 раза (по одному на каждую сторону)
        self.assertEqual(mock_input.call_count, 3)

    @patch("builtins.input", side_effect=["3", "4", "5", "3", "4", "5"])
    def test_process_uses_cache_on_second_call(self, mock_input):
        """
        ИНТЕГРАЦИОННЫЙ тест: при повторном запросе с теми же сторонами
        calculator.calculate НЕ вызывается — результат берётся из БД.
        """
        mock_calculator = MagicMock(wraps=TriangleCalculator())
        controller = TriangleController(
            calculator=mock_calculator,
            database=self.db,
            user_input=ConsoleUserInput(),
            notifier=self.notifier,
        )

        # Первый вызов — вычисление + сохранение
        kind1, _, _ = controller.process()
        self.assertEqual(kind1, "разносторонний")
        self.assertEqual(mock_calculator.calculate.call_count, 1)

        # Второй вызов с теми же сторонами — должен взять из БД
        kind2, _, _ = controller.process()
        self.assertEqual(kind2, "разносторонний")
        # calculate вызван по-прежнему 1 раз (второй раз — из БД)
        self.assertEqual(mock_calculator.calculate.call_count, 1)

    @patch("builtins.input", side_effect=["3", "4", "5"])
    def test_process_calls_notifier_exactly_once(self, mock_input):
        """
        ИНТЕГРАЦИОННЫЙ тест: notifier.send вызывается ровно один раз
        с корректным сообщением.
        """
        mock_notifier = MagicMock()
        controller = TriangleController(
            calculator=TriangleCalculator(),
            database=self.db,
            user_input=ConsoleUserInput(),
            notifier=mock_notifier,
        )

        controller.process()

        self.assertEqual(mock_notifier.send.call_count, 1)
        sent_message = mock_notifier.send.call_args[0][0]
        self.assertIn("разносторонний", sent_message)
        self.assertIn("3", sent_message)
        self.assertIn("4", sent_message)
        self.assertIn("5", sent_message)


if __name__ == "__main__":
    unittest.main()