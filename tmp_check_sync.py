import sqlite3

db_path = r'd:\project\tito\safeTrack\db.sqlite3'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def check_sync():
    print("--- Checking sync between tbl_login and tbl_emp ---")
    cursor.execute("""
        SELECT l.username, l.u_id, e.emp_id, e.name 
        FROM tbl_login l 
        LEFT JOIN tbl_emp e ON l.u_id = e.emp_id 
        WHERE l.user_type = 'employer'
    """)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        if row[2] is None:
            print(f"!!! Error: u_id {row[1]} in tbl_login has no matching emp_id in tbl_emp")

check_sync()
conn.close()
