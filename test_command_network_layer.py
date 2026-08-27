import os
import sys
import io
import json
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from backend.app import app

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def run_tests():
    client = app.test_client()
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

    # 1. Admin Network Stats API
    def test_network_stats():
        res = client.get('/api/admin/network-stats')
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert "volunteers" in data
        assert "hospitals" in data
        assert data["volunteers"]["total"] >= 248
        assert data["volunteers"]["verified"] >= 231
        assert data["volunteers"]["available"] >= 184
        assert data["hospitals"]["total"] >= 42
        assert data["hospitals"]["verified"] >= 38
        assert data["hospitals"]["emergency_beds"] >= 86
    test("GET /api/admin/network-stats aggregated metrics", test_network_stats)

    # 2. Verification Queue API
    def test_verification_queue():
        res = client.get('/api/admin/verification-queue')
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert "pending_volunteers" in data
        assert "pending_hospitals" in data
        assert len(data["pending_volunteers"]) >= 1
        assert len(data["pending_hospitals"]) >= 1
    test("GET /api/admin/verification-queue lists", test_verification_queue)

    # 3. Volunteer Verification API
    def test_verify_volunteer():
        res = client.post('/api/admin/volunteer/verify', json={"volunteer_id": "V-00123"})
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert data["verification_status"] == "VERIFIED"
    test("POST /api/admin/volunteer/verify authorization", test_verify_volunteer)

    # 4. Volunteer Suspension API
    def test_suspend_volunteer():
        res = client.post('/api/admin/volunteer/suspend', json={"volunteer_id": "V-00123"})
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert data["verification_status"] == "SUSPENDED"
    test("POST /api/admin/volunteer/suspend", test_suspend_volunteer)

    # 5. Volunteer Detail Inspector API
    def test_volunteer_detail():
        res = client.get('/api/admin/volunteers/V-001')
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert data["volunteer"]["wari_id"] == "V-001"
        assert "Ramesh Kulkarni" in data["volunteer"]["name"]
    test("GET /api/admin/volunteers/V-001 profile inspector", test_volunteer_detail)

    # 6. Hospital Verification API
    def test_verify_hospital():
        res = client.post('/api/admin/hospital/verify', json={"hospital_id": "H-00124"})
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert data["verification_status"] == "VERIFIED"
    test("POST /api/admin/hospital/verify authorization", test_verify_hospital)

    # 7. Hospital Detail Inspector API
    def test_hospital_detail():
        res = client.get('/api/admin/hospitals/H-001')
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert ("Saswad" in data["hospital"]["name"] or "WariSeva" in data["hospital"]["name"] or "Medical" in data["hospital"]["name"])
    test("GET /api/admin/hospitals/H-001 facility inspector", test_hospital_detail)

    # 8. AI Candidates Ranking & Explainable Scoring API
    def test_emergency_candidates():
        res = client.get('/api/emergency/EM-30555/candidates')
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert len(data["candidate_volunteers"]) >= 3
        top_v = data["candidate_volunteers"][0]
        assert top_v["id"] == "V-001"
        assert top_v["score"] >= 90
        assert "availability" in top_v["factors"]
        assert "distance" in top_v["factors"]
        assert "skills" in top_v["factors"]
        assert "zone" in top_v["factors"]
        assert "workload" in top_v["factors"]
        top_h = data["candidate_facilities"][0]
        assert top_h["id"] in ("H-001", "HOSP-001", "H-002", "HOSP-002")
        assert top_h["score"] >= 85
    test("GET /api/emergency/EM-30555/candidates (Explainable AI reasoning)", test_emergency_candidates)

    # 9. HTML Structure Verification for Command Center Tabs & Modals
    def test_html_command_layer():
        res = client.get('/')
        assert res.status_code == 200
        html = res.data.decode('utf-8')
        assert 'id="cmd-tab-volunteers"' in html
        assert 'id="cmd-tab-hospitals"' in html
        assert 'id="cmd-tab-incident-dive"' in html
        assert 'id="cmd-tab-alerts"' in html
        assert 'id="cmd-run-demo-btn"' in html
        assert 'id="why-responder-modal"' in html
        assert 'id="why-facility-modal"' in html
        assert 'id="vol-detail-modal"' in html
        assert 'id="hosp-detail-modal"' in html
        assert 'id="dive-timeline-list"' in html
    test("Index HTML Command Center Tabs & Modals presence", test_html_command_layer)

    print("\n=======================================================")
    print(f"COMMAND NETWORK LAYER TEST RUN: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("=======================================================")

    if passed == total:
        print("ALL TESTS PASSED PERFECTLY!")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    run_tests()
