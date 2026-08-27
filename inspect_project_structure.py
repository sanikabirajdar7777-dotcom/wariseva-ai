import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

view_matches = re.findall(r'id=["\']([a-zA-Z0-9_-]+-view)["\']', html)
print("Views in index.html:", view_matches)

# Check for safety map components
safety_map = re.findall(r'id=["\']([^"\']*map[^"\']*)["\']', html, re.I)
print("Map IDs in index.html:", safety_map)

# Check triage components
triage = re.findall(r'id=["\']([^"\']*triage[^"\']*)["\']', html, re.I)
print("Triage IDs in index.html:", triage)
