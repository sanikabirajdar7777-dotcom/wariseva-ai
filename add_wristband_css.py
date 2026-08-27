css_addition = """
/* =========================================================================
   WARISEVA PHYSICAL HORIZONTAL QR WRISTBAND STYLES (FRONT & BACK)
   ========================================================================= */

.wb-view-tabs {
    display: flex;
    justify-content: center;
    gap: 8px;
    margin-bottom: 16px;
}
.wb-tab-btn {
    background: var(--bg-surface-0, #0D1117);
    border: 1px solid var(--border-color, #30363D);
    color: var(--text-secondary, #8B949E);
    padding: 8px 16px;
    border-radius: 9999px;
    font-size: 0.8rem;
    font-weight: 800;
    cursor: pointer;
    transition: all 0.2s ease;
}
.wb-tab-btn.active, .wb-tab-btn:hover {
    background: linear-gradient(135deg, #FF6B00, #FF0055);
    border-color: transparent;
    color: #FFFFFF;
    box-shadow: 0 0 15px rgba(255, 107, 0, 0.4);
}

.wristband-print-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
    width: 100%;
}

/* Horizontal Physical Wristband Band (Aspect Ratio ~3.5 : 1) */
.wristband-band {
    width: 100%;
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    border: 2px solid #38BDF8;
    border-radius: 16px;
    display: flex;
    align-items: stretch;
    position: relative;
    overflow: hidden;
    box-shadow: 0 12px 36px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.15);
    min-height: 165px;
    color: #FFFFFF;
}

.wristband-band.back-side {
    background: linear-gradient(135deg, #111827 0%, #1F2937 100%);
    border-color: #F59E0B;
}

/* Fastening / Perforation Tabs */
.wb-fastener-tab {
    width: 24px;
    background: rgba(0, 0, 0, 0.35);
    border-right: 1px dashed rgba(255, 255, 255, 0.25);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-around;
    padding: 10px 0;
}
.wb-fastener-tab.right-edge {
    border-right: none;
    border-left: 1px dashed rgba(255, 255, 255, 0.25);
}
.punch-hole {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #0A0E14;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Main Band Content Layout */
.wb-band-main {
    flex: 1;
    display: grid;
    grid-template-columns: 1.1fr 1.6fr 1.3fr;
    align-items: center;
    padding: 12px 16px;
    gap: 12px;
}

/* Front - Left Section */
.wb-section-left {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 4px;
    border-right: 1px solid rgba(255, 255, 255, 0.12);
    padding-right: 12px;
    height: 100%;
}
.wb-shield-brand {
    font-family: var(--font-display, 'Outfit', sans-serif);
    font-size: 1.15rem;
    font-weight: 900;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    gap: 6px;
    letter-spacing: 0.5px;
}
.wb-tagline {
    font-size: 0.68rem;
    color: #38BDF8;
    font-weight: 800;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.wb-emergency-badge {
    margin-top: 6px;
    background: rgba(255, 0, 85, 0.2);
    border: 1px solid #FF0055;
    color: #FF5252;
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 0.72rem;
    font-weight: 900;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    width: fit-content;
}

/* Front - Center Section */
.wb-section-center {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 4px;
    padding: 0 4px;
}
.wb-palkhi-pill {
    background: #FF6B00;
    color: #FFFFFF;
    padding: 2px 8px;
    border-radius: 9999px;
    font-size: 0.68rem;
    font-weight: 900;
    letter-spacing: 0.5px;
    width: fit-content;
}
.wb-wearer-name {
    font-family: var(--font-display, 'Outfit', sans-serif);
    font-size: 1.45rem;
    font-weight: 900;
    color: #FFFFFF;
    line-height: 1.15;
    text-transform: uppercase;
}
.wb-wearer-id-row {
    display: flex;
    align-items: center;
    gap: 8px;
}
.wb-wearer-id {
    font-family: var(--font-mono, 'JetBrains Mono', monospace);
    font-size: 1rem;
    font-weight: 900;
    color: #38BDF8;
}
.wb-dindi-tag {
    background: rgba(255, 255, 255, 0.12);
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 800;
}

/* Front - Right QR Section */
.wb-section-right {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-left: 1px solid rgba(255, 255, 255, 0.12);
    padding-left: 12px;
    height: 100%;
}
.wb-qr-pure-box {
    background: #FFFFFF;
    padding: 6px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
}
.wb-qr-pure-box canvas, .wb-qr-pure-box img, .wb-qr-pure-box svg {
    display: block !important;
    width: 96px !important;
    height: 96px !important;
}
.wb-scan-hint {
    font-size: 0.68rem;
    font-weight: 800;
    color: #FFD600;
    text-align: center;
    margin-top: 4px;
    letter-spacing: 0.3px;
}
.wb-scan-subhint {
    font-size: 0.6rem;
    color: var(--text-secondary, #8B949E);
    text-align: center;
}

/* Back Band - Content Layout */
.wb-back-main {
    flex: 1;
    display: grid;
    grid-template-columns: 1.1fr 1.8fr 1.1fr;
    align-items: center;
    padding: 12px 16px;
    gap: 12px;
}
.wb-back-title {
    font-family: var(--font-display, 'Outfit', sans-serif);
    font-size: 0.95rem;
    font-weight: 900;
    color: #F59E0B;
}
.wb-no-phone-badge {
    background: rgba(0, 230, 118, 0.15);
    border: 1px solid #00E676;
    color: #00E676;
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 0.72rem;
    font-weight: 900;
    margin-top: 6px;
    width: fit-content;
}
.wb-instructions-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 3px;
    font-size: 0.75rem;
    color: #E2E8F0;
}
.wb-instructions-list li {
    display: flex;
    align-items: flex-start;
    gap: 6px;
}
.wb-instructions-list strong {
    color: #FFD600;
}
.wb-helplines-pill {
    margin-top: 6px;
    font-size: 0.72rem;
    font-weight: 800;
    color: #FF5252;
    background: rgba(255, 0, 85, 0.15);
    padding: 2px 8px;
    border-radius: 4px;
    width: fit-content;
}
.wb-back-meta {
    display: flex;
    flex-direction: column;
    gap: 2px;
    border-left: 1px solid rgba(255, 255, 255, 0.12);
    padding-left: 12px;
    font-size: 0.68rem;
    color: var(--text-secondary, #8B949E);
}
.wb-back-meta strong {
    color: #FFF;
}

/* Responsive adjustments for mobile screens */
@media (max-width: 600px) {
    .wristband-band {
        min-height: auto;
    }
    .wb-band-main, .wb-back-main {
        grid-template-columns: 1fr;
        gap: 10px;
        text-align: center;
    }
    .wb-section-left, .wb-section-right, .wb-back-meta {
        border: none;
        padding: 0;
        align-items: center;
    }
    .wb-wearer-id-row {
        justify-content: center;
    }
}

/* =========================================================================
   CLEAN PRINT MEDIA STYLES
   ========================================================================= */

@media print {
    body {
        background: #FFFFFF !important;
        color: #000000 !important;
        margin: 0 !important;
        padding: 10mm !important;
    }
    /* Hide everything in app except printable wristband */
    header, nav, footer, .demo-control-bar, .emergency-ticker-bar, .view-container,
    .mobile-bottom-nav, .wristband-modal-head, .wb-status-bar, .wb-view-tabs,
    .qr-url-helper-box, .phone-test-instructions-card, .qr-diagnostics-card,
    .wristband-modal-actions, #sos-modal, #wristband-auth-modal, #pilgrim-incident-modal {
        display: none !important;
    }
    .modal-overlay, #wristband-modal {
        position: static !important;
        background: transparent !important;
        inset: auto !important;
        display: block !important;
        padding: 0 !important;
        box-shadow: none !important;
    }
    .modal-card.wristband-modal-card {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        max-width: 100% !important;
        padding: 0 !important;
    }
    .wristband-print-container {
        display: flex !important;
        flex-direction: column !important;
        gap: 25px !important;
    }
    .wristband-band {
        display: flex !important;
        visibility: visible !important;
        border: 2px solid #000000 !important;
        background: #FFFFFF !important;
        color: #000000 !important;
        box-shadow: none !important;
        page-break-inside: avoid !important;
    }
    .wristband-band * {
        color: #000000 !important;
    }
    .wb-shield-brand, .wb-wearer-name {
        color: #000000 !important;
    }
    .wb-palkhi-pill, .wb-emergency-badge, .wb-no-phone-badge {
        border: 1px solid #000000 !important;
        background: #EEEEEE !important;
        color: #000000 !important;
    }
    .wb-qr-pure-box {
        border: 1px solid #000000 !important;
        box-shadow: none !important;
    }
}
"""

with open('static/style.css', 'r', encoding='utf-8') as f:
    existing_css = f.read()

new_css = existing_css + "\n" + css_addition

with open('static/style.css', 'w', encoding='utf-8') as f:
    f.write(new_css)

print("Appended horizontal wristband and print media styles to static/style.css!")
