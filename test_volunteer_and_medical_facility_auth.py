"""
test_volunteer_and_medical_facility_auth.py
Verification suite for Volunteer and Medical Facility Authentication in WariSeva AI.
"""

import unittest
import json
import os
import sys

sys.path.insert(0, os.path.abspath('backend'))
from app import app, init_db

class TestVolunteerAndMedicalFacilityAuth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        cls.client = app.test_client()

    def test_01_volunteer_login_invalid_credentials(self):
        """Verify invalid volunteer credentials return HTTP 401 and clean error message."""
        res = self.client.post('/api/auth/volunteer/login', json={
            'volunteer_id': 'V-001',
            'password': 'wrongpassword'
        })
        self.assertEqual(res.status_code, 401)
        data = res.get_json()
        self.assertFalse(data.get('success'))
        self.assertIn('Invalid Volunteer ID or Password', data.get('error'))

    def test_02_volunteer_login_demo_credentials_1234(self):
        """Verify volunteer ID V-001 logs in successfully with demo password 1234."""
        res = self.client.post('/api/auth/volunteer/login', json={
            'volunteer_id': 'V-001',
            'password': '1234'
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get('success'))
        self.assertEqual(data.get('volunteer', {}).get('id'), 'V-001')
        self.assertIn('Ramesh Kulkarni', data.get('volunteer', {}).get('name'))

    def test_03_hospital_login_invalid_credentials(self):
        """Verify invalid facility credentials return HTTP 401 and clean error message."""
        res = self.client.post('/api/auth/hospital/login', json={
            'facility_id': 'MF-001',
            'password': 'wrongpassword'
        })
        self.assertEqual(res.status_code, 401)
        data = res.get_json()
        self.assertFalse(data.get('success'))
        self.assertIn('Invalid Facility ID or Password', data.get('error'))

    def test_04_hospital_login_demo_credentials_1234(self):
        """Verify facility ID MF-001 logs in successfully with demo password 1234."""
        for f_id in ['MF-001', 'H-001']:
            res = self.client.post('/api/auth/hospital/login', json={
                'facility_id': f_id,
                'password': '1234'
            })
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.assertTrue(data.get('success'))
            self.assertIn('hospital', data)

    def test_05_dom_elements_for_volunteer_and_hospital_auth(self):
        """Verify HTML elements for authentication gates in index.html."""
        with open('templates/index.html', 'r', encoding='utf-8') as f:
            html = f.read()

        # Volunteer Auth Gate
        self.assertIn('VOLUNTEER ACCESS', html)
        self.assertIn('id="vol-auth-gate-card"', html)
        self.assertIn('id="vol-spa-login-id"', html)
        self.assertIn('id="vol-spa-login-pass"', html)
        self.assertIn('id="vol-spa-login-btn"', html)
        self.assertIn('id="vol-spa-login-error"', html)
        self.assertIn('id="vol-spa-login-success"', html)
        self.assertIn('id="volunteer-dashboard-content" class="hidden"', html)

        # Medical Facility Auth Gate
        self.assertIn('MEDICAL FACILITY ACCESS', html)
        self.assertIn('id="hosp-auth-gate-card"', html)
        self.assertIn('id="hosp-spa-login-id"', html)
        self.assertIn('id="hosp-spa-login-pass"', html)
        self.assertIn('id="hosp-spa-login-btn"', html)
        self.assertIn('id="hosp-spa-login-error"', html)
        self.assertIn('id="hosp-spa-login-success"', html)
        self.assertIn('id="hospital-dashboard-content" class="hidden"', html)

    def test_06_wristband_pin_and_sos_unaffected(self):
        """Verify QR Wristband PIN and SOS emergency flow remain 100% intact."""
        # QR lookup returns protected profile
        res_qr = self.client.post('/api/qr/lookup', json={'qr_data': 'WS-28471'})
        self.assertEqual(res_qr.status_code, 200)
        self.assertTrue(res_qr.get_json().get('is_protected'))

        # PIN verification unlocks
        res_pin = self.client.post('/api/qr/verify', json={
            'wari_id': 'WS-28471',
            'pin': '2741'
        })
        self.assertEqual(res_pin.status_code, 200)
        self.assertTrue(res_pin.get_json().get('authorized'))

        # SOS creation works without login
        res_sos = self.client.post('/api/emergency/create', json={
            'wari_id': 'WS-28471',
            'patient_name': 'Tukaram Shinde',
            'emergency_type': 'Medical / Chest Pain',
            'severity': 'CRITICAL',
            'latitude': 18.3444,
            'longitude': 74.0305
        })
        self.assertEqual(res_sos.status_code, 201)
        self.assertTrue(res_sos.get_json().get('success'))

if __name__ == '__main__':
    unittest.main()
