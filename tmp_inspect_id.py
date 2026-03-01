import sqlite3

db_path = r'd:\project\tito\safeTrack\db.sqlite3'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def check_id_4():
    print("--- Checking ID 4 across tables ---")
    
    print("\ntbl_login where u_id=4:")
    cursor.execute("SELECT * FROM tbl_login WHERE u_id=4")
    print(cursor.fetchall())

    print("\ntbl_emp where emp_id=4:")
    cursor.execute("SELECT * FROM tbl_emp WHERE emp_id=4")
    print(cursor.fetchall())
    
    print("\ntbl_vacancy where emp_id='4':")
    cursor.execute("SELECT * FROM tbl_vacancy WHERE emp_id='4'")
    print(cursor.fetchall())
    
    print("\ntbl_myworker where emp_id=4:")
    cursor.execute("SELECT * FROM tbl_myworker WHERE emp_id=4")
    print(cursor.fetchall())

check_id_4()
conn.close()
