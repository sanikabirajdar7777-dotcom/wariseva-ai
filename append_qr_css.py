qr_css = """
/* ==========================================================================
   WARISEVA QR WRISTBAND, SCANNER & PIN AUTHORIZATION STYLING
   ========================================================================== */

.wristband-header-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: linear-gradient(135deg, rgba(0, 229, 255, 0.15), rgba(41, 121, 255, 0.25));
    border: 1px solid rgba(0, 229, 255, 0.4);
    color: var(--accent-cyan, #00E5FF);
    padding: 7px 14px;
    border-radius: var(--radius-full, 9999px);
    font-size: 0.85rem;
    font-weight: 700;
    cursor: pointer;
    transition: all var(--trans-fast, 0.15s ease);
}
.wristband-header-btn:hover {
    background: linear-gradient(135deg, rgba(0, 229, 255, 0.3), rgba(41, 121, 255, 0.45));
    box-shadow: 0 0 15px rgba(0, 229, 255, 0.3);
    transform: translateY(-1px);
}

.wristband-modal-card {
    max-width: 580px;
    width: 95%;
    background: var(--bg-card, #161B22);
    border: 1px solid rgba(0, 229, 255, 0.3);
    border-radius: var(--radius-xl, 18px);
    padding: 24px;
    box-shadow: 0 16px 48px rgba(0, 0, 0, 0.6), 0 0 30px rgba(0, 229, 255, 0.15);
}

.wristband-modal-head {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
}
.wb-shield-icon {
    font-size: 2rem;
}
.wristband-modal-title {
    font-family: var(--font-display);
    font-size: 1.25rem;
    font-weight: 800;
    color: var(--text-primary);
    margin: 0;
}
.wristband-modal-sub {
    font-size: 0.85rem;
    color: var(--text-secondary);
}

/* Printable Physical Wristband / Card Surface */
.wristband-physical-card {
    background: linear-gradient(145deg, #0A1128 0%, #001F54 50%, #034078 100%);
    border: 2px solid var(--accent-cyan, #00E5FF);
    border-radius: 16px;
    padding: 20px;
    color: #FFFFFF;
    box-shadow: inset 0 0 20px rgba(0, 229, 255, 0.2), 0 8px 24px rgba(0, 0, 0, 0.4);
    position: relative;
    overflow: hidden;
}
.wristband-physical-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 4px;
    background: linear-gradient(90deg, #FF6B00, #FFD600, #00E5FF);
}

.wb-card-top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.5px;
}
.wb-brand {
    color: var(--accent-cyan, #00E5FF);
    font-family: var(--font-display);
    font-size: 0.95rem;
}
.wb-palkhi-tag {
    color: #FFD600;
}
.wb-dindi-pill {
    background: #FF6B00;
    color: #FFF;
    padding: 3px 10px;
    border-radius: 9999px;
    font-weight: 800;
}

.wb-card-main-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
}
.wb-card-info-col {
    flex: 1;
}
.wb-kicker {
    font-size: 0.75rem;
    color: #A0C4FF;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.wb-pilgrim-name {
    font-family: var(--font-display);
    font-size: 1.5rem;
    font-weight: 900;
    color: #FFFFFF;
    margin: 4px 0;
    letter-spacing: 0.5px;
}
.wb-id-number {
    font-family: var(--font-mono, monospace);
    font-size: 1.3rem;
    font-weight: 800;
    color: var(--accent-cyan, #00E5FF);
    margin-bottom: 6px;
    letter-spacing: 1px;
}
.wb-sec-desc {
    font-size: 0.85rem;
    color: #E0E1DD;
    margin-bottom: 8px;
}
.wb-help-prompt {
    display: inline-block;
    background: rgba(0, 229, 255, 0.15);
    border: 1px solid rgba(0, 229, 255, 0.4);
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 800;
    color: #00E5FF;
    letter-spacing: 0.5px;
}

.wb-card-qr-col {
    display: flex;
    flex-direction: column;
    align-items: center;
}
.wb-qr-frame {
    background: #FFFFFF;
    padding: 8px;
    border-radius: 10px;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.wb-qr-label {
    display: block;
    color: #0D1117;
    font-family: var(--font-mono, monospace);
    font-size: 0.72rem;
    font-weight: 800;
    margin-top: 4px;
}

.wb-card-foot-bar {
    display: flex;
    justify-content: center;
    gap: 8px;
    margin-top: 16px;
    padding-top: 12px;
    border-top: 1px dashed rgba(255, 255, 255, 0.2);
    font-size: 0.72rem;
    color: #A0C4FF;
    font-weight: 700;
}

.wristband-modal-actions {
    display: flex;
    gap: 12px;
    margin-top: 20px;
}

/* ==========================================================================
   QR SCANNER VIEW
   ========================================================================== */

.qr-scanner-container {
    max-width: 780px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.scanner-header-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--bg-card, #161B22);
    border: 1px solid var(--border-color, #30363D);
    border-radius: var(--radius-lg, 14px);
    padding: 18px 24px;
}
.sh-left {
    display: flex;
    align-items: center;
    gap: 14px;
}
.sh-icon {
    font-size: 2rem;
}
.sh-title {
    font-family: var(--font-display);
    font-size: 1.3rem;
    font-weight: 800;
    color: var(--text-primary);
    margin: 0;
}
.sh-sub {
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin: 2px 0 0 0;
}

.sh-auth-status {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid var(--border-color);
    padding: 6px 14px;
    border-radius: 9999px;
    font-size: 0.8rem;
    font-weight: 700;
}
.auth-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
}
.auth-dot.green { background: #00E676; box-shadow: 0 0 8px #00E676; }
.auth-dot.red { background: #FF5252; box-shadow: 0 0 8px #FF5252; }

.no-phone-banner {
    display: flex;
    align-items: center;
    gap: 14px;
    background: linear-gradient(135deg, rgba(255, 107, 0, 0.1), rgba(255, 214, 0, 0.08));
    border: 1px solid rgba(255, 107, 0, 0.35);
    border-radius: var(--radius-md, 10px);
    padding: 14px 18px;
}
.np-icon {
    font-size: 1.8rem;
}
.np-text {
    font-size: 0.85rem;
    color: var(--text-primary);
    line-height: 1.45;
}
.np-text strong {
    color: var(--accent-orange, #FF6B00);
    display: block;
    margin-bottom: 2px;
}

.scanner-card-box {
    background: var(--bg-card, #161B22);
    border: 1px solid var(--border-color, #30363D);
    border-radius: var(--radius-xl, 18px);
    padding: 24px;
    box-shadow: var(--shadow-card);
}

.gate-head {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 20px;
}
.gate-lock-icon {
    font-size: 2rem;
}
.gate-head h3 {
    font-family: var(--font-display);
    font-size: 1.2rem;
    font-weight: 800;
    color: var(--text-primary);
    margin: 0;
}
.gate-head p {
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin: 4px 0 0 0;
}

.scanner-auth-form {
    display: flex;
    flex-direction: column;
    gap: 16px;
}
.auth-buttons-row {
    display: flex;
    gap: 12px;
    margin-top: 8px;
}
.auth-submit-btn {
    flex: 1;
    padding: 12px;
    border-radius: var(--radius-md);
    font-weight: 700;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.15s ease;
}
.auth-submit-btn.primary {
    background: linear-gradient(135deg, var(--accent-orange), var(--accent-red));
    border: none;
    color: #FFF;
}
.auth-submit-btn.secondary {
    background: rgba(0, 229, 255, 0.1);
    border: 1px solid rgba(0, 229, 255, 0.4);
    color: var(--accent-cyan);
}

/* Active Scanner Stage */
.scanner-stage-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 16px;
}
.stage-vol-tag {
    display: inline-block;
    background: rgba(0, 230, 118, 0.12);
    border: 1px solid rgba(0, 230, 118, 0.4);
    color: #00E676;
    padding: 4px 10px;
    border-radius: 9999px;
    font-size: 0.78rem;
    font-weight: 700;
    margin-bottom: 6px;
}
.stage-prompt {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0;
}

.scanner-viewfinder-frame {
    position: relative;
    height: 280px;
    background: #0D1117;
    border-radius: 14px;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px dashed rgba(0, 229, 255, 0.3);
}
.camera-viewport-stream {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.viewfinder-overlay {
    position: absolute;
    inset: 20px;
    pointer-events: none;
}
.corner-border {
    position: absolute;
    width: 24px;
    height: 24px;
    border-color: var(--accent-cyan, #00E5FF);
    border-style: solid;
}
.corner-border.top-left { top: 0; left: 0; border-width: 3px 0 0 3px; }
.corner-border.top-right { top: 0; right: 0; border-width: 3px 3px 0 0; }
.corner-border.bottom-left { bottom: 0; left: 0; border-width: 0 0 3px 3px; }
.corner-border.bottom-right { bottom: 0; right: 0; border-width: 0 3px 3px 0; }

.laser-scanner-line {
    position: absolute;
    left: 10px;
    right: 10px;
    height: 2px;
    background: linear-gradient(90deg, transparent, #00E5FF, #FF0055, #00E5FF, transparent);
    box-shadow: 0 0 10px #00E5FF;
    animation: scanLaser 2.2s infinite ease-in-out;
}
@keyframes scanLaser {
    0% { top: 10%; opacity: 0.4; }
    50% { top: 85%; opacity: 1; }
    100% { top: 10%; opacity: 0.4; }
}

.scanner-triggers-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 12px;
    margin-top: 18px;
}
.scanner-act-btn {
    padding: 12px;
    border-radius: var(--radius-md);
    font-weight: 800;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.15s ease;
}
.camera-act {
    background: linear-gradient(135deg, #2979FF, #00E5FF);
    border: none;
    color: #FFF;
}
.sim-valid-act {
    background: linear-gradient(135deg, #FF6B00, #FF9100);
    border: none;
    color: #FFF;
}
.sim-invalid-act {
    background: rgba(255, 82, 82, 0.15);
    border: 1px solid rgba(255, 82, 82, 0.4);
    color: #FF5252;
}

/* Scan Result Stage 1: Identity Located */
.scan-found-banner {
    display: flex;
    align-items: center;
    gap: 14px;
    background: rgba(0, 230, 118, 0.12);
    border: 1px solid rgba(0, 230, 118, 0.4);
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 18px;
}
.sfb-check {
    font-size: 1.6rem;
    color: #00E676;
    font-weight: 900;
}
.sfb-title {
    font-size: 0.8rem;
    color: #00E676;
    font-weight: 800;
    display: block;
}
.sfb-id {
    font-family: var(--font-mono, monospace);
    font-size: 1.3rem;
    font-weight: 800;
    color: #FFFFFF;
}

.scan-public-info-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 12px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 14px;
    margin-bottom: 20px;
}
.spi-item {
    display: flex;
    flex-direction: column;
    gap: 2px;
}
.spi-lbl {
    font-size: 0.75rem;
    color: var(--text-secondary);
}

.pin-authorization-box {
    background: linear-gradient(145deg, rgba(255, 107, 0, 0.08), rgba(255, 0, 85, 0.05));
    border: 1px solid rgba(255, 107, 0, 0.35);
    border-radius: 14px;
    padding: 20px;
}
.pin-head {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
}
.pin-lock-icon {
    font-size: 1.8rem;
}
.pin-head h4 {
    font-family: var(--font-display);
    font-size: 1.05rem;
    font-weight: 800;
    color: #FFFFFF;
    margin: 0;
}
.pin-head p {
    font-size: 0.8rem;
    color: var(--text-secondary);
    margin: 2px 0 0 0;
}

.pin-inputs-row {
    display: flex;
    gap: 12px;
    margin-bottom: 8px;
}
.pin-digit-input {
    width: 140px;
    text-align: center;
    font-family: var(--font-mono, monospace);
    font-size: 1.5rem;
    font-weight: 900;
    letter-spacing: 8px;
    background: #0D1117;
    border: 2px solid rgba(0, 229, 255, 0.5);
    border-radius: 8px;
    color: var(--accent-cyan, #00E5FF);
    padding: 8px;
}
.pin-digit-input:focus {
    outline: none;
    border-color: #FF6B00;
    box-shadow: 0 0 12px rgba(255, 107, 0, 0.4);
}
.verify-pin-btn {
    flex: 1;
    background: linear-gradient(135deg, #FF6B00, #FF9100);
    border: none;
    border-radius: 8px;
    color: #FFF;
    font-weight: 800;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.15s ease;
}
.verify-pin-btn:hover {
    box-shadow: 0 0 15px rgba(255, 107, 0, 0.4);
}
.pin-demo-hint {
    font-size: 0.8rem;
    color: #FFD600;
    margin-top: 6px;
}

/* Scan Result Stage 2: Authorized Emergency Profile */
.auth-success-banner {
    display: flex;
    align-items: center;
    gap: 14px;
    background: rgba(0, 230, 118, 0.15);
    border: 1px solid #00E676;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 20px;
}
.asb-icon {
    font-size: 1.8rem;
    color: #00E676;
    font-weight: 900;
}
.auth-success-banner h3 {
    font-family: var(--font-display);
    font-size: 1.1rem;
    font-weight: 800;
    color: #00E676;
    margin: 0;
}
.asb-sub {
    font-size: 0.78rem;
    color: #A0C4FF;
}

.authorized-data-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 12px;
    margin-bottom: 20px;
}
.ad-card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 14px;
}
.ad-card.medical-alert-full {
    grid-column: 1 / -1;
    background: rgba(255, 0, 85, 0.08);
    border-color: rgba(255, 0, 85, 0.35);
}
.ad-label {
    font-size: 0.75rem;
    color: var(--text-secondary);
    display: block;
    margin-bottom: 4px;
}
.ad-val {
    font-size: 1.05rem;
    font-weight: 800;
    color: var(--text-primary);
}

.access-audit-box {
    background: #0D1117;
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 20px;
}
.audit-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.75rem;
    font-weight: 800;
    color: #8B949E;
    margin-bottom: 8px;
}
.audit-status-tag {
    color: #00E676;
}
.audit-details-row {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    font-size: 0.82rem;
    color: var(--text-secondary);
}
.audit-details-row strong {
    color: var(--text-primary);
}

.authorized-actions-bar {
    display: flex;
    flex-direction: column;
    gap: 10px;
}
.qr-mega-sos-btn {
    width: 100%;
    padding: 16px;
    background: linear-gradient(135deg, #FF0055, #FF5252);
    border: none;
    border-radius: 12px;
    color: #FFFFFF;
    font-family: var(--font-display);
    font-size: 1.1rem;
    font-weight: 900;
    cursor: pointer;
    box-shadow: 0 0 25px rgba(255, 0, 85, 0.4);
    transition: all 0.2s ease;
}
.qr-mega-sos-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 35px rgba(255, 0, 85, 0.6);
}

.error-result-box {
    text-align: center;
    padding: 30px 20px;
}
.error-result-head {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
}
.err-icon {
    font-size: 2.5rem;
}
.error-result-head h3 {
    color: #FF5252;
    font-size: 1.3rem;
    margin: 0;
}
"""

with open('static/style.css', 'r', encoding='utf-8') as f:
    style_code = f.read()

new_style_code = style_code + "\n" + qr_css

with open('static/style.css', 'w', encoding='utf-8') as f:
    f.write(new_style_code)

print("Appended QR Wristband and Scanner CSS rules to static/style.css!")
