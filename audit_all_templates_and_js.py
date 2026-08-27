import os
import sys
import io
import json
import urllib.request
import urllib.error

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

BASE_URL = "http://127.0.0.1:5000"

print("======================================================================")
print("AUDITING ALL FLASK API ENDPOINTS AND STATIC ASSETS")
print("======================================================================")

# 1. Test all GET routes
get_endpoints = [
    '/',
    '/wristband',
    '/wristband/WS-28471',
    '/wristband-id',
    '/public/pilgrim/WS-28471',
    '/volunteer/login',
    '/volunteer/register',
    '/hospital/login',
    '/hospital/register',
    '/api/safety-services',
    '/api/network-info',
    '/api/command-center/resources',
    '/api/command-center/emergencies',
    '/api/admin/network-stats',
    '/api/admin/verification-queue',
    '/api/pilgrim/WS-28471',
    '/api/pilgrim/checkpoints/WS-28471',
    '/api/qr/access-logs',
    '/api/volunteer/dashboard-data',
    '/api/hospital/dashboard-data',
    '/api/emergencies/active',
    '/api/crowd/density'
]

errors = []

for ep in get_endpoints:
    url = f"{BASE_URL}{ep}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            status = resp.status
            if status >= 400:
                errors.append(f"GET {ep} returned {status}")
            else:
                print(f"  ✓ [200 OK] {ep}")
    except Exception as e:
        errors.append(f"GET {ep} failed: {e}")

# 2. Test POST /api/emergency/create
valid_payload = json.dumps({
    "wari_id": "WS-28471",
    "emergency_type": "Medical / Chest Pain",
    "severity": "CRITICAL",
    "latitude": 18.3444,
    "longitude": 74.0305
}).encode('utf-8')

try:
    req = urllib.request.Request(f"{BASE_URL}/api/emergency/create", data=valid_payload, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=5) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        if not data.get('success'):
            errors.append("POST /api/emergency/create returned success=False")
        else:
            print("  ✓ [200 OK] POST /api/emergency/create")
except Exception as e:
    errors.append(f"POST /api/emergency/create failed: {e}")

# 3. Test Emergency Lifecycle Action Endpoints
actions = [
    ("/api/emergency/EM-28471/volunteer-accept", {"volunteer_id": "V-001"}),
    ("/api/emergency/EM-28471/volunteer-enroute", {"volunteer_id": "V-001"}),
    ("/api/emergency/EM-28471/volunteer-arrived", {"volunteer_id": "V-001"}),
    ("/api/emergency/EM-28471/hospital-accept", {"hospital_id": "H-001"}),
    ("/api/emergency/EM-28471/transfer", {"hospital_id": "H-001"}),
    ("/api/emergency/EM-28471/resolve", {})
]

for endpoint, payload in actions:
    try:
        req = urllib.request.Request(
            f"{BASE_URL}{endpoint}",
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if not data.get('success'):
                errors.append(f"POST {endpoint} returned success=False: {data}")
            else:
                print(f"  ✓ [200 OK] POST {endpoint}")
    except Exception as e:
        errors.append(f"POST {endpoint} failed: {e}")

# 4. Check results
print("\n======================================================================")
if errors:
    print(f"FOUND {len(errors)} ERROR(S):")
    for err in errors:
        print(f"  [ERROR] {err}")
    sys.exit(1)
else:
    print("ALL 28 TESTED FLASK API ROUTES & EMERGENCY ACTIONS PASSED WITH 0 ERRORS!")
print("======================================================================")
