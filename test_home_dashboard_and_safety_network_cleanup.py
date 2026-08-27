"""
test_home_dashboard_and_safety_network_cleanup.py
Verification suite for Home Dashboard Cleanup and Safety Network Map Categories.
"""

import unittest
import json
import re
import os
import sys

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
import app

class TestHomeDashboardAndSafetyNetworkCleanup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.app.config['TESTING'] = True
        cls.client = app.app.test_client()

        with open('templates/index.html', 'r', encoding='utf-8') as f:
            cls.html = f.read()
        with open('static/style.css', 'r', encoding='utf-8') as f:
            cls.css = f.read()
        with open('static/script.js', 'r', encoding='utf-8') as f:
            cls.js = f.read()

    def test_01_home_dashboard_cards_cleanup(self):
        """Verify Volunteer, Hospital, and Command Desk standalone cards are removed from Home."""
        home_start = self.html.find('id="home-view"')
        home_end = self.html.find('id="emergency-view"')
        self.assertNotEqual(home_start, -1)
        self.assertNotEqual(home_end, -1)
        home_html = self.html[home_start:home_end]

        # Standalone operational cards must NOT exist on Home
        self.assertNotIn('id="home-vol-accept-btn"', home_html)
        self.assertNotIn('id="home-hosp-accept-btn"', home_html)
        self.assertNotIn('<!-- COLUMN 2: VOLUNTEER CONSOLE -->', home_html)
        self.assertNotIn('<!-- COLUMN 3: HOSPITAL CONSOLE -->', home_html)
        self.assertNotIn('<!-- COLUMN 4: COMMAND CENTER -->', home_html)

        # Timeline card MUST remain
        self.assertIn('id="home-op-timeline-badge"', home_html)
        self.assertIn('TIMELINE', home_html)

        # Sidebar navigation must still contain all three pages
        self.assertIn('id="nav-volunteer"', self.html)
        self.assertIn('id="nav-responder"', self.html)
        self.assertIn('id="nav-command"', self.html)

    def test_02_backend_water_category(self):
        """Verify /api/safety-services?type=WATER returns only water points with complete metadata."""
        for q in ['WATER', 'water', 'Water']:
            res = self.client.get(f'/api/safety-services?type={q}')
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.assertTrue(data['success'])
            services = data['services']
            self.assertGreaterEqual(len(services), 5)
            for s in services:
                self.assertEqual(s['type'], 'WATER')
                self.assertIn('name', s)
                self.assertIn('latitude', s)
                self.assertIn('longitude', s)
                self.assertIn('status', s)
                self.assertIn('distance_text', s)

    def test_03_backend_washroom_category(self):
        """Verify /api/safety-services?type=WASHROOM / TOILET returns washrooms with complete metadata."""
        for q in ['WASHROOM', 'washroom', 'TOILET', 'toilet']:
            res = self.client.get(f'/api/safety-services?type={q}')
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.assertTrue(data['success'])
            services = data['services']
            self.assertGreaterEqual(len(services), 2)
            for s in services:
                self.assertIn(s['type'], ('TOILET', 'WASHROOM'))
                self.assertIn('name', s)
                self.assertIn('latitude', s)
                self.assertIn('longitude', s)
                self.assertIn('status', s)

    def test_04_backend_all_category_includes_all_facilities(self):
        """Verify /api/safety-services?type=ALL returns Water, Washroom, Medical, Volunteer, Hospital, Emergency."""
        res = self.client.get('/api/safety-services?type=ALL')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        services = data['services']
        types_present = set(s['type'] for s in services)

        self.assertIn('WATER', types_present)
        self.assertTrue('TOILET' in types_present or 'WASHROOM' in types_present)
        self.assertIn('MEDICAL_CAMP', types_present)
        self.assertIn('VOLUNTEER', types_present)
        self.assertIn('HOSPITAL', types_present)
        self.assertIn('EMERGENCY', types_present)
        self.assertGreaterEqual(len(services), 25)

    def test_05_frontend_home_safety_map_and_filters_wiring(self):
        """Verify frontend script and DOM have home-safety-map and filter buttons properly wired."""
        # Check DOM Elements
        self.assertIn('id="home-safety-map"', self.html)
        self.assertIn('id="map-filter-group-home"', self.html)
        self.assertIn('data-filter="WATER"', self.html)
        self.assertIn('data-filter="TOILET"', self.html)
        self.assertIn('data-filter="ALL"', self.html)

        # Check JS initialization and marker handling
        self.assertIn('function initHomeSafetyMap()', self.js)
        self.assertIn('window.WariState.maps.homeSafety', self.js)
        self.assertIn('window.initHomeSafetyMap', self.js)
        self.assertIn('function loadSafetyMapMarkers(', self.js)
        self.assertIn('map-filter-group-home', self.js)
        self.assertIn('bindPopup', self.js)

        # Auto-fit bounds logic
        self.assertIn('map.fitBounds(bounds', self.js)

    def test_06_previous_dedicated_maps_remain_intact(self):
        """Verify Volunteer Console and Medical Facility maps are still intact."""
        self.assertIn('function renderLiveCrowdAwareNavigationMap(', self.js)
        self.assertIn('function initVolunteerMap()', self.js)
        self.assertIn('function initResponderMap()', self.js)
        self.assertIn('id="volunteer-map"', self.html)
        self.assertIn('id="responder-map"', self.html)

    def test_07_mobile_filter_bar_styling(self):
        """Verify safety-filter-bar allows smooth horizontal scrolling without page overflow."""
        self.assertIn('.safety-filter-bar', self.css)
        self.assertIn('overflow-x: auto', self.css)
        mobile_match = re.search(r'\.safety-filter-bar\s*\{([^}]+)\}', self.css)
        self.assertIsNotNone(mobile_match)

if __name__ == '__main__':
    unittest.main()
