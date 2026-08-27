"""
test_volunteer_map_and_alert_deduplication.py
Verification suite for Volunteer Console Map & Emergency Alert Deduplication in WariSeva AI.
"""

import unittest
import json
import os
import sys

sys.path.insert(0, os.path.abspath('backend'))
from app import app, init_db, get_db_connection

class TestVolunteerMapAndAlertDeduplication(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        cls.client = app.test_client()

    def test_01_volunteer_map_dom_presence_and_order(self):
        """Verify Live Crowd-Aware Navigation Map exists in Volunteer Console with exact order."""
        with open('templates/index.html', 'r', encoding='utf-8') as f:
            html = f.read()

        # Locate volunteer dashboard content
        vol_dash_idx = html.find('id="volunteer-dashboard-content"')
        self.assertNotEqual(vol_dash_idx, -1)
        vol_html = html[vol_dash_idx:html.find('id="responder-view"')]

        # Verify components
        self.assertIn('Ramesh Kulkarni (V-001)', vol_html)
        self.assertIn('id="volunteer-active-response-box"', vol_html)
        self.assertIn('AI Recommendation:', vol_html)
        self.assertIn('class="task-patient-info"', vol_html)
        self.assertIn('📍 Live Crowd-Aware Navigation Map', vol_html)
        self.assertIn('🟢 Safe Bypass (3 min)', vol_html)
        self.assertIn('🔴 Congested Direct (10 min)', vol_html)
        self.assertIn('id="volunteer-map"', vol_html)
        self.assertIn('class="location-sharing-panel"', vol_html)
        self.assertIn('id="vol-timeline-status-strip"', vol_html)
        self.assertIn('id="volunteer-emergency-feed"', vol_html)

        # Verify relative order inside volunteer console
        idx_profile = vol_html.find('class="responder-header-card')
        idx_box = vol_html.find('id="volunteer-active-response-box"')
        idx_ai = vol_html.find('class="ai-rec-banner-small"')
        idx_patient = vol_html.find('class="task-patient-info"')
        idx_map = vol_html.find('id="volunteer-map"')
        idx_controls = vol_html.find('class="location-sharing-panel"')
        idx_timeline = vol_html.find('id="vol-timeline-status-strip"')
        idx_feed = vol_html.find('id="volunteer-emergency-feed"')

        self.assertTrue(idx_profile < idx_box, "Profile should come before Active Box")
        self.assertTrue(idx_box < idx_ai, "Active Box should contain AI Recommendation")
        self.assertTrue(idx_ai < idx_patient, "AI Recommendation should come before Patient Info")
        self.assertTrue(idx_patient < idx_map, "Patient Info should come before Navigation Map")
        self.assertTrue(idx_map < idx_controls, "Navigation Map should come before Emergency Controls")
        self.assertTrue(idx_controls < idx_timeline, "Emergency Controls should come before Timeline Strip")
        self.assertTrue(idx_timeline < idx_feed, "Timeline Strip should come before Volunteer Feed")

    def test_02_volunteer_map_logic_in_script_js(self):
        """Verify initVolunteerMap is defined, uses Leaflet, and is wired to WariState and view switching."""
        with open('static/script.js', 'r', encoding='utf-8') as f:
            js = f.read()

        self.assertIn('function initVolunteerMap()', js)
        self.assertIn('function renderLiveCrowdAwareNavigationMap(', js)
        self.assertIn("renderLiveCrowdAwareNavigationMap('volunteer-map', 'volunteer')", js)
        self.assertIn('window.WariState.maps.volunteer', js)
        self.assertIn('window.initVolunteerMap', js)
        self.assertIn('syncEmergencyStatusAcrossConsoles', js)

    def test_03_backend_volunteer_dashboard_deduplication(self):
        """Verify /api/volunteer/dashboard-data returns each emergency exactly ONCE, no duplicates."""
        # Ensure database has multiple notifications for EM-28471
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO notifications (emergency_id, recipient_id, recipient_type, status) VALUES ('EM-28471', 'V-001', 'VOLUNTEER', 'SENT')")
        c.execute("INSERT INTO notifications (emergency_id, recipient_id, recipient_type, status) VALUES ('EM-28471', 'V-002', 'VOLUNTEER', 'SENT')")
        c.execute("INSERT INTO notifications (emergency_id, recipient_id, recipient_type, status) VALUES ('EM-28471', 'V-003', 'VOLUNTEER', 'SENT')")
        conn.commit()
        conn.close()

        res = self.client.get('/api/volunteer/dashboard-data')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get('success'))

        emergencies = data.get('emergencies', [])
        self.assertGreater(len(emergencies), 0)

        em_ids = [e['emergency_id'] for e in emergencies]
        unique_em_ids = set(em_ids)
        self.assertEqual(len(em_ids), len(unique_em_ids), "Backend emergencies list must have zero duplicate emergency IDs")
        self.assertEqual(em_ids.count('EM-28471'), 1, "EM-28471 must appear exactly once in the emergencies feed")

    def test_04_multiple_distinct_emergencies_preserved(self):
        """Verify distinct emergencies (EM-28471, EM-28472) are both preserved in dashboard."""
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
            INSERT OR REPLACE INTO emergencies 
            (emergency_id, wari_id, reported_by, emergency_type, priority, status, latitude, longitude, wari_zone)
            VALUES ('EM-28472', 'WS-28472', 'Sopanrao Jadhav', 'Medical / Fall', 'HIGH', 'CREATED', 18.3450, 74.0310, 'Zone 04 — Saswad Palkhi Maidan')
        ''')
        conn.commit()
        conn.close()

        res = self.client.get('/api/volunteer/dashboard-data')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        em_ids = [e['emergency_id'] for e in data.get('emergencies', [])]

        self.assertIn('EM-28471', em_ids)
        self.assertIn('EM-28472', em_ids)
        self.assertEqual(em_ids.count('EM-28471'), 1)
        self.assertEqual(em_ids.count('EM-28472'), 1)

    def test_05_state_synchronization_across_roles(self):
        """Verify status change on emergency synchronizes across volunteer, hospital, and command center."""
        # Update emergency status to VOLUNTEER_ACCEPTED
        res = self.client.post('/api/emergency/EM-28471/volunteer/accept', json={'volunteer_id': 'V-001'})
        self.assertEqual(res.status_code, 200)

        # Check volunteer dashboard
        res_vol = self.client.get('/api/volunteer/dashboard-data')
        vol_em = next((e for e in res_vol.get_json()['emergencies'] if e['emergency_id'] == 'EM-28471'), None)
        self.assertIsNotNone(vol_em)
        self.assertEqual(vol_em['status'], 'VOLUNTEER_ACCEPTED')

        # Check hospital dashboard
        res_hosp = self.client.get('/api/hospital/dashboard-data')
        hosp_em = next((e for e in res_hosp.get_json()['emergencies'] if e['emergency_id'] == 'EM-28471'), None)
        self.assertIsNotNone(hosp_em)
        self.assertEqual(hosp_em['status'], 'VOLUNTEER_ACCEPTED')

        # Check command center
        res_cmd = self.client.get('/api/command-center/emergencies')
        cmd_em = next((e for e in res_cmd.get_json()['emergencies'] if e['emergency_id'] == 'EM-28471'), None)
        self.assertIsNotNone(cmd_em)
        self.assertEqual(cmd_em['status'], 'VOLUNTEER_ACCEPTED')

if __name__ == '__main__':
    unittest.main()
