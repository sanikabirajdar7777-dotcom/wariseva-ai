"""
test_emergency_corridor_feature.py
Automated test suite verifying the Emergency Corridor: Crowd-Clearance Coordination feature.

Ensures:
1. Emergency Corridor card and request button exist in the Hospital / Medical Facility Portal.
2. Emergency Corridor dispatch desk and nearby volunteer list exist in the Command Centre.
3. Emergency Corridor urgent alert and progression buttons exist in the Volunteer Portal.
4. API endpoints support the complete lifecycle: REQUESTED -> ASSIGNED -> EN_ROUTE -> CLEARING -> CLEAR -> MOVING -> COMPLETED.
5. Strict preservation of existing SOS, QR scanning, Green Corridor, and role navigation.
"""

import unittest
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
import app as flask_app

class TestEmergencyCorridorFeature(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        flask_app.app.config['TESTING'] = True
        cls.client = flask_app.app.test_client()

        with open('templates/index.html', 'r', encoding='utf-8') as f:
            cls.html = f.read()
        with open('static/script.js', 'r', encoding='utf-8') as f:
            cls.js = f.read()
        with open('static/style.css', 'r', encoding='utf-8') as f:
            cls.css = f.read()

    def test_01_hospital_corridor_dom_elements(self):
        """Verify Emergency Corridor request card and telemetry in Hospital Portal."""
        self.assertIn('id="hospital-emergency-corridor-card"', self.html)
        self.assertIn('id="btn-hosp-request-corridor"', self.html)
        self.assertIn('REQUEST EMERGENCY CORRIDOR', self.html)
        self.assertIn('id="hosp-corridor-status-badge"', self.html)
        self.assertIn('id="hosp-corridor-amb"', self.html)
        self.assertIn('id="hosp-corridor-location"', self.html)
        self.assertIn('id="hosp-corridor-dest"', self.html)

    def test_02_command_center_corridor_dom_elements(self):
        """Verify Emergency Corridor dispatch desk and volunteer list in Command Centre."""
        self.assertIn('id="cmd-emergency-corridor-card"', self.html)
        self.assertIn('EMERGENCY CORRIDOR DISPATCH DESK', self.html)
        self.assertIn('id="btn-cmd-assign-corridor"', self.html)
        self.assertIn('id="btn-cmd-focus-corridor"', self.html)
        self.assertIn('id="btn-cmd-cancel-corridor"', self.html)
        self.assertIn('id="cmd-corridor-volunteers-list"', self.html)
        self.assertIn('Ramesh Kulkarni (V-001)', self.html)
        self.assertIn('Suresh Patil (V-002)', self.html)
        self.assertIn('Aniket Deshmukh (V-003)', self.html)

    def test_03_volunteer_corridor_dom_elements(self):
        """Verify Emergency Corridor alert and progression action buttons in Volunteer Portal."""
        self.assertIn('id="vol-emergency-corridor-card"', self.html)
        self.assertIn('URGENT: EMERGENCY CORRIDOR ASSIGNMENT', self.html)
        self.assertIn('id="btn-vol-corridor-accept"', self.html)
        self.assertIn('id="btn-vol-corridor-enroute"', self.html)
        self.assertIn('id="btn-vol-corridor-location"', self.html)
        self.assertIn('id="btn-vol-corridor-clearing"', self.html)
        self.assertIn('id="btn-vol-corridor-clear"', self.html)
        self.assertIn('id="btn-vol-corridor-moving"', self.html)
        self.assertIn('id="btn-vol-corridor-completed"', self.html)

    def test_04_corridor_api_lifecycle(self):
        """Verify the complete lifecycle of an Emergency Corridor through API endpoints."""
        # 1. Reset state
        res_reset = self.client.post('/api/emergency/EM-28471/corridor/reset')
        self.assertEqual(res_reset.status_code, 200)

        # 2. Get initial state
        res_get = self.client.get('/api/emergency/EM-28471/corridor')
        self.assertEqual(res_get.status_code, 200)
        c = res_get.get_json()['corridor']
        self.assertEqual(c['status'], 'IDLE')
        self.assertEqual(len(c['nearby_volunteers']), 3)

        # 3. Ambulance Requests Corridor
        res_req = self.client.post('/api/emergency/EM-28471/corridor/request')
        self.assertEqual(res_req.status_code, 200)
        c_req = res_req.get_json()['corridor']
        self.assertEqual(c_req['status'], 'REQUESTED')
        self.assertIn('Awaiting Command Centre', c_req['status_label'])

        # 4. Command Centre assigns volunteers
        res_assign = self.client.post('/api/emergency/EM-28471/corridor/assign', json={
            'volunteer_ids': ['V-001', 'V-002', 'V-003']
        })
        self.assertEqual(res_assign.status_code, 200)
        c_assign = res_assign.get_json()['corridor']
        self.assertEqual(c_assign['status'], 'ASSIGNED')
        self.assertEqual(len(c_assign['assigned_volunteers']), 3)

        # 5. Volunteers advance progression: EN_ROUTE -> CLEARING -> CLEAR -> MOVING -> COMPLETED
        for stage in ['EN_ROUTE', 'AT_LOCATION', 'CLEARING', 'CLEAR', 'MOVING', 'COMPLETED']:
            res_stage = self.client.post('/api/emergency/EM-28471/corridor/status', json={
                'status': stage,
                'actor': 'VOLUNTEER V-001'
            })
            self.assertEqual(res_stage.status_code, 200)
            self.assertEqual(res_stage.get_json()['corridor']['status'], stage)

    def test_05_js_and_css_corridor_integration(self):
        """Verify JavaScript functions and CSS scoped styles are present."""
        self.assertIn('loadEmergencyCorridorState', self.js)
        self.assertIn('renderEmergencyCorridorOnMap', self.js)
        self.assertIn('requestEmergencyCorridor', self.js)
        self.assertIn('assignCorridorVolunteers', self.js)
        self.assertIn('updateCorridorStatus', self.js)
        self.assertIn('.emergency-corridor-card', self.css)
        self.assertIn('.vol-emergency-corridor-card', self.css)
        self.assertIn('.cmd-emergency-corridor-card', self.css)
        self.assertIn('.ecc-step-btn', self.css)

    def test_06_existing_workflows_unaffected(self):
        """Verify that existing SOS, QR, and Green Corridor features remain completely functional."""
        # Check Green Corridor still works
        res_gc = self.client.get('/api/emergency/EM-28471/green-corridor')
        self.assertEqual(res_gc.status_code, 200)
        self.assertTrue(res_gc.get_json()['success'])

        # Check PIN verify still works via /api/qr/verify
        res_pin = self.client.post('/api/qr/verify', json={
            'wari_id': 'WS-28471',
            'pin': '2741',
            'volunteer_id': 'V-001'
        })
        self.assertEqual(res_pin.status_code, 200)
        self.assertTrue(res_pin.get_json()['success'])
        self.assertTrue(res_pin.get_json()['authorized'])

if __name__ == '__main__':
    unittest.main()
