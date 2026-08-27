import unittest
import json
from backend.app import app, get_db_connection

class TestMultiRoleEmergencyLifecycle(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_complete_multirole_lifecycle_flow(self):
        """
        Tests the entire Warkari -> Volunteer -> Hospital -> Case Resolved lifecycle:
        1. Warkari presses SOS -> Emergency Created (EM-28471) & Timeline Starts
        2. Notification sent to Volunteer -> Volunteer Logs In & Views Active Emergency
        3. Volunteer Accepts Case -> Status changes to ACCEPTED
        4. Volunteer En Route -> Status EN_ROUTE
        5. Volunteer Arrived -> Status ARRIVED (With Patient)
        6. Hospital Alerted -> Hospital Logs In & Views Case
        7. Hospital Accepts Case -> Bed Reserved & Patient Expected
        8. Patient Transfer -> Ambulance in Transit
        9. Case Resolved -> Status RESOLVED & Response Coordinated
        """
        # Step 1: Warkari Presses SOS -> Emergency Created
        res_create = self.app.post('/api/demo/create-emergency')
        self.assertIn(res_create.status_code, [200, 201])
        data_create = json.loads(res_create.data)
        self.assertTrue(data_create['success'])
        em_id = data_create['emergency_id']
        self.assertEqual(em_id, 'EM-28471')

        # Verify incident is visible in Command Center
        res_cmd = self.app.get('/api/command-center/emergencies')
        self.assertEqual(res_cmd.status_code, 200)
        data_cmd = json.loads(res_cmd.data)
        self.assertTrue(any(e['emergency_id'] == em_id for e in data_cmd['emergencies']))

        # Step 2: Volunteer Alert & Login
        # Volunteer logs in with test account V-001 (Ramesh Kulkarni)
        res_vlogin = self.app.post('/api/volunteer/login', json={
            'volunteer_id': 'V-001',
            'password': 'VOL001'
        })
        self.assertEqual(res_vlogin.status_code, 200)
        data_vlogin = json.loads(res_vlogin.data)
        self.assertTrue(data_vlogin['success'])
        self.assertEqual(data_vlogin['volunteer']['id'], 'V-001')

        # Volunteer checks available active emergency
        res_vcases = self.app.get('/api/volunteer/cases')
        self.assertEqual(res_vcases.status_code, 200)
        data_vcases = json.loads(res_vcases.data)
        self.assertTrue(data_vcases['success'])
        self.assertIsNotNone(data_vcases['active_emergency'])
        self.assertEqual(data_vcases['active_emergency']['emergency_id'], em_id)

        # Step 3: Volunteer Accepts Case
        res_vacpt = self.app.post(f'/api/volunteer/cases/{em_id}/accept')
        self.assertEqual(res_vacpt.status_code, 200)
        data_vacpt = json.loads(res_vacpt.data)
        self.assertTrue(data_vacpt['success'])

        # Step 4: Volunteer En Route
        res_vstart = self.app.post(f'/api/volunteer/cases/{em_id}/start')
        self.assertEqual(res_vstart.status_code, 200)
        data_vstart = json.loads(res_vstart.data)
        self.assertTrue(data_vstart['success'])

        # Step 5: Volunteer Arrived with Patient
        res_varr = self.app.post(f'/api/volunteer/cases/{em_id}/arrived')
        self.assertEqual(res_varr.status_code, 200)
        data_varr = json.loads(res_varr.data)
        self.assertTrue(data_varr['success'])

        # Step 6: Hospital Alert & Login
        # Hospital logs in with test account H-001 (Saswad Rural Hospital)
        res_hlogin = self.app.post('/api/hospital/login', json={
            'facility_id': 'H-001',
            'password': 'HOSP001'
        })
        self.assertEqual(res_hlogin.status_code, 200)
        data_hlogin = json.loads(res_hlogin.data)
        self.assertTrue(data_hlogin['success'])

        # Hospital checks pending incoming cases
        res_hcases = self.app.get('/api/hospital/cases')
        self.assertEqual(res_hcases.status_code, 200)
        data_hcases = json.loads(res_hcases.data)
        self.assertTrue(data_hcases['success'])
        self.assertIsNotNone(data_hcases['active_emergency'])
        self.assertEqual(data_hcases['active_emergency']['emergency_id'], em_id)

        # Step 7: Hospital Accepts Case & Reserves Bed
        res_hacpt = self.app.post(f'/api/hospital/cases/{em_id}/accept')
        self.assertEqual(res_hacpt.status_code, 200)
        data_hacpt = json.loads(res_hacpt.data)
        self.assertTrue(data_hacpt['success'])

        # Step 8: Patient Transfer & Resolution
        res_resolve = self.app.post(f'/api/volunteer/cases/{em_id}/resolve')
        self.assertEqual(res_resolve.status_code, 200)
        data_resolve = json.loads(res_resolve.data)
        self.assertTrue(data_resolve['success'])

        # Step 9: Final Database & Command Center Verification
        conn = get_db_connection()
        row = conn.execute("SELECT status FROM emergencies WHERE emergency_id = ?", (em_id,)).fetchone()
        conn.close()
        self.assertIsNotNone(row)
        self.assertEqual(row['status'], 'RESOLVED')

if __name__ == '__main__':
    unittest.main()
