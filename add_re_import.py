with open('backend/app.py', 'r', encoding='utf-8') as f:
    code = f.read()

if 'import re' not in code:
    code = "import re\n" + code

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Added import re to backend/app.py!")
