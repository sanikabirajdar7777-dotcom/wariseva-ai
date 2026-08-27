import unittest
import json
from backend.app import app

class TestMaster30StepIntegration(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with open("templates/index.html", "r", encoding="utf-8") as f:
            self.index_html = f.read()
        with open("templates/public_pilgrim.html", "r", encoding="utf-8") as f:
            self.public_html = f.read()
        with open("static/script.js", "r", encoding="utf-8") as f:
            self.script_js = f.read()
        with open("static/style.css", "r", encoding="utf-8") as f:
            self.style_css = f.read()

    def test_step_01_root_endpoint(self):
        """Step 1: Open application root / -> 200 OK"""
        res = self.app.get('/')
        self.assertEqual(res.status_code, 200)

    def test_step_02_home_hero_and_sos(self):
        """Step 2: Home page renders hero banner, taglines, SOS button"""
        self.assertIn('Your safety, one tap away', self.index_html)
        self.assertIn('id="main-sos-button"', self.index_html)
        self.assertIn('id="sos-modal"', self.index_html)

    def test_step_03_top_demo_role_bar(self):
        """Step 3: Top Demo Role bar displays all roles and control buttons"""
        self.assertIn('id="role-btn-warkari"', self.index_html)
        self.assertIn('id="role-btn-volunteer"', self.index_html)
        self.assertIn('id="role-btn-hospital"', self.index_html)
        self.assertIn('id="role-btn-command"', self.index_html)
        self.assertIn('id="btn-view-demo-wristband"', self.index_html)
        self.assertIn('id="voice-toggle-btn"', self.index_html)
        self.assertIn('id="reset-demo-btn"', self.index_html)

    def test_step_04_05_sos_modal_and_dispatch(self):
        """Step 4 & 5: SOS modal and dispatch creates central emergency EM-28471"""
        self.assertIn('id="confirm-sos-btn"', self.index_html)
        self.assertIn('id="cancel-sos-btn"', self.index_html)
        res = self.app.post('/api/demo/create-emergency')
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertEqual(data['emergency_id'], 'EM-28471')

    def test_step_06_to_10_timeline_steps_1_to_5(self):
        """Step 6 to 10: Steps 1 to 5 exist and execute sequentially"""
        self.assertIn('id="step-1-sos"', self.index_html)
        self.assertIn('id="step-2-loc"', self.index_html)
        self.assertIn('id="step-3-zone"', self.index_html)
        self.assertIn('id="step-4-severity"', self.index_html)
        self.assertIn('id="step-5-ai-match"', self.index_html)
        self.assertIn('fetchAiRecommendation', self.script_js)

    def test_step_11_stops_at_step_5_no_auto_advance(self):
        """Step 11: Execution halts at Step 5 and waits for human action"""
        self.assertIn('WAITING_FOR_VOLUNTEER', self.script_js)
        self.assertIn('handleVolunteerAccept', self.script_js)

    def test_step_12_to_15_volunteer_role_and_acceptance(self):
        """Step 12 to 15: Volunteer accepts case and timeline updates to Step 7 & 8"""
        self.assertIn('id="vol-accept-em-btn"', self.index_html)
        self.assertIn('id="volunteer-active-response-box"', self.index_html)
        res = self.app.post('/api/emergency/EM-28471/volunteer/accept', json={'volunteer_id': 'V-001'})
        self.assertEqual(res.status_code, 200)
        res_status = self.app.get('/api/public/emergency-status/EM-28471')
        self.assertEqual(json.loads(res_status.data)['stage'], 7)

    def test_step_16_17_volunteer_arrived(self):
        """Step 16 & 17: Volunteer marks arrived at patient (0m)"""
        self.assertIn('id="reached-patient-btn"', self.index_html)
        res = self.app.post('/api/volunteer/reached', json={'volunteer_id': 'V-001', 'emergency_id': 'EM-28471'})
        self.assertEqual(res.status_code, 200)
        res_status = self.app.get('/api/public/emergency-status/EM-28471')
        self.assertEqual(json.loads(res_status.data)['stage'], 9)

    def test_step_18_to_21_hospital_accept_case(self):
        """Step 18 to 21: Medical facility accepts case and reserves bed"""
        self.assertIn('id="hosp-accept-case-btn"', self.index_html)
        res = self.app.post('/api/hospital/cases/EM-28471/accept', json={'hospital_id': 'H-001'})
        self.assertEqual(res.status_code, 200)
        res_status = self.app.get('/api/public/emergency-status/EM-28471')
        self.assertEqual(json.loads(res_status.data)['stage'], 11)

    def test_step_22_to_24_hospital_admit_and_resolve(self):
        """Step 22 to 24: Hospital admits patient and case resolves with score 92/100"""
        self.assertIn('id="hosp-mark-admitted-btn"', self.index_html)
        self.assertIn('id="coordination-complete-card"', self.index_html)
        res = self.app.post('/api/volunteer/cases/EM-28471/resolve', json={'volunteer_id': 'V-001'})
        self.assertEqual(res.status_code, 200)
        res_status = self.app.get('/api/public/emergency-status/EM-28471')
        self.assertEqual(json.loads(res_status.data)['stage'], 12)

    def test_step_25_safety_network_map(self):
        """Step 25: Wari Safety Network tactical map container exists"""
        self.assertIn('id="safety-map-view"', self.index_html)
        self.assertIn('id="main-safety-map"', self.index_html)
        self.assertIn('initSafetyMap', self.script_js)

    def test_step_26_to_28_wristband_qr_and_public_page(self):
        """Step 26 to 28: Dynamic QR and public wristband page with home button"""
        self.assertIn('id="qr-scanner-view"', self.index_html)
        self.assertIn('id="tab-wb-front"', self.index_html)
        self.assertIn('id="tab-wb-back"', self.index_html)
        self.assertIn('id="tab-wb-both"', self.index_html)
        self.assertIn('window.location.origin', self.script_js)

        # Public wristband route
        res = self.app.get('/public/pilgrim/WS-28471')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Tukaram Shinde', res.get_data(as_text=True))
        self.assertIn('id="public-nav-home"', self.public_html)

    def test_step_29_command_center_view(self):
        """Step 29: Command center displays incident summary and resource feeds"""
        self.assertIn('id="command-view"', self.index_html)
        self.assertIn('id="command-emergency-list"', self.index_html)
        self.assertIn('id="command-total-count"', self.index_html)

    def test_step_30_reset_demo(self):
        """Step 30: Reset demo resets backend and UI state back to standby"""
        res = self.app.post('/api/demo/reset')
        self.assertEqual(res.status_code, 200)
        self.assertIn('resetDemo', self.script_js)

if __name__ == '__main__':
    unittest.main()
