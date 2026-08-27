import ast
import json
import os
import re
import sqlite3
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def audit_python_code():
    print("=" * 60)
    print("1. AUDITING PYTHON BACKEND CODE (backend/app.py)")
    print("=" * 60)
    
    with open('backend/app.py', 'r', encoding='utf-8') as f:
        code = f.read()

    try:
        tree = ast.parse(code)
        print("✓ AST Parsing: backend/app.py is syntactically valid!")
    except SyntaxError as e:
        print(f"❌ Syntax Error in backend/app.py: {e}")
        return False

    # Extract all route paths
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

    print(f"✓ Found {len(routes)} registered Flask routes:")
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
        print("⚠️ DUPLICATE ROUTES DETECTED:")
        for r in duplicate_routes:
            print(f"   {r[1]} {r[0]} defined in {r[2]} and {r[3]}")
    else:
        print("✓ ZERO duplicate route registrations found!")

    return True

if __name__ == '__main__':
    audit_python_code()
