import sqlite3

class Database:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS homeworks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            group TEXT,
            homework_number INTEGER,
            github_link TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def execute(self, query: str, params: tuple):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()