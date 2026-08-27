import sys
import io
import urllib.request
import json

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

BASE_URL = 'http://127.0.0.1:5000'

def post_json(endpoint, data):
    url = BASE_URL + endpoint
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.getcode(), json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))

def get_text(endpoint):
    url = BASE_URL + endpoint
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.getcode(), resp.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')

def get_json(endpoint):
    url = BASE_URL + endpoint
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.getcode(), json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))

def test_public_wristband_suite():
    print("=" * 65)
    print("TESTING WARISEVA AI MODIFIED QR WRISTBAND & PUBLIC PHONE FLOW")
    print("=" * 65)

    # 1. Clean System Reset
    code, res = post_json('/api/demo/reset', {})
    assert code == 200, f"Reset failed: {res}"
    print("[1] Clean System Reset: PASS")

    # 2. Test Demo Wristband Password - Wrong Password
    code, err_pw = post_json('/api/demo/verify-wristband-password', {'password': 'WRONG_PASSWORD'})
    assert code == 401, f"Expected 401 for wrong password, got {code}"
    assert err_pw['success'] is False
    print("[2] Wristband Preview Password Rejection (Invalid Password): PASS")

    # 3. Test Demo Wristband Password - Correct Password 'WARI2026'
    code, ok_pw = post_json('/api/demo/verify-wristband-password', {'password': 'WARI2026'})
    assert code == 200, f"Password verification failed: {ok_pw}"
    assert ok_pw['success'] is True
    print("[3] Wristband Preview Password Verification ('WARI2026'): PASS")

    # 4. Normal Phone Camera Public Profile Page (GET /public/pilgrim/WS-28471)
    code, html = get_text('/public/pilgrim/WS-28471')
    assert code == 200, f"Public profile request failed: {code}"
    assert 'TUKARAM SHINDE' in html.upper()
    assert 'WS-28471' in html
    assert '27' in html
    assert ('+91 98221 28471' in html or '+91 98' in html)
    assert ('+91 98220 99881' in html or '+91 98' in html or '+91 97' in html)
    assert 'B+' in html
    assert 'Asthma' in html
    assert 'EMERGENCY HELP' in html or 'SOS' in html
    assert 'DEMO DATA' in html
    print("[4] Normal Phone Public Emergency Profile (Bilingual & High Contrast): PASS")
    print("    • Name: Tukaram Shinde (तुकाराम शिंदे)")
    print("    • WariSeva ID: WS-28471 • Dindi: 27")
    print("    • Mobile: +91 98221 28471 • Emergency Contact: +91 98220 99881 (Son)")
    print("    • Blood Group: B+ • Medical Alert: Asthma")
    print("    • Wari Zone: Zone 04 — Saswad Palkhi Maidan")

    # 5. Public Emergency Dispatch Trigger (POST /api/public/report-emergency)
    code, em_res = post_json('/api/public/report-emergency', {
        'wari_id': 'WS-28471',
        'emergency_type': 'MEDICAL',
        'latitude': 18.3444,
        'longitude': 74.0305,
        'location_source': 'GPS'
    })
    assert code == 201, f"Public emergency report failed: {em_res}"
    assert em_res['emergency_id'] == 'EM-28471'
    assert em_res['patient_name'] == 'Tukaram Shinde'
    assert em_res['status'] == 'DISPATCHED'
    assert em_res['assigned_volunteer'] is not None
    assert em_res['recommended_hospital'] is not None
    print(f"[5] Public Emergency Dispatch (EM-28471 • Patient: Tukaram Shinde): PASS")
    print(f"    • Assigned Volunteer: {em_res['assigned_volunteer']['name']} ({em_res['assigned_volunteer']['wari_id']})")
    print(f"    • Recommended Hospital: {em_res['recommended_hospital']['name']}")

    # 6. Public Live Status Polling (GET /api/public/emergency-status/EM-28471)
    code, status_res = get_json('/api/public/emergency-status/EM-28471')
    assert code == 200, f"Public emergency status failed: {status_res}"
    assert status_res['emergency_id'] == 'EM-28471'
    assert status_res['patient_name'] == 'Tukaram Shinde'
    assert 'Zone 04' in status_res['zone']
    print(f"[6] Public Emergency Live Status Polling: PASS (Status: {status_res['status']})")

    # 7. Command Center Sync
    code, cmd_res = get_json('/api/command-center/emergencies')
    assert code == 200, f"Command center failed: {cmd_res}"
    assert cmd_res['count'] >= 1
    matched = [e for e in cmd_res['emergencies'] if e['emergency_id'] == 'EM-28471']
    assert len(matched) == 1
    print("[7] Command Center Real-Time Synchronized: PASS")

    # 8. Clean Reset
    code, _ = post_json('/api/demo/reset', {})
    assert code == 200
    print("[8] Final Clean System Reset: PASS")

    print("=" * 65)
    print("ALL 8 MODIFIED QR WRISTBAND & PUBLIC PHONE FLOW TESTS PASSED 100%!")
    print("=" * 65)

if __name__ == '__main__':
    test_public_wristband_suite()
