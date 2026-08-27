import unittest
import json
from backend.app import app

class TestSOSExecutionEngine(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with open('static/script.js', 'r', encoding='utf-8') as f:
            self.script_js = f.read()

    def test_01_handle_sos_definition(self):
        """Verify handleSOS is central entry point for SOS creation and timeline start"""
        self.assertIn('function handleSOS()', self.script_js)
        self.assertIn('function setDemoEmergencyStage(stage)', self.script_js)
        self.assertIn('function setTimelineStep(stepNumber', self.script_js)
        self.assertIn('function resetDemo()', self.script_js)

    def test_02_sos_button_calls_handle_sos(self):
        """Verify confirmation modal and SOS triggers call handleSOS"""
        self.assertIn('handleSOS();', self.script_js)
        self.assertIn('confirmSosBtn', self.script_js)

    def test_03_shared_emergency_state_format(self):
        """Verify shared emergency state has id, wristbandId, status, currentStage, location, severity"""
        self.assertIn('id: "EM-28471"', self.script_js)
        self.assertIn('wristbandId: "WS-28471"', self.script_js)
        self.assertIn('status: "CREATED"', self.script_js)
        self.assertIn('currentStage: 1', self.script_js)
        self.assertTrue('severity: chosenSeverity' in self.script_js or 'severity: "CRITICAL"' in self.script_js)

    def test_04_sequential_steps_1_to_4_and_stop_for_volunteer(self):
        """Verify steps 1-4 are automated and stop for volunteer acceptance"""
        # Step 1: Immediately
        self.assertIn('setDemoEmergencyStage(1);', self.script_js)
        # Step 2: 1.5s
        self.assertIn('setDemoEmergencyStage(2);', self.script_js)
        # Step 3: 3.0s
        self.assertIn('setDemoEmergencyStage(3);', self.script_js)
        # Step 4: 4.5s
        self.assertIn('setDemoEmergencyStage(4);', self.script_js)
        # Step 7 Active (Waiting for volunteer)
        self.assertIn('WAITING_FOR_VOLUNTEER', self.script_js)

    def test_05_voice_narration_texts(self):
        """Verify exact voice phrases are spoken for stages"""
        self.assertIn('SOS received. Emergency registered.', self.script_js)
        self.assertIn('Exact location acquired.', self.script_js)
        self.assertIn('Wari zone identified. Saswad Palkhi Maidan.', self.script_js)
        self.assertIn('Emergency classified as critical.', self.script_js)
        self.assertIn('Volunteer has accepted the emergency.', self.script_js)
        self.assertIn('Volunteer has arrived at the emergency location.', self.script_js)
        self.assertIn('Hospital has accepted the case. Patient transfer initiated.', self.script_js)
        self.assertIn('Emergency response completed successfully.', self.script_js)

    def test_06_backend_endpoints_and_lifecycle(self):
        """Verify backend endpoints support the multi-role lifecycle"""
        # 1. Reset
        res_reset = self.app.post('/api/demo/reset')
        self.assertEqual(res_reset.status_code, 200)

        # 2. Create emergency via demo trigger
        res_create = self.app.post('/api/demo/create-emergency')
        self.assertEqual(res_create.status_code, 201)
        data_create = json.loads(res_create.data)
        self.assertEqual(data_create['emergency_id'], 'EM-28471')
        self.assertEqual(data_create['status'], 'CREATED')

        # 3. Verify public status returns stage
        res_pub = self.app.get('/api/public/emergency-status/EM-28471')
        self.assertEqual(res_pub.status_code, 200)
        data_pub = json.loads(res_pub.data)
        self.assertIn(data_pub['stage'], [4, 6])

        # 4. Volunteer accepts
        res_vacpt = self.app.post('/api/volunteer/cases/EM-28471/accept', json={'volunteer_id': 'V-001'})
        self.assertEqual(res_vacpt.status_code, 200)
        res_pub2 = self.app.get('/api/public/emergency-status/EM-28471')
        self.assertEqual(json.loads(res_pub2.data)['stage'], 7)

        # 5. Volunteer arrives
        res_varr = self.app.post('/api/volunteer/cases/EM-28471/arrived', json={'volunteer_id': 'V-001'})
        self.assertEqual(res_varr.status_code, 200)
        res_pub3 = self.app.get('/api/public/emergency-status/EM-28471')
        self.assertEqual(json.loads(res_pub3.data)['stage'], 9)

        # 6. Hospital accepts
        res_hacpt = self.app.post('/api/hospital/cases/EM-28471/accept', json={'hospital_id': 'H-001'})
        self.assertEqual(res_hacpt.status_code, 200)
        res_pub4 = self.app.get('/api/public/emergency-status/EM-28471')
        self.assertEqual(json.loads(res_pub4.data)['stage'], 11)

        # 7. Case resolved
        res_res = self.app.post('/api/volunteer/cases/EM-28471/resolve', json={'volunteer_id': 'V-001'})
        self.assertEqual(res_res.status_code, 200)
        res_pub5 = self.app.get('/api/public/emergency-status/EM-28471')
        self.assertEqual(json.loads(res_pub5.data)['stage'], 12)

if __name__ == '__main__':
    unittest.main()
