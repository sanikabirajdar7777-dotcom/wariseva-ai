with open('backend/app.py', 'r', encoding='utf-8') as f:
    code = f.read()

target = 'cursor.execute("SELECT * FROM access_logs ORDER BY access_time DESC LIMIT 20")'
replacement = 'cursor.execute("SELECT * FROM access_logs ORDER BY id DESC LIMIT 20")'

assert target in code, "Could not find target in backend/app.py"
code = code.replace(target, replacement)

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated access_logs query in backend/app.py to ORDER BY id DESC!")
