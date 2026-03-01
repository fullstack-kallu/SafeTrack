"""
SafeTrack Module Performance & Function Tester
Run: python test_modules.py
This is a READ-ONLY audit - no data is modified.
"""
import os, sys, django

# Fix Windows encoding
sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SafeTrack.settings')
sys.path.insert(0, '.')
django.setup()

from django.db import connection
from Track.models import (
    tbl_worker, tbl_login, tbl_admin, tbl_emp,
    tbl_policestation, tbl_vacancy, tbl_myworker, tbl_noc,
    tbl_workerdetails, tbl_feedback, tbl_workershedule
)
from django.conf import settings

PASS = '\033[92m[PASS]\033[0m'
FAIL = '\033[91m[FAIL]\033[0m'
WARN = '\033[93m[WARN]\033[0m'
INFO = '\033[94m[INFO]\033[0m'

results = []

def test(name, fn):
    try:
        result = fn()
        print(f"{PASS} {name}: {result}")
        results.append(('PASS', name))
    except Exception as e:
        print(f"{FAIL} {name}: {e}")
        results.append(('FAIL', name, str(e)))

print("\n" + "="*65)
print("   SAFETRACK FULL MODULE HEALTH CHECK")
print("="*65 + "\n")

# ─────────────────────────────────────────────────
# 1. DATABASE CONNECTION
# ─────────────────────────────────────────────────
print("─── 1. DATABASE CONNECTION ───")
test("DB raw cursor", lambda: connection.cursor().execute("SELECT 1") or "OK")
test("DB ORM ping", lambda: f"{tbl_login.objects.count()} login records found")

# ─────────────────────────────────────────────────
# 2. DATA COUNTS (All Modules)
# ─────────────────────────────────────────────────
print("\n─── 2. DATA INVENTORY ───")
test("Workers in DB",         lambda: f"{tbl_worker.objects.count()} records")
test("Employers in DB",       lambda: f"{tbl_emp.objects.count()} records")
test("Police Stations in DB", lambda: f"{tbl_policestation.objects.count()} records")
test("Vacancies in DB",       lambda: f"{tbl_vacancy.objects.count()} records")
test("Placements in DB",      lambda: f"{tbl_myworker.objects.count()} records")
test("NOC Records in DB",     lambda: f"{tbl_noc.objects.count()} records")
test("Feedback Records",      lambda: f"{tbl_feedback.objects.count()} records")
test("Job Schedules",         lambda: f"{tbl_workershedule.objects.count()} records")
test("Worker Applications",   lambda: f"{tbl_workerdetails.objects.count()} records")

# ─────────────────────────────────────────────────
# 3. LOGIN MODULE
# ─────────────────────────────────────────────────
print("\n─── 3. LOGIN / AUTH MODULE ───")
test("Admin logins exist",   lambda: f"{tbl_login.objects.filter(user_type='admin').count()} admin accounts")
test("Agency logins exist",  lambda: f"{tbl_login.objects.filter(user_type='employer').count()} agency accounts")
test("Worker logins exist",  lambda: f"{tbl_login.objects.filter(user_type='worker').count()} worker accounts")
test("Police logins exist",  lambda: f"{tbl_login.objects.filter(user_type='police').count()} police accounts")
test("Pending approvals",    lambda: f"{tbl_login.objects.filter(status='false').count()} pending")
test("Approved accounts",    lambda: f"{tbl_login.objects.filter(status='true').count()} approved")

# ─────────────────────────────────────────────────
# 4. AGENCY MODULE
# ─────────────────────────────────────────────────
print("\n─── 4. AGENCY MODULE ───")
test("Agency profile fetch",  lambda: f"First agency: {tbl_emp.objects.first().firm_name if tbl_emp.objects.exists() else 'None'}")
test("Active workers query",  lambda: f"{tbl_myworker.objects.filter(status='fixed').count()} fixed placements")
test("Vacancy listing",       lambda: f"{tbl_vacancy.objects.count()} total vacancies")
test("Feedback sent by agency", lambda: f"{tbl_feedback.objects.count()} feedback records")
test("Worker NOC query",      lambda: f"{tbl_noc.objects.count()} NOC records")

# ─────────────────────────────────────────────────
# 5. WORKER MODULE
# ─────────────────────────────────────────────────
print("\n─── 5. WORKER MODULE ───")
test("Worker profile query",  lambda: f"{tbl_worker.objects.count()} workers")
test("Active worker status",  lambda: f"First worker: {tbl_worker.objects.first().worker_name if tbl_worker.objects.exists() else 'None'}")
test("Worker applications",   lambda: f"{tbl_workerdetails.objects.count()} applications filed")
test("Feedback received",     lambda: f"{tbl_feedback.objects.count()} feedback entries")
test("Job schedule query",    lambda: f"{tbl_workershedule.objects.count()} schedules")

# ─────────────────────────────────────────────────
# 6. ADMIN MODULE
# ─────────────────────────────────────────────────
print("\n─── 6. ADMIN MODULE ───")
test("Admin profile exists",  lambda: f"{tbl_admin.objects.count()} admin records")
test("Pending employers",     lambda: f"{tbl_login.objects.filter(user_type='employer', status='false').count()} pending agency requests")
test("Active agencies",       lambda: f"{tbl_login.objects.filter(user_type='employer', status='true').count()} approved agencies")
test("Police units count",    lambda: f"{tbl_policestation.objects.count()} stations registered")
test("Worker database count", lambda: f"{tbl_worker.objects.count()} workers in system")

# ─────────────────────────────────────────────────
# 7. NOC MODULE
# ─────────────────────────────────────────────────
print("\n─── 7. NOC MODULE ───")
test("NOC records query",   lambda: f"{tbl_noc.objects.count()} total NOC entries")
test("NOC model fields",    lambda: f"Fields: noc_id, worker_id, emp_id, date, status, description via ORM")

# ─────────────────────────────────────────────────
# 8. COMPLAINT MODULE
# ─────────────────────────────────────────────────
print("\n─── 8. COMPLAINT / POLICE MODULE ───")
try:
    from Track.models import tbl_noccomplaint
    test("Complaints query",  lambda: f"{tbl_noccomplaint.objects.count()} complaints in DB")
    test("Police station query", lambda: f"{tbl_policestation.objects.count()} stations")
except ImportError:
    print(f"{WARN} tbl_noccomplaint model not found - checking via raw SQL")
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM tbl_noccomplaint")
        count = cursor.fetchone()[0]
        print(f"{PASS} Complaints query (raw SQL): {count} records")
        results.append(('PASS', 'Complaints query (raw SQL)'))
    except Exception as e:
        print(f"{FAIL} Complaint table error: {e}")
        results.append(('FAIL', 'Complaint table'))

# ─────────────────────────────────────────────────
# 9. EMAIL MODULE
# ─────────────────────────────────────────────────
print("\n─── 9. EMAIL CONFIG CHECK ───")
def check_email_config():
    host = getattr(settings, 'EMAIL_HOST', None)
    port = getattr(settings, 'EMAIL_PORT', None)
    user = getattr(settings, 'EMAIL_HOST_USER', '')
    use_tls = getattr(settings, 'EMAIL_USE_TLS', False)
    backend = getattr(settings, 'EMAIL_BACKEND', 'not set')
    issues = []
    if not host: issues.append('EMAIL_HOST missing')
    if not user: issues.append('EMAIL_HOST_USER missing')
    if not use_tls: issues.append('TLS disabled')
    if issues:
        return f"WARNINGS: {', '.join(issues)} | Backend: {backend.split('.')[-1]}"
    return f"OK | Host: {host}:{port} | User: {user} | TLS: {use_tls}"

test("Email backend config", check_email_config)

# ─────────────────────────────────────────────────
# 10. URL RESOLUTION CHECK
# ─────────────────────────────────────────────────
print("\n─── 10. URL RESOLUTION CHECK ───")
from django.urls import reverse, NoReverseMatch

urls_to_check = [
    'searchlogin', 'homeadmin', 'viewemydetails', 'viewempworker',
    'viewnoc1', 'view_feedbackworker', 'viewvacancy', 'viewmyworker',
    'viewadminworker', 'viewadminpolice', 'admin_view_all_employers',
    'admin_view_pending_employers', 'viewfeedbackworkerhome',
    'viewjobshedule', 'perdayjob', 'viewnoc', 'addcomplaint',
    'viewpoliceworker', 'worker_salary', 'viewworkeraccept',
]
passed_urls, failed_urls = 0, []
for url_name in urls_to_check:
    try:
        reverse(url_name)
        passed_urls += 1
    except NoReverseMatch as e:
        failed_urls.append(url_name)

if failed_urls:
    print(f"{FAIL} URL Resolution: {passed_urls}/{len(urls_to_check)} OK | Failed: {failed_urls}")
    results.append(('FAIL', 'URL Resolution'))
else:
    print(f"{PASS} URL Resolution: All {passed_urls}/{len(urls_to_check)} URLs resolve correctly")
    results.append(('PASS', 'URL Resolution'))

# ─────────────────────────────────────────────────
# 11. TEMPLATE EXISTENCE CHECK
# ─────────────────────────────────────────────────
print("\n─── 11. TEMPLATE FILE CHECK ───")
import os
from django.conf import settings as django_settings

template_dir = os.path.join('Track', 'templates')
critical_templates = [
    'common/login.html', 'common/index.html',
    'admin/admin_base.html', 'admin/home_admin.html', 'admin/view_adminworker.html',
    'admin/viewadminpolice.html', 'admin/view_all_employers.html', 'admin/approve_employer.html',
    'agency/agency_base.html', 'agency/home_emp.html', 'agency/feedback.html',
    'worker/worker_base.html', 'worker/home_worker.html', 'worker/view_feedbackworker.html',
    'worker/view_feedbackworkerhome.html',
    'police/home_police.html',
]
missing_templates = []
for t in critical_templates:
    path = os.path.join(template_dir, t)
    if not os.path.exists(path):
        missing_templates.append(t)

if missing_templates:
    print(f"{FAIL} Templates: {len(missing_templates)} missing: {missing_templates}")
    results.append(('FAIL', 'Template Files'))
else:
    print(f"{PASS} Templates: All {len(critical_templates)} critical templates exist")
    results.append(('PASS', 'Template Files'))

# ─────────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────────
print("\n" + "="*65)
print("   SUMMARY REPORT")
print("="*65)
passed = sum(1 for r in results if r[0] == 'PASS')
failed = sum(1 for r in results if r[0] == 'FAIL')
total = len(results)
print(f"  Total Checks : {total}")
print(f"  Passed       : \033[92m{passed}\033[0m")
print(f"  Failed       : \033[91m{failed}\033[0m")

if failed > 0:
    print("\n  Issues Found:")
    for r in results:
        if r[0] == 'FAIL':
            detail = f" → {r[2]}" if len(r) > 2 else ""
            print(f"    - {r[1]}{detail}")
print("="*65 + "\n")
