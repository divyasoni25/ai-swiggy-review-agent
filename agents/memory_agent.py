import sqlite3
import os

class MemoryAgent:

    def __init__(self, db_path="memory/topics.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS topics (
                topic TEXT PRIMARY KEY,
                embedding BLOB
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS counts (
                date TEXT,
                topic TEXT,
                count INTEGER,
                PRIMARY KEY (date, topic)
            )
        """)
        self.conn.commit()

    def get_topics(self):
        cur = self.conn.cursor()
        cur.execute("SELECT topic, embedding FROM topics")
        return {row[0]: row[1] for row in cur.fetchall()}

    def save_topic(self, topic, embedding):
        
        cur = self.conn.cursor()
        cur.execute("INSERT OR IGNORE INTO topics VALUES (?, ?)", (topic, embedding))
        self.conn.commit()

    def increment_count(self, date, topic):
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO counts (date, topic, count)
            VALUES (?, ?, 1)
            ON CONFLICT(date, topic)
            DO UPDATE SET count = count + 1
        """, (date, topic))
        self.conn.commit()

