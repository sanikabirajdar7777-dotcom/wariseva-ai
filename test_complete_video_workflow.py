import unittest
import json
import re
from backend.app import app

class TestVideoSOSDemonstrationWorkflow(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_01_home_and_confirmation_modal(self):
        """1-4: Home page contains SOS button, Safety ID, and confirmation modal with DISPATCH SOS"""
        res = self.app.get('/')
        self.assertEqual(res.status_code, 200)
        html = res.get_data(as_text=True)
        self.assertIn('id="main-sos-button"', html)
        self.assertIn('id="sos-modal"', html)
        self.assertIn('Trigger Emergency SOS?', html)
        self.assertIn('id="cancel-sos-btn"', html)
        self.assertIn('id="confirm-sos-btn"', html)
        self.assertIn('DISPATCH SOS', html)
        self.assertIn('WS-28471', html)

    def test_02_emergency_page_identity_and_map_elements(self):
        """5-7: Emergency page remains active, shows map container, legend, and patient telemetry"""
        res = self.app.get('/')
        html = res.get_data(as_text=True)
        self.assertIn('id="emergency-view"', html)
        self.assertIn('id="emergency-live-map"', html)
        self.assertIn('🔴 Patient (You)', html)
        self.assertIn('🔵 Volunteer (First Contact)', html)
        self.assertIn('🟠 Medical Responder (Ambulance)', html)
        self.assertIn('🟢 Safe Bypass Corridor', html)
        self.assertIn('Tukaram Shinde', html)
        self.assertIn('Zone 04 — Saswad Palkhi Maidan', html)
        self.assertIn('18.3444, 74.0305', html)

    def test_03_twelve_stage_timeline_in_html(self):
        """8-27: 12-Stage timeline definitions match video specification exactly"""
        res = self.app.get('/')
        html = res.get_data(as_text=True)
        self.assertIn('📊 Emergency Response Timeline (12 Stages)', html)
        for i in range(1, 13):
            self.assertTrue(f'id="step-{i}-' in html or f'step-{i}' in html, f"Missing Step {i}")
        
        self.assertIn('SOS Sent & Registered', html)
        self.assertIn('Exact Location Acquired', html)
        self.assertIn('Wari Zone Identified', html)
        self.assertIn('Emergency Severity Classified', html)
        self.assertIn('AI Responder Recommendation', html)
        self.assertIn('Volunteer Alert Sent', html)
        self.assertIn('Volunteer Accepted', html)
        self.assertIn('Volunteer En Route', html)
        self.assertIn('Volunteer Arrived', html)
        self.assertIn('AI Hospital Recommendation', html)
        self.assertIn('Hospital Transfer / Patient Expected', html)
        self.assertIn('Emergency Resolved', html)

    def test_04_ai_response_engine_and_completion_card(self):
        """16-17 & 26: AI Match Score 94/100 and Coordination Completion Card 92/100"""
        res = self.app.get('/')
        html = res.get_data(as_text=True)
        self.assertIn('AI RESPONSE ENGINE', html)
        self.assertIn('94', html)
        self.assertIn('Ramesh Kulkarni', html)
        self.assertIn('id="coordination-complete-card"', html)
        self.assertIn('RESPONSE COORDINATED', html)
        self.assertIn('92', html)

    def test_05_centralized_demo_state_engine_in_js(self):
        """Rule 14: Centralized demoEmergencyStage engine in script.js"""
        with open('static/script.js', 'r', encoding='utf-8') as f:
            js = f.read()
        self.assertIn('function setDemoEmergencyStage(stage)', js)
        self.assertIn('function runFullSimulation()', js)
        self.assertIn('function resetDemo()', js)
        self.assertIn('speechSynthesis.cancel()', js)
        self.assertIn('en-IN', js)
        for stage in range(1, 13):
            self.assertIn(f'case {stage}:', js)

    def test_06_wristband_home_navigation(self):
        """Section 13: Wristband page and modal have persistent Home button and tabs"""
        res = self.app.get('/public/pilgrim/WS-28471')
        self.assertEqual(res.status_code, 200)
        html = res.get_data(as_text=True)
        self.assertIn('Home', html)
        self.assertIn('public-nav-home', html)
        self.assertIn('WS-28471', html)

        res_home = self.app.get('/')
        html_home = res_home.get_data(as_text=True)
        self.assertIn('FRONT SIDE', html_home)
        self.assertIn('BACK SIDE', html_home)
        self.assertIn('SHOW BOTH', html_home)
        self.assertIn('wb-modal-home-btn', html_home)

if __name__ == '__main__':
    unittest.main()
