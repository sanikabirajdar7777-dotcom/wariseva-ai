import sys
import io
import urllib.request
import json
import sqlite3

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

def get_json(endpoint):
    url = BASE_URL + endpoint
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.getcode(), json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))

def test_qr_suite():
    print("=" * 65)
    print("TESTING WARISEVA AI DEMO QR IDENTITY, SCANNER & PIN AUTHORIZATION")
    print("=" * 65)

    # 1. Reset Demo System
    code, res = post_json('/api/demo/reset', {})
    assert code == 200, f"Reset failed: {res}"
    print("[1] Clean System Reset: PASS")

    # 2. Verify Seeded Demo Pilgrim
    code, pilgrim = get_json('/api/pilgrim/WS-28471')
    assert code == 200, f"Pilgrim retrieval failed: {pilgrim}"
    assert pilgrim['pilgrim']['name'] == 'Tukaram Shinde'
    assert pilgrim['pilgrim']['dindi'] == '27'
    assert pilgrim['pilgrim']['status'] == 'REGISTERED'
    print(f"[2] Seeded Demo Pilgrim (WS-28471 • {pilgrim['pilgrim']['name']} • Dindi {pilgrim['pilgrim']['dindi']}): PASS")

    # 3. Volunteer Login Authentication (Valid Account)
    code, auth = post_json('/api/volunteer/login', {'volunteer_id': 'V-001', 'password': 'wari123'})
    assert code == 200, f"Volunteer login failed: {auth}"
    assert auth['volunteer']['id'] == 'V-001'
    assert auth['volunteer']['name'] == 'Ramesh Kulkarni'
    assert auth['volunteer']['verification_status'] == 'VERIFIED'
    print(f"[3] Volunteer Login (V-001 • Ramesh Kulkarni • VERIFIED): PASS")

    # 4. Volunteer Login Authentication (Invalid Password)
    code, err_auth = post_json('/api/volunteer/login', {'volunteer_id': 'V-001', 'password': 'wrong_password'})
    assert code == 401, f"Expected 401 for wrong password, got {code}"
    print("[4] Volunteer Login Rejection (Invalid Password): PASS")

    # 5. QR Lookup - Valid Identity (WS-28471)
    code, qr_found = post_json('/api/qr/lookup', {'qr_data': 'WS-28471'})
    assert code == 200, f"QR lookup failed: {qr_found}"
    assert qr_found['found'] is True
    assert qr_found['wari_id'] == 'WS-28471'
    assert qr_found['name'] == 'Tukaram Shinde'
    assert qr_found['is_protected'] is True
    # Ensure sensitive data is NOT returned before PIN verification
    assert 'blood_group' not in qr_found
    assert 'medical_alert' not in qr_found
    assert 'emergency_contact' not in qr_found
    print(f"[5] QR Identity Lookup (WS-28471 • Protected Mode Active): PASS")

    # 6. QR Lookup - Invalid Unregistered Identity (WS-99999)
    code, qr_missing = post_json('/api/qr/lookup', {'qr_data': 'WS-99999'})
    assert code == 404, f"Expected 404 for missing QR, got {code}"
    assert qr_missing['found'] is False
    print("[6] QR Lookup Rejection (Unregistered QR WS-99999): PASS")

    # 7. PIN Verification - Wrong PIN (9999)
    code, pin_denied = post_json('/api/qr/verify', {
        'wari_id': 'WS-28471',
        'pin': '9999',
        'volunteer_id': 'V-001',
        'volunteer_name': 'Ramesh Kulkarni'
    })
    assert code == 401, f"Expected 401 for invalid PIN, got {code}"
    assert pin_denied['authorized'] is False
    print("[7] PIN Access Denial (Incorrect PIN 9999): PASS")

    # 8. PIN Verification - Correct Demo PIN (2741)
    code, pin_granted = post_json('/api/qr/verify', {
        'wari_id': 'WS-28471',
        'pin': '2741',
        'volunteer_id': 'V-001',
        'volunteer_name': 'Ramesh Kulkarni'
    })
    assert code == 200, f"PIN verification failed: {pin_granted}"
    assert pin_granted['authorized'] is True
    p = pin_granted['pilgrim']
    assert p['name'] == 'Tukaram Shinde'
    assert p['blood_group'] == 'B+'
    assert 'Asthma' in p['medical_alert']
    assert p['emergency_contact'] in ('+91 98220 99881', '+91 98221 28542')
    print(f"[8] PIN Authorization & Protected Profile Unlocked: PASS")
    print(f"    • Blood Group: {p['blood_group']}")
    print(f"    • Medical Alert: {p['medical_alert']}")
    print(f"    • Emergency Contact: {p['emergency_contact']}")

    # 9. Audit Access Logs Verification
    code, logs = get_json('/api/qr/access-logs')
    assert code == 200, f"Access logs failed: {logs}"
    assert logs['count'] >= 2  # Denied attempt + Authorized attempt
    latest_log = logs['logs'][0]
    assert latest_log['volunteer_id'] == 'V-001'
    assert latest_log['pilgrim_id'] == 'WS-28471'
    assert latest_log['status'] == 'AUTHORIZED'
    print(f"[9] Audited Accountability Access Logs ({logs['count']} records logged): PASS")

    # 10. Report Emergency from Verified QR Profile
    code, em_res = post_json('/api/qr/report-emergency', {
        'wari_id': 'WS-28471',
        'volunteer_id': 'V-001',
        'emergency_type': 'MEDICAL',
        'severity': 'CRITICAL',
        'latitude': 18.3444,
        'longitude': 74.0305
    })
    assert code == 201, f"Report emergency failed: {em_res}"
    assert em_res['emergency_id'] == 'EM-28471'
    assert em_res['patient_name'] == 'Tukaram Shinde'
    assert em_res['ai_recommendation'] is not None
    print(f"[10] Emergency Created via Scanned QR (EM-28471 • AI Dispatched): PASS")
    print(f"     • Matched Responder: {em_res['ai_recommendation']['name']} ({em_res['ai_recommendation']['wari_id']})")
    print(f"     • Score: {em_res['ai_recommendation']['total_score']}/100")

    # 11. Command Center Telemetry Sync
    code, cmd_res = get_json('/api/command-center/emergencies')
    assert code == 200, f"Command center failed: {cmd_res}"
    assert cmd_res['count'] >= 1
    matched = [e for e in cmd_res['emergencies'] if e['emergency_id'] == 'EM-28471']
    assert len(matched) == 1
    assert matched[0]['reported_by'] == 'Tukaram Shinde'
    print(f"[11] Command Center Synchronized with QR Incident: PASS")

    # 12. Final Clean Reset
    code, _ = post_json('/api/demo/reset', {})
    assert code == 200
    print("[12] Final Clean System Reset: PASS")

    print("=" * 65)
    print("ALL 12 QR IDENTITY, SCANNER & PIN AUTHORIZATION TESTS PASSED 100%!")
    print("=" * 65)

if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    test_qr_suite()
