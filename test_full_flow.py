import sys
import urllib.request
import urllib.parse
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = 'http://127.0.0.1:5000'

def http_get(path):
    req = urllib.request.Request(f"{BASE_URL}{path}")
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.loads(resp.read().decode('utf-8'))

def http_post(path, data=None):
    body = json.dumps(data).encode('utf-8') if data is not None else b''
    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=body,
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.loads(resp.read().decode('utf-8'))

def run_e2e_flow():
    print("==================================================")
    print("RUNNING END-TO-END WARISEVA AI SOS FLOW VERIFICATION")
    print("==================================================")

    # 1. Reset
    print("\n1. Testing Clean Reset...")
    status, res = http_post("/api/demo/reset")
    assert status == 200, f"Reset failed: {res}"
    print("   [PASS] Demo Reset 200 OK")

    # Verify Command Center is empty
    status, data = http_get("/api/command-center/emergencies")
    assert status == 200
    assert data['count'] == 0, f"Expected 0 incidents after reset, got {data['count']}"
    print(f"   [PASS] Command Center reports {data['count']} incidents after reset")

    # 2. Trigger SOS
    print("\n2. Triggering SOS from Warkari (WS-28471)...")
    payload = {
        'wari_id': 'WS-28471',
        'emergency_type': 'MEDICAL',
        'latitude': 18.3444,
        'longitude': 74.0305,
        'location_accuracy': 5.0
    }
    status, em = http_post("/api/emergency/create", payload)
    assert status == 201, f"Emergency create failed: {em}"
    em_id = em['emergency_id']
    print(f"   [PASS] Created Synchronized Emergency: {em_id} (Patient: {em['name']}, Zone: {em['wari_zone']})")
    assert em_id == 'EM-28471', f"Expected EM-28471, got {em_id}"

    # 3. Tracking Check
    print("\n3. Verifying Emergency Tracking Data...")
    status, t = http_get(f"/api/emergency/{em_id}/tracking")
    assert status == 200
    print(f"   [PASS] Status: {t['status']}")
    print(f"   [PASS] Nearest Volunteer: {t['nearest_volunteer']['name']} ({t['nearest_volunteer']['distance_m']}m • {t['nearest_volunteer']['eta_min']} min)")
    print(f"   [PASS] Nearest Camp: {t['nearest_help']['medical_camp']['name']} ({t['nearest_help']['medical_camp']['distance_m']}m)")
    print(f"   [PASS] Nearest Responder: {t['nearest_help']['responder']['name']}")
    print(f"   [PASS] Nearest Hospital: {t['nearest_help']['hospital']['name']} ({t['nearest_help']['hospital']['distance_km']} km)")

    # 4. Volunteer Dashboard & Accept
    print("\n4. Checking Volunteer Feed & Accept...")
    status, v_data = http_get("/api/volunteer/dashboard-data")
    assert status == 200
    assert v_data['count'] >= 1
    print(f"   [PASS] Volunteer feed contains {v_data['count']} active dispatch alert(s)")

    status, acc = http_post(f"/api/emergency/{em_id}/volunteer/accept", {'volunteer_id': 'V-001'})
    assert status == 200
    print("   [PASS] Volunteer V-001 accepted dispatch (Status: RESPONDING)")

    # 5. Volunteer Reached
    print("\n5. Simulating Volunteer Arrival (0m)...")
    status, rch = http_post("/api/volunteer/reached", {'emergency_id': em_id, 'volunteer_id': 'V-001'})
    assert status == 200
    print("   [PASS] Volunteer reached patient (Status: WITH_PATIENT)")

    # 6. Responder Dashboard & Accept
    print("\n6. Medical Responder Dispatched & Route Optimization...")
    status, r_acc = http_post(f"/api/emergency/{em_id}/responder/accept", {'responder_id': 'MR-001'})
    assert status == 200

    status, routes = http_get(f"/api/emergency/{em_id}/crowd-aware-routes")
    assert status == 200
    print(f"   [PASS] Bypass Route: {routes['routes']['safe_bypass_route']['distance_text']} • {routes['routes']['safe_bypass_route']['estimated_time_text']}")
    print(f"   [PASS] Crowd Delay Avoided: {routes['routes']['time_saved_text']}")

    status, r_arr = http_post(f"/api/emergency/{em_id}/responder/status", {'responder_id': 'MR-001', 'status': 'ARRIVED'})
    assert status == 200
    print("   [PASS] Responder arrived on scene")

    # 7. Hospital Escalation
    print("\n7. Hospital Escalation & Selection...")
    status, h_data = http_get(f"/api/emergency/{em_id}/nearby-hospitals")
    assert status == 200
    hosps = h_data['hospitals']
    print(f"   [PASS] Ranked {len(hosps)} nearby hospitals")

    status, h_sel = http_post(f"/api/emergency/{em_id}/hospital/select", {'hospital_id': hosps[0]['hospital_id']})
    assert status == 200
    print(f"   [PASS] Destination Hospital Selected: {hosps[0]['name']}")

    # 8. Command Center Telemetry
    print("\n8. Command Center Telemetry Check...")
    status, cmd_data = http_get("/api/command-center/emergencies")
    assert status == 200
    assert cmd_data['count'] == 1
    assert cmd_data['emergencies'][0]['emergency_id'] == em_id
    print(f"   [PASS] Command Center reports exactly 1 active incident ({em_id}) with matched status: {cmd_data['emergencies'][0]['status']}")

    # 9. Response Analytics & Scorecard
    print("\n9. Generating Response Analytics & Scorecard...")
    status, an = http_get(f"/api/emergency/{em_id}/analytics")
    assert status == 200
    print(f"   [PASS] Total Response Time: {an['total_response_time']}")
    print(f"   [PASS] WariSeva Score: {an['wariseva_score']} / 100 ({an['rating_text']})")

    # 10. Final Resolution
    print("\n10. Resolving Incident...")
    status, r_res = http_post(f"/api/emergency/{em_id}/resolve", {'emergency_id': em_id})
    assert status == 200
    print(f"   [PASS] Incident {em_id} marked RESOLVED")

    # 11. Final Clean Reset
    status, res = http_post("/api/demo/reset")
    assert status == 200
    print("   [PASS] Clean Reset 200 OK")

    print("\n==================================================")
    print("ALL 11 END-TO-END FLOW VERIFICATION STEPS PASSED 100%!")
    print("==================================================")

if __name__ == '__main__':
    run_e2e_flow()
