"""
test_unified_crowd_aware_navigation_map.py
Verification suite for the Unified Reusable Live Crowd-Aware Navigation Map Component.
"""

import unittest
import re
import os
import sys

class TestUnifiedCrowdAwareNavigationMap(unittest.TestCase):
    def setUp(self):
        with open('static/style.css', 'r', encoding='utf-8') as f:
            self.css = f.read()
        with open('templates/index.html', 'r', encoding='utf-8') as f:
            self.html = f.read()
        with open('static/script.js', 'r', encoding='utf-8') as f:
            self.js = f.read()

    def test_01_responsive_container_css_specifications(self):
        """Verify the map container adheres to responsive container requirements."""
        # 1. Check tactical-map-deck rules
        deck_match = re.search(r'\.tactical-map-deck\s*\{([^}]+)\}', self.css)
        self.assertIsNotNone(deck_match, ".tactical-map-deck rule must exist")
        deck_css = deck_match.group(1)
        self.assertIn('width: 100%', deck_css)
        self.assertIn('max-width: 100%', deck_css)
        self.assertIn('box-sizing: border-box', deck_css)
        self.assertIn('overflow: hidden', deck_css)
        self.assertIn('position: relative', deck_css)
        self.assertIn('border-radius:', deck_css)

        # 2. Check tactical-leaflet-box desktop height (400px)
        box_match = re.search(r'\.tactical-leaflet-box\s*\{([^}]+)\}', self.css)
        self.assertIsNotNone(box_match, ".tactical-leaflet-box rule must exist")
        box_css = box_match.group(1)
        self.assertIn('height: 400px', box_css)
        self.assertIn('width: 100%', box_css)
        self.assertIn('box-sizing: border-box', box_css)

        # 3. Check tactical-leaflet-box mobile height (300px)
        self.assertIn('@media (max-width: 768px)', self.css)
        mobile_section = self.css[self.css.find('@media (max-width: 768px)'):]
        self.assertIn('height: 300px', mobile_section)

        # 4. Check header natural wrapping
        header_match = re.search(r'\.tactical-map-header\s*\{([^}]+)\}', self.css)
        self.assertIsNotNone(header_match)
        header_css = header_match.group(1)
        self.assertIn('flex-wrap: wrap', header_css)

    def test_02_html_dom_containers_in_both_consoles(self):
        """Verify both Volunteer Console and Medical Facility Console embed the map."""
        # Volunteer Console Map
        vol_idx = self.html.find('id="volunteer-map"')
        self.assertNotEqual(vol_idx, -1, "id='volunteer-map' must exist")
        vol_deck_idx = self.html.rfind('tactical-map-deck', 0, vol_idx)
        self.assertNotEqual(vol_deck_idx, -1, "tactical-map-deck must enclose volunteer-map")
        vol_snippet = self.html[vol_deck_idx : vol_idx + 100]
        self.assertIn('📍 Live Crowd-Aware Navigation Map', vol_snippet)
        self.assertIn('― 🟢 Safe Bypass (3 min)', vol_snippet)
        self.assertIn('--- 🔴 Congested Direct (10 min)', vol_snippet)

        # Medical Facility Console Map
        resp_idx = self.html.find('id="responder-map"')
        self.assertNotEqual(resp_idx, -1, "id='responder-map' must exist")
        resp_deck_idx = self.html.rfind('tactical-map-deck', 0, resp_idx)
        self.assertNotEqual(resp_deck_idx, -1, "tactical-map-deck must enclose responder-map")
        resp_snippet = self.html[resp_deck_idx : resp_idx + 100]
        self.assertIn('📍 Live Crowd-Aware Navigation Map', resp_snippet)
        self.assertIn('― 🟢 Safe Bypass (3 min)', resp_snippet)
        self.assertIn('--- 🔴 Congested Direct (10 min)', resp_snippet)

    def test_03_reusable_single_map_component_logic(self):
        """Verify ONE reusable map function handles both consoles without code duplication."""
        # Function definitions
        self.assertIn('function renderLiveCrowdAwareNavigationMap(containerId, roleType)', self.js)
        self.assertIn('function getEmergencyMapData(roleType)', self.js)
        self.assertIn('function scheduleMapInvalidate(map, container)', self.js)

        # Volunteer Console delegates to reusable component
        self.assertIn("renderLiveCrowdAwareNavigationMap('volunteer-map', 'volunteer')", self.js)

        # Medical Facility Console delegates to exact same reusable component
        self.assertIn("renderLiveCrowdAwareNavigationMap('responder-map', 'hospital')", self.js)

    def test_04_map_instance_reuse_and_invalidation(self):
        """Verify map instances are reused rather than recreated, and size invalidation is scheduled."""
        # Check map reuse logic
        self.assertIn('map.getContainer && map.getContainer() === container', self.js)
        self.assertIn('window.WariState.mapLayers', self.js)
        self.assertIn('map.removeLayer', self.js)

        # Check safe Leaflet container cleanup
        self.assertIn('container._leaflet_id = null', self.js)

        # Check bounds fitting
        self.assertIn('map.fitBounds(bounds, { padding: [40, 40] })', self.js)

        # Check invalidation scheduling
        self.assertIn('scheduleMapInvalidate(map, container)', self.js)
        self.assertIn('window.addEventListener(\'resize\'', self.js)

    def test_05_coordinate_integrity_and_route_colors(self):
        """Verify consistent coordinates and official route styles."""
        # Emergency Tukaram Shinde coordinates: [18.3444, 74.0305]
        self.assertIn('18.3444', self.js)
        self.assertIn('74.0305', self.js)

        # Volunteer coordinates: [18.3470, 74.0330]
        self.assertIn('18.3470', self.js)
        self.assertIn('74.0330', self.js)

        # Medical Facility coordinates: [18.3390, 74.0260]
        self.assertIn('18.3390', self.js)
        self.assertIn('74.0260', self.js)

        # Route colors
        self.assertIn("color: '#00E676'", self.js) # Safe Bypass Green
        self.assertIn("color: '#FF5252'", self.js) # Congested Direct Red
        self.assertIn("dashArray: '6, 6'", self.js)

if __name__ == '__main__':
    unittest.main()
