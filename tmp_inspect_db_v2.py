import sqlite3
import os

db_path = r'd:\project\tito\safeTrack\db.sqlite3'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def check_table(table_name):
    print(f"\n--- {table_name} ---")
    try:
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
        rows = cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({table_name})")
        cols = [c[1] for c in cursor.fetchall()]
        print("Columns:", cols)
        for row in rows:
            print(dict(zip(cols, row)))
    except Exception as e:
        print(f"Error checking {table_name}: {e}")

check_table('tbl_login')
check_table('tbl_emp')
check_table('tbl_vacancy')
check_table('tbl_myworker')

conn.close()
