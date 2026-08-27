import os

css_path = os.path.join(os.path.dirname(__file__), 'static', 'style.css')

mobile_css = """

/* ==========================================================================
   WARISEVA AI — COMPREHENSIVE MOBILE RESPONSIVE & DRAWER ENGINE
   ========================================================================== */

/* Ensure full box-sizing and prevent accidental horizontal page stretch */
*, *::before, *::after {
    box-sizing: border-box;
}

html, body {
    max-width: 100%;
    overflow-x: hidden;
}

/* Tablet & Mobile Breakpoint (<= 992px) */
@media (max-width: 992px) {
    /* Layout Shell */
    .app-wrapper {
        display: block !important;
        width: 100% !important;
        max-width: 100% !important;
        min-height: 100vh !important;
        overflow-x: hidden !important;
        position: relative !important;
    }

    /* Off-Canvas Mobile Drawer Sidebar */
    .sidebar-panel {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        bottom: 0 !important;
        width: 280px !important;
        max-width: 82vw !important;
        height: 100vh !important;
        height: 100dvh !important;
        background: var(--bg-surface-1) !important;
        border-right: 1px solid var(--border-subtle) !important;
        z-index: 9999 !important;
        transform: translateX(-100%) !important;
        transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 6px 0 28px rgba(0, 0, 0, 0.7) !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        overflow-y: auto !important;
        -webkit-overflow-scrolling: touch;
    }

    .sidebar-panel.mobile-open {
        transform: translateX(0) !important;
    }

    /* Mobile Drawer Backdrop */
    .sidebar-backdrop {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        height: 100dvh !important;
        background: rgba(0, 0, 0, 0.65) !important;
        backdrop-filter: blur(4px) !important;
        -webkit-backdrop-filter: blur(4px) !important;
        z-index: 9998 !important;
        transition: opacity 0.25s ease !important;
    }

    .sidebar-backdrop.hidden {
        display: none !important;
    }

    /* Hamburger & Close Buttons */
    .mobile-menu-btn {
        display: flex !important;
        align-items: center;
        justify-content: center;
        width: 36px;
        height: 36px;
        background: var(--bg-surface-2);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-sm);
        color: #FFFFFF;
        font-size: 1.15rem;
        cursor: pointer;
        flex-shrink: 0;
    }

    .sidebar-close-btn {
        display: flex !important;
        align-items: center;
        justify-content: center;
        width: 30px;
        height: 30px;
        background: var(--bg-surface-2);
        border: 1px solid var(--border-subtle);
        border-radius: 50%;
        color: var(--text-primary);
        font-size: 0.9rem;
        cursor: pointer;
        margin-left: auto;
        flex-shrink: 0;
    }

    .sidebar-brand {
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        padding: 14px 12px !important;
    }

    .sidebar-brand-content {
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
    }

    /* Main Application Wrapper */
    .main-wrapper {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        display: flex !important;
        flex-direction: column !important;
        min-height: 100vh !important;
        height: auto !important;
        overflow-x: hidden !important;
    }

    /* Top Navigation Bar */
    .top-nav-bar {
        height: auto !important;
        min-height: 52px !important;
        padding: 8px 12px !important;
        display: flex !important;
        flex-wrap: wrap !important;
        align-items: center !important;
        justify-content: space-between !important;
        gap: 8px !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }

    .top-nav-left {
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
        flex: 1 1 auto !important;
        min-width: 0 !important;
    }

    .top-zone-badge {
        font-size: 0.72rem !important;
        padding: 4px 8px !important;
        white-space: normal !important;
        line-height: 1.2 !important;
        max-width: 100% !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }

    .top-nav-right {
        display: flex !important;
        align-items: center !important;
        gap: 6px !important;
        flex-wrap: wrap !important;
        justify-content: flex-end !important;
    }

    .user-profile-pill {
        max-width: 125px !important;
        font-size: 0.7rem !important;
        padding: 4px 8px !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }

    /* Content Canvas */
    .content-canvas {
        padding: 12px 10px 84px 10px !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        overflow-x: hidden !important;
        height: auto !important;
    }

    /* Home Hero Grid (Vertical Stack) */
    .home-hero-grid {
        grid-template-columns: 1fr !important;
        gap: 14px !important;
        width: 100% !important;
        max-width: 100% !important;
    }

    .hero-card {
        padding: 14px 12px !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }

    /* Operational Deck Grid (Vertical Stack) */
    .operational-deck-grid {
        grid-template-columns: 1fr !important;
        gap: 12px !important;
        width: 100% !important;
        max-width: 100% !important;
    }

    .op-card {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        padding: 12px !important;
    }

    /* SOS Button Proportional Scaling */
    .master-sos-circular-btn {
        width: 114px !important;
        height: 114px !important;
    }

    .sos-ring-pulse {
        width: 136px !important;
        height: 136px !important;
    }

    .sos-label-main {
        font-size: 1.7rem !important;
    }

    .sos-label-sub {
        font-size: 0.56rem !important;
        max-width: 75px !important;
    }

    /* Quick Stats Grid */
    .quick-stats-grid {
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 8px !important;
        width: 100% !important;
    }

    .stat-box {
        padding: 8px !important;
        font-size: 0.72rem !important;
        min-width: 0 !important;
    }

    .stat-box-val {
        font-size: 0.76rem !important;
    }

    /* Safety Network Map & Filter Bar */
    .safety-filter-bar {
        display: flex !important;
        gap: 6px !important;
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        width: 100% !important;
        max-width: 100% !important;
        padding-bottom: 6px !important;
        margin-bottom: 8px !important;
        flex-wrap: nowrap !important;
    }

    .filter-pill-btn {
        flex-shrink: 0 !important;
        padding: 4px 8px !important;
        font-size: 0.72rem !important;
    }

    .safety-map-container-box {
        width: 100% !important;
        max-width: 100% !important;
        height: 220px !important;
        min-height: 200px !important;
        box-sizing: border-box !important;
    }

    /* Fixed Mobile Bottom Navigation Bar */
    .mobile-bottom-nav {
        display: flex !important;
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        width: 100% !important;
        max-width: 100vw !important;
        height: 58px !important;
        background: var(--bg-surface-1) !important;
        border-top: 1px solid var(--border-subtle) !important;
        z-index: 990 !important;
        justify-content: space-around !important;
        align-items: center !important;
        padding: 0 4px !important;
        box-sizing: border-box !important;
        box-shadow: 0 -4px 16px rgba(0, 0, 0, 0.4) !important;
    }

    .mob-nav-btn {
        flex: 1 1 0 !important;
        max-width: 16.66% !important;
        min-width: 0 !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 2px !important;
        padding: 4px 1px !important;
        background: transparent !important;
        border: none !important;
        color: var(--text-muted) !important;
        cursor: pointer !important;
        overflow: hidden !important;
        text-decoration: none !important;
    }

    .mob-nav-btn.active {
        color: #FF6D00 !important;
        font-weight: 700 !important;
    }

    .mob-icon {
        font-size: 1.1rem !important;
        line-height: 1 !important;
    }

    .mob-label {
        font-size: 0.62rem !important;
        line-height: 1 !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        max-width: 100% !important;
        text-align: center !important;
    }

    .mob-sos-btn .mob-sos-circle {
        width: 32px !important;
        height: 32px !important;
        border-radius: 50% !important;
        background: linear-gradient(135deg, #FF1744, #B71C1C) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 0 10px rgba(255, 23, 68, 0.6) !important;
        margin-top: -6px !important;
    }

    /* Secondary Grids & Layouts */
    .ai-recommendations-duo-grid,
    .response-clock-and-audit-grid,
    .cmd-stats-quad,
    .network-portals-grid,
    .inspector-details-grid {
        grid-template-columns: 1fr !important;
        gap: 12px !important;
    }

    .emergency-nearest-relationship-banner .rel-nodes-row {
        flex-direction: column !important;
        align-items: stretch !important;
        gap: 8px !important;
    }

    .rel-connector {
        align-self: center !important;
        transform: rotate(90deg) !important;
        margin: 2px 0 !important;
    }

    .rel-node-card {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }

    /* Modals Responsive */
    .modal-card,
    .wristband-modal-card {
        max-width: 94vw !important;
        width: 94vw !important;
        padding: 14px !important;
        max-height: 90vh !important;
        overflow-y: auto !important;
        box-sizing: border-box !important;
    }

    .wristband-band {
        flex-direction: column !important;
        min-height: auto !important;
        width: 100% !important;
        max-width: 100% !important;
    }

    .wb-band-main {
        grid-template-columns: 1fr !important;
        gap: 8px !important;
        width: 100% !important;
    }
}

/* Small Smartphone Breakpoint (<= 480px) */
@media (max-width: 480px) {
    .top-nav-bar {
        padding: 6px 8px !important;
    }

    .top-zone-badge {
        font-size: 0.68rem !important;
    }

    .lang-btn-group .lang-tab-btn {
        padding: 3px 6px !important;
        font-size: 0.68rem !important;
    }

    .top-action-btn {
        padding: 3px 6px !important;
        font-size: 0.68rem !important;
    }

    .quick-stats-grid {
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 6px !important;
    }

    .stat-box {
        padding: 6px !important;
    }
}

/* Micro Smartphone Breakpoint (<= 360px) */
@media (max-width: 360px) {
    .master-sos-circular-btn {
        width: 102px !important;
        height: 102px !important;
    }

    .sos-ring-pulse {
        width: 122px !important;
        height: 122px !important;
    }

    .sos-label-main {
        font-size: 1.5rem !important;
    }

    .quick-stats-grid {
        grid-template-columns: 1fr !important;
    }

    .mob-label {
        font-size: 0.58rem !important;
    }
}
"""

with open(css_path, 'r', encoding='utf-8') as f:
    current_content = f.read()

# Append mobile styles
updated_content = current_content + mobile_css

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(updated_content)

print(f"Mobile responsive CSS appended successfully! Total length: {len(updated_content)} chars.")
