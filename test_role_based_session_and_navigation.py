"""
test_role_based_session_and_navigation.py
Automated verification for role-based session isolation, entry points, and logout workflows.
"""

import unittest
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
import app as flask_app

class TestRoleBasedSessionAndNavigation(unittest.TestCase):
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

    def test_01_landing_and_warkari_logout_elements_exist(self):
        """Verify Landing screen, Warkari Dashboard, and Warkari LOGOUT elements."""
        self.assertIn('id="first-screen-role-selection"', self.html)
        self.assertIn('id="warkari-user-dashboard"', self.html)
        self.assertIn('id="warkari-logout-btn"', self.html)
        self.assertIn('id="btn-switch-role-from-warkari"', self.html)

    def test_02_volunteer_and_hospital_logout_and_back_elements_exist(self):
        """Verify Volunteer and Hospital top logout and login back buttons exist."""
        self.assertIn('id="vol-top-logout-btn"', self.html)
        self.assertIn('id="vol-login-back-btn"', self.html)
        self.assertIn('id="vol-back-to-roles-btn"', self.html)
        self.assertIn('id="hosp-top-logout-btn"', self.html)
        self.assertIn('id="hosp-login-back-btn"', self.html)
        self.assertIn('id="hosp-back-to-roles-btn"', self.html)

    def test_03_js_session_and_logout_engine(self):
        """Verify JavaScript implements role-based session state and logout methods."""
        self.assertIn('window.activateWarkariRole', self.js)
        self.assertIn('window.showFirstScreenPortal', self.js)
        self.assertIn('window.logoutCurrentRole', self.js)
        self.assertIn("sessionStorage.setItem('wariseva_session_role', 'WARKARI')", self.js)
        self.assertIn("sessionStorage.setItem('wariseva_session_role', 'VOLUNTEER')", self.js)
        self.assertIn("sessionStorage.setItem('wariseva_session_role', 'HOSPITAL')", self.js)
        self.assertIn("sessionStorage.removeItem('wariseva_session_role')", self.js)

    def test_04_volunteer_demo_auth_lifecycle(self):
        """Verify Volunteer login and logout API endpoints."""
        login_res = self.client.post('/api/auth/volunteer/login', json={
            'volunteer_id': 'V-001',
            'password': '1234'
        })
        self.assertEqual(login_res.status_code, 200)
        data = login_res.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['volunteer']['wari_id'], 'V-001')

        logout_res = self.client.post('/api/volunteer/logout')
        self.assertEqual(logout_res.status_code, 200)

    def test_05_hospital_demo_auth_lifecycle(self):
        """Verify Hospital login and logout API endpoints."""
        login_res = self.client.post('/api/auth/hospital/login', json={
            'facility_id': 'MF-001',
            'password': '1234'
        })
        self.assertEqual(login_res.status_code, 200)
        data = login_res.get_json()
        self.assertTrue(data['success'])
        self.assertIn('hospital', data)

        logout_res = self.client.post('/api/hospital/logout')
        self.assertEqual(logout_res.status_code, 200)

    def test_06_css_logout_styles(self):
        """Verify .arb-logout-btn CSS rules exist."""
        self.assertIn('.arb-logout-btn', self.css)

    def test_07_portals_excluded_from_warkari_dashboard(self):
        """Verify JOIN THE WARI SAFETY NETWORK is strictly part of landing and excluded from Warkari Dashboard."""
        landing_start = self.html.find('id="first-screen-role-selection"')
        landing_end = self.html.find('id="warkari-user-dashboard"')
        dash_start = landing_end
        dash_end = self.html.find('<!-- end #warkari-user-dashboard -->')

        landing_html = self.html[landing_start:landing_end]
        dash_html = self.html[dash_start:dash_end]

        # Portals MUST be inside Landing
        self.assertIn('id="home-network-portals"', landing_html)
        self.assertIn('JOIN THE WARI SAFETY NETWORK', landing_html)

        # Portals and Responder registration MUST NOT be inside Warkari Dashboard
        self.assertNotIn('id="home-network-portals"', dash_html)
        self.assertNotIn('JOIN THE WARI SAFETY NETWORK', dash_html)
        self.assertNotIn('VOLUNTEER RESPONDER', dash_html)
        self.assertNotIn('HOSPITAL / MEDICAL FACILITY', dash_html)
        self.assertNotIn('COMMAND CENTER OPERATIONS', dash_html)

if __name__ == '__main__':
    unittest.main()
