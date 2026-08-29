"""
test_green_corridor_feature.py
Automated test suite verifying the Green Corridor: Emergency Route Optimization feature.
Ensures:
1. Green Corridor section exists inside the Hospital / Medical Facility portal.
2. The engine prioritizes emergency arrival time and low congestion over shortest distance.
3. API endpoints return detailed multi-factor telemetry and clear decision rationales.
4. Activation endpoint functions properly.
5. All required DOM, JS, and CSS components are present without altering existing architecture.
"""

import unittest
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
import app as flask_app
from green_corridor import calculate_route_suitability, get_green_corridor_plan

class TestGreenCorridorFeature(unittest.TestCase):
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

    def test_01_green_corridor_dom_elements_in_hospital_portal(self):
        """Verify Green Corridor card and controls are present inside the Hospital Portal."""
        self.assertIn('id="hospital-green-corridor-card"', self.html)
        self.assertIn('GREEN CORRIDOR', self.html)
        self.assertIn('SIMULATED TRAFFIC (DEMO)', self.html)
        self.assertIn('id="btn-gc-activate-corridor"', self.html)
        self.assertIn('id="btn-gc-view-green-route"', self.html)
        self.assertIn('id="btn-gc-view-alt-route"', self.html)
        self.assertIn('id="gc-status-badge"', self.html)
        self.assertIn('id="gc-ambulance-id"', self.html)
        self.assertIn('id="gc-dest-hospital-name"', self.html)
        self.assertIn('id="gc-recommended-eta"', self.html)
        self.assertIn('id="gc-recommended-traffic"', self.html)

    def test_02_green_corridor_api_evaluates_and_recommends_faster_route(self):
        """Verify API recommends Route B (longer distance, faster arrival) over Route A (shorter, congested)."""
        res = self.client.get('/api/emergency/EM-28471/green-corridor')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()

        self.assertTrue(data['success'])
        self.assertEqual(data['feature'], 'GREEN_CORRIDOR')
        self.assertIn('routes', data)
        self.assertGreaterEqual(len(data['routes']), 2)

        routes_by_id = {r['route_id']: r for r in data['routes']}
        route_a = routes_by_id['ROUTE-A']
        route_b = routes_by_id['ROUTE-B']

        # Core Rule Verification: Distance MUST NOT be the only factor
        self.assertGreater(route_b['distance_km'], route_a['distance_km'], "Route B should be geographically longer")
        self.assertLess(route_b['estimated_eta_min'], route_a['estimated_eta_min'], "Route B should have faster emergency ETA")
        self.assertLess(route_b['congestion_percent'], route_a['congestion_percent'], "Route B should have lower congestion")

        # System MUST recommend Route B
        self.assertTrue(route_b['is_recommended'], "Route B must be recommended")
        self.assertFalse(route_a['is_recommended'], "Route A must NOT be recommended")
        self.assertEqual(data['recommended_route_id'], 'ROUTE-B')

        # Decision rationale must clearly explain why
        self.assertIn('decision_rationale', route_b)
        self.assertIn('decision_rationale', route_a)
        self.assertIn('13 minutes faster', route_b['decision_rationale'])

    def test_03_green_corridor_activation_endpoint(self):
        """Verify POST /api/emergency/<id>/green-corridor/activate activates route clearance."""
        res = self.client.post('/api/emergency/EM-28471/green-corridor/activate')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()

        self.assertTrue(data['success'])
        self.assertEqual(data['status'], 'ACTIVE')
        self.assertEqual(data['route_id'], 'ROUTE-B')
        self.assertIn('Green Corridor activated', data['message'])

    def test_04_js_engine_functions_exist(self):
        """Verify JavaScript implements loadGreenCorridorData, renderGreenCorridorOnMap, activateGreenCorridor."""
        self.assertIn('loadGreenCorridorData', self.js)
        self.assertIn('renderGreenCorridorOnMap', self.js)
        self.assertIn('activateGreenCorridor', self.js)
        self.assertIn('btn-gc-activate-corridor', self.js)
        self.assertIn('btn-gc-view-green-route', self.js)
        self.assertIn('btn-gc-view-alt-route', self.js)

    def test_05_css_scoped_rules_exist(self):
        """Verify CSS includes scoped Green Corridor styling and responsive rules."""
        self.assertIn('.green-corridor-card', self.css)
        self.assertIn('.gc-route-option-card', self.css)
        self.assertIn('.gc-action-btn', self.css)

    def test_06_route_scoring_algorithm_penalizes_congestion_heavily(self):
        """Direct unit test of the route scoring algorithm to verify non-shortest route preference."""
        # Short route (5 km) with severe congestion (90%) and 20 min delay
        congested_short_score = calculate_route_suitability(
            distance_km=5.0, congestion_percent=90, traffic_delay_min=20, accessibility_rating='LOW'
        )
        # Long route (9 km) with low congestion (15%) and 2 min delay
        clear_long_score = calculate_route_suitability(
            distance_km=9.0, congestion_percent=15, traffic_delay_min=2, accessibility_rating='HIGH'
        )
        self.assertGreater(clear_long_score, congested_short_score,
            "A longer route with low congestion must score higher than a short congested route")

if __name__ == '__main__':
    unittest.main()
