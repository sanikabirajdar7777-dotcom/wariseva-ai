import re

with open('backend/app.py', encoding='utf-8') as f:
    code = f.read()

routes = re.findall(r"@app\.route\('([^']+)',\s*methods=\[([^\]]+)\]\)", code)
for path, methods in routes:
    print(f"{methods.strip():<20} {path}")

print(f"\nTotal routes found: {len(routes)}")
