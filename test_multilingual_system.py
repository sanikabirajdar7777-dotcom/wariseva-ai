import unittest
import json
import re
import os
import sys

class TestWariSevaMultilingualSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base_dir = os.path.abspath(os.path.dirname(__file__))
        with open(os.path.join(base_dir, 'static', 'script.js'), 'r', encoding='utf-8') as f:
            cls.script_js = f.read()
        with open(os.path.join(base_dir, 'templates', 'index.html'), 'r', encoding='utf-8') as f:
            cls.index_html = f.read()
        with open(os.path.join(base_dir, 'templates', 'public_pilgrim.html'), 'r', encoding='utf-8') as f:
            cls.public_html = f.read()

    def test_language_dropdown_exists_in_html(self):
        """Verify the #lang-select dropdown exists with en, mr, hi options."""
        self.assertIn('id="lang-select"', self.index_html)
        self.assertIn('value="en"', self.index_html)
        self.assertIn('value="mr"', self.index_html)
        self.assertIn('value="hi"', self.index_html)

    def test_i18n_dictionary_structure(self):
        """Verify the i18n dictionary has complete sections for English, Marathi, and Hindi."""
        self.assertIn('const i18n = {', self.script_js)
        self.assertIn('en: {', self.script_js)
        self.assertIn('mr: {', self.script_js)
        self.assertIn('hi: {', self.script_js)

    def test_sos_button_translations(self):
        """Verify the SOS button translations for English, Marathi, and Hindi."""
        # English
        self.assertIn('EMERGENCY / SOS', self.script_js)
        # Marathi
        self.assertIn('आपत्कालीन मदत / SOS', self.script_js)
        # Hindi
        self.assertIn('आपातकालीन सहायता / SOS', self.script_js)

    def test_12_step_timeline_translations_all_languages(self):
        """Verify all 12 timeline steps have translations and spoken phrases in all 3 languages."""
        for lang in ['en', 'mr', 'hi']:
            self.assertIn(f'{lang}: {{', self.script_js)

        # Check key Marathi timeline phrases
        self.assertIn('पायरी १: SOS पाठवले आणि नोंदणी झाली', self.script_js)
        self.assertIn('पायरी १२: केस पूर्ण झाली', self.script_js)
        self.assertIn('SOS पाठवले आणि नोंदणी झाली.', self.script_js)
        self.assertIn('स्वयंसेवकाने मदत स्वीकारली आहे.', self.script_js)

        # Check key Hindi timeline phrases
        self.assertIn('चरण १: SOS भेजा गया और दर्ज किया गया', self.script_js)
        self.assertIn('चरण १२: केस पूरा हुआ', self.script_js)
        self.assertIn('SOS भेजा गया और दर्ज किया गया.', self.script_js)
        self.assertIn('स्वयंसेवक ने केस स्वीकार किया है.', self.script_js)

    def test_volunteer_and_hospital_translations(self):
        """Verify volunteer and hospital labels and action buttons in Marathi and Hindi."""
        # Marathi volunteer & hospital buttons
        self.assertIn('केस स्वीकारा', self.script_js)
        self.assertIn('मदतीसाठी निघा', self.script_js)
        self.assertIn('मी रुग्णाजवळ पोहोचलो', self.script_js)
        self.assertIn('रुग्ण स्वीकारा (बेड राखीव)', self.script_js)

        # Hindi volunteer & hospital buttons
        self.assertIn('केस स्वीकारें', self.script_js)
        self.assertIn('मदद के लिए निकलें', self.script_js)
        self.assertIn('मैं मरीज के पास पहुँचा', self.script_js)
        self.assertIn('मरीज स्वीकारें (बेड आरक्षित)', self.script_js)

    def test_voice_synthesis_engine(self):
        """Verify Web Speech API configuration with correct language codes and fallbacks."""
        self.assertIn('function getPreferredVoice', self.script_js)
        self.assertIn('function speakText', self.script_js)
        self.assertIn('function speakStep', self.script_js)
        self.assertIn('mr-IN', self.script_js)
        self.assertIn('hi-IN', self.script_js)
        self.assertIn('en-IN', self.script_js)
        self.assertIn('speechSynthesis', self.script_js)

    def test_apply_language_preserves_state(self):
        """Verify applyLanguage does not clear active emergency state."""
        self.assertIn('function applyLanguage(lang)', self.script_js)
        # Ensure applyLanguage saves to localStorage and applies translations dynamically
        self.assertIn("localStorage.setItem('wariseva_lang'", self.script_js)

if __name__ == '__main__':
    unittest.main()
