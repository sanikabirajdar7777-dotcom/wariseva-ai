with open('static/script.js', 'r', encoding='utf-8') as f:
    js_code = f.read()

old_show_func = """    function showPhysicalWristbandModal() {
        const modal = document.getElementById('wristband-modal');
        if (!modal) return;
        modal.classList.remove('hidden');

        // Dynamically encode the complete public URL so any normal phone camera scans directly to the public profile
        const publicUrl = window.location.origin + '/public/pilgrim/WS-28471';
        
        const urlTextEl = document.getElementById('wb-qr-url-text');
        if (urlTextEl) urlTextEl.textContent = publicUrl;

        const openLinkEl = document.getElementById('open-public-profile-link');
        if (openLinkEl) openLinkEl.href = publicUrl;

        renderDynamicQrCode('wristband-qr-target', publicUrl, 130);
        showToast("✓ Physical WariSeva QR Wristband Preview Unlocked", "success");
        speakVoice("Demo access verified. Physical wristband preview unlocked.");
    }"""

new_show_func = """    let currentLanQrUrl = `${window.location.origin}/public/pilgrim/WS-28471`;

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

assert old_show_func in js_code, "Could not find old_show_func in script.js"
js_code = js_code.replace(old_show_func, new_show_func)

# Update copy and test link handlers
old_handlers = """        // Copy QR Link Button
        document.getElementById('copy-qr-link-btn')?.addEventListener('click', () => {
            const publicUrl = window.location.origin + '/public/pilgrim/WS-28471';
            navigator.clipboard.writeText(publicUrl).then(() => {
                showToast("✓ Public QR link copied to clipboard!", "success");
            }).catch(() => {
                showToast(`Link: ${publicUrl}`, "info");
            });
        });

        // Test QR Scan Button (Opens public profile in new tab)
        document.getElementById('btn-test-qr-scan')?.addEventListener('click', () => {
            window.open('/public/pilgrim/WS-28471', '_blank');
            showToast("Opened public emergency profile in new tab", "info");
        });"""

new_handlers = """        // Copy QR Link Button (Copies real LAN URL)
        document.getElementById('copy-qr-link-btn')?.addEventListener('click', () => {
            navigator.clipboard.writeText(currentLanQrUrl).then(() => {
                showToast("✓ Real LAN QR link copied to clipboard!", "success");
            }).catch(() => {
                showToast(`Link: ${currentLanQrUrl}`, "info");
            });
        });

        // Copy Diagnostic Phone Test URL Button
        document.getElementById('copy-diag-url-btn')?.addEventListener('click', () => {
            navigator.clipboard.writeText(currentLanQrUrl).then(() => {
                showToast("✓ Phone test URL copied to clipboard!", "success");
            }).catch(() => {
                showToast(`Link: ${currentLanQrUrl}`, "info");
            });
        });

        // Test QR Scan Toolbar Button (Opens LAN URL in new tab)
        document.getElementById('btn-test-qr-scan')?.addEventListener('click', () => {
            window.open(currentLanQrUrl, '_blank');
            showToast("Opened LAN emergency profile in new tab", "info");
        });"""

assert old_handlers in js_code, "Could not find old_handlers in script.js"
js_code = js_code.replace(old_handlers, new_handlers)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js_code)

print("Updated script.js with dynamic LAN IP fetching and high-contrast 220px QR generation!")
