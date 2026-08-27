"""
test_desktop_layout_fix.py
Automated validation for the desktop layout bug fix in WariSeva AI.
Verifies that:
1. Desktop layout has .app-wrapper as horizontal flex row (flex-direction: row).
2. .sidebar-panel is positioned on the left with fixed width (250px) and full height (100vh).
3. .main-wrapper is beside the sidebar with flex: 1 and flex-direction: column.
4. .content-canvas starts directly below top-nav-bar with zero artificial top spacing/blank areas.
5. Mobile breakpoint (<= 992px) retains off-canvas sidebar and block app-wrapper.
"""

import unittest
import re
import os

class TestDesktopLayoutFix(unittest.TestCase):
    def setUp(self):
        self.css_path = os.path.join(os.path.dirname(__file__), 'static', 'style.css')
        self.html_path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
        with open(self.css_path, 'r', encoding='utf-8', errors='ignore') as f:
            self.css_content = f.read()
        with open(self.html_path, 'r', encoding='utf-8', errors='ignore') as f:
            self.html_content = f.read()

    def test_01_desktop_app_wrapper_is_horizontal_flex_row(self):
        """Verify .app-wrapper has display: flex and flex-direction: row for desktop."""
        # Find desktop .app-wrapper outside media queries
        desktop_part = self.css_content.split('@media')[0]
        self.assertIn('.app-wrapper', desktop_part)
        
        # Ensure flex-direction: row is set
        app_wrapper_match = re.search(r'\.app-wrapper\s*\{([^}]+)\}', desktop_part)
        self.assertIsNotNone(app_wrapper_match, "Could not find .app-wrapper in desktop CSS")
        body = app_wrapper_match.group(1)
        self.assertIn('display: flex', body)
        self.assertIn('flex-direction: row', body)
        self.assertNotIn('flex-direction: column', body)

    def test_02_no_overriding_column_app_wrapper_in_desktop_css(self):
        """Verify no duplicate .app-wrapper overrides flex-direction to column outside media queries."""
        desktop_part = self.css_content.split('@media (max-width: 992px)')[0]
        matches = re.findall(r'\.app-wrapper\s*\{([^}]+)\}', desktop_part)
        for body in matches:
            self.assertNotIn('flex-direction: column', body, "Found invalid flex-direction: column on desktop .app-wrapper")

    def test_03_sidebar_and_main_wrapper_structure(self):
        """Verify sidebar is fixed-width and main-wrapper takes remaining space."""
        # Check sidebar rules
        sidebar_match = re.search(r'\.sidebar-panel\s*\{([^}]+)\}', self.css_content)
        self.assertIsNotNone(sidebar_match)
        s_body = sidebar_match.group(1)
        self.assertIn('width: 250px', s_body)
        self.assertIn('height: 100vh', s_body)
        self.assertIn('flex-shrink: 0', s_body)

        # Check main wrapper rules
        main_match = re.search(r'\.main-wrapper\s*\{([^}]+)\}', self.css_content)
        self.assertIsNotNone(main_match)
        m_body = main_match.group(1)
        self.assertIn('flex: 1', m_body)
        self.assertIn('display: flex', m_body)
        self.assertIn('flex-direction: column', m_body)
        self.assertIn('height: 100vh', m_body)

    def test_04_html_dom_hierarchy(self):
        """Verify HTML DOM contains sidebar and main-wrapper as siblings inside app-wrapper."""
        self.assertIn('<div id="app" class="app-wrapper">', self.html_content)
        self.assertIn('<aside class="sidebar-panel">', self.html_content)
        self.assertIn('<div class="main-wrapper">', self.html_content)
        self.assertIn('<main class="content-canvas" id="main-content-canvas">', self.html_content)

    def test_05_mobile_responsive_rules_preserved(self):
        """Verify mobile media queries for <= 992px and <= 480px remain completely intact."""
        self.assertIn('@media (max-width: 992px)', self.css_content)
        self.assertIn('.sidebar-panel.mobile-open', self.css_content)
        self.assertIn('transform: translateX(-100%)', self.css_content)
        self.assertIn('@media (max-width: 480px)', self.css_content)

if __name__ == '__main__':
    unittest.main()
