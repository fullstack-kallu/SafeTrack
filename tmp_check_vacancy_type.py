import sqlite3

db_path = r'd:\project\tito\safeTrack\db.sqlite3'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def check_vacancy_emp_id():
    print("--- emp_id values in tbl_vacancy ---")
    cursor.execute("SELECT DISTINCT emp_id FROM tbl_vacancy")
    rows = cursor.fetchall()
    for row in rows:
        print(f"'{row[0]}' (Type: {type(row[0])})")

check_vacancy_emp_id()
conn.close()
