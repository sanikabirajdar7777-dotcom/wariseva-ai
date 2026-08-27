import urllib.request
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

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

def get_text(endpoint):
    url = BASE_URL + endpoint
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.getcode(), resp.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')

def test_unified_sos_paths():
    print("=" * 65)
    print("TESTING UNIFIED WARISEVA AI SOS WORKFLOW (PATHS A & B)")
    print("=" * 65)

    # 1. Clean Reset
    code, res = post_json('/api/demo/reset', {})
    assert code == 200, f"Reset failed: {res}"
    print("[1] Clean System Reset: PASS")

    # =========================================================================
    # PATH A: MAIN DASHBOARD SOS (Logged-in Warkari User)
    # =========================================================================
    print("\n--- Testing PATH A: Main Dashboard User SOS ---")
    code, em_a = post_json('/api/emergency/create', {
        'wari_id': 'WS-28471',
        'emergency_type': 'MEDICAL',
        'latitude': 18.3444,
        'longitude': 74.0305,
        'location_accuracy': 5.0
    })
    assert code == 201, f"Path A creation failed: {em_a}"
    assert em_a['emergency_id'] == 'EM-28471'
    assert em_a['name'] == 'Tukaram Shinde'
    print(f"    • Created Emergency: {em_a['emergency_id']} for Patient: {em_a['name']}")

    # Volunteer accepts Path A emergency
    code, acc_a = post_json(f"/api/emergency/{em_a['emergency_id']}/volunteer/accept", {
        'volunteer_id': 'V-001'
    })
    assert code == 200
    print(f"    • Volunteer V-001 Accepted Dispatch: Status -> {acc_a['status']}")

    # Check Command Center for Path A
    code, cmd_a = get_json('/api/command-center/emergencies')
    assert code == 200
    assert any(e['emergency_id'] == em_a['emergency_id'] for e in cmd_a['emergencies'])
    print("    • Command Center Synchronized with Path A Incident: PASS")

    # Reset for Path B
    post_json('/api/demo/reset', {})

    # =========================================================================
    # PATH B: QR WRISTBAND SCAN SOS (Bystander / Normal Phone)
    # =========================================================================
    print("\n--- Testing PATH B: Scanned QR Profile SOS ---")
    # 1. Open Public Profile
    code, profile_html = get_text('/public/pilgrim/WS-28471')
    assert code == 200
    assert 'TUKARAM SHINDE' in profile_html.upper()
    assert 'WS-28471' in profile_html
    assert 'SOS — REQUEST EMERGENCY HELP' in profile_html
    assert 'tel:108' not in profile_html, "Must not contain raw 108 dial button as primary action!"
    assert 'tel:112' not in profile_html, "Must not contain raw 112 dial button as primary action!"
    print("    • Public QR Profile Loaded (No raw 108/112 buttons • Unified SOS Action): PASS")

    # 2. Trigger Unified Emergency via QR
    code, em_b = post_json('/api/public/report-emergency', {
        'source': 'QR_WARI_ID',
        'wari_id': 'WS-28471',
        'patient_name': 'Tukaram Shinde',
        'reporter_type': 'QR_PUBLIC_USER',
        'emergency_type': 'MEDICAL',
        'latitude': 18.3444,
        'longitude': 74.0305,
        'location_source': 'GPS'
    })
    assert code == 201, f"Path B creation failed: {em_b}"
    assert em_b['emergency_id'] == 'EM-28471'
    assert em_b['patient_name'] == 'Tukaram Shinde'
    assert em_b['source'] == 'QR_WARI_ID'
    assert em_b['status'] == 'DISPATCHED'
    assert em_b['assigned_volunteer'] is not None
    assert em_b['nearest_camp'] is not None
    assert em_b['recommended_hospital'] is not None
    print(f"    • Created Emergency: {em_b['emergency_id']} (Patient: Tukaram Shinde, Source: QR_WARI_ID)")
    print(f"    • AI Allocated Responder: {em_b['assigned_volunteer']['name']} ({em_b['assigned_volunteer']['wari_id']})")
    print(f"    • Nearest Camp: {em_b['nearest_camp']['name']}")
    print(f"    • Recommended Hospital: {em_b['recommended_hospital']['name']}")

    # 3. Volunteer accepts Path B emergency via the SAME volunteer workflow
    code, acc_b = post_json(f"/api/emergency/{em_b['emergency_id']}/volunteer/accept", {
        'volunteer_id': 'V-001'
    })
    assert code == 200
    print(f"    • Volunteer V-001 Accepted Dispatch on Shared Workflow: Status -> {acc_b['status']}")

    # 4. Live Polling on Phone
    code, status_b = get_json(f"/api/public/emergency-status/{em_b['emergency_id']}")
    assert code == 200
    assert status_b['emergency_id'] == 'EM-28471'
    assert status_b['patient_name'] == 'Tukaram Shinde'
    assert status_b['status'] in ('ACCEPTED', 'RESPONDING', 'VOLUNTEER_ACCEPTED')
    print(f"    • Phone Live Polling Updated to: {status_b['status']} (Assigned: {status_b['assigned_volunteer']})")

    # 5. Check Command Center for Path B
    code, cmd_b = get_json('/api/command-center/emergencies')
    assert code == 200
    matched = next((e for e in cmd_b['emergencies'] if e['emergency_id'] == em_b['emergency_id']), None)
    assert matched is not None
    assert matched['reported_by'] == 'Tukaram Shinde'
    assert matched['status'] in ('ACCEPTED', 'RESPONDING', 'VOLUNTEER_ACCEPTED')
    print("    • Command Center Synchronized with Path B Incident (Status: RESPONDING): PASS")

    # 6. Clean Reset
    post_json('/api/demo/reset', {})
    print("\n[✓] Final Clean Reset: PASS")

    print("=" * 65)
    print("ALL UNIFIED SOS WORKFLOW TESTS (PATHS A & B) PASSED 100%!")
    print("=" * 65)

if __name__ == '__main__':
    test_unified_sos_paths()
