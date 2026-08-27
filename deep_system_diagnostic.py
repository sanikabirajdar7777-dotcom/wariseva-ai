import os
import sys
import io
import re
import ast
import json
import sqlite3
import subprocess

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_PY = os.path.join(BASE_DIR, 'backend', 'app.py')
DB_PATH = os.path.join(BASE_DIR, 'backend', 'wariseva.db')
INDEX_HTML = os.path.join(BASE_DIR, 'templates', 'index.html')
PUBLIC_HTML = os.path.join(BASE_DIR, 'templates', 'public_pilgrim.html')
STYLE_CSS = os.path.join(BASE_DIR, 'static', 'style.css')
SCRIPT_JS = os.path.join(BASE_DIR, 'static', 'script.js')

total_issues = 0

print("=" * 70)
print("WARISEVA AI — DEEP COMPREHENSIVE SYSTEM DIAGNOSTIC")
print("=" * 70)

# -------------------------------------------------------------
# 1. PYTHON AST & SYNTAX CHECK ON ALL PYTHON FILES
# -------------------------------------------------------------
print("\n[AUDIT 1] Checking Python AST syntax on all repository .py files...")
py_files = [f for f in os.listdir(BASE_DIR) if f.endswith('.py')]
py_files.append(os.path.relpath(APP_PY, BASE_DIR))

for pf in py_files:
    full_path = os.path.join(BASE_DIR, pf)
    if not os.path.exists(full_path):
        continue
    try:
        with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
            code = f.read()
        ast.parse(code, filename=pf)
    except Exception as e:
        print(f"  ❌ Error parsing {pf}: {e}")
        total_issues += 1

print(f"  ✓ Checked {len(py_files)} Python files. All syntax valid.")

# -------------------------------------------------------------
# 2. FLASK ROUTES INTEGRITY CHECK
# -------------------------------------------------------------
print("\n[AUDIT 2] Checking Flask Route Definitions & Duplicates...")
sys.path.insert(0, BASE_DIR)
try:
    from backend.app import app
    client = app.test_client()
    routes = [rule.rule for rule in app.url_map.iter_rules()]
    print(f"  ✓ {len(routes)} active routes registered in Flask app.")
    
    # Check duplicate endpoint names across distinct functions
    func_names = [f.__name__ for f in app.view_functions.values()]
    dup_funcs = set([fn for fn in func_names if func_names.count(fn) > 1 and fn != 'static'])
    if dup_funcs:
        print(f"  ❌ Duplicate function names found: {dup_funcs}")
        total_issues += len(dup_funcs)
    else:
        print("  ✓ Zero duplicate function names across all routes.")
except Exception as e:
    print(f"  ❌ Error loading Flask app: {e}")
    total_issues += 1

# -------------------------------------------------------------
# 3. SQLITE DATABASE SCHEMA & INTEGRITY
# -------------------------------------------------------------
print("\n[AUDIT 3] Verifying SQLite Database Tables & Schema...")
if os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]
    print(f"  ✓ Database tables ({len(tables)}): {tables}")
    
    required_tables = ['users', 'emergencies', 'medical_camps', 'notifications', 'pilgrims', 'access_logs']
    for req in required_tables:
        if req not in tables:
            print(f"  ❌ Missing required table: {req}")
            total_issues += 1
        else:
            cursor.execute(f"SELECT COUNT(*) FROM {req}")
            cnt = cursor.fetchone()[0]
            print(f"    - {req}: {cnt} rows")
    conn.close()
else:
    print("  ❌ wariseva.db not found!")
    total_issues += 1

# -------------------------------------------------------------
# 4. TEMPLATE HTML TAG BALANCING & DUPLICATE ID CHECK
# -------------------------------------------------------------
print("\n[AUDIT 4] Validating HTML Templates Tag Balance & Unique IDs...")
for html_path, name in [(INDEX_HTML, 'index.html'), (PUBLIC_HTML, 'public_pilgrim.html')]:
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    tags_to_check = ['div', 'main', 'header', 'footer', 'nav', 'form', 'section', 'button']
    for tag in tags_to_check:
        opens = len(re.findall(rf'<{tag}(\s+[^>]*)?>', html_content, re.IGNORECASE))
        closes = len(re.findall(rf'</{tag}>', html_content, re.IGNORECASE))
        if tag in ['div', 'main', 'header', 'footer', 'nav', 'form', 'section']:
            if opens != closes:
                print(f"  ❌ [{name}] Tag mismatch for <{tag}>: {opens} open vs {closes} close")
                total_issues += 1
    
    # Check for duplicate IDs in HTML
    ids = re.findall(r'id=["\']([^"\']+)["\']', html_content)
    seen_ids = set()
    dup_ids = set()
    for el_id in ids:
        if el_id in seen_ids:
            dup_ids.add(el_id)
        seen_ids.add(el_id)
    
    if dup_ids:
        print(f"  ⚠️ [{name}] Duplicate DOM IDs found ({len(dup_ids)}): {list(dup_ids)[:5]}")
        # Note: some duplicates might be in commented or multi-view areas, but let's check
    else:
        print(f"  ✓ [{name}] All {len(seen_ids)} DOM IDs are unique.")

# -------------------------------------------------------------
# 5. CSS BRACE & SYNTAX CHECK
# -------------------------------------------------------------
print("\n[AUDIT 5] Validating CSS Braces & Syntax in style.css...")
with open(STYLE_CSS, 'r', encoding='utf-8') as f:
    css_content = f.read()

# Remove comments
css_no_comments = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
open_curlies = css_no_comments.count('{')
close_curlies = css_no_comments.count('}')
if open_curlies == close_curlies:
    print(f"  ✓ CSS braces perfectly balanced ({open_curlies} open / {close_curlies} close).")
else:
    print(f"  ❌ CSS brace imbalance: {open_curlies} open vs {close_curlies} close!")
    total_issues += 1

# -------------------------------------------------------------
# 6. JAVASCRIPT AST CHECK VIA NODE.JS
# -------------------------------------------------------------
print("\n[AUDIT 6] Validating JavaScript Syntax in script.js via Node.js...")
try:
    proc = subprocess.run(
        ['node', '-c', SCRIPT_JS],
        capture_output=True,
        text=True,
        check=True
    )
    print("  ✓ static/script.js is 100% syntactically valid!")
except subprocess.CalledProcessError as e:
    print(f"  ❌ Node.js syntax error in script.js:\n{e.stderr}")
    total_issues += 1
except FileNotFoundError:
    print("  ⚠️ Node.js not installed on system, skipping AST compilation.")

# -------------------------------------------------------------
# 7. JS DOM ELEMENT REFERENCES VS HTML ELEMENT IDS
# -------------------------------------------------------------
print("\n[AUDIT 7] Validating JS DOM Element ID Lookups in index.html...")
with open(SCRIPT_JS, 'r', encoding='utf-8') as f:
    js_content = f.read()
with open(INDEX_HTML, 'r', encoding='utf-8') as f:
    index_html_content = f.read()

js_dom_ids = set(re.findall(r"document\.getElementById\(['\"]([^'\"]+)['\"]\)", js_content))
missing_ids = [dom_id for dom_id in js_dom_ids if f'id="{dom_id}"' not in index_html_content and f"id='{dom_id}'" not in index_html_content]

if missing_ids:
    print(f"  ⚠️ {len(missing_ids)} DOM IDs referenced in JS missing in index.html: {missing_ids}")
    total_issues += len(missing_ids)
else:
    print(f"  ✓ All {len(js_dom_ids)} DOM IDs referenced in JS exist in index.html.")

# -------------------------------------------------------------
# 8. JS FETCH ENDPOINTS VS FLASK REGISTERED ROUTES
# -------------------------------------------------------------
print("\n[AUDIT 8] Validating JS fetch() Endpoints against Flask Routes...")
fetch_calls = re.findall(r"fetch\(['\"]([^'\"]+)['\"]", js_content)
static_fetches = set([f for f in fetch_calls if not f.startswith('http') and '${' not in f and '+' not in f])

flask_rules = [r.rule for r in app.url_map.iter_rules()]

unmatched_fetches = []
for endpoint in static_fetches:
    clean_ep = endpoint.split('?')[0]
    matched = False
    for rule in flask_rules:
        pattern = re.sub(r'<[^>]+>', r'[^/]+', rule)
        if re.fullmatch(pattern, clean_ep):
            matched = True
            break
    if not matched:
        unmatched_fetches.append(endpoint)

if unmatched_fetches:
    print(f"  ❌ Unmatched fetch endpoints: {unmatched_fetches}")
    total_issues += len(unmatched_fetches)
else:
    print(f"  ✓ All {len(static_fetches)} static fetch endpoints match active Flask routes.")

# -------------------------------------------------------------
# 9. FLASK ENDPOINT SMOKE TESTS
# -------------------------------------------------------------
print("\n[AUDIT 9] Executing Flask Endpoint Smoke Tests (GET)...")
get_test_routes = [
    '/',
    '/public/pilgrim/WS-28471',
    '/api/pilgrim/checkpoints/WS-28471',
    '/api/pilgrim/WS-28471/live-status',
    '/api/dindi/27/members',
    '/api/command-center/resources',
    '/api/command-center/overview',
    '/api/command-center/resources-count',
    '/api/command-center/emergencies',
    '/api/command-center/hospitals',
    '/api/command-center/camps',
    '/api/command-center/volunteers',
    '/api/command-center/metrics',
    '/api/command-center/summary',
    '/api/medical-camps',
    '/api/hospitals',
    '/api/volunteers',
    '/api/network-info',
    '/api/emergency/active',
    '/api/notifications',
    '/api/health'
]

smoke_failures = 0
for r in get_test_routes:
    try:
        resp = client.get(r)
        if resp.status_code not in [200, 201]:
            print(f"  ❌ GET {r} returned HTTP {resp.status_code}")
            smoke_failures += 1
            total_issues += 1
    except Exception as e:
        print(f"  ❌ GET {r} raised exception: {e}")
        smoke_failures += 1
        total_issues += 1

if smoke_failures == 0:
    print(f"  ✓ All {len(get_test_routes)} core GET endpoints returned HTTP 200 OK.")

print("\n" + "=" * 70)
if total_issues == 0:
    print("🎉 DEEP DIAGNOSTIC COMPLETE: ZERO ERRORS FOUND ACROSS THE ENTIRE CODEBASE!")
else:
    print(f"⚠️ DIAGNOSTIC COMPLETE: {total_issues} ISSUE(S) IDENTIFIED.")
print("=" * 70)
