"""
test_pin_protection_after_qr_scan.py
Comprehensive test suite for PIN Protection of Medical Profile after QR Scan in WariSeva AI.
"""

import unittest
import json
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))
from app import app, init_db, get_db_connection

class TestPinProtectionAfterQrScan(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        cls.client = app.test_client()

    def test_01_qr_scan_returns_identification_only(self):
        """Verify QR lookup returns basic identity and marks medical data as protected."""
        res = self.client.post('/api/qr/lookup', json={'qr_data': 'WS-28471'})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get('success'))
        self.assertTrue(data.get('found'))
        self.assertEqual(data.get('wari_id'), 'WS-28471')
        self.assertEqual(data.get('name'), 'Tukaram Shinde')
        self.assertTrue(data.get('is_protected'))

        # Ensure sensitive medical details are NOT leaked in public lookup
        self.assertNotIn('blood_group', data)
        self.assertNotIn('medical_alert', data)
        self.assertNotIn('emergency_contact', data)

    def test_02_wrong_pin_keeps_profile_locked(self):
        """Verify wrong PIN returns 401 error and does NOT authorize medical details."""
        res = self.client.post('/api/qr/verify', json={
            'wari_id': 'WS-28471',
            'pin': '9999',
            'volunteer_id': 'V-001'
        })
        self.assertEqual(res.status_code, 401)
        data = res.get_json()
        self.assertFalse(data.get('success'))
        self.assertFalse(data.get('authorized'))
        self.assertIn('Incorrect PIN', data.get('error'))
        self.assertNotIn('pilgrim', data)

    def test_03_correct_pin_unlocks_medical_profile(self):
        """Verify correct PIN (2741 or WARI2026) authorizes and reveals medical profile."""
        for valid_pin in ['2741', 'WARI2026']:
            res = self.client.post('/api/qr/verify', json={
                'wari_id': 'WS-28471',
                'pin': valid_pin,
                'volunteer_id': 'V-001',
                'volunteer_name': 'Ramesh Kulkarni'
            })
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.assertTrue(data.get('success'))
            self.assertTrue(data.get('authorized'))
            self.assertIn('pilgrim', data)
            
            p = data['pilgrim']
            self.assertEqual(p.get('name'), 'Tukaram Shinde')
            self.assertEqual(p.get('wari_id'), 'WS-28471')
            self.assertEqual(p.get('blood_group'), 'B+')
            self.assertIn('Asthma', p.get('medical_alert'))
            self.assertIn('9822', p.get('emergency_contact'))

    def test_04_report_this_warkari_works_without_pin(self):
        """Verify safety report can be submitted without entering medical PIN."""
        res = self.client.post('/api/warkari/report', json={
            'wari_id': 'WS-28471',
            'name': 'Tukaram Shinde',
            'reason': 'Lost / Separated',
            'notes': 'Spotted near Palkhi Tent B',
            'zone': 'Zone 04 — Saswad Palkhi Maidan'
        })
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertTrue(data.get('success'))
        self.assertEqual(data.get('wari_id'), 'WS-28471')
        self.assertEqual(data.get('reason'), 'Lost / Separated')
        self.assertEqual(data.get('message'), 'The Wari Safety Network has been notified.')

    def test_05_sos_works_without_pin(self):
        """Verify SOS emergency can be triggered immediately without medical PIN."""
        sos_payload = {
            'wari_id': 'WS-28471',
            'latitude': 18.3444,
            'longitude': 74.0305,
            'emergency_type': 'Medical / Chest Pain',
            'severity': 'CRITICAL',
            'patient_name': 'Tukaram Shinde'
        }
        res = self.client.post('/api/emergency/create', json=sos_payload)
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertTrue(data.get('success'))
        self.assertTrue(data.get('emergency_id').startswith('EM-'))
        self.assertIn('notified_volunteers', data)

    def test_06_dom_elements_in_index_html(self):
        """Verify UI elements for PIN entry and password-free actions in index.html."""
        with open('templates/index.html', 'r', encoding='utf-8') as f:
            html = f.read()

        # Check Protected Card & PIN form
        self.assertIn('id="scan-result-protected-card"', html)
        self.assertIn('id="pin-input-field"', html)
        self.assertIn('id="submit-pin-btn"', html)
        self.assertIn('id="pin-error-text"', html)
        self.assertIn('PROTECTED MEDICAL PROFILE', html)
        self.assertIn('Enter Wristband PIN', html)

        # Check Password-Free Action Buttons
        self.assertIn('id="btn-report-this-warkari-scan"', html)
        self.assertIn('id="btn-qr-report-warkari"', html)
        self.assertIn('SOS — REQUEST EMERGENCY HELP', html)

        # Check Authorized Profile Card (initially hidden)
        self.assertIn('id="scan-authorized-profile-card"', html)
        self.assertIn('id="ap-blood"', html)
        self.assertIn('id="ap-alert"', html)
        self.assertIn('id="ap-contact"', html)

    def test_07_dom_elements_in_public_pilgrim_html(self):
        """Verify UI elements for PIN protection in public_pilgrim.html."""
        with open('templates/public_pilgrim.html', 'r', encoding='utf-8') as f:
            html = f.read()

        self.assertIn('id="public-protected-pin-box"', html)
        self.assertIn('id="public-pin-input"', html)
        self.assertIn('id="public-verify-pin-btn"', html)
        self.assertIn('id="public-pin-error"', html)
        self.assertIn('id="public-unlocked-medical-box"', html)
        self.assertIn('id="public-report-warkari-btn"', html)
        self.assertIn('id="public-sos-btn"', html)

if __name__ == '__main__':
    unittest.main()
