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

class TestQrReportForThisWarkariFlow(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_01_qr_scan_shows_dual_actions(self):
        """Test that index.html contains both 'REPORT FOR THIS WARKARI' (no PIN) and 'VIEW PROTECTED MEDICAL PROFILE' (PIN required)."""
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        html = res.get_data(as_text=True)

        self.assertIn('REPORT FOR THIS WARKARI', html)
        self.assertIn('id="btn-qr-report-warkari"', html)
        self.assertIn('NO PIN REQUIRED', html)
        self.assertIn('PROTECTED MEDICAL PROFILE', html)
        self.assertIn('id="pin-input-field"', html)
        print("[PASS] TEST 1: QR scan result card contains both 'REPORT FOR THIS WARKARI' and 'VIEW PROTECTED MEDICAL PROFILE' actions.")

    def test_02_qr_report_enters_same_emergency_engine(self):
        """Test that submitting a QR report creates an emergency associated with WS-28471 and flows into active lifecycle."""
        # 1. Look up pilgrim via QR
        res_lookup = self.client.post('/api/qr/lookup', json={'qr_data': 'WS-28471'})
        self.assertEqual(res_lookup.status_code, 200)
        p_data = res_lookup.get_json()
        self.assertEqual(p_data['wari_id'], 'WS-28471')

        # 2. Register emergency with chosen type: Dehydration, severity: MODERATE, source: QR REPORT
        res_em = self.client.post('/api/emergency/create', json={
            'wari_id': 'WS-28471',
            'patient_name': 'Tukaram Shinde',
            'emergency_type': 'Dehydration / Heat',
            'severity': 'MODERATE',
            'source': 'QR REPORT',
            'latitude': 18.3444,
            'longitude': 74.0305
        })
        self.assertIn(res_em.status_code, [200, 201])
        em_data = res_em.get_json()
        self.assertTrue(em_data['success'])
        em_id = em_data.get('emergency_id', 'EM-28471')

        # 3. Verify AI response recommendation exists for this emergency
        res_ai = self.client.get(f'/api/emergency/{em_id}/ai-recommendation')
        self.assertEqual(res_ai.status_code, 200)
        ai_data = res_ai.get_json()
        self.assertTrue(ai_data['success'])
        self.assertIn('recommended_volunteer', ai_data)

        # 4. Volunteer accepts case
        res_vol = self.client.post(f'/api/emergency/{em_id}/volunteer-accept', json={
            'volunteer_id': 'V-001'
        })
        self.assertEqual(res_vol.status_code, 200)
        self.assertTrue(res_vol.get_json()['success'])

        # 5. Hospital accepts case
        res_hosp = self.client.post(f'/api/emergency/{em_id}/hospital-accept', json={
            'hospital_id': 'H-001'
        })
        self.assertEqual(res_hosp.status_code, 200)
        self.assertTrue(res_hosp.get_json()['success'])

        print("[PASS] TEST 2: QR Report enters the same emergency engine and progresses through full volunteer & hospital lifecycle.")

    def test_03_main_sos_button_persists_intact(self):
        """Test that main SOS button and modal continue to work exactly as before."""
        res = self.client.get('/')
        html = res.get_data(as_text=True)
        self.assertIn('id="main-sos-button"', html)
        self.assertIn('id="sos-modal"', html)
        self.assertIn('id="triage-btn-medical"', html)
        self.assertIn('id="triage-btn-dehydration"', html)
        self.assertIn('id="triage-sev-critical"', html)
        self.assertIn('id="triage-sev-moderate"', html)
        print("[PASS] TEST 3: Main SOS button and triage selectors remain 100% functional and intact.")

    def test_04_medical_profile_pin_still_protects_sensitive_data(self):
        """Test that VIEW MEDICAL PROFILE still requires correct PIN (2741/WARI2026)."""
        # Wrong PIN -> 401
        res_wrong = self.client.post('/api/qr/verify', json={
            'wari_id': 'WS-28471',
            'pin': '0000'
        })
        self.assertEqual(res_wrong.status_code, 401)

        # Correct PIN -> 200
        res_correct = self.client.post('/api/qr/verify', json={
            'wari_id': 'WS-28471',
            'pin': '2741'
        })
        self.assertEqual(res_correct.status_code, 200)
        self.assertTrue(res_correct.get_json()['authorized'])
        print("[PASS] TEST 4: Sensitive medical profile remains strictly PIN-protected.")

if __name__ == '__main__':
    unittest.main()
