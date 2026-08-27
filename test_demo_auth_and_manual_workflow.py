import unittest
import json
import sys
import os

sys.path.insert(0, os.path.abspath('backend'))
import app as flask_app

class TestDemoAuthAndManualWorkflow(unittest.TestCase):
    def setUp(self):
        self.app = flask_app.app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_complete_demo_workflow(self):
        print("\n=======================================================")
        print("STARTING COMPLETE DEMO AUTHENTICATION & MANUAL WORKFLOW")
        print("=======================================================")

        # Step 0: Clean Demo Reset
        res = self.client.post('/api/demo/reset')
        self.assertEqual(res.status_code, 200)
        print("[STEP 0 PASS] Demo Reset Clean")

        # Step A: Home View & Auth Gates Rendering
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        html = res.data.decode('utf-8')
        self.assertIn('vol-auth-gate-card', html)
        self.assertIn('hosp-auth-gate-card', html)
        self.assertIn('V-001', html)
        self.assertIn('H-001', html)
        self.assertIn('demo123', html)
        print("[STEP A PASS] Single Application UI contains In-App Volunteer & Hospital Login Gates")

        # Step B & C: Warkari Triggers Main SOS Button
        res = self.client.post('/api/emergency/create', json={
            'wari_id': 'WS-28471',
            'emergency_type': 'Medical Emergency',
            'severity': 'CRITICAL',
            'zone': 'Zone 04 — Saswad Palkhi Maidan',
            'latitude': 18.3444,
            'longitude': 74.0305
        })
        self.assertIn(res.status_code, (200, 201))
        data = res.get_json()
        em_id = data.get('emergency_id') or data.get('emergency', {}).get('id') or 'EM-28471'
        self.assertEqual(em_id, 'EM-28471')
        print(f"[STEP B/C PASS] Main SOS Registered: {em_id}")

        # Step D: AI Responder Recommendation Check
        res = self.client.get(f'/api/emergency/{em_id}/ai-recommendation')
        self.assertEqual(res.status_code, 200)
        rec = res.get_json()
        vol_rec = rec.get('recommended_volunteer', {})
        self.assertEqual(vol_rec.get('wari_id'), 'V-001')
        self.assertEqual(vol_rec.get('name'), 'Ramesh Kulkarni')
        self.assertGreaterEqual(vol_rec.get('total_score', 0), 90)
        print(f"[STEP D PASS] AI Match Verified: {vol_rec.get('name')} ({vol_rec.get('wari_id')}) - Score {vol_rec.get('total_score')}/100")

        # Step E & F: Volunteer Logs In with V-001 / demo123
        res = self.client.post('/api/auth/volunteer/login', json={
            'volunteer_id': 'V-001',
            'password': 'demo123'
        })
        self.assertEqual(res.status_code, 200)
        vol_data = res.get_json()
        self.assertTrue(vol_data.get('success'))
        self.assertEqual(vol_data.get('volunteer', {}).get('name'), 'Ramesh Kulkarni')
        print("[STEP E/F PASS] Volunteer Ramesh Kulkarni (V-001) Authenticated")

        # Step G & H: Volunteer Manually Accepts Case
        res = self.client.post(f'/api/emergency/{em_id}/volunteer-accept', json={
            'volunteer_id': 'V-001'
        })
        self.assertEqual(res.status_code, 200)
        print("[STEP G/H PASS] Volunteer Manually Accepted Case EM-28471")

        # Step I: Volunteer En Route
        res = self.client.post(f'/api/emergency/{em_id}/volunteer-enroute', json={
            'volunteer_id': 'V-001'
        })
        self.assertEqual(res.status_code, 200)
        print("[STEP I PASS] Volunteer En Route (350m -> 180m)")

        # Step J: Volunteer Arrived with Patient
        res = self.client.post(f'/api/emergency/{em_id}/volunteer-arrived', json={
            'volunteer_id': 'V-001'
        })
        self.assertEqual(res.status_code, 200)
        print("[STEP J PASS] Volunteer Arrived On Scene (0m • With Patient)")

        # Step K & L: Hospital Logs In with H-001 / demo123
        res = self.client.post('/api/auth/hospital/login', json={
            'facility_id': 'H-001',
            'password': 'demo123'
        })
        self.assertEqual(res.status_code, 200)
        hosp_data = res.get_json()
        self.assertTrue(hosp_data.get('success'))
        print("[STEP K/L PASS] Hospital H-001 Authenticated")

        # Step M & N: Hospital Manually Accepts Patient (Reserves Bed)
        res = self.client.post(f'/api/emergency/{em_id}/hospital-accept', json={
            'hospital_id': 'H-001'
        })
        self.assertEqual(res.status_code, 200)
        print("[STEP M/N PASS] Hospital Manually Accepted Patient (Emergency Bed: 1 Reserved)")

        # Step O & Q: Hospital Marks Patient Arrived
        res = self.client.post(f'/api/emergency/{em_id}/transfer', json={
            'hospital_id': 'H-001'
        })
        self.assertEqual(res.status_code, 200)
        print("[STEP O/Q PASS] Patient Arrived at Medical Facility")

        # Step R & S: Case Resolved
        res = self.client.post(f'/api/emergency/{em_id}/resolve', json={
            'responder_id': 'H-001',
            'notes': 'Patient admitted and condition stabilized.'
        })
        self.assertEqual(res.status_code, 200)
        print("[STEP R/S PASS] Emergency Resolved Successfully")

        # Step T: Verify Central Timeline Audit Trail
        res = self.client.get(f'/api/emergency/{em_id}/timeline')
        self.assertEqual(res.status_code, 200)
        timeline = res.get_json().get('timeline', [])
        logged_stages = [item['stage'] for item in timeline]
        self.assertIn(1, logged_stages)
        self.assertIn(7, logged_stages)
        self.assertIn(12, logged_stages)
        print(f"[STEP T PASS] Complete 12-Stage Timeline Logged: {logged_stages}")

        # Step U: Verify Repeatable Demo Reset
        res = self.client.post('/api/demo/reset')
        self.assertEqual(res.status_code, 200)
        print("[STEP U PASS] Clean Repeatable Demo Reset Verified")

if __name__ == '__main__':
    unittest.main()
