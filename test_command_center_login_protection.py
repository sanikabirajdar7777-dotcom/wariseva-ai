"""
test_command_center_login_protection.py
Verification suite for Command Center Login Protection in WariSeva AI.
"""

import unittest
import json
import re
import os
import sys

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
import app

class TestCommandCenterLoginProtection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.app.config['TESTING'] = True
        cls.client = app.app.test_client()

        with open('templates/index.html', 'r', encoding='utf-8') as f:
            cls.html = f.read()
        with open('static/style.css', 'r', encoding='utf-8') as f:
            cls.css = f.read()
        with open('static/script.js', 'r', encoding='utf-8') as f:
            cls.js = f.read()

    def test_01_command_login_invalid_credentials(self):
        """Verify invalid command center credentials return HTTP 401 and clean error message."""
        res = self.client.post('/api/auth/command/login', json={
            'username': 'admin',
            'password': 'wrongpassword'
        })
        self.assertEqual(res.status_code, 401)
        data = res.get_json()
        self.assertFalse(data.get('success'))
        self.assertIn('Invalid username or password', data.get('error'))

    def test_02_command_login_demo_credentials_admin_admin123(self):
        """Verify admin credentials (admin / admin123) return HTTP 200 and Login Successful."""
        res = self.client.post('/api/auth/command/login', json={
            'username': 'admin',
            'password': 'admin123'
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get('success'))
        self.assertEqual(data.get('message'), 'Login Successful')
        self.assertEqual(data.get('user', {}).get('username'), 'admin')

    def test_03_command_logout_endpoint(self):
        """Verify command center logout endpoint terminates the session."""
        res = self.client.post('/api/auth/command/logout', json={})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get('success'))

    def test_04_html_command_center_login_elements(self):
        """Verify HTML elements for the Command Center login screen are correctly defined."""
        # Gate card & title
        self.assertIn('id="cmd-auth-gate-card"', self.html)
        self.assertIn('COMMAND CENTER ACCESS', self.html)
        self.assertIn('Authorized personnel only', self.html)

        # Demo credentials notice
        self.assertIn('Username: <code', self.html)
        self.assertIn('admin', self.html)
        self.assertIn('admin123', self.html)
        self.assertIn('id="cmd-quick-fill-btn"', self.html)

        # Inputs & buttons
        self.assertIn('id="cmd-spa-login-user"', self.html)
        self.assertIn('id="cmd-spa-login-pass"', self.html)
        self.assertIn('id="cmd-spa-login-btn"', self.html)
        self.assertIn('id="cmd-spa-login-error"', self.html)
        self.assertIn('id="cmd-spa-login-success"', self.html)

        # Authenticated content container is hidden initially
        self.assertIn('id="command-dashboard-content" class="hidden"', self.html)
        self.assertIn('id="cmd-spa-logout-btn"', self.html)

    def test_05_home_page_command_center_button_routing(self):
        """Verify Home page has Command Center button routed to the protected view."""
        self.assertIn('id="home-command-center-btn"', self.html)
        self.assertIn('COMMAND CENTER', self.html)
        self.assertIn("document.getElementById('nav-command').click()", self.html)

    def test_06_javascript_auth_gate_and_session_protection(self):
        """Verify JavaScript implements checkCommandAuth, login and logout logic."""
        self.assertIn('checkCommandAuth', self.js)
        self.assertIn('wariseva_command_auth', self.js)
        self.assertIn('performCommandLogin', self.js)
        self.assertIn('cmd-spa-logout-btn', self.js)
        self.assertIn('/api/auth/command/login', self.js)
        self.assertIn('/api/auth/command/logout', self.js)

        # Protected in switchView
        self.assertIn("viewId === 'command-view'", self.js)
        self.assertIn("checkCommandAuth()", self.js)

    def test_07_existing_command_center_structure_preserved(self):
        """Verify all existing Command Center tabs, controls, and features remain intact."""
        self.assertIn('id="cmd-tab-operations"', self.html)
        self.assertIn('id="cmd-tab-volunteers"', self.html)
        self.assertIn('id="cmd-tab-hospitals"', self.html)
        self.assertIn('id="cmd-tab-incident-dive"', self.html)
        self.assertIn('id="cmd-tab-heatmap"', self.html)
        self.assertIn('id="cmd-tab-readiness"', self.html)
        self.assertIn('id="command-map"', self.html)

if __name__ == '__main__':
    unittest.main()
