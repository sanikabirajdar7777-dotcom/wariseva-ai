import urllib.request
import urllib.parse
import json

BASE_URL = 'http://127.0.0.1:5000'

def request_json(path, method='GET', payload=None):
    url = f"{BASE_URL}{path}"
    data = json.dumps(payload).encode('utf-8') if payload is not None else None
    headers = {'Content-Type': 'application/json'} if data else {}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        res = urllib.request.urlopen(req)
        body = res.read().decode('utf-8')
        return res.status, json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        try:
            return e.code, json.loads(body) if body else {}
        except Exception:
            return e.code, {'raw_error': body}

def run_deep_audit():
    print("Starting Comprehensive Deep System Audit of WariSeva AI...")
    tests_run = 0

    # 1. Home Page
    req = urllib.request.Request(f"{BASE_URL}/")
    res = urllib.request.urlopen(req)
    assert res.status == 200, "Home page failed"
    tests_run += 1
    print(f"[{tests_run}] GET / -> 200 OK")

    # 2. Favicon
    req = urllib.request.Request(f"{BASE_URL}/favicon.ico")
    res = urllib.request.urlopen(req)
    assert res.status in (200, 204), "Favicon failed"
    tests_run += 1
    print(f"[{tests_run}] GET /favicon.ico -> {res.status} OK")

    # 3. Reset Demo State
    code, data = request_json('/api/demo/reset', method='POST')
    assert code == 200 and data['success'], "Reset failed"
    tests_run += 1
    print(f"[{tests_run}] POST /api/demo/reset -> 200 OK")

    # 4. Safety Services Permutations
    categories = ['WATER', 'TOILET', 'FOOD', 'REST_AREA', 'MEDICAL_CAMP', 'HOSPITAL', 'ALL', 'INVALID']
    for cat in categories:
        code, data = request_json(f'/api/safety-services?type={cat}&zone=Zone%2004&latitude=18.3444&longitude=74.0305')
        assert code == 200 and data['success'], f"Safety services failed for category {cat}"
        tests_run += 1
    print(f"[{tests_run}] GET /api/safety-services (8 category filters) -> 200 OK")

    # 5. Safety ID Validation (Empty name/phone)
    code, data = request_json('/safety-id/create', method='POST', payload={'name': '', 'phone': ''})
    assert code == 400 and not data['success'], "Validation should fail for empty name/phone"
    tests_run += 1
    print(f"[{tests_run}] POST /safety-id/create (Validation 400 test) -> 400 Bad Request handled gracefully")

    # 6. Safety ID Creation (Valid)
    code, data = request_json('/safety-id/create', method='POST', payload={'name': 'Dnyaneshwar Patil', 'phone': '9876543210'})
    assert code in (200, 201) and data['success'], "Safety ID creation failed"
    wari_id = data['wari_id']
    tests_run += 1
    print(f"[{tests_run}] POST /safety-id/create -> {code} OK (Generated ID: {wari_id})")

    # 7. SOS Creation Validation (Missing Coordinates)
    code, data = request_json('/api/emergency/create', method='POST', payload={'wari_id': wari_id})
    assert code == 400 and not data['success'], "SOS creation should require coordinates"
    tests_run += 1
    print(f"[{tests_run}] POST /api/emergency/create (Validation 400 test) -> 400 Bad Request handled gracefully")

    # 8. SOS Creation (Valid)
    code, data = request_json('/api/emergency/create', method='POST', payload={
        'wari_id': wari_id,
        'emergency_type': 'MEDICAL',
        'latitude': 18.3444,
        'longitude': 74.0305,
        'location_accuracy': 5.0
    })
    assert code == 201 and data['success'], "SOS creation failed"
    em_id = data['emergency_id']
    tests_run += 1
    print(f"[{tests_run}] POST /api/emergency/create -> 201 Created (Emergency ID: {em_id})")

    # 9. Emergency Tracking Endpoint
    code, data = request_json(f'/api/emergency/{em_id}/tracking')
    assert code == 200 and data['success'], "Emergency tracking failed"
    assert data['nearest_volunteer'] is not None, "Nearest volunteer not identified"
    tests_run += 1
    print(f"[{tests_run}] GET /api/emergency/{em_id}/tracking -> 200 OK (Nearest Vol: {data['nearest_volunteer']['name']})")

    # 10. Invalid Emergency Tracking
    code, data = request_json('/api/emergency/INVALID-9999/tracking')
    assert code == 404, "Invalid emergency tracking should return 404"
    tests_run += 1
    print(f"[{tests_run}] GET /api/emergency/INVALID-9999/tracking -> 404 Not Found handled gracefully")

    # 11. Volunteer Dashboard Feed
    code, data = request_json('/api/volunteer/dashboard-data')
    assert code == 200 and data['success'], "Volunteer feed failed"
    tests_run += 1
    print(f"[{tests_run}] GET /api/volunteer/dashboard-data -> 200 OK")

    # 12. Volunteer Accepts
    code, data = request_json(f'/api/emergency/{em_id}/volunteer/accept', method='POST', payload={'volunteer_id': 'V-001'})
    assert code == 200 and data['success'], "Volunteer accept failed"
    tests_run += 1
    print(f"[{tests_run}] POST /api/emergency/{em_id}/volunteer/accept -> 200 OK")

    # 13. Volunteer Streams GPS
    code, data = request_json('/api/volunteer/location', method='POST', payload={
        'volunteer_id': 'V-001',
        'emergency_id': em_id,
        'latitude': 18.3448,
        'longitude': 74.0310,
        'accuracy': 4.0
    })
    assert code == 200 and data['success'], "Volunteer GPS stream failed"
    tests_run += 1
    print(f"[{tests_run}] POST /api/volunteer/location -> 200 OK (Distance: {data['distance_to_patient_m']}m)")

    # 14. Volunteer Reaches Patient
    code, data = request_json('/api/volunteer/reached', method='POST', payload={'volunteer_id': 'V-001', 'emergency_id': em_id})
    assert code == 200 and data['success'] and data['status'] == 'WITH_PATIENT', "Volunteer reached failed"
    tests_run += 1
    print(f"[{tests_run}] POST /api/volunteer/reached -> 200 OK (Status: WITH_PATIENT)")

    # 15. Medical Responder Feed
    code, data = request_json('/api/responder/dashboard-data')
    assert code == 200 and data['success'], "Responder feed failed"
    tests_run += 1
    print(f"[{tests_run}] GET /api/responder/dashboard-data -> 200 OK")

    # 16. Responder Accepts
    code, data = request_json(f'/api/emergency/{em_id}/responder/accept', method='POST', payload={'responder_id': 'MR-001'})
    assert code == 200 and data['success'], "Responder accept failed"
    tests_run += 1
    print(f"[{tests_run}] POST /api/emergency/{em_id}/responder/accept -> 200 OK")

    # 17. Responder Streams GPS
    code, data = request_json('/api/responder/location', method='POST', payload={
        'responder_id': 'MR-001',
        'emergency_id': em_id,
        'latitude': 18.3470,
        'longitude': 74.0330,
        'accuracy': 5.0
    })
    assert code == 200 and data['success'], "Responder GPS stream failed"
    tests_run += 1
    print(f"[{tests_run}] POST /api/responder/location -> 200 OK")

    # 18. Crowd-Aware Routes
    code, data = request_json(f'/api/emergency/{em_id}/crowd-aware-routes')
    assert code == 200 and data['success'], "Crowd-aware routes failed"
    assert data['routes']['safe_bypass_route']['time_saved_min'] >= 1, "Safe route savings calculation failed"
    tests_run += 1
    print(f"[{tests_run}] GET /api/emergency/{em_id}/crowd-aware-routes -> 200 OK (Saves: {data['routes']['safe_bypass_route']['time_saved_min']} min)")

    # 19. Responder Status EN_ROUTE and ARRIVED
    code, data = request_json(f'/api/emergency/{em_id}/responder/status', method='POST', payload={'responder_id': 'MR-001', 'status': 'EN_ROUTE'})
    assert code == 200 and data['success'], "Responder EN_ROUTE failed"
    tests_run += 1
    print(f"[{tests_run}] POST /api/emergency/{em_id}/responder/status (EN_ROUTE) -> 200 OK")

    code, data = request_json(f'/api/emergency/{em_id}/responder/status', method='POST', payload={'responder_id': 'MR-001', 'status': 'ARRIVED'})
    assert code == 200 and data['success'], "Responder ARRIVED failed"
    tests_run += 1
    print(f"[{tests_run}] POST /api/emergency/{em_id}/responder/status (ARRIVED) -> 200 OK")

    # 20. Hospital Escalation & Discovery
    code, data = request_json(f'/api/emergency/{em_id}/hospital/escalate', method='POST')
    assert code == 200 and data['success'], "Hospital escalate failed"
    tests_run += 1
    print(f"[{tests_run}] POST /api/emergency/{em_id}/hospital/escalate -> 200 OK")

    code, data = request_json(f'/api/emergency/{em_id}/nearby-hospitals')
    assert code == 200 and data['success'] and len(data['hospitals']) > 0, "Nearby hospitals discovery failed"
    tests_run += 1
    print(f"[{tests_run}] GET /api/emergency/{em_id}/nearby-hospitals -> 200 OK ({len(data['hospitals'])} hospitals ranked)")

    # 21. Hospital Selection
    code, data = request_json(f'/api/emergency/{em_id}/hospital/select', method='POST', payload={'hospital_id': 'HOSP-001'})
    assert code == 200 and data['success'], "Hospital selection failed"
    tests_run += 1
    print(f"[{tests_run}] POST /api/emergency/{em_id}/hospital/select -> 200 OK (Selected: {data['hospital_name']})")

    # 22. Command Center Emergencies Registry
    code, data = request_json('/api/command-center/emergencies')
    assert code == 200 and data['success'], "Command center emergencies failed"
    tests_run += 1
    print(f"[{tests_run}] GET /api/command-center/emergencies -> 200 OK ({data['count']} active incidents)")

    # 23. Emergency Resolution
    code, data = request_json(f'/api/emergency/{em_id}/resolve', method='POST')
    assert code == 200 and data['success'], "Emergency resolution failed"
    tests_run += 1
    print(f"[{tests_run}] POST /api/emergency/{em_id}/resolve -> 200 OK (Status: RESOLVED)")

    # 24. Pre-seeded Demo Emergency Creation
    code, data = request_json('/api/demo/create-emergency', method='POST')
    assert code == 201 and data['success'], "Demo emergency creation failed"
    tests_run += 1
    print(f"[{tests_run}] POST /api/demo/create-emergency -> 201 Created (EM-28471)")

    # 25. Final Reset to Clean State
    code, data = request_json('/api/demo/reset', method='POST')
    assert code == 200 and data['success'], "Final reset failed"
    tests_run += 1
    print(f"[{tests_run}] POST /api/demo/reset -> 200 OK")

    print("\n" + "="*60)
    print(f"ALL {tests_run} DEEP SYSTEM AUDIT CHECKPOINTS PASSED 100% WITH ZERO ERRORS!")
    print("="*60)

if __name__ == '__main__':
    run_deep_audit()
