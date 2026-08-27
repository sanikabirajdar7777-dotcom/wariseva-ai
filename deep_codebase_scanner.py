import os
import re
import sys
import io
import json
import sqlite3

if sys.platform == 'win32':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    elif hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    elif hasattr(sys.stderr, 'buffer'):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')

print("======================================================================")
print("WARISEVA AI — DEEP FORENSIC CODEBASE AUDIT")
print("======================================================================")

# 1. Collect all HTML IDs
html_ids = set()
for root, _, files in os.walk(TEMPLATES_DIR):
    for file in files:
        if file.endswith('.html'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                matches = re.findall(r'id=["\']([^"\']+)["\']', content)
                for m in matches:
                    html_ids.add(m)

print(f"[HTML] Total unique IDs found across all templates: {len(html_ids)}")

# 2. Check JavaScript for getElementById and querySelector(#...)
js_path = os.path.join(STATIC_DIR, 'script.js')
missing_ids = []
with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

get_elem_matches = re.findall(r"document\.getElementById\(['\"]([^'\"]+)['\"]\)", js_content)
query_id_matches = re.findall(r"document\.querySelector(?:All)?\(['\"]#([^'\s,\.\:\[\>]+)", js_content)
all_js_ids = set(get_elem_matches + query_id_matches)

print(f"[JS] Total unique element IDs queried in script.js: {len(all_js_ids)}")
for jid in sorted(all_js_ids):
    if jid not in html_ids:
        # Check where in JS this ID is queried
        occurrences = [m.start() for m in re.finditer(re.escape(jid), js_content)]
        missing_ids.append((jid, len(occurrences)))

print(f"[JS -> HTML Audit] Missing IDs queried in JS ({len(missing_ids)}):")
for mid, count in missing_ids:
    print(f"   - ID: '{mid}' (queried {count} time(s))")

# 3. Check CSS rules vs HTML classes
css_path = os.path.join(STATIC_DIR, 'style.css')
with open(css_path, 'r', encoding='utf-8') as f:
    css_content = f.read()

# Balance check
cleaned_css = re.sub(r'/\*[\s\S]*?\*/', '', css_content)
open_c = cleaned_css.count('{')
close_c = cleaned_css.count('}')
print(f"[CSS] Braces: {open_c} open, {close_c} close (Balanced: {open_c == close_c})")

# 4. Check Backend Routes & Handlers
sys.path.insert(0, BACKEND_DIR)
from app import app, get_db_connection

routes = [str(p) for p in app.url_map.iter_rules()]
print(f"[Flask] Total registered routes in app.py: {len(routes)}")

# 5. Check Database Integrity & Tables
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("PRAGMA integrity_check")
diag = cursor.fetchone()[0]
print(f"[SQLite] Database PRAGMA integrity_check: {diag}")

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cursor.fetchall()]
print(f"[SQLite] Tables present ({len(tables)}): {', '.join(tables)}")
conn.close()

print("\nAudit Complete.")
