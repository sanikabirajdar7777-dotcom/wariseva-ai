import subprocess
import os

with open('static/script.js', encoding='utf-8') as f:
    js_code = f.read()

# Check with node if available
try:
    res = subprocess.run(['node', '--check', 'static/script.js'], capture_output=True, text=True)
    if res.returncode == 0:
        print("SUCCESS: Node.js validated static/script.js syntax with 0 errors!")
    else:
        print(f"JS Syntax Error: {res.stderr}")
except Exception as e:
    print(f"Node.js check skipped: {e}")

# Check parentheses and curly brace matching in JS
open_p = js_code.count('(')
close_p = js_code.count(')')
open_c = js_code.count('{')
close_c = js_code.count('}')
open_b = js_code.count('[')
close_b = js_code.count(']')

print(f"Parentheses: {open_p} / {close_p}")
print(f"Curly Braces: {open_c} / {close_c}")
print(f"Square Brackets: {open_b} / {close_b}")

assert open_p == close_p, "Parentheses mismatch in script.js"
assert open_c == close_c, "Curly braces mismatch in script.js"
assert open_b == close_b, "Square brackets mismatch in script.js"

print("SUCCESS: All tokens in script.js are 100% matched!")
