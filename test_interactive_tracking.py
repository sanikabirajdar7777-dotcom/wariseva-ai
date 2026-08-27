import urllib.request
import json
import time

BASE_URL = 'http://127.0.0.1:5000'

def test_interactive_tracking_flow():
    print("Testing WariSeva AI Interactive Emergency Tracking...")

    # 1. Reset Demo
    req = urllib.request.Request(f'{BASE_URL}/api/demo/reset', data=b'{}', headers={'Content-Type': 'application/json'})
    res = urllib.request.urlopen(req)
    assert res.status == 200, "Reset failed"
    print("[OK] Reset Demo passed")

    # 2. Create SOS Emergency
    em_payload = json.dumps({
        'wari_id': 'WS-28471',
        'emergency_type': 'MEDICAL',
        'latitude': 18.3444,
        'longitude': 74.0305,
        'location_accuracy': 5.0
    }).encode('utf-8')
    req = urllib.request.Request(f'{BASE_URL}/api/emergency/create', data=em_payload, headers={'Content-Type': 'application/json'})
    res = urllib.request.urlopen(req)
    data = json.loads(res.read().decode('utf-8'))
    assert res.status == 201 and data['success'], "Create SOS failed"
    em_id = data['emergency_id']
    print(f"[OK] SOS Created: {em_id}")

    # 3. Check Tracking endpoint returns Nearest Volunteer candidate
    res = urllib.request.urlopen(f'{BASE_URL}/api/emergency/{em_id}/tracking')
    data = json.loads(res.read().decode('utf-8'))
    assert data['success'], "Tracking failed"
    assert data['nearest_volunteer'] is not None, "Missing nearest volunteer candidate"
    assert data['nearest_volunteer']['id'] in ('V-001', 'V-002'), f"Unexpected volunteer: {data['nearest_volunteer']['id']}"
    print(f"[OK] Nearest Volunteer candidate found: {data['nearest_volunteer']['name']} ({data['nearest_volunteer']['distance_m']}m away)")

    # 4. Volunteer Accepts
    vol_accept_payload = json.dumps({'volunteer_id': 'V-001'}).encode('utf-8')
    req = urllib.request.Request(f'{BASE_URL}/api/emergency/{em_id}/volunteer/accept', data=vol_accept_payload, headers={'Content-Type': 'application/json'})
    res = urllib.request.urlopen(req)
    assert res.status == 200, "Volunteer accept failed"
    print("[OK] Volunteer V-001 accepted")

    # 5. Volunteer Streams Location
    loc_payload = json.dumps({
        'volunteer_id': 'V-001',
        'emergency_id': em_id,
        'latitude': 18.3448,
        'longitude': 74.0310,
        'accuracy': 4.0
    }).encode('utf-8')
    req = urllib.request.Request(f'{BASE_URL}/api/volunteer/location', data=loc_payload, headers={'Content-Type': 'application/json'})
    res = urllib.request.urlopen(req)
    data = json.loads(res.read().decode('utf-8'))
    assert data['success'], "Volunteer location update failed"
    print(f"[OK] Volunteer streamed location: {data['distance_to_patient_m']}m to patient")

    # 6. Volunteer Reaches Patient
    reached_payload = json.dumps({'volunteer_id': 'V-001', 'emergency_id': em_id}).encode('utf-8')
    req = urllib.request.Request(f'{BASE_URL}/api/volunteer/reached', data=reached_payload, headers={'Content-Type': 'application/json'})
    res = urllib.request.urlopen(req)
    data = json.loads(res.read().decode('utf-8'))
    assert data['success'] and data['status'] == 'WITH_PATIENT', "Volunteer reached failed"
    print("[OK] Volunteer marked: WITH_PATIENT")

    # 7. Medical Responder Accepts & En Route
    resp_accept_payload = json.dumps({'responder_id': 'MR-001'}).encode('utf-8')
    req = urllib.request.Request(f'{BASE_URL}/api/emergency/{em_id}/responder/accept', data=resp_accept_payload, headers={'Content-Type': 'application/json'})
    res = urllib.request.urlopen(req)
    assert res.status == 200, "Responder accept failed"

    resp_status_payload = json.dumps({'responder_id': 'MR-001', 'status': 'EN_ROUTE'}).encode('utf-8')
    req = urllib.request.Request(f'{BASE_URL}/api/emergency/{em_id}/responder/status', data=resp_status_payload, headers={'Content-Type': 'application/json'})
    res = urllib.request.urlopen(req)
    assert res.status == 200, "Responder status EN_ROUTE failed"
    print("[OK] Medical Responder MR-001 EN_ROUTE")

    # 8. Crowd Aware Routes
    res = urllib.request.urlopen(f'{BASE_URL}/api/emergency/{em_id}/crowd-aware-routes')
    data = json.loads(res.read().decode('utf-8'))
    assert data['success'], "Crowd routes failed"
    assert data['routes']['safe_bypass_route']['time_saved_min'] >= 1, "Route savings calculation invalid"
    print(f"[OK] Crowd-aware routing verified: Safe bypass saves {data['routes']['safe_bypass_route']['time_saved_min']} min")

    # 9. Hospital Escalation & Selection
    req = urllib.request.Request(f'{BASE_URL}/api/emergency/{em_id}/hospital/escalate', data=b'{}', headers={'Content-Type': 'application/json'})
    res = urllib.request.urlopen(req)
    assert res.status == 200, "Hospital escalate failed"

    hosp_select_payload = json.dumps({'hospital_id': 'H-001'}).encode('utf-8')
    req = urllib.request.Request(f'{BASE_URL}/api/emergency/{em_id}/hospital/select', data=hosp_select_payload, headers={'Content-Type': 'application/json'})
    res = urllib.request.urlopen(req)
    assert res.status == 200, "Hospital select failed"
    print("[OK] Hospital H-001 selected for escalation")

    # 10. Mark Resolved
    req = urllib.request.Request(f'{BASE_URL}/api/emergency/{em_id}/resolve', data=b'{}', headers={'Content-Type': 'application/json'})
    res = urllib.request.urlopen(req)
    assert res.status == 200, "Emergency resolve failed"
    print("[OK] Emergency marked: RESOLVED")

    print("\nSUCCESS: ALL 10 INTERACTIVE TRACKING TEST SCENARIOS PASSED 100%!")

if __name__ == '__main__':
    test_interactive_tracking_flow()
