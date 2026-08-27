"""
test_report_this_warkari_feature.py
Comprehensive automated test suite for the new "REPORT THIS WARKARI" functionality in WariSeva AI.
"""

import unittest
import json
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))
from app import app, init_db, get_db_connection

class TestReportThisWarkariFeature(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        cls.client = app.test_client()

    def test_01_qr_scan_direct_profile_no_pin(self):
        """Verify QR scanning WS-28471 directly identifies the Warkari with full details."""
        res = self.client.post('/api/qr/lookup', json={'qr_data': 'WS-28471'})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get('success'))
        self.assertTrue(data.get('found'))
        self.assertEqual(data.get('wari_id'), 'WS-28471')
        self.assertEqual(data.get('name'), 'Tukaram Shinde')

    def test_02_report_warkari_endpoint_all_reasons(self):
        """Test reporting a Warkari with each of the 7 official report reasons."""
        reasons = [
            "Medical Assistance",
            "Lost / Separated",
            "Safety Concern",
            "Separated From Dindi",
            "Dehydration / Weakness",
            "Requires Medical Attention",
            "Other"
        ]

        for r in reasons:
            payload = {
                'wari_id': 'WS-28471',
                'name': 'Tukaram Shinde',
                'reason': r,
                'notes': f'Testing report reason: {r}',
                'zone': 'Zone 04 — Saswad Palkhi Maidan',
                'reported_by': 'Volunteer V-001'
            }
            res = self.client.post('/api/warkari/report', json=payload)
            self.assertEqual(res.status_code, 201)
            data = res.get_json()
            self.assertTrue(data.get('success'))
            self.assertEqual(data.get('wari_id'), 'WS-28471')
            self.assertEqual(data.get('name'), 'Tukaram Shinde')
            self.assertEqual(data.get('reason'), r)
            self.assertEqual(data.get('message'), 'The Wari Safety Network has been notified.')
            self.assertTrue(data.get('report_id').startswith('REP-'))

    def test_03_report_warkari_optional_blank_notes(self):
        """Verify report can be submitted with empty/blank optional notes."""
        payload = {
            'wari_id': 'WS-28471',
            'name': 'Tukaram Shinde',
            'reason': 'Dehydration / Weakness',
            'notes': '',
            'zone': 'Zone 04 — Saswad Palkhi Maidan'
        }
        res = self.client.post('/api/warkari/report', json=payload)
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertTrue(data.get('success'))
        self.assertEqual(data.get('notes'), '')
        self.assertEqual(data.get('message'), 'The Wari Safety Network has been notified.')

    def test_04_notifications_created_for_reports(self):
        """Verify reports create recorded notification events in the database."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM notifications WHERE notification_type LIKE 'WARKARI_REPORT%' ORDER BY id DESC LIMIT 5")
        rows = cursor.fetchall()
        conn.close()
        self.assertGreater(len(rows), 0)
        self.assertIn('WARKARI_REPORT', rows[0]['notification_type'])

    def test_05_dom_structure_in_index_html(self):
        """Verify all required modal and action elements exist in templates/index.html."""
        with open('templates/index.html', 'r', encoding='utf-8') as f:
            html = f.read()

        # Check Action Button
        self.assertIn('id="btn-report-this-warkari"', html)
        self.assertIn('REPORT THIS WARKARI', html)

        # Check Report Modal
        self.assertIn('id="warkari-report-modal"', html)
        self.assertIn('id="rep-modal-name"', html)
        self.assertIn('id="rep-modal-wari-id"', html)
        self.assertIn('id="rep-modal-zone"', html)
        self.assertIn('id="warkari-report-reasons"', html)
        self.assertIn('id="rep-additional-notes"', html)
        self.assertIn('id="submit-warkari-report-btn"', html)
        self.assertIn('id="cancel-warkari-report-btn"', html)
        self.assertIn('id="warkari-report-success-view"', html)
        self.assertIn('The Wari Safety Network has been notified.', html)

        # Check all 7 report reasons in markup
        self.assertIn('data-reason="Medical Assistance"', html)
        self.assertIn('data-reason="Lost / Separated"', html)
        self.assertIn('data-reason="Safety Concern"', html)
        self.assertIn('data-reason="Separated From Dindi"', html)
        self.assertIn('data-reason="Dehydration / Weakness"', html)
        self.assertIn('data-reason="Requires Medical Attention"', html)
        self.assertIn('data-reason="Other"', html)

    def test_06_dom_structure_in_public_pilgrim_html(self):
        """Verify required report action button and modal in templates/public_pilgrim.html."""
        with open('templates/public_pilgrim.html', 'r', encoding='utf-8') as f:
            html = f.read()

        self.assertIn('id="public-report-warkari-btn"', html)
        self.assertIn('REPORT THIS WARKARI', html)
        self.assertIn('id="warkari-report-modal"', html)
        self.assertIn('id="submit-warkari-report-btn"', html)
        self.assertIn('The Wari Safety Network has been notified.', html)

    def test_07_main_sos_unaffected(self):
        """Verify that standard SOS workflow remains 100% operational."""
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
        self.assertIn('status', data)

if __name__ == '__main__':
    unittest.main()
