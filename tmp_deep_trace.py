import sqlite3

db_path = r'd:\project\tito\safeTrack\db.sqlite3'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def check_all_data(emp_id):
    print(f"--- Comprehensive check for Employer {emp_id} ---")
    
    # Vacancies
    cursor.execute(f"SELECT * FROM tbl_vacancy WHERE emp_id='{emp_id}'")
    v = cursor.fetchall()
    print(f"Vacancies found: {len(v)}")
    for row in v:
        v_id = row[0]
        print(f"  Vacancy ID {v_id}: {row[3]}")
        
        # Applications
        cursor.execute(f"SELECT * FROM tbl_workerdetails WHERE vacancy_id='{v_id}'")
        apps = cursor.fetchall()
        print(f"    Applications for this vacancy: {len(apps)}")
        for app in apps:
            print(f"      Worker ID {app[1]} applied")

    # MyWorkers
    cursor.execute(f"SELECT * FROM tbl_myworker WHERE emp_id={emp_id} AND status='fixed'")
    mw = cursor.fetchall()
    print(f"MyWorkers (fixed): {len(mw)}")
    for row in mw:
        print(f"  Worker ID {row[2]} assigned to Vacancy {row[3]}")

check_all_data(4)
conn.close()
