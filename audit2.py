import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

base = 'Track/templates'
no_extends = []
font_mismatch = []

FOLDER_FONT = {
    'worker': 'Open+Sans',
    'agency': 'Open+Sans',
    'admin': 'Outfit',
    'police': 'Inter',
    'common': None,
}

for root, dirs, files in os.walk(base):
    for f in files:
        if not f.endswith('.html'):
            continue
        path = os.path.join(root, f)
        rel = os.path.relpath(path, base).replace(os.sep, '/')
        folder = rel.split('/')[0]

        with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
            c = fh.read()

        ext = re.findall(r"extends\s+[\"'](.*?)[\"']", c)
        is_base = any(x in f.lower() for x in ['base', 'header', 'heder'])

        if not ext and not is_base:
            size = os.path.getsize(path)
            no_extends.append((rel, size, folder))

print('='*70)
print('  ORPHAN TEMPLATES (no base extension) by folder')
print('='*70)

by_folder = {}
for t, s, folder in sorted(no_extends):
    by_folder.setdefault(folder, []).append((t, s))

for folder, items in sorted(by_folder.items()):
    print(f'\n  [{folder.upper()}] - {len(items)} templates without base:')
    for t, s in items:
        print(f'    {t:<55} ({s} bytes)')

print()
print('='*70)
print('  FONT CONSISTENCY ACROSS BASE TEMPLATES')
print('='*70)
bases = {
    'worker': 'worker/worker_base.html',
    'agency': 'agency/agency_base.html',
    'admin':  'admin/admin_base.html',
    'police': 'police/policeheder.html',
}
for role, tpl in bases.items():
    path = os.path.join(base, tpl.replace('/', os.sep))
    if not os.path.exists(path):
        print(f'  {role:8} base: FILE MISSING - {tpl}')
        continue
    with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
        c = fh.read()
    fonts = re.findall(r'family=([A-Za-z0-9+]+)', c)
    ff    = re.findall(r"font-family:\s*'?([A-Za-z ,]+)'?", c)
    vp    = 'width=device-width' in c
    resp  = '@media' in c
    print(f'  {role:8} | {tpl}')
    print(f'           Google Fonts  : {fonts[:3] if fonts else ["NONE"]}')
    print(f'           font-family   : {ff[:2] if ff else ["NONE"]}')
    print(f'           Viewport meta : {"YES" if vp else "NO - MISSING!"}')
    print(f'           Media queries : {"YES (responsive)" if resp else "NO - not responsive"}')
    print()

print('='*70)
print('  SUMMARY')
print('='*70)
print(f'  Total orphan templates: {len(no_extends)}')
total_by_folder = {k: len(v) for k, v in by_folder.items()}
for k, v in sorted(total_by_folder.items()):
    print(f'    {k}: {v} orphan templates')
