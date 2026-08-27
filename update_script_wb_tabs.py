with open('static/script.js', 'r', encoding='utf-8') as f:
    js_code = f.read()

# Add setWristbandViewMode and update showPhysicalWristbandModal
old_show_func = """    let currentLanQrUrl = `${window.location.origin}/public/pilgrim/WS-28471`;

    function showPhysicalWristbandModal() {
        const modal = document.getElementById('wristband-modal');
        if (!modal) return;
        modal.classList.remove('hidden');

        // Fetch machine's real LAN IP dynamically from the backend for physical phone scanning
        fetch('/api/network-info')
        .then(res => res.json())
        .then(data => {
            if (data.success && data.lan_ip) {
                const lanIp = data.lan_ip;
                const port = data.port || 5000;
                currentLanQrUrl = data.qr_target_url || `http://${lanIp}:${port}/public/pilgrim/WS-28471`;

                const lanIpEl = document.getElementById('wb-lan-ip-display');
                if (lanIpEl) lanIpEl.textContent = `${lanIp}:${port}`;

                const diagLanEl = document.getElementById('diag-lan-ip');
                if (diagLanEl) diagLanEl.textContent = `${lanIp}:${port}`;

                const urlTextEl = document.getElementById('wb-qr-url-text');
                if (urlTextEl) urlTextEl.textContent = currentLanQrUrl;

                const urlSubTextEl = document.getElementById('wb-qr-url-subtext');
                if (urlSubTextEl) urlSubTextEl.textContent = currentLanQrUrl;

                const openLinkEl = document.getElementById('open-public-profile-link');
                if (openLinkEl) openLinkEl.href = currentLanQrUrl;

                // Render high-contrast 220x220px machine-readable QR code
                renderDynamicQrCode('wristband-qr-target', currentLanQrUrl, 220);
            }
        })
        .catch(() => {
            currentLanQrUrl = `${window.location.origin}/public/pilgrim/WS-28471`;
            renderDynamicQrCode('wristband-qr-target', currentLanQrUrl, 220);
        });

        showToast("✓ Physical WariSeva QR Wristband Preview Unlocked", "success");
        speakVoice("Demo access verified. Physical wristband preview unlocked.");
    }"""

new_show_func = """    let currentLanQrUrl = `${window.location.origin}/public/pilgrim/WS-28471`;

    function setWristbandViewMode(mode) {
        const tabFront = document.getElementById('tab-wb-front');
        const tabBack = document.getElementById('tab-wb-back');
        const tabBoth = document.getElementById('tab-wb-both');
        const bandFront = document.getElementById('wb-band-front');
        const bandBack = document.getElementById('wb-band-back');

        [tabFront, tabBack, tabBoth].forEach(t => t?.classList.remove('active'));

        if (mode === 'front') {
            if (tabFront) tabFront.classList.add('active');
            if (bandFront) bandFront.classList.remove('hidden');
            if (bandBack) bandBack.classList.add('hidden');
        } else if (mode === 'back') {
            if (tabBack) tabBack.classList.add('active');
            if (bandFront) bandFront.classList.add('hidden');
            if (bandBack) bandBack.classList.remove('hidden');
        } else if (mode === 'both') {
            if (tabBoth) tabBoth.classList.add('active');
            if (bandFront) bandFront.classList.remove('hidden');
            if (bandBack) bandBack.classList.remove('hidden');
        }
    }

    function showPhysicalWristbandModal() {
        const modal = document.getElementById('wristband-modal');
        if (!modal) return;
        modal.classList.remove('hidden');
        setWristbandViewMode('front');

        // Fetch machine's real LAN IP dynamically from the backend for physical phone scanning
        fetch('/api/network-info')
        .then(res => res.json())
        .then(data => {
            if (data.success && data.lan_ip) {
                const lanIp = data.lan_ip;
                const port = data.port || 5000;
                currentLanQrUrl = data.qr_target_url || `http://${lanIp}:${port}/public/pilgrim/WS-28471`;

                const lanIpEl = document.getElementById('wb-lan-ip-display');
                if (lanIpEl) lanIpEl.textContent = `${lanIp}:${port}`;

                const diagLanEl = document.getElementById('diag-lan-ip');
                if (diagLanEl) diagLanEl.textContent = `${lanIp}:${port}`;

                const urlTextEl = document.getElementById('wb-qr-url-text');
                if (urlTextEl) urlTextEl.textContent = currentLanQrUrl;

                const openLinkEl = document.getElementById('open-public-profile-link');
                if (openLinkEl) openLinkEl.href = currentLanQrUrl;

                // Render high-contrast 100x100px machine-readable QR code inside pure quiet box
                renderDynamicQrCode('wristband-qr-target', currentLanQrUrl, 96);
            }
        })
        .catch(() => {
            currentLanQrUrl = `${window.location.origin}/public/pilgrim/WS-28471`;
            renderDynamicQrCode('wristband-qr-target', currentLanQrUrl, 96);
        });

        showToast("✓ Physical WariSeva QR Wristband Preview Unlocked", "success");
        speakVoice("Demo access verified. Physical wristband preview unlocked.");
    }"""

assert old_show_func in js_code, "Could not find old_show_func in script.js"
js_code = js_code.replace(old_show_func, new_show_func)

# Add event listeners for the wristband tabs
tab_binding = """        // --- Wristband Tab Switcher ---
        document.getElementById('tab-wb-front')?.addEventListener('click', () => setWristbandViewMode('front'));
        document.getElementById('tab-wb-back')?.addEventListener('click', () => setWristbandViewMode('back'));
        document.getElementById('tab-wb-both')?.addEventListener('click', () => setWristbandViewMode('both'));
"""

target_marker = "document.getElementById('print-wristband-btn')?.addEventListener('click', () => {"
assert target_marker in js_code, "Could not find print-wristband-btn marker in script.js"

js_code = js_code.replace(target_marker, tab_binding + "\n        " + target_marker)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js_code)

print("Updated static/script.js with Wristband Front/Back tab switcher handlers!")
