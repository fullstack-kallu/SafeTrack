"""
SafeTrack Template Design & Consistency Audit
Read-only check - no data modified
"""
import os, sys, re

sys.stdout.reconfigure(encoding='utf-8')

base = 'Track/templates'
results = {}

for root, dirs, files in os.walk(base):
    for f in files:
        if not f.endswith('.html'):
            continue
        path = os.path.join(root, f)
        rel = path.replace(base + os.sep, '').replace('\\', '/')
        with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
            content = fh.read()

        extends_match = re.findall(r"extends\s+'([^']+)'", content)
        has_google_font = 'fonts.googleapis.com' in content
        folder = rel.split('/')[0]

        results[rel] = {
            'extends': extends_match[0] if extends_match else None,
            'has_google_font': has_google_font,
            'folder': folder,
            'size': os.path.getsize(path),
            'has_viewport': 'width=device-width' in content,
            'is_base': 'base' in f.lower(),
            'content': content,
        }

print()
print('='*90)
print('   TEMPLATE INHERITANCE & FONT AUDIT')
print('='*90)
print(f"  {'TEMPLATE':<45} {'EXTENDS':<35} {'GFONT'}")
print('-'*90)

for rel in sorted(results):
    info = results[rel]
    ext = info['extends'] or '[base/standalone]'
    gf = 'YES' if info['has_google_font'] else '(inherited)'
    print(f"  {rel:<45} {ext[:35]:<35} {gf}")

print()
print('='*90)
print('   BASE TEMPLATE FONT DETAILS')
print('='*90)
bases = ['worker/worker_base.html', 'agency/agency_base.html', 'admin/admin_base.html', 'police/policeheder.html']
for b in bases:
    if b not in results:
        print(f"  {b} -- NOT FOUND")
        continue
    c = results[b]['content']
    fonts = re.findall(r'family=([A-Za-z0-9+]+)', c)
    ff    = re.findall(r"font-family:\s*'?([A-Za-z, ]+)'?", c)
    print(f"  [{b}]")
    print(f"    Google Fonts loaded : {fonts[:4] if fonts else 'NONE'}")
    print(f"    font-family in CSS  : {ff[:3] if ff else 'NONE'}")
    print()

print()
print('='*90)
print('   RESPONSIVENESS CHECK (viewport meta tag presence in base templates)')
print('='*90)
for b in bases:
    if b not in results:
        continue
    has = results[b]['has_viewport']
    status = 'OK  - has viewport meta' if has else 'WARN - missing viewport meta'
    print(f"  {b:<45} : {status}")

print()
print('='*90)
print('   PAGES NOT EXTENDING ANY BASE (may have inconsistent design)')
print('='*90)
for rel, info in sorted(results.items()):
    if not info['extends'] and not info['is_base']:
        print(f"  !! {rel:<45} size={info['size']} bytes")

print()
print('='*90)
print('   DESIGN CONSISTENCY ISSUES')
print('='*90)

# Check if all worker templates extend worker_base
worker_issues = []
agency_issues = []
admin_issues  = []
police_issues = []

for rel, info in results.items():
    ext = info['extends'] or ''
    if rel.startswith('worker/') and not info['is_base']:
        if 'worker_base' not in ext:
            worker_issues.append(rel)
    if rel.startswith('agency/') and not info['is_base']:
        if 'agency_base' not in ext and 'worker_base' not in ext:
            agency_issues.append(rel)
    if rel.startswith('admin/') and not info['is_base']:
        if 'admin_base' not in ext:
            admin_issues.append(rel)
    if rel.startswith('police/') and not info['is_base']:
        if 'worker_base' not in ext and 'police' not in ext.lower() and ext:
            police_issues.append(rel)

if worker_issues:
    print(f"  WORKER pages NOT extending worker_base:")
    for w in worker_issues: print(f"    - {w}")
else:
    print(f"  Worker pages: All extend worker_base  [OK]")

if agency_issues:
    print(f"  AGENCY pages NOT extending agency_base:")
    for a in agency_issues: print(f"    - {a}")
else:
    print(f"  Agency pages: All extend agency_base  [OK]")

if admin_issues:
    print(f"  ADMIN pages NOT extending admin_base:")
    for a in admin_issues: print(f"    - {a}")
else:
    print(f"  Admin pages: All extend admin_base    [OK]")

print()
print('='*90)
print('   SUMMARY')
print('='*90)
total = len(results)
with_extends = sum(1 for r in results.values() if r['extends'])
print(f"  Total templates scanned  : {total}")
print(f"  Templates with extends   : {with_extends}")
print(f"  Standalone/base templates: {total - with_extends}")
print(f"  Worker folder issues     : {len(worker_issues)}")
print(f"  Agency folder issues     : {len(agency_issues)}")
print(f"  Admin folder issues      : {len(admin_issues)}")
print()
