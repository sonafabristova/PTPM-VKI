import sqlite3


class DatabaseRepository:
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                message TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def get_by_id(self, comment_id: int):
        cur = self.conn.execute(
            "SELECT id, name, message FROM comments WHERE id = ?",
            (comment_id,),
        )
        row = cur.fetchone()
        if row is None:
            return None
        return {"id": row["id"], "name": row["name"], "message": row["message"]}

    def get_by_name(self, username: str):
        cur = self.conn.execute(
            "SELECT id, name, message FROM comments WHERE name = ?",
            (username,),
        )
        return [
            {"id": r["id"], "name": r["name"], "message": r["message"]}
            for r in cur.fetchall()
        ]

    def add(self, comment_id: int, username: str, message: str) -> bool:
        if not isinstance(comment_id, int):
            raise TypeError("comment_id должен быть int")
        if not isinstance(username, str) or not isinstance(message, str):
            raise TypeError("username и message должны быть str")
        if len(username) > 256:
            raise ValueError("name длиннее 256 символов")
        if len(message) > 8096:
            raise ValueError("message длиннее 8096 символов")

        try:
            self.conn.execute(
                "INSERT INTO comments (id, name, message) VALUES (?, ?, ?)",
                (comment_id, username, message),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            raise ValueError(f"Запись с id={comment_id} уже существует")

    def update(self, comment_id: int, new_message: str) -> bool:
        if not isinstance(comment_id, int):
            raise TypeError("comment_id должен быть int")
        if not isinstance(new_message, str):
            raise TypeError("new_message должен быть str")
        if len(new_message) > 8096:
            raise ValueError("message длиннее 8096 символов")

        cur = self.conn.execute(
            "UPDATE comments SET message = ? WHERE id = ?",
            (new_message, comment_id),
        )
        self.conn.commit()
        return cur.rowcount > 0

    def delete(self, comment_id: int) -> bool:
        if not isinstance(comment_id, int):
            raise TypeError("comment_id должен быть int")
        cur = self.conn.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
        self.conn.commit()
        return cur.rowcount > 0

    def close(self):
        self.conn.close()