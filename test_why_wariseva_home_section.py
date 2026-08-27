"""
test_why_wariseva_home_section.py
Verification suite for the 'Why WariSeva AI?' informational section on the Home page.
"""

import unittest
import os
import sys

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
import app

class TestWhyWariSevaHomeSection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.app.config['TESTING'] = True
        cls.client = app.app.test_client()

        with open('templates/index.html', 'r', encoding='utf-8') as f:
            cls.html = f.read()
        with open('static/style.css', 'r', encoding='utf-8') as f:
            cls.css = f.read()

    def test_01_section_title_and_position(self):
        """Verify the section appears on Home after JOIN THE WARI SAFETY NETWORK."""
        pos_portals = self.html.find('id="home-network-portals"')
        pos_why = self.html.find('id="home-why-wariseva"')
        pos_home_end = self.html.find('id="emergency-view"')

        self.assertNotEqual(pos_portals, -1)
        self.assertNotEqual(pos_why, -1)
        self.assertNotEqual(pos_home_end, -1)

        # Must appear AFTER portals and inside home-view
        self.assertGreater(pos_why, pos_portals)
        self.assertLess(pos_why, pos_home_end)

        # Title and subtitles
        self.assertIn('WHY WARISEVA AI?', self.html)
        self.assertIn('Designed for the realities of Wari', self.html)
        self.assertIn('Built around the real challenges of a large, moving pilgrimage.', self.html)

    def test_02_four_key_differentiators_content(self):
        """Verify all 4 cards contain the exact specified text and icons."""
        section_start = self.html.find('id="home-why-wariseva"')
        section_end = self.html.find('</section>', section_start)
        section_html = self.html[section_start:section_end]

        # Card 1
        self.assertIn('📱', section_html)
        self.assertIn('NO SMARTPHONE REQUIRED', section_html)
        self.assertIn('QR wristband identifies the Warkari.', section_html)
        self.assertIn('A Warkari can be identified even when they do not have a smartphone.', section_html)

        # Card 2
        self.assertIn('📍', section_html)
        self.assertIn('EXACT EMERGENCY LOCATION', section_html)
        self.assertIn('Responders know where to go.', section_html)
        self.assertIn('Emergency location is shared with the response network to help responders reach the incident faster.', section_html)

        # Card 3
        self.assertIn('🩺', section_html)
        self.assertIn('PROTECTED MEDICAL INFORMATION', section_html)
        self.assertIn('Medical profile requires PIN.', section_html)
        self.assertIn('The QR identifies the wristband, while sensitive medical information remains protected behind PIN verification.', section_html)

        # Card 4
        self.assertIn('🚨', section_html)
        self.assertIn('COORDINATED RESPONSE', section_html)
        self.assertIn('Volunteer → Medical Facility → Command Center', section_html)
        self.assertIn('WariSeva connects the complete emergency-response chain instead of handling only one part of the emergency.', section_html)

    def test_03_informational_only_no_buttons(self):
        """Verify cards are informational and not clickable interactive elements."""
        section_start = self.html.find('id="home-why-wariseva"')
        section_end = self.html.find('</section>', section_start)
        section_html = self.html[section_start:section_end]

        # No <button>, <a>, or onclick handlers inside why-wariseva-grid
        grid_start = section_html.find('class="why-wariseva-grid"')
        grid_html = section_html[grid_start:]
        self.assertNotIn('<button', grid_html)
        self.assertNotIn('<a ', grid_html)
        self.assertNotIn('onclick=', grid_html)

    def test_04_css_styling_and_responsive_rules(self):
        """Verify CSS styles for the grid and cards, including responsive breakpoints."""
        self.assertIn('.why-wariseva-grid', self.css)
        self.assertIn('.why-card', self.css)
        self.assertIn('grid-template-columns: repeat(4, 1fr)', self.css)
        self.assertIn('grid-template-columns: repeat(2, 1fr)', self.css)
        self.assertIn('grid-template-columns: 1fr', self.css)

if __name__ == '__main__':
    unittest.main()
