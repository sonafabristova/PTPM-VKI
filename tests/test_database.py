import unittest
from src.database import DatabaseRepository


class TestDatabaseRepository(unittest.TestCase):
    def setUp(self):
        # для тестов используем БД в памяти — быстро и не оставляет файлов
        self.repo = DatabaseRepository(":memory:")

    def tearDown(self):
        self.repo.close()

    #  add
    def test_add_success(self):
        self.assertTrue(self.repo.add(1, "alice", "hello"))
        row = self.repo.get_by_id(1)
        self.assertEqual(row["name"], "alice")
        self.assertEqual(row["message"], "hello")

    def test_add_duplicate_id_raises(self):
        self.repo.add(1, "alice", "hello")
        with self.assertRaises(ValueError):
            self.repo.add(1, "bob", "world")

    def test_add_name_too_long_raises(self):
        with self.assertRaises(ValueError):
            self.repo.add(2, "x" * 257, "msg")

    def test_add_message_too_long_raises(self):
        with self.assertRaises(ValueError):
            self.repo.add(3, "bob", "x" * 8097)

    def test_add_wrong_type_raises(self):
        with self.assertRaises(TypeError):
            self.repo.add("1", "alice", "hello")

    #  get_by_id
    def test_get_by_id_exists(self):
        self.repo.add(10, "carol", "hi")
        row = self.repo.get_by_id(10)
        self.assertIsNotNone(row)
        self.assertEqual(row["id"], 10)

    def test_get_by_id_missing_returns_none(self):
        self.assertIsNone(self.repo.get_by_id(999))

    #  get_by_name
    def test_get_by_name_returns_list(self):
        self.repo.add(1, "dave", "one")
        self.repo.add(2, "dave", "two")
        self.repo.add(3, "eve", "three")
        rows = self.repo.get_by_name("dave")
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(r["name"] == "dave" for r in rows))

    def test_get_by_name_missing_returns_empty(self):
        self.assertEqual(self.repo.get_by_name("nobody"), [])

    #  update
    def test_update_success(self):
        self.repo.add(1, "alice", "old")
        self.assertTrue(self.repo.update(1, "new"))
        self.assertEqual(self.repo.get_by_id(1)["message"], "new")

    def test_update_missing_returns_false(self):
        self.assertFalse(self.repo.update(999, "new"))

    def test_update_message_too_long_raises(self):
        self.repo.add(1, "alice", "old")
        with self.assertRaises(ValueError):
            self.repo.update(1, "x" * 8097)

    #  delete
    def test_delete_success(self):
        self.repo.add(1, "alice", "hello")
        self.assertTrue(self.repo.delete(1))
        self.assertIsNone(self.repo.get_by_id(1))

    def test_delete_missing_returns_false(self):
        self.assertFalse(self.repo.delete(999))

    def test_delete_wrong_type_raises(self):
        with self.assertRaises(TypeError):
            self.repo.delete("1")


if __name__ == "__main__":
    unittest.main()