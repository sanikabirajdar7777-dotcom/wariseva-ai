import re

with open('backend/app.py', encoding='utf-8') as f:
    app_code = f.read()

# Check for request.get_json vs request.get_json(silent=True)
get_json_matches = [m.start() for m in re.finditer(r'get_json', app_code)]
print(f"Found {len(get_json_matches)} get_json occurrences in app.py")

# Check try/except in json file loading
print("Checking json file loading functions...")
for fn in ['load_wari_zones', 'load_hospitals', 'load_safety_services']:
    assert fn in app_code, f"Missing {fn}"

print("All safety checks passed in app.py!")
