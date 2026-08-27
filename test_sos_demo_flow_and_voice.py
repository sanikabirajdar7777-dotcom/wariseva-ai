import unittest
import re
import os

class TestSosDemoFlowAndVoice(unittest.TestCase):
    def setUp(self):
        with open("templates/index.html", "r", encoding="utf-8") as f:
            self.index_html = f.read()
        with open("templates/public_pilgrim.html", "r", encoding="utf-8") as f:
            self.public_html = f.read()
        with open("static/script.js", "r", encoding="utf-8") as f:
            self.script_js = f.read()
        with open("static/style.css", "r", encoding="utf-8") as f:
            self.style_css = f.read()

    def test_part1_wristband_top_left_home_button(self):
        """Verify prominent Home button exists in top-left of public_pilgrim.html and wristband modal."""
        # Public Pilgrim Page
        self.assertIn('id="public-nav-home"', self.public_html)
        self.assertIn('Home', self.public_html)
        self.assertIn('href="/"', self.public_html)

        # Wristband Modal
        self.assertIn('id="wb-modal-home-btn"', self.index_html)
        self.assertIn('id="wb-auth-home-btn"', self.index_html)

    def test_part2_and_3_all_12_timeline_steps_present(self):
        """Verify all 12 stages exist with correct IDs and headers."""
        expected_steps = [
            ('step-1-sos', 'SOS Sent & Registered'),
            ('step-2-loc', 'Exact Location Acquired'),
            ('step-3-zone', 'Wari Zone Identified'),
            ('step-4-severity', 'Emergency Severity Classified'),
            ('step-5-ai-match', 'AI Responder Recommendation'),
            ('step-6-vol-alert', 'Volunteer Alert Sent'),
            ('step-7-vol-accept', 'Volunteer Accepted'),
            ('step-8-vol-enroute', 'Volunteer En Route'),
            ('step-9-vol-reached', 'Volunteer Arrived'),
            ('step-10-resp-dispatched', 'AI Hospital Recommendation'),
            ('step-11-hosp-recommended', 'Hospital Transfer / Patient Expected'),
            ('step-12-coordinated', 'Emergency Resolved'),
        ]
        for step_id, title_substr in expected_steps:
            self.assertIn(f'id="{step_id}"', self.index_html, f"Missing timeline step id: {step_id}")
            self.assertIn(title_substr, self.index_html, f"Missing title substr '{title_substr}' in index.html")

    def test_part4_progressive_timeline_styling(self):
        """Verify CSS contains active pulsing orange highlight, green done, and voice guidance badge."""
        self.assertIn('.timeline-step.step-active', self.style_css)
        self.assertIn('.timeline-step.step-done', self.style_css)
        self.assertIn('activeStepPulse', self.style_css)
        self.assertIn('.voice-guidance-pill', self.style_css)

    def test_part5_and_6_voice_narration_sentences(self):
        """Verify SpeechSynthesis function speaks all 12 exact narration phrases."""
        expected_narrations = [
            "SOS received. Emergency registered.",
            "Exact location acquired.",
            "Wari zone identified. Saswad Palkhi Maidan.",
            "Emergency classified as critical.",
            "Nearest suitable volunteer identified.",
            "Emergency alert sent to the nearest volunteer.",
            "Volunteer has accepted the emergency.",
            "Volunteer is on the way.",
            "Volunteer has arrived at the emergency location.",
            "Suitable medical facility identified.",
            "Hospital has accepted the case. Patient transfer initiated.",
            "Emergency response completed successfully."
        ]
        for phrase in expected_narrations:
            self.assertIn(phrase, self.script_js, f"Missing exact voice narration phrase: {phrase}")

        # Check en-IN voice preference in script.js
        self.assertIn('en-IN', self.script_js)
        self.assertIn('getPreferredVoice', self.script_js)

    def test_part10_ai_response_engine_card(self):
        """Verify AI response engine card has score 94/100 and explainable criteria."""
        self.assertIn('AI RESPONSE ENGINE', self.index_html)
        self.assertIn('94', self.index_html)
        self.assertIn('Why this responder?', self.index_html)
        self.assertIn('350m from patient', self.index_html)
        self.assertIn('First-aid certified', self.index_html)
        self.assertIn('AI-assisted responder recommendation', self.index_html)

    def test_part13_coordination_complete_card(self):
        """Verify final coordination complete card has score 92/100 and tactical map/share buttons."""
        self.assertIn('id="coordination-complete-card"', self.index_html)
        self.assertIn('RESPONSE COORDINATED', self.index_html)
        self.assertIn('92 / 100', self.index_html)
        self.assertIn('id="coord-view-map-btn"', self.index_html)
        self.assertIn('id="coord-share-btn"', self.index_html)
        self.assertIn('id="coord-view-details-btn"', self.index_html)

    def test_part14_reset_demo_behavior(self):
        """Verify reset demo cancels speech synthesis and resets all 12 timeline steps."""
        self.assertIn('speechSynthesis.cancel()', self.script_js)
        self.assertIn('for (let i = 1; i <= 12; i++)', self.script_js)
        self.assertIn('coordination-complete-card', self.script_js)

if __name__ == '__main__':
    unittest.main()
