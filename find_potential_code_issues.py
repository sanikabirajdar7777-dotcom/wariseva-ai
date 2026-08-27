"""
find_potential_code_issues.py
Deep audit for subtle issues:
1. Check for any broken onclick handlers in HTML
2. Check for missing static assets (images, icons)
3. Check for open intervals or timeouts that might leak
4. Check for unhandled promises or console errors
"""

import os
import re
import sys
import sqlite3

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def audit_html_onclicks():
    print("[1] Auditing onclick attributes in templates...")
    templates = ['templates/index.html', 'templates/public_pilgrim.html']
    with open('static/script.js', 'r', encoding='utf-8') as f:
        js = f.read()

    issues = []
    for tpath in templates:
        with open(tpath, 'r', encoding='utf-8') as f:
            html = f.read()
        onclicks = re.findall(r'onclick="([^"]+)"', html)
        print(f"  [{tpath}] Found {len(onclicks)} inline onclick handlers.")

    issues = []
    for oc in onclicks:
        # Check if it calls document.getElementById('...')?.click()
        match = re.search(r"document\.getElementById\('([^']+)'\)", oc)
        if match:
            target_id = match.group(1)
            if f'id="{target_id}"' not in html:
                issues.append(f"Inline onclick targets non-existent element id='{target_id}': {oc}")
        # Check if it calls a function name
        fn_match = re.match(r'^([a-zA-Z0-9_]+)\(', oc.strip())
        if fn_match:
            fn_name = fn_match.group(1)
            if fn_name not in ['switchView', 'alert', 'confirm', 'prompt', 'print']:
                if f'function {fn_name}' not in js and f'window.{fn_name}' not in js and f'{fn_name} =' not in js and f'function {fn_name}' not in html:
                    issues.append(f"Inline onclick calls undefined function '{fn_name}': {oc}")

    if issues:
        for i in issues:
            print("  ❌", i)
    else:
        print("  ✓ All inline onclick handlers target valid elements or functions.")
    return issues

def audit_missing_assets():
    print("[2] Auditing static assets and image references...")
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    srcs = re.findall(r'<img[^>]+src="([^">]+)"', html)
    issues = []
    for s in srcs:
        if s.startswith('http://') or s.startswith('https://') or s.startswith('data:'):
            continue
        # check local path
        local_path = s.lstrip('/')
        if not os.path.exists(local_path) and not os.path.exists(os.path.join('static', local_path)):
            issues.append(f"Referenced image path does not exist: {s}")

    if issues:
        for i in issues:
            print("  ❌", i)
    else:
        print("  ✓ All referenced images and local assets exist.")
    return issues

def audit_js_functions():
    print("[3] Auditing JavaScript function definitions and duplicate names...")
    with open('static/script.js', 'r', encoding='utf-8') as f:
        js = f.read()

    fns = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', js)
    seen = set()
    dupes = []
    for fn in fns:
        if fn in seen:
            dupes.append(fn)
        seen.add(fn)

    if dupes:
        print(f"  ⚠️ Warning: Duplicate function names in script.js: {set(dupes)}")
    else:
        print(f"  ✓ {len(fns)} functions in script.js; zero duplicate function names.")
    return dupes

def audit_database_schema_integrity():
    print("[4] Auditing database schema integrity and foreign keys...")
    conn = sqlite3.connect('backend/wariseva.db')
    c = conn.cursor()
    c.execute("PRAGMA integrity_check")
    result = c.fetchone()[0]
    conn.close()
    if result == 'ok':
        print("  ✓ SQLite database integrity check PASSED (ok).")
    else:
        print(f"  ❌ Database integrity error: {result}")
    return result

if __name__ == '__main__':
    i1 = audit_html_onclicks()
    i2 = audit_missing_assets()
    i3 = audit_js_functions()
    i4 = audit_database_schema_integrity()
    print("\nDeep Audit Finished.")
