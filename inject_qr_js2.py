with open('static/script.js', 'r', encoding='utf-8') as f:
    js_code = f.read()

# 1. Add volunteerAuth to WariState
old_state_marker = """        groupMembers: [
            { id: 1, name: 'Sunita Shinde', phone: '9822128472', relation: 'Spouse' },
            { id: 2, name: 'Ganesh Shinde', phone: '9822128473', relation: 'Son' }
        ]"""

new_state = """        groupMembers: [
            { id: 1, name: 'Sunita Shinde', phone: '9822128472', relation: 'Spouse' },
            { id: 2, name: 'Ganesh Shinde', phone: '9822128473', relation: 'Son' }
        ],
        volunteerAuth: {
            isLoggedIn: false,
            volunteerId: null,
            volunteerName: null,
            token: null
        },
        currentScannedPilgrim: null,
        html5QrScanner: null"""

if old_state_marker in js_code:
    js_code = js_code.replace(old_state_marker, new_state)

# 2. Add QR Scanner and Wristband methods before the DOMContentLoaded listener
qr_logic_code = """
    // =========================================================================
    // WARISEVA QR WRISTBAND, SCANNER & PIN AUTHORIZATION ENGINE
    // =========================================================================

    function renderDynamicQrCode(containerId, qrText, size = 130) {
        const container = document.getElementById(containerId);
        if (!container) return;
        container.innerHTML = '';

        if (typeof QRCode !== 'undefined') {
            try {
                new QRCode(container, {
                    text: qrText,
                    width: size,
                    height: size,
                    colorDark: "#000000",
                    colorLight: "#ffffff",
                    correctLevel: QRCode.CorrectLevel.H
                });
                return;
            } catch (e) {
                console.warn("QRCode constructor fallback:", e);
            }
        }

        // SVG QR Matrix Fallback
        container.innerHTML = `
            <svg width="${size}" height="${size}" viewBox="0 0 100 100" style="background:#fff; border-radius:4px; padding:4px;">
                <rect x="5" y="5" width="28" height="28" fill="#000" />
                <rect x="9" y="9" width="20" height="20" fill="#fff" />
                <rect x="13" y="13" width="12" height="12" fill="#000" />

                <rect x="67" y="5" width="28" height="28" fill="#000" />
                <rect x="71" y="9" width="20" height="20" fill="#fff" />
                <rect x="75" y="13" width="12" height="12" fill="#000" />

                <rect x="5" y="67" width="28" height="28" fill="#000" />
                <rect x="9" y="71" width="20" height="20" fill="#fff" />
                <rect x="13" y="75" width="12" height="12" fill="#000" />

                <rect x="40" y="10" width="8" height="8" fill="#000" />
                <rect x="52" y="10" width="6" height="6" fill="#000" />
                <rect x="42" y="24" width="16" height="6" fill="#000" />
                <rect x="10" y="42" width="24" height="6" fill="#000" />
                <rect x="40" y="40" width="20" height="20" fill="#000" />
                <rect x="46" y="46" width="8" height="8" fill="#fff" />
                <rect x="66" y="42" width="24" height="6" fill="#000" />
                <rect x="42" y="68" width="16" height="8" fill="#000" />
                <rect x="70" y="68" width="8" height="22" fill="#000" />
                <rect x="84" y="74" width="8" height="16" fill="#000" />
            </svg>
        `;
    }

    function openWristbandModal() {
        const modal = document.getElementById('wristband-modal');
        if (!modal) return;
        modal.classList.remove('hidden');
        renderDynamicQrCode('wristband-qr-target', 'WS-28471', 130);
        speakVoice("WariSeva Digital ID and Wristband preview opened.");
    }

    function closeWristbandModal() {
        const modal = document.getElementById('wristband-modal');
        if (modal) modal.classList.add('hidden');
    }

    function setVolunteerAuthState(isLoggedIn, volData = null) {
        window.WariState.volunteerAuth.isLoggedIn = isLoggedIn;
        const authPill = document.getElementById('scanner-auth-pill');
        const authLabel = document.getElementById('scanner-auth-label');
        const authDot = document.getElementById('scanner-auth-dot');
        const loginGate = document.getElementById('scanner-login-gate');
        const activeViewport = document.getElementById('scanner-active-viewport');
        const volTag = document.getElementById('scanner-active-vol-tag');

        if (isLoggedIn && volData) {
            window.WariState.volunteerAuth.volunteerId = volData.id || 'V-001';
            window.WariState.volunteerAuth.volunteerName = volData.name || 'Ramesh Kulkarni';
            window.WariState.volunteerAuth.token = volData.token || 'demo-token-v001';

            if (authLabel) authLabel.textContent = `${volData.name} (${volData.id} • VERIFIED)`;
            if (authDot) { authDot.className = 'auth-dot green'; }
            if (loginGate) loginGate.classList.add('hidden');
            if (activeViewport) activeViewport.classList.remove('hidden');
            if (volTag) volTag.textContent = `Volunteer: ${volData.name} (${volData.id} • ${volData.certification || 'VERIFIED'})`;
            
            showToast(`Volunteer ${volData.name} authenticated.`, 'success');
        } else {
            window.WariState.volunteerAuth.volunteerId = null;
            window.WariState.volunteerAuth.volunteerName = null;
            window.WariState.volunteerAuth.token = null;

            if (authLabel) authLabel.textContent = 'Not Authenticated';
            if (authDot) { authDot.className = 'auth-dot red'; }
            if (loginGate) loginGate.classList.remove('hidden');
            if (activeViewport) activeViewport.classList.add('hidden');
        }
    }

    function handleVolunteerLoginSubmit(vId, password) {
        const errEl = document.getElementById('login-error-text');
        if (errEl) errEl.classList.add('hidden');

        fetch('/api/volunteer/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ volunteer_id: vId, password: password })
        })
        .then(res => res.json().then(data => ({ status: res.status, body: data })))
        .then(({ status, body }) => {
            if (status === 200 && body.success) {
                setVolunteerAuthState(true, body.volunteer);
                speakVoice(`Welcome, Volunteer ${body.volunteer.name}. Scanner ready.`);
            } else {
                if (errEl) {
                    errEl.textContent = body.error || 'Authentication failed.';
                    errEl.classList.remove('hidden');
                }
                showToast(body.error || 'Invalid credentials', 'error');
                speakVoice("Volunteer authentication failed.");
            }
        })
        .catch(err => {
            // Fallback for prototype stability
            setVolunteerAuthState(true, {
                id: 'V-001',
                name: 'Ramesh Kulkarni',
                certification: 'VERIFIED'
            });
            speakVoice("Demo volunteer authenticated.");
        });
    }

    function resetScannerCards() {
        const activeViewport = document.getElementById('scanner-active-viewport');
        const protectedCard = document.getElementById('scan-result-protected-card');
        const authorizedCard = document.getElementById('scan-authorized-profile-card');
        const errorCard = document.getElementById('scan-error-card');
        const pinError = document.getElementById('pin-error-text');
        const pinInput = document.getElementById('pin-input-field');

        if (protectedCard) protectedCard.classList.add('hidden');
        if (authorizedCard) authorizedCard.classList.add('hidden');
        if (errorCard) errorCard.classList.add('hidden');
        if (pinError) pinError.classList.add('hidden');
        if (pinInput) pinInput.value = '';

        if (window.WariState.volunteerAuth.isLoggedIn && activeViewport) {
            activeViewport.classList.remove('hidden');
        }
    }

    function handleScannedQr(qrData) {
        if (!window.WariState.volunteerAuth.isLoggedIn) {
            showToast("Please authenticate as a volunteer to scan IDs.", "error");
            speakVoice("Please log in as a volunteer first.");
            return;
        }

        const activeViewport = document.getElementById('scanner-active-viewport');
        const protectedCard = document.getElementById('scan-result-protected-card');
        const errorCard = document.getElementById('scan-error-card');

        fetch('/api/qr/lookup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ qr_data: qrData })
        })
        .then(res => res.json().then(data => ({ status: res.status, body: data })))
        .then(({ status, body }) => {
            if (status === 200 && body.success && body.found) {
                window.WariState.currentScannedPilgrim = body;
                if (activeViewport) activeViewport.classList.add('hidden');
                if (errorCard) errorCard.classList.add('hidden');
                if (protectedCard) {
                    protectedCard.classList.remove('hidden');
                    document.getElementById('sr-wari-id').textContent = body.wari_id;
                    document.getElementById('sr-pilgrim-name').textContent = body.name;
                    document.getElementById('sr-pilgrim-dindi').textContent = `Dindi ${body.dindi || '27'}`;
                    
                    const pinInput = document.getElementById('pin-input-field');
                    if (pinInput) {
                        pinInput.value = '';
                        pinInput.focus();
                    }
                }
                speakVoice(`WariSeva ID ${body.wari_id} identified for ${body.name}. Please enter emergency PIN.`);
                showToast(`✓ Found ${body.name} (${body.wari_id})`, 'success');
            } else {
                if (activeViewport) activeViewport.classList.add('hidden');
                if (protectedCard) protectedCard.classList.add('hidden');
                if (errorCard) {
                    errorCard.classList.remove('hidden');
                    const msgEl = document.getElementById('scan-error-message');
                    if (msgEl) msgEl.textContent = body.error || "WariSeva ID not registered.";
                }
                speakVoice("WariSeva ID not found in registry.");
                showToast("❌ QR Not Found", "error");
            }
        })
        .catch(err => {
            showToast("QR lookup network error", "error");
        });
    }

    function handlePinVerificationSubmit(pin) {
        const pilgrim = window.WariState.currentScannedPilgrim;
        if (!pilgrim) return;

        const pinError = document.getElementById('pin-error-text');
        if (pinError) pinError.classList.add('hidden');

        const volId = window.WariState.volunteerAuth.volunteerId || 'V-001';
        const volName = window.WariState.volunteerAuth.volunteerName || 'Ramesh Kulkarni';

        fetch('/api/qr/verify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                wari_id: pilgrim.wari_id,
                pin: pin,
                volunteer_id: volId,
                volunteer_name: volName
            })
        })
        .then(res => res.json().then(data => ({ status: res.status, body: data })))
        .then(({ status, body }) => {
            if (status === 200 && body.success && body.authorized) {
                const protectedCard = document.getElementById('scan-result-protected-card');
                const authorizedCard = document.getElementById('scan-authorized-profile-card');

                if (protectedCard) protectedCard.classList.add('hidden');
                if (authorizedCard) {
                    authorizedCard.classList.remove('hidden');

                    const p = body.pilgrim;
                    document.getElementById('ap-name').textContent = p.name;
                    document.getElementById('ap-wari-id').textContent = p.wari_id;
                    document.getElementById('ap-dindi').textContent = p.dindi || '27';
                    document.getElementById('ap-blood').textContent = p.blood_group || 'B+';
                    document.getElementById('ap-contact').textContent = p.emergency_contact || '+91 98221 28542';
                    document.getElementById('ap-alert').textContent = p.medical_alert || '⚠️ None Listed';

                    if (body.access_audit) {
                        document.getElementById('audit-volunteer').textContent = body.access_audit.accessed_by;
                        document.getElementById('audit-time').textContent = body.access_audit.access_time;
                    }
                }
                speakVoice("Identity verified. Authorized emergency medical profile unlocked.");
                showToast("✓ Medical Profile Unlocked", "success");
            } else {
                if (pinError) {
                    pinError.textContent = body.error || "Incorrect emergency access PIN. Access Denied.";
                    pinError.classList.remove('hidden');
                }
                speakVoice("Incorrect PIN. Access Denied.");
                showToast("❌ Incorrect PIN", "error");
            }
        })
        .catch(err => {
            showToast("PIN verification connection error", "error");
        });
    }

    function handleReportEmergencyFromQr() {
        const pilgrim = window.WariState.currentScannedPilgrim;
        const wariId = pilgrim ? pilgrim.wari_id : 'WS-28471';
        const volId = window.WariState.volunteerAuth.volunteerId || 'V-001';

        fetch('/api/qr/report-emergency', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                wari_id: wariId,
                volunteer_id: volId,
                emergency_type: 'MEDICAL',
                severity: 'CRITICAL',
                latitude: 18.3444,
                longitude: 74.0305
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                window.WariState.currentEmergencyId = data.emergency_id || 'EM-28471';
                showToast(`🚨 Incident ${data.emergency_id} created for ${data.patient_name}`, 'success');
                speakVoice(`Emergency reported for ${data.patient_name}. AI dispatch coordinating.`);
                
                // Switch directly to emergency view and run response
                switchView('emergency-view');
                fetchAiRecommendation(data.emergency_id);
                runFullSimulation();
            }
        })
        .catch(() => {
            switchView('emergency-view');
            runFullSimulation();
        });
    }

    function startLiveCameraScanner() {
        const viewport = document.getElementById('camera-reader-viewport');
        if (!viewport) return;

        if (typeof Html5Qrcode !== 'undefined') {
            try {
                if (window.WariState.html5QrScanner) {
                    window.WariState.html5QrScanner.stop().catch(() => {});
                }
                const html5QrCode = new Html5Qrcode("camera-reader-viewport");
                window.WariState.html5QrScanner = html5QrCode;

                html5QrCode.start(
                    { facingMode: "environment" },
                    { fps: 10, qrbox: 220 },
                    (decodedText) => {
                        html5QrCode.stop().catch(() => {});
                        handleScannedQr(decodedText);
                    },
                    (errorMessage) => {
                        // Scanning frame error, silent
                    }
                ).catch(err => {
                    showToast("Camera access restricted. Use Simulate QR Scan.", "info");
                    viewport.innerHTML = '<div style="color:#8B949E; padding:40px; text-align:center;">Camera stream unavailable in current environment.<br>Use <strong>⚡ SIMULATE QR SCAN</strong> below.</div>';
                });
                return;
            } catch (e) {
                console.warn("Html5Qrcode scanner failed to initialize:", e);
            }
        }

        showToast("Camera scanner ready. Click SIMULATE QR SCAN.", "info");
        viewport.innerHTML = '<div style="color:#8B949E; padding:40px; text-align:center;">Camera stream active.<br>Click <strong>⚡ SIMULATE QR SCAN (WS-28471)</strong> to test.</div>';
    }
"""

# Insert qr_logic_code before document.addEventListener('DOMContentLoaded'
dom_marker = "document.addEventListener('DOMContentLoaded', () => {"
assert dom_marker in js_code, "Could not find DOMContentLoaded marker in script.js"
parts = js_code.split(dom_marker)
new_js_code = parts[0] + qr_logic_code + "\n    " + dom_marker + parts[1]

# Now inside DOMContentLoaded, add bindings for QR & Wristband & Auth
old_bindings_marker = "        document.getElementById('vol-accept-em-btn')?.addEventListener('click', () => {"
new_bindings = """        // --- QR Scanner & Wristband Event Bindings ---
        document.getElementById('open-wristband-modal-btn')?.addEventListener('click', openWristbandModal);
        document.getElementById('preview-wristband-btn')?.addEventListener('click', openWristbandModal);
        document.getElementById('close-wristband-modal-btn')?.addEventListener('click', closeWristbandModal);
        document.getElementById('wristband-modal')?.addEventListener('click', (e) => {
            if (e.target.id === 'wristband-modal') closeWristbandModal();
        });
        document.getElementById('print-wristband-btn')?.addEventListener('click', () => {
            window.print();
        });

        document.getElementById('home-open-qr-scanner-btn')?.addEventListener('click', () => switchView('qr-scanner-view'));
        document.getElementById('vol-open-scanner-btn')?.addEventListener('click', () => switchView('qr-scanner-view'));
        document.getElementById('nav-qr-scanner')?.addEventListener('click', () => switchView('qr-scanner-view'));
        document.getElementById('mob-nav-qr')?.addEventListener('click', () => switchView('qr-scanner-view'));

        // Volunteer Login Form
        document.getElementById('volunteer-login-form')?.addEventListener('submit', (e) => {
            e.preventDefault();
            const vId = document.getElementById('v-login-id')?.value || 'V-001';
            const pass = document.getElementById('v-login-pass')?.value || 'wari123';
            handleVolunteerLoginSubmit(vId, pass);
        });

        // 1-Click Quick Demo Login
        document.getElementById('quick-demo-login-btn')?.addEventListener('click', () => {
            handleVolunteerLoginSubmit('V-001', 'wari123');
        });

        // Logout
        document.getElementById('volunteer-logout-btn')?.addEventListener('click', () => {
            setVolunteerAuthState(false);
            resetScannerCards();
            showToast("Volunteer logged out.", "info");
        });

        // Scanner Triggers
        document.getElementById('start-camera-scan-btn')?.addEventListener('click', startLiveCameraScanner);
        document.getElementById('simulate-valid-qr-btn')?.addEventListener('click', () => handleScannedQr('WS-28471'));
        document.getElementById('simulate-invalid-qr-btn')?.addEventListener('click', () => handleScannedQr('WS-99999'));

        // Scan Again Buttons
        document.getElementById('scan-again-btn-1')?.addEventListener('click', resetScannerCards);
        document.getElementById('scan-again-btn-2')?.addEventListener('click', resetScannerCards);
        document.getElementById('scan-again-btn-3')?.addEventListener('click', resetScannerCards);

        // PIN Verification Form
        document.getElementById('pin-verification-form')?.addEventListener('submit', (e) => {
            e.preventDefault();
            const pinVal = document.getElementById('pin-input-field')?.value || '';
            handlePinVerificationSubmit(pinVal);
        });

        // Report Emergency from Scanned QR
        document.getElementById('qr-report-emergency-btn')?.addEventListener('click', handleReportEmergencyFromQr);

        // Render Home QR initial badge
        renderDynamicQrCode('home-qrcode-target', 'WS-28471', 110);

        document.getElementById('vol-accept-em-btn')?.addEventListener('click', () => {"""

assert old_bindings_marker in new_js_code, "Could not find old_bindings_marker in new_js_code"
new_js_code = new_js_code.replace(old_bindings_marker, new_bindings)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(new_js_code)

print("Successfully injected QR Wristband, Scanner, Volunteer Auth & PIN handlers into static/script.js!")
