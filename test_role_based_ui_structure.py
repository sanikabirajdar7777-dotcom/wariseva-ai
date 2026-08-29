import unittest
import os
import re

class TestRoleBasedUIStructure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(base_dir, 'templates', 'index.html')
        css_path = os.path.join(base_dir, 'static', 'style.css')
        js_path = os.path.join(base_dir, 'static', 'script.js')

        with open(html_path, 'r', encoding='utf-8') as f:
            cls.html = f.read()

        with open(css_path, 'r', encoding='utf-8') as f:
            cls.css = f.read()

        with open(js_path, 'r', encoding='utf-8') as f:
            cls.js = f.read()

    def test_first_screen_role_selection_container_exists(self):
        self.assertIn('id="first-screen-role-selection"', self.html)
        self.assertIn('first-screen-portal-container', self.html)

    def test_logo_and_brand_strip(self):
        self.assertIn("logo.png", self.html)
        self.assertIn('first-screen-brand-logo', self.html)
        self.assertIn('WariSeva', self.html)

    def test_central_question(self):
        self.assertIn('id="first-screen-main-question"', self.html)
        self.assertIn('How can we help you?', self.html)
        self.assertIn('data-i18n="role_prompt_question"', self.html)

    def test_three_primary_role_cards(self):
        # Role 1: Warkari / User
        self.assertIn('id="card-role-warkari"', self.html)
        self.assertIn('id="btn-select-role-warkari"', self.html)
        self.assertIn('WARKARI / USER', self.html)
        self.assertIn('Access safety services, emergency help and nearby facilities.', self.html)

        # Role 2: Volunteer
        self.assertIn('id="card-role-volunteer"', self.html)
        self.assertIn('id="btn-select-role-volunteer"', self.html)
        self.assertIn('VOLUNTEER', self.html)
        self.assertIn('Respond to emergencies, assist Warkaris and scan wristband QR codes.', self.html)

        # Role 3: Hospital / Medical Facility
        self.assertIn('id="card-role-hospital"', self.html)
        self.assertIn('id="btn-select-role-hospital"', self.html)
        self.assertIn('HOSPITAL / MEDICAL FACILITY', self.html)
        self.assertIn('Receive emergency cases, accept patients and coordinate medical care.', self.html)

    def test_command_centre_operational_strip(self):
        self.assertIn('id="card-role-command"', self.html)
        self.assertIn('id="btn-select-role-command"', self.html)
        self.assertIn('COMMAND CENTRE OPERATIONS', self.html)

    def test_warkari_active_banner_and_switch_role(self):
        self.assertIn('id="warkari-user-dashboard"', self.html)
        self.assertIn('id="warkari-active-role-banner"', self.html)
        self.assertIn('id="btn-switch-role-from-warkari"', self.html)

    def test_role_navigation_in_volunteer_hospital_command_views(self):
        # Volunteer
        self.assertIn('id="vol-active-role-banner"', self.html)
        self.assertIn('id="vol-back-to-roles-btn"', self.html)
        self.assertIn('id="vol-qr-action-banner"', self.html)

        # Hospital
        self.assertIn('id="hosp-active-role-banner"', self.html)
        self.assertIn('id="hosp-back-to-roles-btn"', self.html)

        # Command Centre
        self.assertIn('id="cmd-active-role-banner"', self.html)
        self.assertIn('id="cmd-back-to-roles-btn"', self.html)

    def test_css_classes_exist(self):
        self.assertIn('.first-screen-portal-container', self.css)
        self.assertIn('.first-screen-hero-card', self.css)
        self.assertIn('.role-portal-card', self.css)
        self.assertIn('.warkari-portal-card', self.css)
        self.assertIn('.volunteer-portal-card', self.css)
        self.assertIn('.hospital-portal-card', self.css)
        self.assertIn('.active-role-sticky-banner', self.css)
        self.assertIn('.vol-qr-action-banner', self.css)

    def test_js_role_engine_wired(self):
        self.assertIn('initRolePortalWorkflow', self.js)
        self.assertIn('activateWarkariRole', self.js)
        self.assertIn('showFirstScreenPortal', self.js)
        self.assertIn('btn-select-role-warkari', self.js)
        self.assertIn('btn-select-role-volunteer', self.js)
        self.assertIn('btn-select-role-hospital', self.js)
        self.assertIn('btn-select-role-command', self.js)
        self.assertIn('role_prompt_question', self.js)

if __name__ == '__main__':
    unittest.main()
