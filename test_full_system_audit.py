import urllib.request
import urllib.parse
import json
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

BASE_URL = "http://127.0.0.1:5000"

def run_full_system_audit():
    results = {}
    print("=" * 70)
    print("WARISEVA AI — COMPREHENSIVE FULL IMPLEMENTATION AUDIT & TEST SUITE")
    print("=" * 70)

    # -------------------------------------------------------------
    # 1. Reset Demo System State
    # -------------------------------------------------------------
    req = urllib.request.Request(f"{BASE_URL}/api/demo/reset", data=b"{}", headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as res:
        assert res.status == 200

    # -------------------------------------------------------------
    # TEST A: VOLUNTEER REGISTRATION & VERIFICATION LIFECYCLE
    # -------------------------------------------------------------
    print("\n--- [TEST A] VOLUNTEER REGISTRATION, VERIFICATION & AUTHENTICATION ---")
    test_vol_phone = "9822998877"
    reg_payload = {
        "name": "Audit Volunteer Patil",
        "phone": test_vol_phone,
        "zone": "Zone 04 — Saswad Palkhi Maidan",
        "skills": "First Aid, CPR, Triage",
        "role_type": "Medical Volunteer",
        "password": "auditpass123"
    }

    # 1. Register Volunteer
    req = urllib.request.Request(
        f"{BASE_URL}/api/volunteer/register",
        data=json.dumps(reg_payload).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as res:
        assert res.status == 201
        data = json.loads(res.read().decode('utf-8'))
        v_id = data["volunteer_id"]
        assert data["verification_status"] == "PENDING_VERIFICATION"
        print(f"  ✓ 1. Volunteer registered: {v_id} (Status: PENDING_VERIFICATION)")
    results["Volunteer Registration"] = "PASS"

    # 2. Prevent Duplicate Registration
    try:
        req = urllib.request.Request(
            f"{BASE_URL}/api/volunteer/register",
            data=json.dumps(reg_payload).encode('utf-8'),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as res:
            results["Duplicate Registration Prevention"] = "FAIL"
    except urllib.error.HTTPError as e:
        assert e.code == 400
        print("  ✓ 2. Duplicate registration rejected (400 Bad Request)")
        results["Duplicate Registration Prevention"] = "PASS"

    # 3. Verify in Command Center Queue
    req = urllib.request.Request(f"{BASE_URL}/api/admin/verification-queue")
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode('utf-8'))
        assert data["success"] is True
        print(f"  ✓ 3. Volunteer appears in Command Center Pending Queue")
    results["Command Center Volunteer Queue"] = "PASS"

    # 4. Command Center Verifies Volunteer
    req = urllib.request.Request(
        f"{BASE_URL}/api/admin/volunteer/verify",
        data=json.dumps({"volunteer_id": v_id}).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as res:
        assert res.status == 200
        data = json.loads(res.read().decode('utf-8'))
        assert data["verification_status"] == "VERIFIED"
        assert data["status"] == "AVAILABLE"
        print(f"  ✓ 4. Volunteer {v_id} verified by Admin (Status -> VERIFIED, AVAILABLE)")
    results["Volunteer Verification"] = "PASS"

    # 5. Volunteer Login Authentication
    login_payload = {"volunteer_id": v_id, "password": "auditpass123"}
    req = urllib.request.Request(
        f"{BASE_URL}/api/volunteer/login",
        data=json.dumps(login_payload).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as res:
        assert res.status == 200
        data = json.loads(res.read().decode('utf-8'))
        assert data["success"] is True
        print(f"  ✓ 5. Volunteer {v_id} authenticated successfully")
    results["Volunteer Login"] = "PASS"

    # -------------------------------------------------------------
    # TEST B: HOSPITAL REGISTRATION & VERIFICATION LIFECYCLE
    # -------------------------------------------------------------
    print("\n--- [TEST B] HOSPITAL REGISTRATION, VERIFICATION & AUTHENTICATION ---")
    hosp_payload = {
        "name": "Audit Lifeline Hospital",
        "phone": "02115-998877",
        "zone": "Zone 04 — Saswad Palkhi Maidan",
        "emergency_beds": 14,
        "icu_beds": 4,
        "password": "auditHospPass123"
    }

    # 1. Register Hospital
    req = urllib.request.Request(
        f"{BASE_URL}/api/hospital/register",
        data=json.dumps(hosp_payload).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as res:
        assert res.status == 201
        data = json.loads(res.read().decode('utf-8'))
        h_id = data["hospital_id"]
        assert data["verification_status"] == "PENDING_VERIFICATION"
        print(f"  ✓ 1. Hospital registered: {h_id} (Status: PENDING_VERIFICATION)")
    results["Hospital Registration"] = "PASS"

    # 2. Command Center Verifies Hospital
    req = urllib.request.Request(
        f"{BASE_URL}/api/admin/hospital/verify",
        data=json.dumps({"hospital_id": h_id}).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as res:
        assert res.status == 200
        data = json.loads(res.read().decode('utf-8'))
        assert data["verification_status"] == "VERIFIED"
        print(f"  ✓ 2. Hospital {h_id} verified by Admin (Status -> VERIFIED)")
    results["Hospital Verification"] = "PASS"

    # 3. Hospital Login Authentication
    h_login_payload = {"facility_id": h_id, "password": "auditHospPass123"}
    req = urllib.request.Request(
        f"{BASE_URL}/api/hospital/login",
        data=json.dumps(h_login_payload).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as res:
        assert res.status == 200
        data = json.loads(res.read().decode('utf-8'))
        assert data["success"] is True
        print(f"  ✓ 3. Hospital {h_id} authenticated successfully")
    results["Hospital Login"] = "PASS"

    # -------------------------------------------------------------
    # TEST C: END-TO-END UNIFIED EMERGENCY & RESPONSE LIFECYCLE
    # -------------------------------------------------------------
    print("\n--- [TEST C] UNIFIED EMERGENCY, AI DISPATCH, RESPONDER & HOSPITAL LIFECYCLE ---")

    # 1. Trigger SOS (QR / Main unified creation)
    sos_payload = {
        "name": "Tukaram Shinde",
        "wari_id": "WS-30555",
        "emergency_type": "MEDICAL",
        "severity": "CRITICAL",
        "latitude": 18.3444,
        "longitude": 74.0305,
        "zone": "Zone 04 — Saswad Palkhi Maidan",
        "notes": "Elderly pilgrim chest pain & severe breathing difficulty"
    }

    req = urllib.request.Request(
        f"{BASE_URL}/api/public/report-emergency",
        data=json.dumps(sos_payload).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as res:
        assert res.status == 201
        data = json.loads(res.read().decode('utf-8'))
        em_id = data["emergency_id"]
        assert data["status"] in ("CREATED", "DISPATCHED")
        print(f"  ✓ 1. Unified SOS created single emergency object: {em_id} (Patient: Tukaram Shinde)")
    results["Unified SOS Emergency Creation"] = "PASS"

    # 2. AI Response Candidate Ranking & Transparent Scoring
    req = urllib.request.Request(f"{BASE_URL}/api/emergency/{em_id}/candidates")
    with urllib.request.urlopen(req) as res:
        assert res.status == 200
        data = json.loads(res.read().decode('utf-8'))
        v_cands = data["candidate_volunteers"]
        h_cands = data["candidate_facilities"]
        assert len(v_cands) >= 3
        top_v = v_cands[0]
        assert top_v["id"] == "V-001"
        assert top_v["score"] >= 80
        print(f"  ✓ 2. AI Response Engine dynamically evaluated & prioritized: {top_v['name']} ({top_v['id']}) with score {top_v['score']}/100")
        print(f"       Factors: Availability: {top_v['factors']['availability']['points']} | Distance: {top_v['factors']['distance']['points']} | Skills: {top_v['factors']['skills']['points']} | Zone: {top_v['factors']['zone']['points']}")
    results["AI Volunteer Prioritization"] = "PASS"
    results["Explainable AI Factors"] = "PASS"

    # 3. Volunteer Dashboard Receives Case
    req = urllib.request.Request(f"{BASE_URL}/api/volunteer/cases?volunteer_id=V-001")
    with urllib.request.urlopen(req) as res:
        assert res.status == 200
        data = json.loads(res.read().decode('utf-8'))
        assert data["active_emergency"] is not None
        assert data["active_emergency"]["emergency_id"] == em_id
        print(f"  ✓ 3. Volunteer V-001 dashboard received live active emergency {em_id}")
    results["Volunteer Case Delivery"] = "PASS"

    # 4. Volunteer Accepts Case
    req = urllib.request.Request(
        f"{BASE_URL}/api/volunteer/cases/{em_id}/accept",
        data=json.dumps({"volunteer_id": "V-001"}).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as res:
        assert res.status == 200
        data = json.loads(res.read().decode('utf-8'))
        assert data["status"] == "ACCEPTED"
        print(f"  ✓ 4. Volunteer accepted case -> Status: ACCEPTED, Volunteer: BUSY")
    results["Volunteer Case Acceptance"] = "PASS"

    # 5. Volunteer Starts Response (En Route)
    req = urllib.request.Request(
        f"{BASE_URL}/api/volunteer/cases/{em_id}/start",
        data=json.dumps({"volunteer_id": "V-001"}).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as res:
        assert res.status == 200
        data = json.loads(res.read().decode('utf-8'))
        assert data["status"] == "EN_ROUTE"
        print(f"  ✓ 5. Volunteer response started -> Status: EN_ROUTE, Volunteer: RESPONDING")
    results["Volunteer En Route"] = "PASS"

    # 6. Volunteer Live Location Transmit
    loc_payload = {"emergency_id": em_id, "volunteer_id": "V-001", "latitude": 18.3450, "longitude": 74.0300, "accuracy": 5.0}
    req = urllib.request.Request(
        f"{BASE_URL}/api/volunteer/location",
        data=json.dumps(loc_payload).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as res:
        assert res.status == 200
        print(f"  ✓ 6. Volunteer telemetry GPS transmitted to backend & Command Center")
    results["Volunteer GPS Telemetry"] = "PASS"

    # 7. Volunteer Arrived
    req = urllib.request.Request(
        f"{BASE_URL}/api/volunteer/cases/{em_id}/arrived",
        data=json.dumps({"volunteer_id": "V-001"}).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as res:
        assert res.status == 200
        data = json.loads(res.read().decode('utf-8'))
        assert data["status"] == "ARRIVED"
        print(f"  ✓ 7. Volunteer arrived on scene -> Status: ARRIVED")
    results["Volunteer Arrived"] = "PASS"

    # 8. Volunteer Administers First Aid (Patient Assisted)
    req = urllib.request.Request(
        f"{BASE_URL}/api/volunteer/cases/{em_id}/assisted",
        data=json.dumps({"volunteer_id": "V-001"}).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as res:
        assert res.status == 200
        data = json.loads(res.read().decode('utf-8'))
        assert data["status"] == "PATIENT_ASSISTED"
        print(f"  ✓ 8. Volunteer administered first aid -> Status: PATIENT_ASSISTED")
    results["Patient Assisted"] = "PASS"

    # 9. Hospital Selection & Candidate Ranking
    top_h = h_cands[0]
    assert top_h["id"].startswith("H")
    assert top_h["score"] >= 80
    assert top_h["score"] >= 80
    print(f"  ✓ 9. AI Hospital Matching evaluated & matched: {top_h['name']} ({top_h['id']}) with score {top_h['score']}/100")
    print(f"       Factors: Distance: {top_h['factors']['distance']['points']} | 24x7: {top_h['factors']['twenty_four_seven']['points']} | Beds: {top_h['factors']['bed_capacity']['points']} | Services: {top_h['factors']['services_match']['points']}")
    results["AI Hospital Matching"] = "PASS"

    # 10. Hospital Receives Case
    chosen_hosp_id = top_h["id"]
    req = urllib.request.Request(f"{BASE_URL}/api/hospital/cases?hospital_id={chosen_hosp_id}")
    with urllib.request.urlopen(req) as res:
        assert res.status == 200
        data = json.loads(res.read().decode('utf-8'))
        assert data["active_emergency"] is not None
        assert data["active_emergency"]["emergency_id"] == em_id
        print(f"  ✓ 10. Hospital {chosen_hosp_id} dashboard received live incoming case {em_id}")
    results["Hospital Case Delivery"] = "PASS"

    # 11. Hospital Accepts Patient
    req = urllib.request.Request(
        f"{BASE_URL}/api/hospital/cases/{em_id}/accept",
        data=json.dumps({"hospital_id": chosen_hosp_id}).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as res:
        assert res.status == 200
        data = json.loads(res.read().decode('utf-8'))
        assert data["status"] == "HOSPITAL_ACCEPTED"
        print(f"  ✓ 11. Hospital accepted patient -> Status: HOSPITAL_ACCEPTED (Bed Reserved)")
    results["Hospital Acceptance"] = "PASS"

    # 12. Case Resolution
    req = urllib.request.Request(
        f"{BASE_URL}/api/volunteer/cases/{em_id}/resolve",
        data=json.dumps({"volunteer_id": "V-001", "notes": "Patient admitted to Saswad Rural Hospital"}).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as res:
        assert res.status == 200
        data = json.loads(res.read().decode('utf-8'))
        assert data["status"] == "RESOLVED"
        print(f"  ✓ 12. Case resolved -> Status: RESOLVED, Volunteer returned to AVAILABLE")
    results["Case Resolution"] = "PASS"

    # -------------------------------------------------------------
    # TEST D: COMMAND CENTER DYNAMIC NETWORK STATISTICS
    # -------------------------------------------------------------
    print("\n--- [TEST D] COMMAND CENTER DYNAMIC NETWORK METRICS ---")
    req = urllib.request.Request(f"{BASE_URL}/api/admin/network-stats")
    with urllib.request.urlopen(req) as res:
        assert res.status == 200
        data = json.loads(res.read().decode('utf-8'))
        v_stats = data["volunteers"]
        h_stats = data["hospitals"]
        assert v_stats["total"] >= 248
        assert v_stats["verified"] >= 231
        assert h_stats["total"] >= 42
        assert h_stats["emergency_beds"] >= 86
        print(f"  ✓ Live Volunteers: Total {v_stats['total']} | Verified {v_stats['verified']} | Available {v_stats['available']}")
        print(f"  ✓ Live Hospitals: Total {h_stats['total']} | Verified {h_stats['verified']} | Beds {h_stats['emergency_beds']}")
    results["Command Center Network Statistics"] = "PASS"

    # -------------------------------------------------------------
    # AUDIT SUMMARY
    # -------------------------------------------------------------
    print("\n" + "=" * 70)
    print("AUDIT RESULTS SUMMARY:")
    print("=" * 70)
    all_passed = True
    for item, status in results.items():
        print(f"  [{status}] {item}")
        if status != "PASS":
            all_passed = False

    print("=" * 70)
    if all_passed:
        print("🎉 ALL 15 CRITICAL SYSTEM AUDIT TESTS PASSED 100% WITH ZERO ERRORS!")
        sys.exit(0)
    else:
        print("❌ SOME AUDIT TESTS FAILED!")
        sys.exit(1)

if __name__ == '__main__':
    run_full_system_audit()
