import sqlite3

db_path = r'd:\project\tito\safeTrack\db.sqlite3'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def check_login_types():
    print("--- User types in tbl_login ---")
    cursor.execute("SELECT DISTINCT user_type FROM tbl_login")
    print(cursor.fetchall())
    
    print("\n--- Example rows from tbl_login ---")
    cursor.execute("SELECT * FROM tbl_login LIMIT 10")
    print(cursor.fetchall())

check_login_types()
conn.close()
