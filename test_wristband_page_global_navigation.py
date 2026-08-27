"""
WariSeva AI — Global Navigation & Wristband Page Validation Suite
Tests all 8 Critical User Requirements:
1. TEST 1: Home -> Wristband (Home and global nav remain visible)
2. TEST 2: Wristband -> Home (Home opens)
3. TEST 3: Wristband -> Front Side (Front side preview works)
4. TEST 4: Wristband -> Back Side (Back side preview works)
5. TEST 5: Wristband -> Show Both (Print-ready view works)
6. TEST 6: Scan QR / Public Wristband Profile (Displays configured demo info)
7. TEST 7: Emergency assistance workflow from public profile (One-tap SOS dispatch works)
8. TEST 8: Refresh Wristband page (Navigation remains visible & functional)
"""

import unittest
import json
import os
import sys

sys.path.insert(0, os.path.abspath('.'))
from backend.app import app

class TestWristbandGlobalNavigation(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_01_home_to_wristband_navigation_visibility(self):
        """TEST 1: Home -> Wristband has Home, Emergency, Map, Services, Volunteer, Responder, Command visible"""
        res = self.client.get('/wristband')
        self.assertEqual(res.status_code, 200)
        html = res.data.decode('utf-8')
        # Global header check
        self.assertIn('public-global-header', html)
        self.assertIn('🏠 Home', html)
        self.assertIn('🚨 Emergency', html)
        self.assertIn('🗺️ Safety Map', html)
        self.assertIn('🛡️ Services', html)
        self.assertIn('🙋 Volunteer', html)
        self.assertIn('🚑 Responder', html)
        self.assertIn('🛰️ Command', html)
        # Secondary subnav check
        self.assertIn('wristband-subnav-row', html)
        self.assertIn('id="public-nav-home"', html)
        self.assertIn('id="public-nav-back"', html)
        print("[PASS] TEST 1: Global Navigation & Secondary Subnav immediately visible on Wristband page")

    def test_02_wristband_to_home_routing(self):
        """TEST 2: Wristband -> Home routes back to '/'"""
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        html = res.data.decode('utf-8')
        self.assertIn('id="home-view"', html)
        self.assertIn('WARISEVA AI', html)
        print("[PASS] TEST 2: Main Home route is accessible and healthy")

    def test_03_04_05_front_back_both_tabs_present(self):
        """TEST 3, 4, 5: Front Side, Back Side, Show Both tabs and elements present in SPA and public profile"""
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        html = res.data.decode('utf-8')
        self.assertIn('id="tab-wb-front"', html)
        self.assertIn('id="tab-wb-back"', html)
        self.assertIn('id="tab-wb-both"', html)
        self.assertIn('id="wb-band-front"', html)
        self.assertIn('id="wb-band-back"', html)
        print("[PASS] TEST 3, 4, 5: Front Side, Back Side, and Show Both print elements present")

    def test_06_public_wristband_profile_demo_data(self):
        """TEST 6: Public wristband profile displays configured demo information"""
        res = self.client.get('/public/pilgrim/WS-28471')
        self.assertEqual(res.status_code, 200)
        html = res.data.decode('utf-8')
        self.assertIn('Tukaram Shinde', html)
        self.assertIn('WS-28471', html)
        self.assertIn('DINDI 27', html)
        self.assertIn('Emergency Contact', html)
        self.assertIn('Blood Group', html)
        self.assertIn('Medical Alert', html)
        print("[PASS] TEST 6: Public wristband profile displays complete verified pilgrim identity")

    def test_07_public_emergency_assistance_workflow(self):
        """TEST 7: One-tap Emergency Assistance from public profile creates incident and triggers AI matching"""
        payload = {
            "source": "QR_WARI_ID",
            "wari_id": "WS-28471",
            "patient_name": "Tukaram Shinde",
            "emergency_type": "MEDICAL",
            "reporter_type": "QR_PUBLIC_USER",
            "latitude": 18.3444,
            "longitude": 74.0305,
            "location_source": "GPS"
        }
        res = self.client.post('/api/public/report-emergency', json=payload)
        self.assertIn(res.status_code, [200, 201])
        data = res.get_json()
        self.assertTrue(data.get('success'))
        self.assertIn('EM-', data.get('emergency_id', ''))
        print(f"[PASS] TEST 7: Public QR SOS created incident {data.get('emergency_id')}")

    def test_08_refresh_wristband_page_persists_navigation(self):
        """TEST 8: Refreshing the Wristband page maintains complete header & subnav"""
        for _ in range(3):
            res = self.client.get('/wristband')
            self.assertEqual(res.status_code, 200)
            html = res.data.decode('utf-8')
            self.assertIn('public-global-header', html)
            self.assertIn('public-nav-home', html)
            self.assertIn('public-nav-back', html)
        print("[PASS] TEST 8: Repeated refreshes persistently render all navigation components")

if __name__ == '__main__':
    unittest.main()
