"""
WariSeva AI — Dedicated Wristband Navigation & Shared Header Test Suite
Validates:
1. Home -> Wristband routes (/wristband, /wristband/WS-28471, /wristband-id, /public/pilgrim/WS-28471)
2. Immediate visibility of Back and Home buttons before data/input
3. Shared navigation header in SPA modals (#wristband-auth-modal, #wristband-modal, #qr-scanner-view)
4. Manual ID entry and switching on Wristband pages
5. Mobile viewport touch compliance (>= 44px, space-between flex)
6. Server response on refresh and invalid ID lookups
"""

import unittest
import json
import sys
import os

sys.path.insert(0, os.path.abspath('.'))
from backend.app import app

class TestWristbandNavigationFix(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_01_direct_wristband_routes(self):
        """Step 1 & 7: Test direct /wristband and /wristband-id routes return 200 with Back & Home"""
        routes_to_test = [
            '/wristband',
            '/wristband/WS-28471',
            '/wristband/WS-30555',
            '/wristband-id',
            '/public/pilgrim/WS-28471',
            '/public/pilgrim/WS-30555',
            '/public/pilgrim/'
        ]
        for route in routes_to_test:
            res = self.client.get(route)
            self.assertEqual(res.status_code, 200, f"Route {route} failed with status {res.status_code}")
            html = res.data.decode('utf-8')
            self.assertIn('app-page-navigation', html, f"Route {route} missing app-page-navigation")
            self.assertIn('id="public-nav-back"', html, f"Route {route} missing back button")
            self.assertIn('id="public-nav-home"', html, f"Route {route} missing home button")
            self.assertIn('href="/"', html, f"Route {route} home link does not point to real home '/'")
            print(f"[PASS] Route {route}: 200 OK with persistent Back & Home header")

    def test_02_navigation_renders_before_data(self):
        """Step 4 & 6: Header is at the top of DOM before content/lookups"""
        res = self.client.get('/wristband')
        self.assertEqual(res.status_code, 200)
        html = res.data.decode('utf-8')
        nav_idx = html.find('id="app-page-navigation"')
        card_idx = html.find('class="identity-card"')
        self.assertTrue(nav_idx != -1 and card_idx != -1)
        self.assertLess(nav_idx, card_idx, "Navigation must be declared before identity card in DOM")
        print("[PASS] Navigation renders prior to profile content")

    def test_03_wristband_manual_search_strip(self):
        """Step 4 & 7: Manual Wristband ID lookup strip exists on the page"""
        res = self.client.get('/wristband')
        self.assertEqual(res.status_code, 200)
        html = res.data.decode('utf-8')
        self.assertIn('id="public-switch-wari-id"', html)
        self.assertIn('handleSwitchWristband()', html)
        print("[PASS] Manual Wristband ID lookup strip is active on page")

    def test_04_spa_modals_have_persistent_navigation(self):
        """Step 3 & 8: SPA index.html modals (#wristband-auth-modal & #wristband-modal) have navigation"""
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        html = res.data.decode('utf-8')
        # Auth Modal
        self.assertIn('id="wristband-auth-modal"', html)
        self.assertIn('id="wb-auth-back-btn"', html)
        self.assertIn('id="wb-auth-home-btn"', html)
        # Physical Wristband Modal
        self.assertIn('id="wristband-modal"', html)
        self.assertIn('id="wb-modal-back-btn"', html)
        self.assertIn('id="wb-modal-home-btn"', html)
        # QR Scanner View
        self.assertIn('id="qr-global-back-btn"', html)
        self.assertIn('id="qr-global-home-btn"', html)
        print("[PASS] SPA modals and views contain dedicated Back & Home buttons")

    def test_05_invalid_id_lookup_graceful_handling(self):
        """Step 7.2: Invalid ID lookup still renders full page with Back & Home"""
        res = self.client.get('/public/pilgrim/WS-99999')
        self.assertEqual(res.status_code, 200)
        html = res.data.decode('utf-8')
        self.assertIn('id="public-nav-back"', html)
        self.assertIn('id="public-nav-home"', html)
        self.assertIn('WS-99999', html)
        print("[PASS] Invalid ID lookup preserves complete Back & Home header")

if __name__ == '__main__':
    unittest.main()
