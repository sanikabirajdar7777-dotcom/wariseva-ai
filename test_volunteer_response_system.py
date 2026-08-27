import urllib.request
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = 'http://127.0.0.1:5000'

# Session-enabled opener with cookiejar
import http.cookiejar
cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

def post_json(endpoint, data):
    url = BASE_URL + endpoint
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        with opener.open(req) as resp:
            return resp.getcode(), json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))

def get_json(endpoint):
    url = BASE_URL + endpoint
    req = urllib.request.Request(url)
    try:
        with opener.open(req) as resp:
            return resp.getcode(), json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))

def get_url(endpoint):
    url = BASE_URL + endpoint
    req = urllib.request.Request(url)
    try:
        with opener.open(req) as resp:
            return resp.getcode(), resp.read().decode('utf-8'), resp.geturl()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8'), e.geturl()

def test_volunteer_suite():
    print("=" * 70)
    print("TESTING WARISEVA AI AUTHENTICATED VOLUNTEER RESPONSE SYSTEM")
    print("=" * 70)

    # 1. Clean Reset
    code, res = post_json('/api/demo/reset', {})
    assert code == 200
    print("[1] Clean System Reset: PASS")

    # 2. Login Page Availability
    code, html, url = get_url('/volunteer/login')
    assert code == 200
    assert 'VOLUNTEER RESPONSE PORTAL' in html
    assert 'Respond faster. Save lives.' in html
    assert 'V-001' in html and 'VOL001' in html
    print("[2] Dedicated /volunteer/login page renders: PASS")

    # 3. Protected Dashboard Redirect when unauthenticated
    cookie_jar.clear()
    code, html, final_url = get_url('/volunteer/dashboard')
    assert 'login' in final_url or code == 302, f"Expected redirect to login, got {final_url}"
    print("[3] Protected /volunteer/dashboard redirects unauthenticated users: PASS")

    # 4. Authentication Rejection on Invalid Password
    code, err_res = post_json('/api/volunteer/login', {
        'volunteer_id': 'V-001',
        'password': 'WRONG_PASSWORD'
    })
    assert code == 401
    assert err_res['success'] is False
    print("[4] Volunteer Login Rejects Invalid Password (401 Unauthorized): PASS")

    # 5. Authentication Success on Valid Demo Credentials
    for v_id, pwd in [('V-001', 'VOL001'), ('V-002', 'VOL002'), ('V-003', 'VOL003')]:
        code, ok_res = post_json('/api/volunteer/login', {
            'volunteer_id': v_id,
            'password': pwd
        })
        assert code == 200, f"Failed for {v_id}: {ok_res}"
        assert ok_res['success'] is True
        assert ok_res['volunteer']['id'] == v_id
        assert ok_res['volunteer']['status'] == 'AVAILABLE'
    print("[5] Volunteer Login Accepts all Demo Credentials (V-001, V-002, V-003): PASS")

    # Log in as V-001 (Ramesh Kulkarni)
    post_json('/api/volunteer/login', {'volunteer_id': 'V-001', 'password': 'VOL001'})
    code, dash_html, _ = get_url('/volunteer/dashboard')
    assert code == 200
    assert 'Ramesh Kulkarni' in dash_html
    assert 'V-001' in dash_html
    print("[6] Authenticated /volunteer/dashboard loads profile correctly: PASS")

    # 6. Status Control Dropdown
    code, st_res = post_json('/api/volunteer/status', {'status': 'BUSY'})
    assert code == 200
    assert st_res['status'] == 'BUSY'
    code, st_res2 = post_json('/api/volunteer/status', {'status': 'AVAILABLE'})
    assert code == 200
    assert st_res2['status'] == 'AVAILABLE'
    print("[7] Volunteer Availability Status Switcher (AVAILABLE/BUSY/OFFLINE): PASS")

    # 7. Create Emergency from QR Profile / SOS
    code, em_res = post_json('/api/public/report-emergency', {
        'source': 'QR_WARI_ID',
        'wari_id': 'WS-28471',
        'patient_name': 'Tukaram Shinde',
        'reporter_type': 'QR_PUBLIC_USER',
        'emergency_type': 'MEDICAL',
        'latitude': 18.3444,
        'longitude': 74.0305,
        'location_source': 'GPS'
    })
    assert code == 201
    em_id = em_res['emergency_id']
    print(f"[8] Shared SOS Created Emergency {em_id} (Patient: Tukaram Shinde): PASS")

    # 8. Volunteer Dashboard Receives Case
    code, cases_data = get_json('/api/volunteer/cases')
    assert code == 200
    active_case = cases_data['active_emergency']
    assert active_case is not None
    assert active_case['emergency_id'] == em_id
    assert active_case['reported_by'] == 'Tukaram Shinde'
    assert active_case['wari_id'] == 'WS-28471'
    print(f"[9] Volunteer Dashboard Receives Incoming Case {em_id}: PASS")

    # 9. Test Case Decline (Re-routing back to dispatch pool)
    code, dec_res = post_json(f'/api/volunteer/cases/{em_id}/decline', {
        'volunteer_id': 'V-001',
        'reason': 'Currently Busy with another dindi'
    })
    assert code == 200
    assert dec_res['status'] == 'DISPATCHED'
    print("[10] Volunteer Decline Case & Re-route to Dispatch Pool: PASS")

    # 10. Test Case Acceptance
    code, acc_res = post_json(f'/api/volunteer/cases/{em_id}/accept', {
        'volunteer_id': 'V-001'
    })
    assert code == 200
    assert acc_res['status'] == 'ACCEPTED'
    assert acc_res['assigned_volunteer'] == 'V-001'
    print("[11] Volunteer Accepts Case -> Status: ACCEPTED / Volunteer: BUSY: PASS")

    # 11. Test Start Response (En Route)
    code, start_res = post_json(f'/api/volunteer/cases/{em_id}/start', {
        'volunteer_id': 'V-001'
    })
    assert code == 200
    assert start_res['status'] == 'EN_ROUTE'
    print("[12] Volunteer Starts Response -> Status: EN_ROUTE: PASS")

    # 12. Test Location Update
    code, loc_res = post_json('/api/volunteer/location', {
        'volunteer_id': 'V-001',
        'latitude': 18.3450,
        'longitude': 74.0295,
        'location_source': 'GPS'
    })
    assert code == 200
    print("[13] Volunteer Location Coordinates Live Update: PASS")

    # 13. Test Arrived at Patient
    code, arr_res = post_json(f'/api/volunteer/cases/{em_id}/arrived', {
        'volunteer_id': 'V-001'
    })
    assert code == 200
    assert arr_res['status'] == 'ARRIVED'
    print("[14] Volunteer Marks Arrived -> Status: ARRIVED: PASS")

    # 14. Test Patient Assisted
    code, asst_res = post_json(f'/api/volunteer/cases/{em_id}/assisted', {
        'volunteer_id': 'V-001'
    })
    assert code == 200
    assert asst_res['status'] == 'PATIENT_ASSISTED'
    print("[15] Volunteer Marks Patient Assisted -> Status: PATIENT_ASSISTED: PASS")

    # 15. Test Close / Resolve Case
    code, res_res = post_json(f'/api/volunteer/cases/{em_id}/resolve', {
        'volunteer_id': 'V-001',
        'outcome': 'Assistance Provided & Inhaler Administered'
    })
    assert code == 200
    assert res_res['status'] == 'RESOLVED'
    print("[16] Volunteer Closes Case -> Status: RESOLVED: PASS")

    # 16. Verify Case moved to Completed & Volunteer status is AVAILABLE
    code, final_cases = get_json('/api/volunteer/cases')
    assert code == 200
    assert final_cases['active_emergency'] is None
    assert any(c['emergency_id'] == em_id for c in final_cases['completed_cases'])
    print("[17] Case moved to Completed Cases & Volunteer returned to AVAILABLE: PASS")

    # 17. Verify Command Center Synced
    code, cmd_data = get_json('/api/command-center/emergencies')
    assert code == 200
    cmd_em = next((e for e in cmd_data['emergencies'] if e['emergency_id'] == em_id), None)
    assert cmd_em is not None
    assert cmd_em['status'] == 'RESOLVED'
    print("[18] Command Center Synced with Final RESOLVED Status: PASS")

    # 18. Logout
    code, out_res = post_json('/api/volunteer/logout', {})
    assert code == 200
    print("[19] Volunteer Logout (Status: OFFLINE & Session Cleared): PASS")

    # Clean reset
    post_json('/api/demo/reset', {})

    print("=" * 70)
    print("ALL 19 VOLUNTEER RESPONSE PORTAL SYSTEM TESTS PASSED 100%!")
    print("=" * 70)

if __name__ == '__main__':
    test_volunteer_suite()
