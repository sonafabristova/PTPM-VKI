import sqlite3


class TriangleDatabase:
    """Класс работы с БД SQLite для хранения результатов по треугольникам."""

    def __init__(self, db_path=":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS triangles (
                side1 REAL NOT NULL,
                side2 REAL NOT NULL,
                side3 REAL NOT NULL,
                kind TEXT NOT NULL,
                error TEXT NOT NULL DEFAULT '',
                PRIMARY KEY (side1, side2, side3)
            )
        """)
        self.conn.commit()

    def add(self, s1, s2, s3, kind, error=""):
        """Добавить запись. Если такая уже есть — обновить."""
        self.conn.execute("""
            INSERT OR REPLACE INTO triangles (side1, side2, side3, kind, error)
            VALUES (?, ?, ?, ?, ?)
        """, (float(s1), float(s2), float(s3), kind, error))
        self.conn.commit()

    def get(self, s1, s2, s3):
        """Вернуть (kind, error) или None, если записи нет."""
        cur = self.conn.execute("""
            SELECT kind, error FROM triangles
            WHERE side1 = ? AND side2 = ? AND side3 = ?
        """, (float(s1), float(s2), float(s3)))
        row = cur.fetchone()
        return (row["kind"], row["error"]) if row else None

    def delete(self, s1, s2, s3):
        """Удалить запись. Вернуть True, если что-то удалилось."""
        cur = self.conn.execute("""
            DELETE FROM triangles
            WHERE side1 = ? AND side2 = ? AND side3 = ?
        """, (float(s1), float(s2), float(s3)))
        self.conn.commit()
        return cur.rowcount > 0

    def close(self):
        self.conn.close()