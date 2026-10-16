import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.database import TriangleDatabase


class TestTriangleDatabase(unittest.TestCase):

    def setUp(self):
        # Каждый тест — свежая БД в памяти
        self.db = TriangleDatabase(":memory:")

    def tearDown(self):
        self.db.close()

    def test_add_and_get_returns_stored_record(self):
        """add сохраняет, get возвращает те же данные."""
        self.db.add("3", "4", "5", "разносторонний", "")
        result = self.db.get("3", "4", "5")
        self.assertEqual(result, ("разносторонний", ""))

    def test_get_returns_none_for_missing_record(self):
        """get для несуществующей записи возвращает None."""
        result = self.db.get("10", "20", "30")
        self.assertIsNone(result)

    def test_delete_removes_record(self):
        """delete удаляет запись и возвращает True; повторный delete → False."""
        self.db.add("3", "4", "5", "разносторонний", "")
        self.assertTrue(self.db.delete("3", "4", "5"))
        self.assertIsNone(self.db.get("3", "4", "5"))
        self.assertFalse(self.db.delete("3", "4", "5"))


if __name__ == "__main__":
    unittest.main()