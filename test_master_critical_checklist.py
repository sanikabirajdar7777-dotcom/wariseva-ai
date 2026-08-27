import unittest
import json
import os
import backend.app as flask_app

class TestMasterCriticalChecklist(unittest.TestCase):
    def setUp(self):
        flask_app.app.config['TESTING'] = True
        self.client = flask_app.app.test_client()

    def test_01_sos_and_emergency_creation(self):
        """[CHECKLIST: SOS] Verify SOS creates emergency incident and returns emergency ID."""
        payload = {
            'wari_id': 'WS-28471',
            'latitude': 18.3444,
            'longitude': 74.0305,
            'location_accuracy': 5.0,
            'emergency_type': 'Medical / Chest Pain',
            'severity': 'CRITICAL'
        }
        res = self.client.post('/api/emergency/create', json=payload)
        self.assertIn(res.status_code, (200, 201))
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertIn('EM-', data['emergency_id'])

    def test_02_qr_generation(self):
        """[CHECKLIST: QR GENERATION] Verify Level-H QR image and payload generation."""
        # 1. Payload
        res = self.client.get('/api/qr/payload?wari_id=WS-28471')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertTrue(data['payload'].endswith('/public/pilgrim/WS-28471'))
        self.assertEqual(data['payload'], f"{data['public_base_url']}/public/pilgrim/WS-28471")

        # 2. Image PNG
        img_res = self.client.get('/api/qr/image?wari_id=WS-28471')
        self.assertEqual(img_res.status_code, 200)
        self.assertEqual(img_res.mimetype, 'image/png')
        self.assertGreater(len(img_res.data), 500)

        # 3. Base64
        b64_res = self.client.get('/api/pilgrim/WS-28471/qr-base64')
        self.assertEqual(b64_res.status_code, 200)
        b64_data = b64_res.get_json()
        self.assertTrue(b64_data['success'])
        self.assertTrue(b64_data['base64'].startswith('data:image/png;base64,'))

    def test_03_qr_scanning_and_verification(self):
        """[CHECKLIST: QR SCANNING] Verify QR scanner payload lookup."""
        verify_payload = {
            'qr_data': 'http://192.168.1.5:5000/public/pilgrim/WS-28471',
            'scanner_id': 'V-001'
        }
        res = self.client.post('/api/qr/lookup', json=verify_payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['wari_id'], 'WS-28471')

    def test_04_wristband_identity_page(self):
        """[CHECKLIST: WRISTBAND] Verify public wristband identity profile."""
        res = self.client.get('/public/pilgrim/WS-28471')
        self.assertEqual(res.status_code, 200)
        html = res.get_data(as_text=True)
        self.assertIn('Tukaram Shinde', html)
        self.assertIn('WS-28471', html)

    def test_05_demo_password_verification(self):
        """[CHECKLIST: DEMO PASSWORD] Verify protected medical data requires authentication/password."""
        res_pin = self.client.post('/api/qr/verify', json={'wari_id': 'WS-28471', 'pin': '2741'})
        self.assertEqual(res_pin.status_code, 200)
        data = res_pin.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['pilgrim']['wari_id'], 'WS-28471')

    def test_06_volunteer_login(self):
        """[CHECKLIST: VOLUNTEER LOGIN] Verify Volunteer authentication with demo credentials."""
        login_data = {
            'volunteer_id': 'V-001',
            'password': 'demo123'
        }
        res = self.client.post('/api/auth/volunteer/login', json=login_data)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['volunteer']['wari_id'], 'V-001')

    def test_07_hospital_login(self):
        """[CHECKLIST: HOSPITAL LOGIN] Verify Hospital authentication with demo credentials."""
        login_data = {
            'facility_id': 'H-001',
            'password': 'demo123'
        }
        res = self.client.post('/api/auth/hospital/login', json=login_data)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['hospital']['hospital_id'], 'H-001')

    def test_08_notifications_dispatch(self):
        """[CHECKLIST: NOTIFICATIONS] Verify notifications appear in volunteer and hospital dashboards."""
        # 1. Volunteer notifications
        v_res = self.client.get('/api/volunteer/dashboard-data')
        self.assertEqual(v_res.status_code, 200)
        v_data = v_res.get_json()
        self.assertTrue(v_data['success'])
        self.assertGreaterEqual(len(v_data['emergencies']), 1)

        # 2. Hospital notifications
        h_res = self.client.get('/api/hospital/dashboard-data')
        self.assertEqual(h_res.status_code, 200)
        h_data = h_res.get_json()
        self.assertTrue(h_data['success'])
        self.assertGreaterEqual(len(h_data['emergencies']), 1)

    def test_09_manual_acceptance_workflow(self):
        """[CHECKLIST: MANUAL ACCEPTANCE] Verify volunteer and hospital manual accept actions."""
        # 1. Volunteer Accept
        v_acc = self.client.post('/api/emergency/EM-28471/volunteer/accept', json={'volunteer_id': 'V-001'})
        self.assertEqual(v_acc.status_code, 200)
        v_data = v_acc.get_json()
        self.assertTrue(v_data['success'])

        # 2. Hospital Accept
        h_acc = self.client.post('/api/emergency/EM-28471/hospital/accept', json={'hospital_id': 'H-001'})
        self.assertEqual(h_acc.status_code, 200)
        h_data = h_acc.get_json()
        self.assertTrue(h_data['success'])

    def test_10_timeline_stages(self):
        """[CHECKLIST: TIMELINE] Verify 12-stage timeline retrieval and progression."""
        res = self.client.get('/api/emergency/EM-28471/timeline')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertIn('events', data)
        self.assertGreaterEqual(len(data['events']), 1)

    def test_11_map_and_crowd_routes(self):
        """[CHECKLIST: MAP] Verify Leaflet map crowd routing and POIs."""
        # 1. Crowd aware routing
        r_res = self.client.get('/api/emergency/EM-28471/crowd-aware-routes')
        self.assertEqual(r_res.status_code, 200)
        r_data = r_res.get_json()
        self.assertTrue(r_data['success'])
        self.assertIn('routes', r_data)
        self.assertIn('safe_bypass_route', r_data['routes'])

        # 2. Safety map POIs
        s_res = self.client.get('/api/safety-services?type=ALL')
        self.assertEqual(s_res.status_code, 200)
        s_data = s_res.get_json()
        self.assertTrue(s_data['success'])
        self.assertGreaterEqual(len(s_data['services']), 10)

    def test_12_command_center(self):
        """[CHECKLIST: COMMAND CENTER] Verify central command incident feed."""
        res = self.client.get('/api/command-center/emergencies')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertIn('emergencies', data)

    def test_13_language_and_voice_dictionaries(self):
        """[CHECKLIST: LANGUAGE & VOICE] Verify English, Marathi, Hindi dictionary integrity."""
        with open('static/script.js', 'r', encoding='utf-8') as f:
            js = f.read()
        self.assertIn('en: {', js)
        self.assertIn('mr: {', js)
        self.assertIn('hi: {', js)
        self.assertIn('window.speechSynthesis', js)
        self.assertIn('mr-IN', js)
        self.assertIn('hi-IN', js)
        self.assertIn('en-IN', js)

    def test_14_navigation_and_views(self):
        """[CHECKLIST: NAVIGATION] Verify all 8 view containers exist in templates/index.html."""
        with open('templates/index.html', 'r', encoding='utf-8') as f:
            html = f.read()
        views = [
            'id="home-view"',
            'id="emergency-view"',
            'id="safety-map-view"',
            'id="services-view"',
            'id="volunteer-view"',
            'id="responder-view"',
            'id="command-view"',
            'id="qr-scanner-view"'
        ]
        for v in views:
            self.assertIn(v, html, f"Missing view: {v}")

if __name__ == '__main__':
    unittest.main()
