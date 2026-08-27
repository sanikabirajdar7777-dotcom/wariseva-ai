with open('static/script.js', 'r', encoding='utf-8') as f:
    js_code = f.read()

# Replace openWristbandModal implementation with password modal trigger
old_wb_func = """    function openWristbandModal() {
        const modal = document.getElementById('wristband-modal');
        if (!modal) return;
        modal.classList.remove('hidden');
        renderDynamicQrCode('wristband-qr-target', 'WS-28471', 130);
        speakVoice("WariSeva Digital ID and Wristband preview opened.");
    }

    function closeWristbandModal() {
        const modal = document.getElementById('wristband-modal');
        if (modal) modal.classList.add('hidden');
    }"""

new_wb_func = """    function triggerWristbandAuthModal() {
        const authModal = document.getElementById('wristband-auth-modal');
        const passInput = document.getElementById('wb-password-input');
        const errEl = document.getElementById('wb-password-error');
        if (errEl) errEl.classList.add('hidden');
        if (passInput) {
            passInput.value = '';
        }
        if (authModal) {
            authModal.classList.remove('hidden');
            if (passInput) passInput.focus();
        }
        speakVoice("Please enter demo password WARI2026 to preview pilgrim wristband.");
    }

    function closeWristbandAuthModal() {
        const authModal = document.getElementById('wristband-auth-modal');
        if (authModal) authModal.classList.add('hidden');
    }

    function handleWristbandPasswordSubmit(enteredPassword) {
        const errEl = document.getElementById('wb-password-error');
        if (errEl) errEl.classList.add('hidden');

        fetch('/api/demo/verify-wristband-password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password: enteredPassword })
        })
        .then(res => res.json().then(data => ({ status: res.status, body: data })))
        .then(({ status, body }) => {
            if (status === 200 && body.success) {
                closeWristbandAuthModal();
                showPhysicalWristbandModal();
            } else {
                if (errEl) {
                    errEl.textContent = body.error || "❌ Incorrect demo password. Enter WARI2026.";
                    errEl.classList.remove('hidden');
                }
                showToast(body.error || "Incorrect demo password", "error");
                speakVoice("Incorrect demo password.");
            }
        })
        .catch(() => {
            // Fallback for prototype stability
            if (enteredPassword.toUpperCase() === 'WARI2026') {
                closeWristbandAuthModal();
                showPhysicalWristbandModal();
            } else {
                if (errEl) {
                    errEl.textContent = "❌ Incorrect demo password. Enter WARI2026.";
                    errEl.classList.remove('hidden');
                }
            }
        });
    }

    function showPhysicalWristbandModal() {
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
    }

    function closeWristbandModal() {
        const modal = document.getElementById('wristband-modal');
        if (modal) modal.classList.add('hidden');
    }"""

assert old_wb_func in js_code, "Could not find old_wb_func in script.js"
js_code = js_code.replace(old_wb_func, new_wb_func)

# Replace wristband event bindings in DOMContentLoaded
old_wb_bindings = """        document.getElementById('open-wristband-modal-btn')?.addEventListener('click', openWristbandModal);
        document.getElementById('preview-wristband-btn')?.addEventListener('click', openWristbandModal);
        document.getElementById('close-wristband-modal-btn')?.addEventListener('click', closeWristbandModal);
        document.getElementById('wristband-modal')?.addEventListener('click', (e) => {
            if (e.target.id === 'wristband-modal') closeWristbandModal();
        });
        document.getElementById('print-wristband-btn')?.addEventListener('click', () => {
            window.print();
        });"""

new_wb_bindings = """        // --- Wristband Password & Physical Preview Event Bindings ---
        document.getElementById('open-wristband-modal-btn')?.addEventListener('click', triggerWristbandAuthModal);
        document.getElementById('btn-view-demo-wristband')?.addEventListener('click', triggerWristbandAuthModal);
        document.getElementById('preview-wristband-btn')?.addEventListener('click', triggerWristbandAuthModal);
        
        document.getElementById('cancel-wb-pass-btn')?.addEventListener('click', closeWristbandAuthModal);
        document.getElementById('wristband-auth-modal')?.addEventListener('click', (e) => {
            if (e.target.id === 'wristband-auth-modal') closeWristbandAuthModal();
        });

        // Submit Wristband Password Form
        document.getElementById('wristband-pass-form')?.addEventListener('submit', (e) => {
            e.preventDefault();
            const passVal = document.getElementById('wb-password-input')?.value || '';
            handleWristbandPasswordSubmit(passVal);
        });

        document.getElementById('close-wristband-modal-btn')?.addEventListener('click', closeWristbandModal);
        document.getElementById('wristband-modal')?.addEventListener('click', (e) => {
            if (e.target.id === 'wristband-modal') closeWristbandModal();
        });
        document.getElementById('print-wristband-btn')?.addEventListener('click', () => {
            window.print();
        });

        // Copy QR Link Button
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

assert old_wb_bindings in js_code, "Could not find old_wb_bindings in script.js"
js_code = js_code.replace(old_wb_bindings, new_wb_bindings)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js_code)

print("Updated static/script.js with Wristband Password Flow and Public QR Link handlers!")
