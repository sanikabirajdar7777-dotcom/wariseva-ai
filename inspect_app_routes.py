import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
from app import app

print("--- REGISTERED FLASK ROUTES ---")
for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
    methods = [m for m in rule.methods if m not in ['HEAD', 'OPTIONS']]
    print(f"{rule.rule:<40} {','.join(methods):<15} {rule.endpoint}")
