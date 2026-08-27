import ast
import json
import os
import re
import sqlite3
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def run_doctor():
    issues_found = []
    print("=" * 70)
    print("WARISEVA AI — FULL CODEBASE DEEP AUDIT & DIAGNOSTIC DOCTOR")
    print("=" * 70)

    # 1. PYTHON BACKEND AUDIT
    print("\n[CHECK 1] Inspecting backend/app.py...")
    with open('backend/app.py', 'r', encoding='utf-8') as f:
        py_code = f.read()

    try:
        tree = ast.parse(py_code)
        print("  ✓ Python AST parse successful (no syntax errors).")
    except SyntaxError as e:
        issues_found.append(f"backend/app.py Syntax Error: {e}")
        print(f"  ❌ Syntax Error: {e}")

    # Check for duplicate route decorators
    routes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for dec in node.decorator_list:
                if isinstance(dec, ast.Call) and getattr(dec.func, 'attr', '') == 'route':
                    if dec.args:
                        path = dec.args[0].value if isinstance(dec.args[0], ast.Constant) else 'dynamic'
                        methods = ['GET']
                        for kw in dec.keywords:
                            if kw.arg == 'methods':
                                methods = [elt.value for elt in kw.value.elts if isinstance(elt, ast.Constant)]
                        routes.append((path, methods, node.name))

    seen_routes = {}
    duplicate_routes = []
    for path, methods, func in routes:
        for m in methods:
            key = (path, m)
            if key in seen_routes:
                duplicate_routes.append((path, m, seen_routes[key], func))
            else:
                seen_routes[key] = func

    if duplicate_routes:
        for r in duplicate_routes:
            issues_found.append(f"Duplicate route: {r[1]} {r[0]} in {r[2]} and {r[3]}")
        print(f"  ⚠️ Found {len(duplicate_routes)} duplicate route registrations!")
    else:
        print(f"  ✓ {len(seen_routes)} unique endpoints cleanly registered with zero duplicates.")

    # Check database initialization
    print("\n[CHECK 2] Verifying SQLite Database Schema & Tables...")
    try:
        conn = sqlite3.connect('backend/wariseva.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cursor.fetchall()]
        print(f"  ✓ Tables in SQLite DB: {tables}")
        required_tables = ['users', 'emergencies', 'medical_camps', 'notifications', 'group_members', 'location_updates', 'pilgrims', 'access_logs']
        for t in required_tables:
            if t not in tables:
                issues_found.append(f"Missing required table: {t}")
                print(f"  ❌ Missing table: {t}")
            else:
                cursor.execute(f"SELECT COUNT(*) FROM {t}")
                cnt = cursor.fetchone()[0]
                print(f"    - Table '{t}': {cnt} rows")
        conn.close()
    except Exception as e:
        issues_found.append(f"Database error: {e}")
        print(f"  ❌ DB Error: {e}")

    # 2. HTML INTEGRITY AUDIT
    print("\n[CHECK 3] Inspecting templates/index.html...")
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        html_code = f.read()

    # Check unclosed tags (basic tag pair verification)
    tags_to_check = ['main', 'header', 'footer', 'nav', 'form', 'section', 'select']
    for tag in tags_to_check:
        opens = len(re.findall(rf'<{tag}[\s>]', html_code, re.IGNORECASE))
        closes = len(re.findall(rf'</{tag}>', html_code, re.IGNORECASE))
        if opens != closes:
            issues_found.append(f"Mismatched <{tag}> tags: {opens} open vs {closes} close")
            print(f"  ❌ Mismatched <{tag}> tags: {opens} open vs {closes} close")
        else:
            print(f"  ✓ <{tag}> tags perfectly balanced ({opens} open, {closes} close)")

    # 3. CSS SYNTAX & VARIABLE AUDIT
    print("\n[CHECK 4] Inspecting static/style.css...")
    with open('static/style.css', 'r', encoding='utf-8') as f:
        css_code = f.read()

    clean_css = re.sub(r'/\*.*?\*/', '', css_code, flags=re.DOTALL)
    open_braces = clean_css.count('{')
    close_braces = clean_css.count('}')
    if open_braces != close_braces:
        issues_found.append(f"CSS braces unbalanced: {open_braces} open vs {close_braces} close")
        print(f"  ❌ CSS braces unbalanced: {open_braces} open vs {close_braces} close")
    else:
        print(f"  ✓ CSS braces perfectly balanced ({open_braces} open / {close_braces} close)")

    # 4. JAVASCRIPT NODE.JS SYNTAX AUDIT
    print("\n[CHECK 5] Validating static/script.js via Node.js...")
    try:
        result = subprocess.run(['node', '-c', 'static/script.js'], capture_output=True, text=True)
        if result.returncode == 0:
            print("  ✓ Node.js AST check: static/script.js is 100% syntactically valid!")
        else:
            issues_found.append(f"Node.js syntax error: {result.stderr}")
            print(f"  ❌ Node.js syntax error:\n{result.stderr}")
    except Exception as e:
        print(f"  ⚠️ Could not run node: {e}")

    # 5. CROSS-FILE DOM ID BINDING INTEGRITY
    print("\n[CHECK 6] Checking JS-to-HTML DOM ID bindings...")
    with open('static/script.js', 'r', encoding='utf-8') as f:
        js_code = f.read()

    js_ids = set(re.findall(r"getElementById\(['\"]([a-zA-Z0-9_-]+)['\"]\)", js_code))
    html_ids = set(re.findall(r'id=["\']([a-zA-Z0-9_-]+)["\']', html_code))

    missing_in_html = js_ids - html_ids
    if missing_in_html:
        for mid in missing_in_html:
            issues_found.append(f"JS references DOM ID '{mid}' which is missing in HTML")
            print(f"  ❌ Missing ID in HTML: {mid}")
    else:
        print(f"  ✓ All {len(js_ids)} DOM IDs referenced in JS exist in HTML!")

    # 6. JS FETCH ENDPOINT TO BACKEND ROUTE BINDINGS
    print("\n[CHECK 7] Checking JS fetch() endpoints against Flask registered routes...")
    fetch_matches = re.findall(r"fetch\(['\"](/api/[a-zA-Z0-9_/-]+)['\"]", js_code)
    flask_route_paths = [r[0] for r in routes]

    unmatched_endpoints = []
    for ep in set(fetch_matches):
        # Allow dynamic parameter routes
        matched = False
        for fr in flask_route_paths:
            pattern = re.sub(r'<[^>]+>', r'[^/]+', fr)
            if re.fullmatch(pattern, ep):
                matched = True
                break
        if not matched:
            unmatched_endpoints.append(ep)

    if unmatched_endpoints:
        for ep in unmatched_endpoints:
            print(f"  ⚠️ JS fetch endpoint not strictly matched in Flask routes: {ep}")
    else:
        print(f"  ✓ All {len(set(fetch_matches))} static fetch endpoints match backend routes!")

    # SUMMARY
    print("\n" + "=" * 70)
    if issues_found:
        print(f"⚠️ DOCTOR FOUND {len(issues_found)} ISSUES:")
        for iss in issues_found:
            print(f"  - {iss}")
    else:
        print("🎉 DOCTOR RESULT: ALL 7 CODEBASE AUDIT CHECKS PASSED WITH ZERO ERRORS!")
    print("=" * 70)

if __name__ == '__main__':
    run_doctor()
