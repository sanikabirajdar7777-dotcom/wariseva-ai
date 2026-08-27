with open('static/style.css', encoding='utf-8') as f:
    css = f.read()

# Check open/close braces
open_c = css.count('{')
close_c = css.count('}')
print(f"CSS Braces: {open_c} open / {close_c} close")
assert open_c == close_c, "CSS braces mismatch"

# Check for undefined variables in var(--...)
import re
defined_vars = set(re.findall(r'(--[a-zA-Z0-9_-]+)\s*:', css))
used_vars = set(re.findall(r'var\((--[a-zA-Z0-9_-]+)', css))
missing_vars = used_vars - defined_vars
print(f"Defined CSS variables: {len(defined_vars)}")
print(f"Used CSS variables: {len(used_vars)}")
if missing_vars:
    print(f"Notice: Missing variable definitions: {missing_vars}")
else:
    print("SUCCESS: All CSS variables are defined in :root or component rules!")
