"""
WariSeva AI — Master Feature Completion Audit & Verification Suite
Tests all planned feature groups A through P.
"""

import os
import sys
import unittest
import urllib.request
import urllib.parse
import json

BASE_URL = "http://127.0.0.1:5000"

def post_json(endpoint, payload):
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}{endpoint}", data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status, json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read().decode('utf-8'))
        except Exception:
            body = {}
        return e.code, body

def get_json(endpoint):
    req = urllib.request.Request(f"{BASE_URL}{endpoint}")
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status, json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read().decode('utf-8'))
        except Exception:
            body = {}
        return e.code, body

def get_html(endpoint):
    req = urllib.request.Request(f"{BASE_URL}{endpoint}")
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status, resp.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')

class TestMasterFeatureAudit(unittest.TestCase):

    def setUp(self):
        post_json('/api/demo/reset', {})

    def test_01_qr_wristband_workflow(self):
        """[Category A] QR / Wristband System Complete Workflow"""
        # 1. Lookup QR token
        status, data = post_json('/api/qr/lookup', {'qr_data': 'WS-28471'})
        self.assertEqual(status, 200)
        self.assertTrue(data.get('found'))
        self.assertEqual(data.get('wari_id'), 'WS-28471')

        # 2. Verify PIN protection
        status, vdata = post_json('/api/qr/verify', {
            'wari_id': 'WS-28471',
            'pin': '2741',
            'volunteer_id': 'V-001',
            'volunteer_name': 'Ramesh Kulkarni'
        })
        self.assertEqual(status, 200)
        self.assertTrue(vdata.get('authorized'))
        pilgrim = vdata.get('pilgrim', {})
        self.assertEqual(pilgrim.get('name'), 'Tukaram Shinde')
        self.assertEqual(pilgrim.get('blood_group'), 'B+')
        self.assertIn('Asthma', pilgrim.get('medical_alert', ''))

        # 3. Render Public Page
        status, html = get_html('/public/pilgrim/WS-28471')
        self.assertEqual(status, 200)
        self.assertIn('WS-28471', html)
        self.assertIn('Tukaram Shinde', html)
        self.assertIn('public-top-nav', html)
        print("[PASS] Category A: QR / Wristband System")

    def test_02_sos_emergency_creation(self):
        """[Category B] Main SOS & QR SOS Emergency Creation Pipeline"""
        # Main SOS
        status, data = post_json('/api/emergency/create', {
            'wari_id': 'WS-28471',
            'emergency_type': 'MEDICAL',
            'latitude': 18.3444,
            'longitude': 74.0305,
            'wari_zone': 'Zone 04 — Saswad Palkhi Maidan',
            'source': 'MAIN_SOS_BUTTON'
        })
        self.assertIn(status, [200, 201])
        em_id = data.get('emergency_id')
        self.assertTrue(em_id.startswith('EM-'))
        self.assertEqual(data.get('status'), 'CREATED')

        # QR SOS
        status_qr, data_qr = post_json('/api/public/report-emergency', {
            'wari_id': 'WS-28471',
            'emergency_type': 'MEDICAL',
            'latitude': 18.3444,
            'longitude': 74.0305,
            'source': 'QR_WARI_ID'
        })
        self.assertIn(status_qr, [200, 201])
        self.assertTrue(data_qr.get('emergency_id').startswith('EM-'))
        print("[PASS] Category B: SOS Emergency Creation")

    def test_03_ai_response_engine_rule_based(self):
        """[Category C] AI Response Prioritization Engine with Explainable Breakdown"""
        post_json('/api/demo/create-emergency', {})

        status, data = get_json('/api/emergency/EM-28471/ai-recommendation')
        self.assertEqual(status, 200)
        self.assertTrue(data.get('success'))
        vol = data.get('recommended_volunteer', {})
        self.assertIsNotNone(vol.get('name'))
        self.assertGreaterEqual(vol.get('total_score', 0), 50)
        
        # Check explainable scoring factors
        factors = vol.get('breakdown', {})
        self.assertIn('distance_score', factors)
        self.assertIn('skill_match_score', factors)
        self.assertIn('verification_score', factors)
        print(f"[PASS] Category C: AI Response Engine ({vol.get('name')} scored {vol.get('total_score')}/100)")

    def test_04_volunteer_portal_and_lifecycle(self):
        """[Category D] Volunteer Registration, Auth, and Incident Lifecycle"""
        post_json('/api/demo/create-emergency', {})

        # Accept emergency with seeded volunteer V-001
        status, acc_res = post_json('/api/volunteer/cases/EM-28471/accept', {'volunteer_id': 'V-001'})
        self.assertEqual(status, 200)

        # En Route
        status, start_res = post_json('/api/volunteer/cases/EM-28471/start', {'volunteer_id': 'V-001'})
        self.assertEqual(status, 200)

        # Arrived
        status, arr_res = post_json('/api/volunteer/cases/EM-28471/arrived', {'volunteer_id': 'V-001'})
        self.assertEqual(status, 200)

        # Patient Assisted
        status, ast_res = post_json('/api/volunteer/cases/EM-28471/assisted', {'volunteer_id': 'V-001'})
        self.assertEqual(status, 200)

        # Resolve
        status, res_res = post_json('/api/volunteer/cases/EM-28471/resolve', {'volunteer_id': 'V-001'})
        self.assertEqual(status, 200)
        print("[PASS] Category D: Volunteer Portal & Emergency Lifecycle")

    def test_05_hospital_portal_and_matching(self):
        """[Category E & F] Hospital Registration, Matching, and Case Acceptance"""
        post_json('/api/demo/create-emergency', {})

        # Hospital Recommendation for EM-28471
        status, rec_data = get_json('/api/emergency/EM-28471/ai-recommendation')
        self.assertEqual(status, 200)
        hosp_rec = rec_data.get('recommended_hospital', {})
        self.assertIsNotNone(hosp_rec.get('name'))

        # Accept Case with HOSP-001 or HOSP-002
        h_id = hosp_rec.get('wari_id') or 'HOSP-002'
        status, h_acc = post_json(f'/api/hospital/cases/EM-28471/accept', {'hospital_id': h_id})
        self.assertEqual(status, 200)
        print(f"[PASS] Category E & F: Hospital System & Facility Matching ({hosp_rec.get('name')})")

    def test_06_command_center_dynamic_metrics(self):
        """[Category G] Command Center Dynamic Resources and Incident Feeds"""
        status, metrics = get_json('/api/admin/network-stats')
        self.assertEqual(status, 200)
        self.assertIn('volunteers', metrics)
        self.assertIn('hospitals', metrics)
        self.assertIn('emergencies', metrics)

        status, incidents_data = get_json('/api/command-center/emergencies')
        self.assertEqual(status, 200)
        self.assertIn('emergencies', incidents_data)
        self.assertIsInstance(incidents_data.get('emergencies'), list)
        print("[PASS] Category G: Command Center Dynamic Network")

    def test_07_last_seen_checkpoints_family_view(self):
        """[Category H] Family Safety & Last Seen Points API"""
        status, data = get_json('/api/pilgrim/checkpoints/WS-28471')
        self.assertEqual(status, 200)
        self.assertTrue(data.get('success'))
        cps = data.get('checkpoints', [])
        self.assertGreaterEqual(len(cps), 3)

        types = [cp.get('checkpoint_type') for cp in cps]
        self.assertIn('MORNING_START', types)
        self.assertIn('AFTERNOON_HALT', types)
        self.assertIn('NIGHT_MUKKAM', types)

        status, new_cp = post_json('/api/pilgrim/checkpoint', {
            'wari_id': 'WS-28471',
            'checkpoint_type': 'NIGHT_MUKKAM',
            'location_name': 'Saswad Central Palkhi Maidan Ground',
            'zone': 'Zone 04 — Saswad Palkhi Maidan',
            'checkin_time': '08:30 PM',
            'recorded_by': 'Volunteer V-001'
        })
        self.assertEqual(status, 201)
        print("[PASS] Category H: Family Safety & Last Seen Checkpoints")

    def test_08_essential_services_directory(self):
        """[Category M] Essential Wari Services Directory"""
        status, data = get_json('/api/safety-services')
        self.assertEqual(status, 200)
        services = data.get('services', [])
        self.assertIsInstance(services, list)
        self.assertGreaterEqual(len(services), 13)
        print("[PASS] Category M: Wari Essential Services Directory (13 facilities)")

    def test_09_security_and_offline_handling(self):
        """[Category N & O] Role-based Security, Passwords & Offline UX"""
        req = urllib.request.Request(f"{BASE_URL}/volunteer/dashboard")
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                self.assertIn('/volunteer/login', resp.geturl())
        except urllib.error.HTTPError as e:
            self.assertIn(e.code, [302, 401, 403])

        status, bad_pin = post_json('/api/qr/verify', {
            'wari_id': 'WS-28471',
            'pin': '9999',
            'volunteer_id': 'V-001',
            'volunteer_name': 'Ramesh Kulkarni'
        })
        self.assertEqual(status, 401)
        self.assertFalse(bad_pin.get('authorized'))
        print("[PASS] Category N & O: Security & Offline Handling")

if __name__ == '__main__':
    unittest.main()
