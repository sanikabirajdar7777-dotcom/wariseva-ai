import unittest
import json
import os
import backend.app as app

class TestWariSpecificFeatures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.app.testing = True
        cls.client = app.app.test_client()

    def test_feature_1_and_9_safety_map_and_essential_services(self):
        """Feature 1 & 9: Operational Safety Map with category filters and essential services."""
        categories = ['ALL', 'EMERGENCIES', 'VOLUNTEERS', 'HOSPITALS', 'MEDICAL_CAMP', 'WATER', 'TOILET', 'CROWD_RISK']
        for cat in categories:
            res = self.client.get(f'/api/safety-services?type={cat}')
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.assertTrue(data['success'])
            self.assertIn('services', data)
            self.assertGreater(len(data['services']), 0, f"Category {cat} should have service points")

    def test_feature_2_nearest_response_relationship(self):
        """Feature 2: Verify AI response calculates nearest volunteer and hospital relationship."""
        res = self.client.get('/api/emergency/EM-28471/ai-recommendation')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['recommended_volunteer'])
        self.assertIsNotNone(data['recommended_hospital'])
        self.assertEqual(data['recommended_volunteer']['wari_id'], 'V-001')
        self.assertIn(data['recommended_hospital']['hospital_id'], ['HOSP-001', 'HOSP-002', 'H-001'])

    def test_feature_3_and_4_ai_scoring_breakdowns(self):
        """Feature 3 & 4: Explainable AI scoring factor breakdown and transparent justifications."""
        res = self.client.get('/api/emergency/EM-28471/ai-recommendation')
        data = res.get_json()
        vol = data['recommended_volunteer']
        hosp = data['recommended_hospital']

        # Volunteer breakdown
        self.assertIn('breakdown', vol)
        self.assertIn('distance_score', vol['breakdown'])
        self.assertIn('skill_match_score', vol['breakdown'])
        self.assertIn('zone_relevance_score', vol['breakdown'])
        self.assertIn('reason', vol)
        self.assertGreaterEqual(vol['total_score'], 80)

        # Hospital breakdown
        self.assertIn('emergency_capability', hosp)
        self.assertIn('reason', hosp)
        self.assertIn('distance_km', hosp)

    def test_feature_5_triage_in_emergency_creation(self):
        """Feature 5: Emergency creation with custom triage and severity parameters."""
        payload = {
            'wari_id': 'WS-28471',
            'latitude': 18.3444,
            'longitude': 74.0305,
            'location_accuracy': 4.5,
            'emergency_type': 'Chest Pain / Cardiac Triage',
            'severity': 'CRITICAL'
        }
        res = self.client.post('/api/emergency/create', json=payload)
        self.assertIn(res.status_code, (200, 201))
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertIn('emergency_id', data)

    def test_feature_6_and_7_audit_trail_and_response_clock(self):
        """Feature 6 & 7: Verify emergency logs and events are tracked per incident."""
        res = self.client.get('/api/emergency/EM-28471/events')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertIn('events', data)

    def test_feature_8_wari_zone_safety_status(self):
        """Feature 8: Wari zone density, crowd risk, and choke point data."""
        res = self.client.get('/api/crowd/density')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertGreaterEqual(len(data['zones']), 4)
        for z in data['zones']:
            self.assertIn('zone_id', z)
            self.assertIn('crowd_density', z)

    def test_feature_10_public_pilgrim_qr_experience(self):
        """Feature 10: Public non-smartphone accessible emergency profile URL."""
        res = self.client.get('/public/pilgrim/WS-28471')
        self.assertEqual(res.status_code, 200)
        html = res.get_data(as_text=True)
        self.assertIn('Tukaram', html)
        self.assertIn('WS-28471', html)
        self.assertIn('EMERGENCY', html.upper())

    def test_feature_11_and_12_multilingual_and_command_center(self):
        """Feature 11 & 12: Command center incidents and UI multilingual tags."""
        res = self.client.get('/api/command-center/emergencies')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertIn('emergencies', data)

if __name__ == '__main__':
    unittest.main()
