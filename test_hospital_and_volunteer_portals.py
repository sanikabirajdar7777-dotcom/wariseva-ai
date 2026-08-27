import urllib.request
import urllib.parse
import json
import http.cookiejar
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

BASE_URL = "http://127.0.0.1:5000"

def run_tests():
    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
    urllib.request.install_opener(opener)

    passed = 0
    total = 0

    def test(desc, fn):
        nonlocal passed, total
        total += 1
        print(f"[{total:02d}] Testing {desc}...", end=" ", flush=True)
        try:
            fn()
            print("[PASS]")
            passed += 1
        except Exception as e:
            print(f"[FAIL]: {e}")

    # 1. Main Landing Page Portals Section
    def test_home_portals():
        req = urllib.request.Request(f"{BASE_URL}/")
        with opener.open(req) as res:
            assert res.status == 200
            html = res.read().decode('utf-8')
            assert "JOIN THE WARI SAFETY NETWORK" in html
            assert "VOLUNTEER" in html
            assert "HOSPITAL / MEDICAL FACILITY" in html
            assert "COMMAND CENTER" in html
            assert "/volunteer/register" in html
            assert "/volunteer/login" in html
            assert "/hospital/register" in html
            assert "/hospital/login" in html
    test("Landing Page 'JOIN THE WARI SAFETY NETWORK' section with 3 cards", test_home_portals)

    # 2. Volunteer Register Page
    def test_vol_register_page():
        req = urllib.request.Request(f"{BASE_URL}/volunteer/register")
        with opener.open(req) as res:
            assert res.status == 200
            html = res.read().decode('utf-8')
            assert "VOLUNTEER" in html
            assert "vol-register-form" in html
    test("GET /volunteer/register page rendering", test_vol_register_page)

    # 3. Volunteer Register API
    new_vol_id = None
    def test_vol_register_api():
        nonlocal new_vol_id
        payload = {
            "name": "Eknath Maharaj Sevak",
            "phone": "9876543210",
            "wari_id": "V-00482",
            "role_type": "Medical Volunteer",
            "skills": "First Aid, CPR, Triage",
            "zone": "Zone 04 — Saswad Palkhi Maidan",
            "password": "volpass123"
        }
        req = urllib.request.Request(
            f"{BASE_URL}/api/volunteer/register",
            data=json.dumps(payload).encode('utf-8'),
            headers={"Content-Type": "application/json"}
        )
        with opener.open(req) as res:
            assert res.status == 201
            data = json.loads(res.read().decode('utf-8'))
            assert data["success"] is True
            new_vol_id = data.get("volunteer_id") or data.get("wari_id")
            assert new_vol_id is not None
    test("POST /api/volunteer/register endpoint", test_vol_register_api)

    # 4. Volunteer Login API
    def test_vol_login():
        payload = {"volunteer_id": "V-001", "password": "VOL001"}
        req = urllib.request.Request(
            f"{BASE_URL}/api/volunteer/login",
            data=json.dumps(payload).encode('utf-8'),
            headers={"Content-Type": "application/json"}
        )
        with opener.open(req) as res:
            assert res.status == 200
            data = json.loads(res.read().decode('utf-8'))
            assert data["success"] is True
            assert (data["volunteer"].get("wari_id") == "V-001" or data["volunteer"].get("id") == "V-001")
    test("POST /api/volunteer/login with V-001/VOL001", test_vol_login)

    # 5. Volunteer Profile Page
    def test_vol_profile():
        req = urllib.request.Request(f"{BASE_URL}/volunteer/profile")
        with opener.open(req) as res:
            assert res.status == 200
            html = res.read().decode('utf-8')
            assert "V-001" in html
            assert "VERIFIED VOLUNTEER" in html
    test("GET /volunteer/profile page (Authenticated)", test_vol_profile)

    # 6. Volunteer Dashboard Page
    def test_vol_dashboard():
        req = urllib.request.Request(f"{BASE_URL}/volunteer/dashboard")
        with opener.open(req) as res:
            assert res.status == 200
            html = res.read().decode('utf-8')
            assert "V-001" in html
            assert "RESPONDER" in html or "VOLUNTEER" in html or "Dashboard" in html
    test("GET /volunteer/dashboard page (Authenticated)", test_vol_dashboard)

    # 7. Hospital Register Page
    def test_hosp_register_page():
        req = urllib.request.Request(f"{BASE_URL}/hospital/register")
        with opener.open(req) as res:
            assert res.status == 200
            html = res.read().decode('utf-8')
            assert "REGISTER MEDICAL FACILITY" in html
            assert "hosp-register-form" in html
    test("GET /hospital/register page rendering", test_hosp_register_page)

    # 8. Hospital Register API
    new_hosp_id = None
    def test_hosp_register_api():
        nonlocal new_hosp_id
        payload = {
            "name": "Saswad Trauma & Emergency Clinic",
            "facility_type": "Emergency Center",
            "license_no": "MH-MED-28472",
            "phone": "02115-224455",
            "emergency_phone": "9870011111",
            "address": "Pune-Saswad Bypass Road, Purandar",
            "city": "Saswad",
            "zone": "Zone 04 — Saswad Palkhi Maidan",
            "emergency_beds": 15,
            "icu_beds": 4,
            "ambulance": True,
            "twenty_four_seven": True,
            "capabilities": "Emergency Care, Trauma, ICU",
            "admin_name": "Dr. Arvind Shinde",
            "password": "HOSP001"
        }
        req = urllib.request.Request(
            f"{BASE_URL}/api/hospital/register",
            data=json.dumps(payload).encode('utf-8'),
            headers={"Content-Type": "application/json"}
        )
        with opener.open(req) as res:
            assert res.status == 201
            data = json.loads(res.read().decode('utf-8'))
            assert data["success"] is True
            assert data["verification_status"] == "PENDING_VERIFICATION"
            new_hosp_id = data["hospital_id"]
    test("POST /api/hospital/register endpoint", test_hosp_register_api)

    # 9. Hospital Login API
    def test_hosp_login():
        payload = {"facility_id": "H-001", "password": "HOSP001"}
        req = urllib.request.Request(
            f"{BASE_URL}/api/hospital/login",
            data=json.dumps(payload).encode('utf-8'),
            headers={"Content-Type": "application/json"}
        )
        with opener.open(req) as res:
            assert res.status == 200
            data = json.loads(res.read().decode('utf-8'))
            assert data["success"] is True
            assert data["hospital_id"] == "H-001"
    test("POST /api/hospital/login with H-001/HOSP001", test_hosp_login)

    # 10. Hospital Dashboard Page
    def test_hosp_dashboard():
        req = urllib.request.Request(f"{BASE_URL}/hospital/dashboard")
        with opener.open(req) as res:
            assert res.status == 200
            html = res.read().decode('utf-8')
            assert "Saswad" in html or "H-001" in html
            assert "Live Bed & Ambulance Capacity" in html
    test("GET /hospital/dashboard page (Authenticated)", test_hosp_dashboard)

    # 11. Hospital Profile Page
    def test_hosp_profile():
        req = urllib.request.Request(f"{BASE_URL}/hospital/profile")
        with opener.open(req) as res:
            assert res.status == 200
            html = res.read().decode('utf-8')
            assert "Saswad" in html or "H-001" in html
            assert "VERIFIED MEDICAL FACILITY" in html
    test("GET /hospital/profile page (Authenticated)", test_hosp_profile)

    # 12. Hospital Capacity Update API
    def test_hosp_capacity():
        payload = {"hospital_id": "H-001", "emergency_beds": 14, "icu_beds": 3}
        req = urllib.request.Request(
            f"{BASE_URL}/api/hospital/capacity",
            data=json.dumps(payload).encode('utf-8'),
            headers={"Content-Type": "application/json"}
        )
        with opener.open(req) as res:
            assert res.status == 200
            data = json.loads(res.read().decode('utf-8'))
            assert data["success"] is True
            assert data["available_beds"] == 14
            assert data["icu_beds"] == 3
    test("POST /api/hospital/capacity endpoint", test_hosp_capacity)

    # 13. Hospital Status API
    def test_hosp_status():
        payload = {"hospital_id": "H-001", "status": "ACCEPTING"}
        req = urllib.request.Request(
            f"{BASE_URL}/api/hospital/status",
            data=json.dumps(payload).encode('utf-8'),
            headers={"Content-Type": "application/json"}
        )
        with opener.open(req) as res:
            assert res.status == 200
            data = json.loads(res.read().decode('utf-8'))
            assert data["success"] is True
            assert data["status"] == "ACCEPTING"
    test("POST /api/hospital/status endpoint", test_hosp_status)

    # 14. Admin Verification Queue API
    def test_admin_verification_queue():
        req = urllib.request.Request(f"{BASE_URL}/api/admin/verification-queue")
        with opener.open(req) as res:
            assert res.status == 200
            data = json.loads(res.read().decode('utf-8'))
            assert data["success"] is True
            assert "pending_volunteers" in data
            assert "pending_hospitals" in data
            assert "verified_volunteers" in data
            assert "verified_hospitals" in data
    test("GET /api/admin/verification-queue endpoint", test_admin_verification_queue)

    # 15. Admin Verify Volunteer API
    def test_admin_verify_vol():
        if not new_vol_id:
            return
        payload = {"volunteer_id": new_vol_id}
        req = urllib.request.Request(
            f"{BASE_URL}/api/admin/volunteer/verify",
            data=json.dumps(payload).encode('utf-8'),
            headers={"Content-Type": "application/json"}
        )
        with opener.open(req) as res:
            assert res.status == 200
            data = json.loads(res.read().decode('utf-8'))
            assert data["success"] is True
            assert data["verification_status"] == "VERIFIED"
            assert data["status"] == "AVAILABLE"
    test("POST /api/admin/volunteer/verify endpoint", test_admin_verify_vol)

    # 16. Admin Verify Hospital API
    def test_admin_verify_hosp():
        if not new_hosp_id:
            return
        payload = {"hospital_id": new_hosp_id}
        req = urllib.request.Request(
            f"{BASE_URL}/api/admin/hospital/verify",
            data=json.dumps(payload).encode('utf-8'),
            headers={"Content-Type": "application/json"}
        )
        with opener.open(req) as res:
            assert res.status == 200
            data = json.loads(res.read().decode('utf-8'))
            assert data["success"] is True
            assert data["verification_status"] == "VERIFIED"
    test("POST /api/admin/hospital/verify endpoint", test_admin_verify_hosp)

    # 17. Hospital Active Cases API
    def test_hosp_cases():
        req = urllib.request.Request(f"{BASE_URL}/api/hospital/cases")
        with opener.open(req) as res:
            assert res.status == 200
            data = json.loads(res.read().decode('utf-8'))
            assert data["success"] is True
            assert "active_emergency" in data
    test("GET /api/hospital/cases endpoint", test_hosp_cases)

    # 18. Hospital Accept Patient Case API
    def test_hosp_accept_case():
        payload = {"hospital_id": "H-001"}
        req = urllib.request.Request(
            f"{BASE_URL}/api/hospital/cases/EM-28471/accept",
            data=json.dumps(payload).encode('utf-8'),
            headers={"Content-Type": "application/json"}
        )
        with opener.open(req) as res:
            assert res.status == 200
            data = json.loads(res.read().decode('utf-8'))
            assert data["success"] is True
            assert data["hospital_status"] == "ACCEPTED"
    test("POST /api/hospital/cases/EM-28471/accept endpoint", test_hosp_accept_case)

    # 19. Hospital Decline / Re-route Case API
    def test_hosp_decline_case():
        payload = {"hospital_id": "H-001", "reason": "No ICU beds"}
        req = urllib.request.Request(
            f"{BASE_URL}/api/hospital/cases/EM-28471/decline",
            data=json.dumps(payload).encode('utf-8'),
            headers={"Content-Type": "application/json"}
        )
        with opener.open(req) as res:
            assert res.status == 200
            data = json.loads(res.read().decode('utf-8'))
            assert data["success"] is True
            assert "re_routed_to" in data
    test("POST /api/hospital/cases/EM-28471/decline (Re-routing) endpoint", test_hosp_decline_case)

    # 20. Hospital Logout API
    def test_hosp_logout():
        req = urllib.request.Request(
            f"{BASE_URL}/api/hospital/logout",
            data=json.dumps({}).encode('utf-8'),
            headers={"Content-Type": "application/json"}
        )
        with opener.open(req) as res:
            assert res.status == 200
            data = json.loads(res.read().decode('utf-8'))
            assert data["success"] is True
    test("POST /api/hospital/logout endpoint", test_hosp_logout)

    print("\n=======================================================")
    print(f"TEST RUN COMPLETE: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("=======================================================")

    if passed == total:
        print("ALL TESTS PASSED PERFECTLY!")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    run_tests()
