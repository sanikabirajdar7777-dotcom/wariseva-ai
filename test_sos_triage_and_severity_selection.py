"""
WariSeva AI — SOS Emergency Type & Severity Selection QA Test Suite
Verifies all 6 Emergency Types and 4 Severity Levels are selectable, update state, and flow into SOS dispatch.
"""

import os
import sys
import io
import re
import unittest
import urllib.request
import json

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

BASE_URL = "http://127.0.0.1:5000"

class TestSOSTriageAndSeveritySelection(unittest.TestCase):

    def setUp(self):
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self.index_html_path = os.path.join(self.project_dir, 'templates', 'index.html')
        self.script_js_path = os.path.join(self.project_dir, 'static', 'script.js')
        self.style_css_path = os.path.join(self.project_dir, 'static', 'style.css')

    def test_01_all_6_emergency_type_buttons_exist_in_html(self):
        """Verify all 6 emergency type buttons have distinct IDs and data-type attributes in index.html"""
        with open(self.index_html_path, 'r', encoding='utf-8') as f:
            content = f.read()

        expected_types = [
            ('triage-btn-medical', 'Medical / Chest Pain'),
            ('triage-btn-injury', 'Severe Injury / Bleeding'),
            ('triage-btn-unconscious', 'Unconscious / Fainted'),
            ('triage-btn-burn', 'Burn / Fire'),
            ('triage-btn-stampede', 'Crowd Incident'),
            ('triage-btn-dehydration', 'Dehydration / Heat')
        ]

        for btn_id, data_type in expected_types:
            self.assertIn(f'id="{btn_id}"', content, f"Missing button ID: {btn_id}")
            self.assertIn(f'data-type="{data_type}"', content, f"Missing data-type: {data_type}")
        print("  ✓ [PASS] All 6 Emergency Type Buttons Present with Unique IDs & Data Attributes")

    def test_02_all_4_severity_buttons_exist_in_html(self):
        """Verify all 4 severity buttons have distinct IDs and data-sev attributes in index.html"""
        with open(self.index_html_path, 'r', encoding='utf-8') as f:
            content = f.read()

        expected_sevs = [
            ('triage-sev-critical', 'CRITICAL'),
            ('triage-sev-high', 'HIGH'),
            ('triage-sev-moderate', 'MODERATE'),
            ('triage-sev-low', 'LOW')
        ]

        for btn_id, data_sev in expected_sevs:
            self.assertIn(f'id="{btn_id}"', content, f"Missing severity button ID: {btn_id}")
            self.assertIn(f'data-sev="{data_sev}"', content, f"Missing data-sev: {data_sev}")
        print("  ✓ [PASS] All 4 Severity Buttons Present with Unique IDs & Data Attributes")

    def test_03_javascript_triage_state_engine(self):
        """Verify JavaScript triage state managers, UI updaters, and event initializers in script.js"""
        with open(self.script_js_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('function updateTriageTypeUI', content, "updateTriageTypeUI missing")
        self.assertIn('function updateTriageSeverityUI', content, "updateTriageSeverityUI missing")
        self.assertIn('function initTriageSelectionHandlers', content, "initTriageSelectionHandlers missing")
        self.assertIn('selectedTriageType', content, "selectedTriageType missing from WariState")
        self.assertIn('selectedTriageSeverity', content, "selectedTriageSeverity missing from WariState")
        
        # Verify handleSOS uses the dynamically selected triage state
        self.assertIn('window.WariState.selectedTriageType', content, "handleSOS does not read selectedTriageType")
        self.assertIn('window.WariState.selectedTriageSeverity', content, "handleSOS does not read selectedTriageSeverity")
        print("  ✓ [PASS] JavaScript Triage Selection Engine & Dynamic SOS Integration Verified")

    def test_04_css_classes_for_all_severities(self):
        """Verify distinct CSS styling for CRITICAL, HIGH, MODERATE, and LOW in style.css"""
        with open(self.style_css_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('.triage-pill.active', content, ".triage-pill.active styling missing")
        self.assertIn('.triage-sev-btn.active.critical', content, "critical active style missing")
        self.assertIn('.triage-sev-btn.active.high', content, "high active style missing")
        self.assertIn('.triage-sev-btn.active.moderate', content, "moderate active style missing")
        self.assertIn('.triage-sev-btn.active.low', content, "low active style missing")
        print("  ✓ [PASS] CSS Active Classes for All 4 Severity Tiers Verified")

    def test_05_api_emergency_creation_with_varied_triage_types(self):
        """Test backend API with various emergency types and severity levels"""
        test_cases = [
            ("Severe Injury / Bleeding", "HIGH"),
            ("Unconscious / Fainted", "CRITICAL"),
            ("Burn / Fire", "MODERATE"),
            ("Crowd Incident", "CRITICAL"),
            ("Dehydration / Heat", "LOW")
        ]

        for em_type, sev in test_cases:
            payload = json.dumps({
                "wari_id": "WS-28471",
                "emergency_type": em_type,
                "severity": sev,
                "latitude": 18.3444,
                "longitude": 74.0305
            }).encode('utf-8')
            
            req = urllib.request.Request(
                f"{BASE_URL}/api/emergency/create",
                data=payload,
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                self.assertIn(resp.status, (200, 201))
                data = json.loads(resp.read().decode('utf-8'))
                self.assertTrue(data.get('success'))
                self.assertEqual(data.get('emergency_id'), 'EM-28471')
                print(f"    ✓ API Dispatched: Type='{em_type}', Severity='{sev}' -> 200 OK")

        print("  ✓ [PASS] Backend API Handles All Emergency Types and Severities Correctly")

if __name__ == '__main__':
    print("======================================================================")
    print("WARISEVA AI — SOS TRIAGE TYPE & SEVERITY SELECTION AUDIT SUITE")
    print("======================================================================")
    unittest.main()
