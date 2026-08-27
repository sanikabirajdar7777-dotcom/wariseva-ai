"""
WariSeva AI — Final UI Cleanup & Wristband Navigation QA Suite
"""

import os
import sys
import unittest
import urllib.request
import urllib.parse
import json

BASE_URL = "http://127.0.0.1:5000"

class TestFinalUICleanupAndNavigation(unittest.TestCase):

    def setUp(self):
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self.index_html_path = os.path.join(self.project_dir, 'templates', 'index.html')
        self.public_html_path = os.path.join(self.project_dir, 'templates', 'public_pilgrim.html')
        self.script_js_path = os.path.join(self.project_dir, 'static', 'script.js')
        self.style_css_path = os.path.join(self.project_dir, 'static', 'style.css')

    def test_01_elders_mode_removed_from_index_html(self):
        """Verify Elders Mode UI is completely removed from index.html"""
        with open(self.index_html_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertNotIn('id="elder-mode-toggle"', content, "elder-mode-toggle button still exists in index.html")
        self.assertNotIn('id="elder-mode-container"', content, "elder-mode-container still exists in index.html")
        self.assertNotIn('data-i18n="elder_mode"', content, "elder_mode i18n data tag still exists in index.html")
        self.assertNotIn('class="elder-mode-screen"', content, "elder-mode-screen class still exists in index.html")
        print("[PASS] TEST 1: Elders Mode removed from index.html")

    def test_02_elders_mode_removed_from_script_js(self):
        """Verify elderMode state, translations, and event listeners removed from script.js"""
        with open(self.script_js_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertNotIn('elderMode:', content, "elderMode state property still in script.js")
        self.assertNotIn('elder_screen_title', content, "elder translations still in script.js")
        self.assertNotIn('elder-mode-toggle', content, "elder-mode-toggle listener still in script.js")
        self.assertNotIn('elder-sos-action-btn', content, "elder-sos listener still in script.js")
        print("[PASS] TEST 2: Elders Mode removed from script.js")

    def test_03_persistent_qr_nav_in_index_html(self):
        """Verify persistent Back and Home buttons in QR scanner and wristband modal"""
        with open(self.index_html_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('id="qr-global-back-btn"', content, "qr-global-back-btn missing from index.html")
        self.assertIn('id="qr-global-home-btn"', content, "qr-global-home-btn missing from index.html")
        self.assertIn('id="wb-modal-back-btn"', content, "wb-modal-back-btn missing from index.html")
        self.assertIn('id="wb-modal-home-btn"', content, "wb-modal-home-btn missing from index.html")
        self.assertIn('id="manual-wristband-id-input"', content, "manual-wristband-id-input missing")
        self.assertIn('id="lookup-manual-wristband-btn"', content, "lookup-manual-wristband-btn missing")
        print("[PASS] TEST 3: Persistent QR & Wristband navigation present in SPA")

    def test_04_public_pilgrim_profile_navigation(self):
        """Verify public pilgrim profile template has persistent Back and Home buttons"""
        with open(self.public_html_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('id="public-nav-back"', content, "public-nav-back missing from public_pilgrim.html")
        self.assertIn('id="public-nav-home"', content, "public-nav-home missing from public_pilgrim.html")
        self.assertIn('handlePublicBack()', content, "handlePublicBack handler missing")
        self.assertIn('href="/"', content, "Home link to / missing")
        self.assertIn('WARISEVA WRISTBAND', content, "WARISEVA WRISTBAND kicker missing")
        self.assertIn('Wristband ID:', content, "Wristband ID banner missing")
        print("[PASS] TEST 4: Public Pilgrim profile has persistent navigation and clean header")

    def test_05_public_pilgrim_server_render(self):
        """Test HTTP rendering of public pilgrim profiles for WS-28471 and WS-30555"""
        req1 = urllib.request.Request(f"{BASE_URL}/public/pilgrim/WS-28471")
        with urllib.request.urlopen(req1, timeout=5) as resp:
            self.assertEqual(resp.status, 200)
            text1 = resp.read().decode('utf-8')
            self.assertIn('WS-28471', text1)
            self.assertIn('public-top-nav', text1)
            self.assertIn('Back', text1)
            self.assertIn('Home', text1)

        req2 = urllib.request.Request(f"{BASE_URL}/public/pilgrim/WS-30555")
        with urllib.request.urlopen(req2, timeout=5) as resp:
            self.assertEqual(resp.status, 200)
            text2 = resp.read().decode('utf-8')
            self.assertIn('WS-30555', text2)
            self.assertIn('Anandi Gopal Joshi', text2)
        print("[PASS] TEST 5: Server correctly renders public pilgrim profiles with nav")

    def test_06_qr_lookup_and_verify_api(self):
        """Test QR lookup and PIN verification backend flow"""
        # Lookup
        lookup_data = json.dumps({"qr_data": "WS-30555"}).encode('utf-8')
        req = urllib.request.Request(f"{BASE_URL}/api/qr/lookup", data=lookup_data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode('utf-8'))
            self.assertTrue(data.get('found'))
            self.assertEqual(data.get('wari_id'), 'WS-30555')

        # Verify PIN
        verify_data = json.dumps({
            "wari_id": "WS-30555",
            "pin": "3055",
            "volunteer_id": "V-001",
            "volunteer_name": "Ramesh Kulkarni"
        }).encode('utf-8')
        req2 = urllib.request.Request(f"{BASE_URL}/api/qr/verify", data=verify_data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req2, timeout=5) as resp:
            self.assertEqual(resp.status, 200)
            v_data = json.loads(resp.read().decode('utf-8'))
            self.assertTrue(v_data.get('authorized'))
            self.assertEqual(v_data.get('pilgrim', {}).get('name'), 'Anandi Gopal Joshi')
        print("[PASS] TEST 6: QR lookup and PIN verification work 100%")

    def test_07_mobile_touch_target_css_compliance(self):
        """Verify CSS contains touch targets with min-height: 44px for mobile UX"""
        with open(self.style_css_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('.qr-persistent-nav', content)
        self.assertIn('min-height: 44px', content)
        self.assertIn('.wb-nav-btn', content)
        self.assertIn('.manual-wristband-entry-box', content)
        print("[PASS] TEST 7: Mobile touch target CSS compliant (>= 44px)")

if __name__ == '__main__':
    unittest.main()
