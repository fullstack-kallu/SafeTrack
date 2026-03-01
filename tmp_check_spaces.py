import sqlite3

db_path = r'd:\project\tito\safeTrack\db.sqlite3'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def check_spaces():
    print("--- Checking for trailing spaces in emp_id ---")
    
    tables = [('tbl_vacancy', 'emp_id'), ('tbl_myworker', 'emp_id'), ('tbl_feedback', 'emp_id')]
    for table, col in tables:
        cursor.execute(f"SELECT {col} FROM {table}")
        rows = cursor.fetchall()
        for row in rows:
            val = str(row[0])
            if val != val.strip():
                print(f"Space found in {table}.{col}: '{val}'")
            else:
                print(f"No spaces in {table}.{col}: '{val}'")

check_spaces()
conn.close()
