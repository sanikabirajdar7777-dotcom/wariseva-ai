import os
import sys
import io
import json
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from backend.app import app

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

class TestWristbandQrPinFlow(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_01_qr_scan_identifies_wristband_without_revealing_medical_info(self):
        """STEP 1: Scanning QR identifies wristband WS-28471 but keeps sensitive medical data protected."""
        # 1. Test scanning raw ID
        res = self.client.post('/api/qr/lookup', json={'qr_data': 'WS-28471'})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertTrue(data['found'])
        self.assertEqual(data['wari_id'], 'WS-28471')
        self.assertEqual(data['name'], 'Tukaram Shinde')
        self.assertTrue(data['is_protected'])
        # Ensure sensitive blood group and medical alerts are NOT returned at this step
        self.assertNotIn('blood_group', data)
        self.assertNotIn('medical_alert', data)

        # 2. Test scanning full URL (e.g. from camera scan)
        res_url = self.client.post('/api/qr/lookup', json={'qr_data': 'http://192.168.1.15:5000/public/pilgrim/WS-28471'})
        self.assertEqual(res_url.status_code, 200)
        data_url = res_url.get_json()
        self.assertTrue(data_url['success'])
        self.assertEqual(data_url['wari_id'], 'WS-28471')
        self.assertNotIn('blood_group', data_url)
        print("[PASS] STEP 1: QR scan locates wristband WS-28471 without exposing protected medical data.")

    def test_02_step_2_verification_ui_elements_in_html(self):
        """STEP 2: Verify HTML contains Step 2 Verification screen with PIN prompt."""
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        html = res.get_data(as_text=True)

        self.assertIn('WRISTBAND VERIFIED', html)
        self.assertIn('PROTECTED MEDICAL PROFILE', html)
        self.assertIn('Enter Wristband PIN:', html)
        self.assertIn('id="pin-input-field"', html)
        self.assertIn('[ VERIFY & VIEW PROFILE ]', html)
        print("[PASS] STEP 2: Verification screen & PIN entry elements verified in UI.")

    def test_03_wrong_pin_keeps_profile_locked_and_allows_retry(self):
        """STEP 4: Entering an incorrect PIN denies access and keeps profile locked."""
        res = self.client.post('/api/qr/verify', json={
            'wari_id': 'WS-28471',
            'pin': '9999',
            'volunteer_id': 'V-001'
        })
        self.assertEqual(res.status_code, 401)
        data = res.get_json()
        self.assertFalse(data['success'])
        self.assertFalse(data['authorized'])
        self.assertIn('Incorrect PIN', data['error'])
        self.assertNotIn('pilgrim', data)
        print("[PASS] STEP 4: Incorrect PIN returns 401 Access Denied and keeps medical profile locked.")

    def test_04_correct_pin_unlocks_full_medical_profile(self):
        """STEP 3: Entering correct PIN (2741 or WARI2026) unlocks the full medical profile."""
        res = self.client.post('/api/qr/verify', json={
            'wari_id': 'WS-28471',
            'pin': '2741',
            'volunteer_id': 'V-001',
            'volunteer_name': 'Ramesh Kulkarni'
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertTrue(data['authorized'])
        self.assertIn('pilgrim', data)
        p = data['pilgrim']
        self.assertEqual(p['wari_id'], 'WS-28471')
        self.assertEqual(p['name'], 'Tukaram Shinde')
        self.assertEqual(p['blood_group'], 'B+')
        self.assertIn('+91 9822', p['emergency_contact'])
        self.assertIn('Asthma', p['medical_alert'])
        print("[PASS] STEP 3: Correct PIN unlocks full protected medical profile for WS-28471.")

    def test_05_wristband_preview_opens_directly(self):
        """Verify Wristband section opens directly without upfront password gating."""
        js_path = os.path.join(os.path.dirname(__file__), 'static', 'script.js')
        with open(js_path, 'r', encoding='utf-8') as f:
            js = f.read()
        self.assertIn("document.getElementById('open-wristband-modal-btn')?.addEventListener('click', showPhysicalWristbandModal)", js)
        self.assertIn("document.getElementById('btn-view-demo-wristband')?.addEventListener('click', showPhysicalWristbandModal)", js)
        print("[PASS] Wristband preview opens directly without upfront password prompt.")

if __name__ == '__main__':
    unittest.main()
