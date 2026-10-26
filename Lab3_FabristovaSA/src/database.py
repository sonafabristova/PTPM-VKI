import sqlite3

class Database:
    def __init__(self, db_path=":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS triangles (
                side1 TEXT NOT NULL,
                side2 TEXT NOT NULL,
                side3 TEXT NOT NULL,
                kind TEXT NOT NULL,
                error TEXT NOT NULL DEFAULT '',
                PRIMARY KEY (side1, side2, side3)
            )
        """)
        self.conn.commit()

    def add_record(self, s1, s2, s3, kind, error=""):
        self.conn.execute(
            "INSERT OR REPLACE INTO triangles (side1, side2, side3, kind, error) VALUES (?, ?, ?, ?, ?)",
            (str(s1), str(s2), str(s3), kind, error)
        )
        self.conn.commit()

    def get_record(self, s1, s2, s3):
        cur = self.conn.execute(
            "SELECT kind, error FROM triangles WHERE side1 = ? AND side2 = ? AND side3 = ?",
            (str(s1), str(s2), str(s3))
        )
        row = cur.fetchone()
        return (row["kind"], row["error"]) if row else None

    def delete_record(self, s1, s2, s3):
        cur = self.conn.execute(
            "DELETE FROM triangles WHERE side1 = ? AND side2 = ? AND side3 = ?",
            (str(s1), str(s2), str(s3))
        )
        self.conn.commit()
        return cur.rowcount > 0

    def close(self):
        self.conn.close()