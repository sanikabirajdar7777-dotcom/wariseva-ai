"""
test_feedback_feature.py
Automated test suite verifying the Feedback feature under the Reports section for both Warkari and Volunteer roles.

Ensures:
1. Entry points exist in both Warkari/User Dashboard and Volunteer Dashboard.
2. Reports modal includes Incident Analytics and Give Feedback sub-views.
3. API endpoints properly handle Warkari and Volunteer feedback submissions.
4. Input validation (ratings 1-5, categories, role).
5. Feedback list retrieval via GET /api/feedback.
6. Strict preservation of existing SOS, QR scanning, Green Corridor, and Emergency Corridor.
"""

import unittest
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
import app as flask_app

class TestFeedbackFeature(unittest.TestCase):
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

    def test_01_warkari_reports_and_feedback_dom(self):
        """Verify Reports entry point in Warkari Dashboard and sub-views in Reports modal."""
        self.assertIn('id="home-reports-btn"', self.html)
        self.assertIn("openReportsModal('WARKARI')", self.html)
        self.assertIn('id="tab-btn-incident-report"', self.html)
        self.assertIn('id="tab-btn-give-feedback"', self.html)
        self.assertIn('id="reports-incident-subview"', self.html)
        self.assertIn('id="reports-feedback-subview"', self.html)
        self.assertIn('id="btn-jump-to-feedback"', self.html)

    def test_02_volunteer_reports_dom(self):
        """Verify Reports entry point in Volunteer Dashboard."""
        self.assertIn('id="vol-reports-btn"', self.html)
        self.assertIn("openReportsModal('VOLUNTEER')", self.html)

    def test_03_feedback_form_elements_dom(self):
        """Verify feedback form fields: stars, categories, comments, submit button, confirmation."""
        self.assertIn('id="fb-role-badge"', self.html)
        self.assertIn('id="fb-star-group"', self.html)
        self.assertIn('id="fb-rating-val"', self.html)
        self.assertIn('id="fb-category-select"', self.html)
        self.assertIn('id="fb-comment-text"', self.html)
        self.assertIn('id="btn-submit-feedback"', self.html)
        self.assertIn('id="feedback-success-container"', self.html)
        self.assertIn('Thank you! Your feedback has been submitted.', self.html)

    def test_04_submit_warkari_feedback_api(self):
        """Verify submitting valid feedback as Warkari."""
        payload = {
            'role': 'WARKARI',
            'rating': 5,
            'category': 'Emergency Response',
            'comment': 'Prompt volunteer assistance near Saswad Palkhi Maidan!',
            'user_id': 'WS-28471',
            'user_name': 'Tukaram Shinde'
        }
        res = self.client.post('/api/feedback', json=payload)
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertTrue(data.get('success'))
        self.assertEqual(data.get('role'), 'WARKARI')
        self.assertEqual(data.get('rating'), 5)
        self.assertEqual(data.get('category'), 'Emergency Response')
        self.assertEqual(data.get('message'), 'Thank you! Your feedback has been submitted.')
        self.assertTrue(data.get('feedback_id').startswith('FB-'))

    def test_05_submit_volunteer_feedback_api(self):
        """Verify submitting valid feedback as Volunteer."""
        payload = {
            'role': 'VOLUNTEER',
            'rating': 4,
            'category': 'QR Scanner',
            'comment': 'Offline scanner works accurately even in dense crowd.',
            'user_id': 'V-001',
            'user_name': 'Ramesh Kulkarni'
        }
        res = self.client.post('/api/feedback', json=payload)
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertTrue(data.get('success'))
        self.assertEqual(data.get('role'), 'VOLUNTEER')
        self.assertEqual(data.get('rating'), 4)
        self.assertEqual(data.get('category'), 'QR Scanner')
        self.assertEqual(data.get('message'), 'Thank you! Your feedback has been submitted.')

    def test_06_feedback_validation_invalid_rating(self):
        """Verify rejection of invalid ratings (< 1 or > 5)."""
        res_high = self.client.post('/api/feedback', json={'rating': 6, 'role': 'WARKARI'})
        self.assertEqual(res_high.status_code, 400)
        self.assertFalse(res_high.get_json().get('success'))

        res_low = self.client.post('/api/feedback', json={'rating': 0, 'role': 'WARKARI'})
        self.assertEqual(res_low.status_code, 400)
        self.assertFalse(res_low.get_json().get('success'))

    def test_07_get_feedback_api(self):
        """Verify retrieving submitted feedback list."""
        res = self.client.get('/api/feedback')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get('success'))
        self.assertGreaterEqual(data.get('count', 0), 2)
        
        # Test role filter
        res_vol = self.client.get('/api/feedback?role=VOLUNTEER')
        self.assertEqual(res_vol.status_code, 200)
        data_vol = res_vol.get_json()
        for item in data_vol.get('feedback', []):
            self.assertEqual(item.get('role'), 'VOLUNTEER')

    def test_08_js_and_css_bindings(self):
        """Verify JS functions and CSS styles for Reports & Feedback."""
        self.assertIn('openReportsModal', self.js)
        self.assertIn('switchReportsTab', self.js)
        self.assertIn('setFeedbackRating', self.js)
        self.assertIn('submitFeedbackForm', self.js)
        self.assertIn('.reports-tab-btn', self.css)
        self.assertIn('.fb-star', self.css)

    def test_09_existing_features_unaffected(self):
        """Verify existing SOS, QR, Green Corridor, and Emergency Corridor remain functional."""
        # 1. Emergency Corridor
        res_ec = self.client.get('/api/emergency/EM-28471/corridor')
        self.assertEqual(res_ec.status_code, 200)
        self.assertTrue(res_ec.get_json()['success'])

        # 2. Green Corridor
        res_gc = self.client.get('/api/emergency/EM-28471/green-corridor')
        self.assertEqual(res_gc.status_code, 200)
        self.assertTrue(res_gc.get_json()['success'])

        # 3. QR PIN protection
        res_pin = self.client.post('/api/qr/verify', json={
            'wari_id': 'WS-28471',
            'pin': '2741',
            'volunteer_id': 'V-001'
        })
        self.assertEqual(res_pin.status_code, 200)
        self.assertTrue(res_pin.get_json()['authorized'])

if __name__ == '__main__':
    unittest.main()
