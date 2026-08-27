import re
import os

with open("static/script.js", "r", encoding="utf-8") as f:
    js_content = f.read()

with open("templates/index.html", "r", encoding="utf-8") as f:
    index_html = f.read()

with open("backend/app.py", "r", encoding="utf-8") as f:
    app_py = f.read()

print("=== 1. Checking Fetch Endpoints in script.js against backend/app.py ===")
fetch_patterns = re.findall(r"fetch\(\s*['\"`](/api/[^'\"`\?]+)", js_content)
# Normalize dynamic route strings like /api/emergency/${emId}/volunteer/accept -> /api/emergency/<emergency_id>/volunteer/accept
app_routes = re.findall(r"@app\.route\(\s*['\"]([^'\"]+)['\"]", app_py)

print(f"Total fetch calls found in script.js: {len(fetch_patterns)}")
print(f"Total backend app routes found: {len(app_routes)}")

unmatched_fetches = []
for endpoint in set(fetch_patterns):
    # Convert js template literal or static endpoint to regex
    pattern = endpoint
    # check if direct match in app_py or pattern matches
    matched = False
    for r in app_routes:
        # replace <var> in route with regex [^/]+
        r_regex = "^" + re.sub(r"<[^>]+>", r"[^/]+", r) + "$"
        if re.match(r_regex, endpoint) or endpoint.startswith(r.split('<')[0]):
            matched = True
            break
    if not matched:
        unmatched_fetches.append(endpoint)

if unmatched_fetches:
    print("UNMATCHED FETCH CALLS:")
    for uf in unmatched_fetches:
        print("  -", uf)
else:
    print("[ALL FETCH CALLS MATCH FLASK ROUTES]")

print("\n=== 2. Checking DOM IDs in script.js against index.html ===")
dom_id_matches = re.findall(r"document\.getElementById\(\s*['\"]([^'\"]+)['\"]\)", js_content)
all_template_ids = set(re.findall(r'id=["\']([^"\']+)["\']', index_html))

missing_ids = []
for d_id in set(dom_id_matches):
    if d_id not in all_template_ids:
        # Check if it might be in public_pilgrim.html or created dynamically
        missing_ids.append(d_id)

print(f"Total getElementById queries: {len(dom_id_matches)}")
print(f"Unique IDs in index.html: {len(all_template_ids)}")
print(f"IDs not directly in index.html: {len(missing_ids)}")
for mi in sorted(missing_ids):
    print("  ?", mi)
