with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add mob-nav-services and home-open-safety-map-btn
old_mob_nav = """        <!-- ================= 4. MOBILE BOTTOM NAVIGATION ================= -->
        <nav class="mobile-bottom-nav" role="navigation" aria-label="Mobile Navigation">
            <button type="button" class="mob-nav-btn active" data-view="home-view" id="mob-nav-home">
                <span class="mob-icon">🏠</span>
                <span class="mob-label" data-i18n="nav_home">Home</span>
            </button>
            <button type="button" class="mob-nav-btn" data-view="safety-map-view" id="mob-nav-map">
                <span class="mob-icon">🗺️</span>
                <span class="mob-label" data-i18n="nav_map">Map</span>
            </button>
            <button type="button" class="mob-nav-btn mob-sos-btn" data-view="emergency-view" id="mob-nav-sos">
                <div class="mob-sos-circle">
                    <span class="mob-sos-icon">🚨</span>
                </div>
                <span class="mob-label" data-i18n="nav_emergency">SOS</span>
            </button>
            <button type="button" class="mob-nav-btn" data-view="qr-scanner-view" id="mob-nav-qr">
                <span class="mob-icon">📸</span>
                <span class="mob-label">QR Scan</span>
            </button>
            <button type="button" class="mob-nav-btn" data-view="command-view" id="mob-nav-command">
                <span class="mob-icon">🛰️</span>
                <span class="mob-label" data-i18n="nav_command">Command</span>
            </button>
        </nav>"""

new_mob_nav = """        <!-- ================= 4. MOBILE BOTTOM NAVIGATION ================= -->
        <nav class="mobile-bottom-nav" role="navigation" aria-label="Mobile Navigation">
            <button type="button" class="mob-nav-btn active" data-view="home-view" id="mob-nav-home">
                <span class="mob-icon">🏠</span>
                <span class="mob-label" data-i18n="nav_home">Home</span>
            </button>
            <button type="button" class="mob-nav-btn" data-view="safety-map-view" id="mob-nav-map">
                <span class="mob-icon">🗺️</span>
                <span class="mob-label" data-i18n="nav_map">Map</span>
            </button>
            <button type="button" class="mob-nav-btn mob-sos-btn" data-view="emergency-view" id="mob-nav-sos">
                <div class="mob-sos-circle">
                    <span class="mob-sos-icon">🚨</span>
                </div>
                <span class="mob-label" data-i18n="nav_emergency">SOS</span>
            </button>
            <button type="button" class="mob-nav-btn" data-view="qr-scanner-view" id="mob-nav-qr">
                <span class="mob-icon">📸</span>
                <span class="mob-label">QR Scan</span>
            </button>
            <button type="button" class="mob-nav-btn" data-view="services-view" id="mob-nav-services">
                <span class="mob-icon">🛡️</span>
                <span class="mob-label">Services</span>
            </button>
            <button type="button" class="mob-nav-btn" data-view="command-view" id="mob-nav-command">
                <span class="mob-icon">🛰️</span>
                <span class="mob-label" data-i18n="nav_command">Command</span>
            </button>
        </nav>"""

if old_mob_nav in html:
    html = html.replace(old_mob_nav, new_mob_nav)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated mobile bottom nav in index.html!")
