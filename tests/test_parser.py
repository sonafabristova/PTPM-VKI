import unittest
import os
from src.database import DatabaseRepository
from src.parser import ForumParser


FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "fixtures", "quotes_sample.html")


class TestForumParser(unittest.TestCase):
    def setUp(self):
        with open(FIXTURE_PATH, encoding="utf-8") as f:
            self.html = f.read()
        self.parser = ForumParser()

    # ---------- parse_html ----------
    def test_parse_html_returns_all_quotes(self):
        data = self.parser.parse_html(self.html)
        self.assertEqual(len(data), 3)

    def test_parse_html_extracts_fields(self):
        data = self.parser.parse_html(self.html)
        first = data[0]
        self.assertEqual(first["id"], 1)
        self.assertEqual(first["name"], "Albert Einstein")
        self.assertIn("The world as we have created it", first["message"])

    def test_parse_html_preserves_html_in_message(self):
        data = self.parser.parse_html(self.html)
        self.assertIn("<span", data[0]["message"])

    def test_parse_html_fallback_id_when_no_data_id(self):
        html = """
        <div class="quote">
          <span class="text">"Test"</span>
          <small class="author">Tester</small>
        </div>
        """
        data = self.parser.parse_html(html)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], 1)

    def test_parse_html_skips_incomplete_quotes(self):
        html = """
        <div class="quote"><span class="text">"No author"</span></div>
        <div class="quote"><small class="author">No message</small></div>
        """
        data = self.parser.parse_html(html)
        self.assertEqual(data, [])

    # ---------- save_to_db ----------
    def test_save_to_db_saves_all(self):
        repo = DatabaseRepository(":memory:")
        data = self.parser.parse_html(self.html)
        saved = self.parser.save_to_db(data, repo)
        self.assertEqual(saved, 3)
        self.assertIsNotNone(repo.get_by_id(1))
        repo.close()

    def test_save_to_db_skips_duplicates(self):
        repo = DatabaseRepository(":memory:")
        repo.add(1, "existing", "msg")
        data = [{"id": 1, "name": "Albert Einstein", "message": "<span>x</span>"}]
        saved = self.parser.save_to_db(data, repo)
        self.assertEqual(saved, 0)
        repo.close()


if __name__ == "__main__":
    unittest.main()