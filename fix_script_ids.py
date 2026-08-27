import os

js_path = os.path.join(os.path.dirname(__file__), 'static', 'script.js')
with open(js_path, 'r', encoding='utf-8') as f:
    js_text = f.read()

# Update script.js translation hooks
old_block = """        // 2. Main SOS Button Translations
        const sosMainBtn = document.getElementById('home-sos-btn') || document.getElementById('sos-button-main');
        if (sosMainBtn) {
            const titleEl = sosMainBtn.querySelector('.sos-btn-text') || sosMainBtn.querySelector('.sos-text-main');
            const subEl = sosMainBtn.querySelector('.sos-btn-sub') || sosMainBtn.querySelector('.sos-text-sub');
            if (titleEl) titleEl.textContent = dict.sos_btn_text.replace('🚨 ', '');
            if (subEl) subEl.textContent = dict.sos_btn_sub;
        }"""

new_block = """        // 2. Main SOS Button Translations
        const sosMainBtn = document.getElementById('main-sos-button');
        if (sosMainBtn) {
            const titleEl = sosMainBtn.querySelector('.sos-label-main') || sosMainBtn.querySelector('.sos-btn-text');
            const subEl = sosMainBtn.querySelector('.sos-label-sub') || sosMainBtn.querySelector('.sos-btn-sub');
            if (titleEl) titleEl.textContent = dict.sos_btn_text ? dict.sos_btn_text.replace('🚨 ', '') : 'SOS';
            if (subEl) subEl.textContent = dict.sos_btn_sub || dict.sos_touch_text || 'TAP FOR EMERGENCY';
        }"""

js_text = js_text.replace(old_block, new_block)

old_vol_block = """        // 4. Update Volunteer Dashboard Controls
        const volAcceptBtn = document.getElementById('vol-accept-case-btn');
        if (volAcceptBtn) volAcceptBtn.textContent = dict.vol_accept_btn;

        const volEnrouteBtn = document.getElementById('vol-start-response-btn');
        if (volEnrouteBtn) volEnrouteBtn.textContent = dict.vol_enroute_btn;

        const volArrivedBtn = document.getElementById('vol-mark-arrived-btn');
        if (volArrivedBtn) volArrivedBtn.textContent = dict.vol_arrived_btn;

        const volScanBtn = document.getElementById('vol-scan-wristband-btn');
        if (volScanBtn) volScanBtn.textContent = dict.vol_scan_wb_btn;

        const volEscalateBtn = document.getElementById('vol-escalate-btn');
        if (volEscalateBtn) volEscalateBtn.textContent = dict.vol_escalate_btn;"""

new_vol_block = """        // 4. Update Volunteer Dashboard Controls
        const volAcceptBtn = document.getElementById('vol-accept-em-btn');
        if (volAcceptBtn) volAcceptBtn.textContent = dict.vol_accept_btn;

        const volEnrouteBtn = document.getElementById('vol-start-response-btn');
        if (volEnrouteBtn) volEnrouteBtn.textContent = dict.vol_enroute_btn;"""

js_text = js_text.replace(old_vol_block, new_vol_block)

# Brand click -> Home
js_text = js_text.replace("document.getElementById('nav-brand-home')?.addEventListener", "document.getElementById('nav-home-btn')?.addEventListener")

# See all services
js_text = js_text.replace("document.getElementById('home-see-all-services-btn')?.addEventListener", "document.getElementById('see-all-services-btn')?.addEventListener")

# Preview wristband
js_text = js_text.replace("document.getElementById('preview-wristband-btn')?.addEventListener('click', triggerWristbandAuthModal);", "")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_text)

print("script.js updated cleanly.")
