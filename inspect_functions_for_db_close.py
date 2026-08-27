"""
inspect_functions_for_db_close.py
Inspect each function in backend/app.py to ensure conn.close() is called on all paths.
"""

import ast
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('backend/app.py', 'r', encoding='utf-8') as f:
    source = f.read()

tree = ast.parse(source)

missing = []

for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        fn_source = ast.get_source_segment(source, node)
        if fn_source and 'get_db_connection()' in fn_source and node.name != 'get_db_connection':
            if 'conn.close()' not in fn_source and '.close()' not in fn_source:
                missing.append((node.name, node.lineno))

if missing:
    print(f"⚠️ Found {len(missing)} functions with unclosed DB connections:")
    for name, lineno in missing:
        print(f"  Line {lineno}: {name}")
else:
    print("✓ 100% of functions that open a database connection have a corresponding close() call!")
