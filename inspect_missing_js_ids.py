import os
import re

js_path = os.path.join(os.path.dirname(__file__), 'static', 'script.js')
with open(js_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

missing_ids = [
    'ai-kicker', 'ai-reason-1', 'ai-reason-2', 'ai-reason-3', 'ai-reason-4', 'ai-why-heading',
    'create-another-btn', 'display-user-name', 'display-wari-id', 'form-error',
    'home-see-all-services-btn', 'home-sos-btn', 'nav-brand-home', 'preview-wristband-btn',
    'qr-id-caption', 'safety-id-form', 'safety-id-result', 'sos-button-main',
    'user-name', 'user-phone', 'vol-accept-case-btn', 'vol-escalate-btn',
    'vol-mark-arrived-btn', 'vol-scan-wristband-btn'
]

for mid in missing_ids:
    print(f"\n=================== ID: '{mid}' ===================")
    for idx, line in enumerate(lines):
        if mid in line:
            start = max(0, idx - 2)
            end = min(len(lines), idx + 3)
            for j in range(start, end):
                print(f"{j+1:4d}: {lines[j].rstrip()}")
