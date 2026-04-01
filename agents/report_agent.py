import pandas as pd
from datetime import datetime, timedelta
import sqlite3
import os

class ReportAgent:
    def generate(self, target_date, window=30):
        conn = sqlite3.connect("memory/topics.db")
        cur = conn.cursor()

        dates = [
            (datetime.strptime(target_date, "%Y-%m-%d") - timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range(window)
        ]

        cur.execute("SELECT DISTINCT topic FROM counts")
        topics = [row[0] for row in cur.fetchall()]

        table = []

        for topic in topics:
            row = {"Topic": topic}
            for d in dates:
                cur.execute("SELECT count FROM counts WHERE date=? AND topic=?", (d, topic))
                res = cur.fetchone()
                row[d] = res[0] if res else 0
            table.append(row)

        df = pd.DataFrame(table)

        # Create output directory FIRST
        os.makedirs("output", exist_ok=True)

        # Then save file
        df.to_csv("output/trend_report_T.csv", index=False)

        conn.close()

