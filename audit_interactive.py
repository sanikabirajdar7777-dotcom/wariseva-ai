import re
from html.parser import HTMLParser

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('static/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Extract all IDs from HTML
button_form_ids = re.findall(r'<(?:button|form|input|select)\b[^>]*\bid=["\']([^"\']+)["\']', html)
print(f"Total interactive element IDs in HTML: {len(button_form_ids)}")

unhandled = []
for el_id in button_form_ids:
    if el_id not in js:
        unhandled.append(el_id)

print(f"Interactive element IDs not directly referenced in JS ({len(unhandled)}):")
for u in unhandled:
    print(f"  - {u}")
