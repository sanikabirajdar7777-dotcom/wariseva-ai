import unittest
import json
import os
import sys

# Ensure backend directory is in python path
sys.path.insert(0, os.path.abspath('.'))
from backend.app import app, get_db_connection, init_db

class TestFullIntegratedEmergencyWorkflow(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        init_db()

    def test_full_manual_emergency_lifecycle(self):
        print("\n--- 1. Testing Reset API ---")
        res = self.client.post('/api/demo/reset')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get('success'))

        print("--- 2. Testing Main SOS Creation ---")
        sos_payload = {
            'wari_id': 'WS-28471',
            'name': 'Tukaram Shinde',
            'mobile': '+91 98221 28471',
            'emergency_contact': '+91 98220 99881',
            'blood_group': 'B+',
            'dindi_no': 'Dindi 27',
            'latitude': 18.3444,
            'longitude': 74.0305,
            'zone': 'Zone 04 — Saswad Palkhi Maidan',
            'emergency_type': 'Medical Emergency',
            'severity': 'CRITICAL'
        }
        res = self.client.post('/api/emergency/create', json=sos_payload)
        self.assertIn(res.status_code, [200, 201])
        sos_res = res.get_json()
        self.assertTrue(sos_res.get('success'))
        em_id = sos_res.get('emergency_id')
        self.assertEqual(em_id, 'EM-28471')
        print(f"Created emergency: {em_id} for {sos_res.get('patient_name')}")

        print("--- 3. Testing Active Emergencies API ---")
        res = self.client.get('/api/emergencies/active')
        self.assertEqual(res.status_code, 200)
        active_data = res.get_json()
        self.assertTrue(active_data.get('success'))
        emergencies = active_data.get('emergencies', [])
        self.assertGreaterEqual(len(emergencies), 1)
        found = next((e for e in emergencies if e['emergency_id'] == 'EM-28471'), None)
        self.assertIsNotNone(found)
        self.assertEqual(found['patient_name'], 'Tukaram Shinde')
        self.assertEqual(found['current_status'], 'CREATED')
        self.assertEqual(found['volunteer_status'], 'WAITING')
        self.assertEqual(found['hospital_status'], 'PENDING')

        print("--- 4. Testing Volunteer Authentication (demo123) ---")
        res = self.client.post('/api/volunteer/login', json={'volunteer_id': 'V-001', 'password': 'demo123'})
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.get_json().get('success'))

        print("--- 5. Testing Manual Volunteer Accept ---")
        res = self.client.post(f'/api/emergency/{em_id}/volunteer-accept', json={'volunteer_id': 'V-001'})
        self.assertEqual(res.status_code, 200)
        vol_accept_res = res.get_json()
        self.assertTrue(vol_accept_res.get('success'))
        self.assertEqual(vol_accept_res.get('volunteer_status'), 'ACCEPTED')

        print("--- 6. Testing Manual Volunteer En Route ---")
        res = self.client.post(f'/api/emergency/{em_id}/volunteer-enroute', json={'volunteer_id': 'V-001'})
        self.assertEqual(res.status_code, 200)
        enroute_res = res.get_json()
        self.assertTrue(enroute_res.get('success'))
        self.assertEqual(enroute_res.get('volunteer_status'), 'EN_ROUTE')

        print("--- 7. Testing Manual Volunteer Arrived ---")
        res = self.client.post(f'/api/emergency/{em_id}/volunteer-arrived', json={'volunteer_id': 'V-001'})
        self.assertEqual(res.status_code, 200)
        arrived_res = res.get_json()
        self.assertTrue(arrived_res.get('success'))
        self.assertEqual(arrived_res.get('volunteer_status'), 'ARRIVED')

        print("--- 8. Testing Hospital Authentication (demo123) ---")
        res = self.client.post('/api/hospital/login', json={'hospital_id': 'H-001', 'password': 'demo123'})
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.get_json().get('success'))

        print("--- 9. Testing Manual Hospital Accept ---")
        res = self.client.post(f'/api/emergency/{em_id}/hospital-accept', json={'hospital_id': 'H-001'})
        self.assertEqual(res.status_code, 200)
        hosp_accept_res = res.get_json()
        self.assertTrue(hosp_accept_res.get('success'))
        self.assertEqual(hosp_accept_res.get('hospital_status'), 'ACCEPTED')

        print("--- 10. Testing Manual Hospital Patient Transfer ---")
        res = self.client.post(f'/api/emergency/{em_id}/transfer')
        self.assertEqual(res.status_code, 200)
        transfer_res = res.get_json()
        self.assertTrue(transfer_res.get('success'))
        self.assertEqual(transfer_res.get('hospital_status'), 'TRANSFERRED')

        print("--- 11. Testing Manual Case Resolution ---")
        res = self.client.post(f'/api/emergency/{em_id}/resolve')
        self.assertEqual(res.status_code, 200)
        resolve_res = res.get_json()
        self.assertTrue(resolve_res.get('success'))
        self.assertEqual(resolve_res.get('status'), 'RESOLVED')
        self.assertEqual(resolve_res.get('volunteer_status'), 'COMPLETED')

        print("--- 12. Testing Timeline Audit Trail ---")
        res = self.client.get(f'/api/emergency/{em_id}/timeline')
        self.assertEqual(res.status_code, 200)
        tl_data = res.get_json()
        self.assertTrue(tl_data.get('success'))
        events = tl_data.get('events', [])
        stages = [ev['stage'] for ev in events]
        print(f"Logged timeline stages: {stages}")
        self.assertIn(1, stages) # Created
        self.assertIn(7, stages) # Vol Accept
        self.assertIn(8, stages) # Vol En Route
        self.assertIn(9, stages) # Vol Arrived
        self.assertIn(10, stages) # Hosp Accept
        self.assertIn(11, stages) # Transfer
        self.assertIn(12, stages) # Resolved

        print("--- 13. Testing QR Wristband Trigger ---")
        qr_payload = {
            'wari_id': 'WS-28471',
            'emergency_type': 'MEDICAL',
            'reporter_type': 'QR_PUBLIC_USER',
            'latitude': 18.3444,
            'longitude': 74.0305,
            'location_source': 'GPS'
        }
        res = self.client.post('/api/public/report-emergency', json=qr_payload)
        self.assertIn(res.status_code, [200, 201])
        qr_res = res.get_json()
        self.assertTrue(qr_res.get('success'))
        self.assertEqual(qr_res.get('emergency_id'), 'EM-28471')
        print("QR Wristband emergency successfully unified with EM-28471 workflow!")

if __name__ == '__main__':
    unittest.main()
