import re

with open('templates/index.html', encoding='utf-8') as f:
    html = f.read()

with open('static/script.js', encoding='utf-8') as f:
    js = f.read()

with open('static/style.css', encoding='utf-8') as f:
    css = f.read()

# Check CSS braces
open_braces = css.count('{')
close_braces = css.count('}')
print(f'CSS open braces: {open_braces}, close braces: {close_braces}')
if open_braces != close_braces:
    print(f'ERROR: CSS braces mismatch! Diff: {open_braces - close_braces}')
else:
    print('SUCCESS: CSS braces balanced!')

# Check JS DOM references
ids_in_html = set(re.findall(r'id=["\']([^"\']+)["\']', html))
ids_in_js = set(re.findall(r'getElementById\(["\']([^"\']+)["\']\)', js))
missing = ids_in_js - ids_in_html
print(f'DOM IDs queried in JS: {len(ids_in_js)}')
print(f'DOM IDs present in HTML: {len(ids_in_html)}')
if missing:
    print(f'WARNING: Missing IDs referenced in JS: {sorted(list(missing))}')
else:
    print('SUCCESS: 100% of DOM IDs referenced in JS exist in HTML!')
