with open('templates/index.html', 'r', encoding='utf-8') as f:
    html_code = f.read()

target = """        <!-- ================= 6. WARISEVA PHYSICAL QR WRISTBAND MODAL ================= -->
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

replacement = """        <!-- ================= 6. WARISEVA PHYSICAL QR WRISTBAND MODAL ================= -->
        <div id="wristband-modal" class="modal-overlay hidden" role="dialog" aria-modal="true">
            <div class="modal-card wristband-modal-card" style="max-width: 640px;">
                <div class="wristband-modal-head">
                    <span class="wb-shield-icon">🛡️</span>
                    <div>
                        <h3 class="wristband-modal-title">WariSeva PHYSICAL QR WRISTBAND</h3>
                        <span class="wristband-modal-sub">Scan using any NORMAL PHONE CAMERA / Google Lens (No app required)</span>
                    </div>
                </div>

                <!-- Connection & LAN Status Strip -->
                <div class="wb-status-bar" style="display: flex; align-items: center; justify-content: space-between; background: rgba(0, 230, 118, 0.12); border: 1px solid #00E676; border-radius: 8px; padding: 8px 12px; margin-bottom: 14px; flex-wrap: wrap; gap: 6px;">
                    <span style="color: #00E676; font-weight: 800; font-size: 0.82rem;">🟢 PHONE SCAN READY</span>
                    <span style="font-size: 0.78rem; color: var(--text-secondary);">LAN Address: <strong id="wb-lan-ip-display" style="color: #00E5FF; font-family: var(--font-mono);">192.168.1.5:5000</strong></span>
                    <span style="font-size: 0.78rem; color: #FFD600; font-weight: 700;">QR Target: Emergency Profile</span>
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
                            <div class="wb-qr-frame" style="padding: 10px; background: #FFFFFF; border-radius: 12px; box-shadow: 0 4px 18px rgba(0,0,0,0.5);">
                                <div id="wristband-qr-target" style="display: flex; align-items: center; justify-content: center; min-width: 200px; min-height: 200px;"></div>
                                <span class="wb-qr-label" style="display: block; color: #0D1117; font-family: var(--font-display); font-size: 0.75rem; font-weight: 800; margin-top: 6px;">SCAN WITH ANY PHONE</span>
                                <span id="wb-qr-url-subtext" style="display: block; color: #57606A; font-family: var(--font-mono); font-size: 0.68rem; font-weight: 700; word-break: break-all; margin-top: 2px;">http://192.168.1.5:5000/public/pilgrim/WS-28471</span>
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
                        🔗 <strong>PUBLIC QR DESTINATION URL (LAN IP):</strong>
                    </div>
                    <div style="display: flex; align-items: center; justify-content: space-between; gap: 8px; flex-wrap: wrap;">
                        <span id="wb-qr-url-text" style="font-family: var(--font-mono); font-size: 0.82rem; color: var(--accent-cyan); word-break: break-all;">http://192.168.1.5:5000/public/pilgrim/WS-28471</span>
                        <div style="display: flex; gap: 8px;">
                            <button type="button" id="copy-qr-link-btn" class="text-link-btn" style="background: rgba(0,229,255,0.15); color: #00E5FF; padding: 6px 12px; border-radius: 6px; font-size: 0.78rem; font-weight: 800; border: none; cursor: pointer;">📋 Copy QR Link</button>
                            <a id="open-public-profile-link" href="/public/pilgrim/WS-28471" target="_blank" class="text-link-btn" style="background: rgba(0,230,118,0.15); color: #00E676; padding: 6px 12px; border-radius: 6px; font-size: 0.78rem; font-weight: 800; text-decoration: none;">🌐 Test QR Link ↗</a>
                        </div>
                    </div>
                </div>

                <!-- Phone Test Instructions Box -->
                <div class="phone-test-instructions-card" style="margin-top: 10px; background: rgba(255, 107, 0, 0.08); border: 1px solid rgba(255, 107, 0, 0.35); border-radius: 10px; padding: 12px 14px; text-align: left;">
                    <div style="font-size: 0.8rem; font-weight: 800; color: var(--accent-orange); margin-bottom: 4px;">
                        📱 PHONE TEST INSTRUCTIONS:
                    </div>
                    <ol style="font-size: 0.78rem; color: var(--text-secondary); margin-left: 18px; line-height: 1.45;">
                        <li>Connect your phone and laptop to the <strong>SAME Wi-Fi network</strong>.</li>
                        <li>Open your phone's camera app or Google Lens and point at the QR code.</li>
                        <li>Tap the link banner on your phone screen to open the public emergency profile.</li>
                        <li>The emergency profile loads with one-tap SOS reporting for Tukaram Shinde!</li>
                    </ol>
                </div>

                <!-- QR Connection Diagnostics & Troubleshooting Card -->
                <div class="qr-diagnostics-card" style="margin-top: 10px; background: #0D1117; border: 1px solid var(--border-color); border-radius: 10px; padding: 12px 14px; text-align: left;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span style="font-size: 0.78rem; font-weight: 800; color: #8B949E;">🔍 QR CONNECTION TEST & DIAGNOSTICS</span>
                        <button type="button" id="copy-diag-url-btn" style="background: transparent; border: 1px solid rgba(0, 229, 255, 0.4); color: #00E5FF; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; cursor: pointer;">📋 Copy Phone Test URL</button>
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 6px; font-size: 0.75rem; color: var(--text-secondary);">
                        <div>Computer: <strong style="color: #00E676;">✓ Flask running</strong></div>
                        <div>LAN IP: <strong id="diag-lan-ip" style="color: #00E5FF; font-family: var(--font-mono);">192.168.1.5</strong></div>
                        <div>Server: <strong style="color: #00E676;">✓ 0.0.0.0:5000</strong></div>
                        <div>Public Profile: <strong style="color: #00E676;">✓ /public/pilgrim/WS-28471</strong></div>
                    </div>
                    <div style="font-size: 0.72rem; color: #8B949E; margin-top: 6px; border-top: 1px dashed rgba(255,255,255,0.1); padding-top: 6px;">
                        ℹ️ <em>If phone cannot reach the demo server: Ensure laptop and phone are on the same Wi-Fi and Windows Firewall allows Python on Private networks.</em>
                    </div>
                </div>

                <div class="wristband-modal-actions" style="margin-top: 14px;">
                    <button type="button" id="print-wristband-btn" class="modal-btn confirm-btn">
                        🖨️ PRINT / PREVIEW WRISTBAND
                    </button>
                    <button type="button" id="close-wristband-modal-btn" class="modal-btn cancel-btn">
                        CLOSE
                    </button>
                </div>
            </div>
        </div>"""

assert target in html_code, "Could not find target in index.html"
html_code = html_code.replace(target, replacement)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

print("Updated templates/index.html with full phone diagnostic and physical wristband layout!")
