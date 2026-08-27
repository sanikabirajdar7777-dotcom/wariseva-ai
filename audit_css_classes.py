import re

with open('templates/index.html', encoding='utf-8') as f:
    html = f.read()
with open('static/style.css', encoding='utf-8') as f:
    css = f.read()

classes_in_html = set(re.findall(r'class=["\']([^"\']+)["\']', html))
all_classes = set()
for c_str in classes_in_html:
    for c in c_str.split():
        if not c.startswith('{{'):
            all_classes.add(c)

css_classes = set(re.findall(r'\.([a-zA-Z0-9_-]+)', css))
missing = all_classes - css_classes
print(f'Total HTML classes: {len(all_classes)}')
print(f'CSS classes defined: {len(css_classes)}')
print(f'Missing classes in CSS ({len(missing)}):')
for m in sorted(list(missing)):
    print(f' - {m}')
