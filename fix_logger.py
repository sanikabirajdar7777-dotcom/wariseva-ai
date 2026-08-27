with open('backend/app.py', 'r', encoding='utf-8') as f:
    code = f.read()

target = """    # Standardized Flask stdout logger
    print(f"\\n=======================================================")
    print(f"🔍 QR PAYLOAD GENERATED: {payload}")
    print(f"   Specs: 540x540px • Error Correction: Level H • Quiet Zone: 4 modules")
    print(f"=======================================================\\n")"""

replacement = """    # Standardized Flask stdout logger (ASCII-safe for Windows consoles)
    print("\\n" + "=" * 55)
    print(f"QR PAYLOAD GENERATED: {payload}")
    print(f"Specs: 540x540px | Error Correction: Level H | Quiet Zone: 4 modules")
    print("=" * 55 + "\\n")"""

assert target in code, "Could not find target logger in app.py"
code = code.replace(target, replacement)

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Fixed Windows console stdout logger in app.py!")
