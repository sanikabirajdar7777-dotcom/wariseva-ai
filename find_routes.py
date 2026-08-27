with open('backend/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'def ' in line or '@app.route' in line:
        if 'responder' in line.lower() or 'dashboard' in line.lower():
            print(f"{i+1}: {line.strip()}")
