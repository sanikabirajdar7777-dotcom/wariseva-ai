with open('templates/index.html', 'r', encoding='utf-8') as f:
    html_code = f.read()

# 1. Update toolbar to add [ VIEW DEMO WRISTBAND ] and [ TEST QR SCAN ]
old_toolbar_actions = """            <div class="demo-bar-actions">
                <button type="button" id="voice-toggle-btn" class="demo-pill-btn voice-btn" title="Toggle Spoken Voice Assistance">
                    🔊 Voice: ON
                </button>
                <button type="button" id="run-simulation-demo-btn" class="demo-action-btn pulse-orange" title="Auto-advance complete emergency response lifecycle">
                    ▶ SIMULATE RESPONSE
                </button>
                <button type="button" id="create-demo-em-btn" class="demo-action-btn primary">
                    ⚡ CREATE DEMO EMERGENCY
                </button>
                <button type="button" id="reset-demo-btn" class="demo-action-btn secondary" data-i18n="reset_demo">
                    🔄 RESET
                </button>
            </div>"""

new_toolbar_actions = """            <div class="demo-bar-actions">
                <button type="button" id="voice-toggle-btn" class="demo-pill-btn voice-btn" title="Toggle Spoken Voice Assistance">
                    🔊 Voice: ON
                </button>
                <button type="button" id="btn-view-demo-wristband" class="demo-action-btn" style="background: linear-gradient(135deg, #00E5FF, #2979FF); color:#FFF; font-weight:800;" title="Preview WariSeva Physical QR Wristband (Password Required)">
                    🪪 VIEW DEMO WRISTBAND
                </button>
                <button type="button" id="btn-test-qr-scan" class="demo-action-btn" style="background: rgba(255, 214, 0, 0.15); border: 1px solid #FFD600; color:#FFD600; font-weight:800;" title="Test Public QR Profile URL directly in browser">
                    ⚡ TEST QR SCAN
                </button>
                <button type="button" id="run-simulation-demo-btn" class="demo-action-btn pulse-orange" title="Auto-advance complete emergency response lifecycle">
                    ▶ SIMULATE RESPONSE
                </button>
                <button type="button" id="reset-demo-btn" class="demo-action-btn secondary" data-i18n="reset_demo">
                    🔄 RESET
                </button>
            </div>"""

if old_toolbar_actions in html_code:
    html_code = html_code.replace(old_toolbar_actions, new_toolbar_actions)

# 2. Add Wristband Password Modal and Enhanced Wristband Modal
old_wristband_block = """        <!-- ================= 6. WARISEVA DIGITAL WRISTBAND ID MODAL ================= -->
        <div id="wristband-modal" class="modal-overlay hidden" role="dialog" aria-modal="true">
            <div class="modal-card wristband-modal-card">
                <div class="wristband-modal-head">
                    <span class="wb-shield-icon">🛡️</span>
                    <div>
                        <h3 class="wristband-modal-title">WariSeva DIGITAL ID & WRISTBAND</h3>
                        <span class="wristband-modal-sub">Waterproof Pilgrim Safety & Emergency Identity</span>
                    </div>
                </div>

                <!-- Printable Wristband Card Surface -->
                <div class="wristband-physical-card" id="printable-wristband-surface">
                    <div class="wb-card-top-bar">
                        <span class="wb-brand">WARISEVA AI</span>
                        <span class="wb-palkhi-tag">🚩 SANT DNYANESHWAR & TUKARAM WARI</span>
                        <span class="wb-dindi-pill">DINDI 27</span>
                    </div>
                    <div class="wb-card-main-row">
                        <div class="wb-card-info-col">
                            <span class="wb-kicker">PILGRIM IDENTITY / वारकरी ओळख</span>
                            <h2 class="wb-pilgrim-name" id="wb-display-name">TUKARAM SHINDE</h2>
                            <div class="wb-id-number" id="wb-display-id">WS-28471</div>
                            <div class="wb-sec-desc">Emergency Assistance ID • Dindi 27</div>
                            <div class="wb-help-prompt">SCAN FOR EMERGENCY ASSISTANCE</div>
                        </div>
                        <div class="wb-card-qr-col">
                            <div class="wb-qr-frame">
                                <div id="wristband-qr-target"></div>
                                <span class="wb-qr-label">WS-28471</span>
                            </div>
                        </div>
                    </div>
                    <div class="wb-card-foot-bar">
                        <span>DEMO / PROTOTYPE WRISTBAND</span>
                        <span>•</span>
                        <span>📵 NO SMARTPHONE REQUIRED</span>
                        <span>•</span>
                        <span>PROTECTED PIN AUTHORIZATION</span>
                    </div>
                </div>

                <div class="wristband-modal-actions">
                    <button type="button" id="print-wristband-btn" class="modal-btn confirm-btn">
                        🖨️ PRINT / PREVIEW WRISTBAND
                    </button>
                    <button type="button" id="close-wristband-modal-btn" class="modal-btn cancel-btn">
                        CLOSE
                    </button>
                </div>
            </div>
        </div>"""

new_wristband_block = """        <!-- ================= 5B. WRISTBAND DEMO ACCESS PASSWORD MODAL ================= -->
        <div id="wristband-auth-modal" class="modal-overlay hidden" role="dialog" aria-modal="true">
            <div class="modal-card">
                <div class="modal-icon-header">🔐</div>
                <h3 class="modal-title">WariSeva Demo Access</h3>
                <p class="modal-msg">Enter demo password to preview the registered pilgrim wristband.</p>
                
                <form id="wristband-pass-form" class="safety-form-grid">
                    <div class="form-field">
                        <label class="field-label">Demo Password</label>
                        <input type="password" id="wb-password-input" class="field-input" placeholder="Enter Demo Password" required autocomplete="off">
                    </div>
                    <div class="pin-demo-hint" style="text-align: left; margin-bottom: 6px;">
                        💡 <em>Demo Password: <strong>WARI2026</strong></em>
                    </div>
                    <div id="wb-password-error" class="form-error-text hidden" role="alert"></div>

                    <div class="modal-actions" style="margin-top: 12px;">
                        <button type="button" id="cancel-wb-pass-btn" class="modal-btn cancel-btn">CANCEL</button>
                        <button type="submit" id="verify-wb-pass-btn" class="modal-btn confirm-btn">VERIFY</button>
                    </div>
                </form>
            </div>
        </div>

        <!-- ================= 6. WARISEVA PHYSICAL QR WRISTBAND MODAL ================= -->
        <div id="wristband-modal" class="modal-overlay hidden" role="dialog" aria-modal="true">
            <div class="modal-card wristband-modal-card">
                <div class="wristband-modal-head">
                    <span class="wb-shield-icon">🛡️</span>
                    <div>
                        <h3 class="wristband-modal-title">WariSeva QR WRISTBAND (PHYSICAL PROTOTYPE)</h3>
                        <span class="wristband-modal-sub">Scan using any NORMAL PHONE CAMERA / Google Lens (No app required)</span>
                    </div>
                </div>

                <!-- Printable Wristband Card Surface -->
                <div class="wristband-physical-card" id="printable-wristband-surface">
                    <div class="wb-card-top-bar">
                        <span class="wb-brand">WARISEVA AI</span>
                        <span class="wb-palkhi-tag">🚩 SANT DNYANESHWAR & TUKARAM WARI</span>
                        <span class="wb-dindi-pill">DINDI 27</span>
                    </div>
                    <div class="wb-card-main-row">
                        <div class="wb-card-info-col">
                            <span class="wb-kicker">PILGRIM IDENTITY / वारकरी ओळख</span>
                            <h2 class="wb-pilgrim-name" id="wb-display-name">TUKARAM SHINDE</h2>
                            <div class="wb-id-number" id="wb-display-id">WS-28471</div>
                            <div class="wb-sec-desc">Emergency Assistance ID • Dindi 27</div>
                            <div class="wb-help-prompt">📱 SCAN WITH ANY PHONE CAMERA</div>
                        </div>
                        <div class="wb-card-qr-col">
                            <div class="wb-qr-frame">
                                <div id="wristband-qr-target"></div>
                                <span class="wb-qr-label" id="wb-qr-scan-label">SCAN QR</span>
                            </div>
                        </div>
                    </div>
                    <div class="wb-card-foot-bar">
                        <span>DEMO / PROTOTYPE WRISTBAND</span>
                        <span>•</span>
                        <span>📵 NO SMARTPHONE REQUIRED FOR PILGRIM</span>
                        <span>•</span>
                        <span>PUBLIC PROFILE ACCESS</span>
                    </div>
                </div>

                <!-- Direct Public URL & Link Helpers for Testers/Judges -->
                <div class="qr-url-helper-box" style="margin-top: 14px; background: rgba(0,0,0,0.3); border: 1px dashed rgba(0,229,255,0.3); border-radius: 10px; padding: 12px 14px; text-align: left;">
                    <div style="font-size: 0.78rem; color: var(--text-secondary); margin-bottom: 4px;">
                        🔗 <strong>PUBLIC QR DESTINATION URL:</strong>
                    </div>
                    <div style="display: flex; align-items: center; justify-content: space-between; gap: 8px; flex-wrap: wrap;">
                        <span id="wb-qr-url-text" style="font-family: var(--font-mono); font-size: 0.82rem; color: var(--accent-cyan); word-break: break-all;">http://127.0.0.1:5000/public/pilgrim/WS-28471</span>
                        <div style="display: flex; gap: 8px;">
                            <button type="button" id="copy-qr-link-btn" class="text-link-btn" style="background: rgba(0,229,255,0.15); color: #00E5FF; padding: 4px 10px; border-radius: 6px; font-size: 0.78rem; font-weight: 700; border: none; cursor: pointer;">📋 Copy Link</button>
                            <a id="open-public-profile-link" href="/public/pilgrim/WS-28471" target="_blank" class="text-link-btn" style="background: rgba(0,230,118,0.15); color: #00E676; padding: 4px 10px; border-radius: 6px; font-size: 0.78rem; font-weight: 700; text-decoration: none;">🌐 Open Profile ↗</a>
                        </div>
                    </div>
                </div>

                <div class="wristband-modal-actions">
                    <button type="button" id="print-wristband-btn" class="modal-btn confirm-btn">
                        🖨️ PRINT / PREVIEW WRISTBAND
                    </button>
                    <button type="button" id="close-wristband-modal-btn" class="modal-btn cancel-btn">
                        CLOSE
                    </button>
                </div>
            </div>
        </div>"""

if old_wristband_block in html_code:
    html_code = html_code.replace(old_wristband_block, new_wristband_block)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

print("Updated templates/index.html with Wristband Password Modal and Public QR URL helpers!")
