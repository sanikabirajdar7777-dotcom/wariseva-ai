"""
audit_backend_db_connections.py
Check that all get_db_connection calls have corresponding conn.close().
"""

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('backend/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

opens = 0
closes = 0
open_lines = []
close_lines = []

for idx, line in enumerate(lines):
    if 'get_db_connection()' in line and not line.strip().startswith('def '):
        opens += 1
        open_lines.append(idx + 1)
    if 'conn.close()' in line:
        closes += 1
        close_lines.append(idx + 1)

print(f"Total get_db_connection calls: {opens}")
print(f"Total conn.close() calls: {closes}")

if opens == closes:
    print("✓ Every get_db_connection has a matching conn.close() call!")
else:
    print(f"⚠️ Difference between opens ({opens}) and closes ({closes})")
