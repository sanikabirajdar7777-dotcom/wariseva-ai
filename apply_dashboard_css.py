import re

sidebar_and_dashboard_css = """
/* ==========================================================================
   WARISEVA AI — RESTORED MASTER DASHBOARD & SIDEBAR DESIGN SYSTEM
   ========================================================================== */

/* App Wrapper: Full Viewport Horizontal Flex Layout */
.app-wrapper {
    display: flex !important;
    flex-direction: row !important;
    min-height: 100vh !important;
    width: 100vw !important;
    max-width: 100% !important;
    margin: 0 !important;
    background-color: var(--bg-app);
    overflow: hidden;
    position: relative;
}

/* ================= LEFT SIDEBAR NAVIGATION ================= */
.sidebar-panel {
    width: 250px;
    min-width: 250px;
    max-width: 250px;
    height: 100vh;
    background: var(--bg-surface-1);
    border-right: 1px solid var(--border-subtle);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    z-index: 100;
    position: relative;
    user-select: none;
}

/* Sidebar Brand Header */
.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 16px 14px;
    border-bottom: 1px solid var(--border-subtle);
    background: rgba(0, 0, 0, 0.2);
}

.sidebar-logo-img {
    width: 38px;
    height: 38px;
    border-radius: var(--radius-sm);
    object-fit: cover;
    border: 1px solid rgba(255, 109, 0, 0.4);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
}

.sidebar-brand-text {
    display: flex;
    flex-direction: column;
}

.sidebar-brand-title {
    font-family: var(--font-display);
    font-size: 1.15rem;
    font-weight: 800;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    gap: 6px;
    line-height: 1.2;
}

.sidebar-ai-tag {
    font-size: 0.65rem;
    font-weight: 900;
    background: #FF6D00;
    color: #FFFFFF;
    padding: 1px 6px;
    border-radius: var(--radius-sm);
    letter-spacing: 0.05em;
}

.sidebar-brand-tagline {
    font-size: 0.7rem;
    color: var(--text-muted);
    line-height: 1.2;
}

/* Sidebar Navigation List */
.sidebar-nav-list {
    list-style: none;
    padding: 10px 8px;
    margin: 0;
    overflow-y: auto;
    max-height: calc(100vh - 170px);
    display: flex;
    flex-direction: column;
    gap: 3px;
}

.sidebar-nav-item {
    width: 100%;
}

.sidebar-panel .nav-link-btn {
    width: 100%;
    background: transparent;
    color: var(--text-secondary);
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 0.84rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 10px;
    transition: all var(--transition-fast);
    border: 1px solid transparent;
    cursor: pointer;
    text-align: left;
}

.sidebar-panel .nav-link-btn:hover {
    background: var(--bg-surface-2);
    color: #FFFFFF;
    border-color: rgba(255, 255, 255, 0.08);
}

.sidebar-panel .nav-link-btn.active {
    background: linear-gradient(135deg, #8B0000, #B71C1C) !important;
    color: #FFFFFF !important;
    font-weight: 700;
    border-color: #D32F2F;
    box-shadow: 0 3px 12px rgba(183, 28, 28, 0.45);
}

.sidebar-panel .nav-icon {
    font-size: 1.05rem;
    width: 20px;
    text-align: center;
}

.nav-badge {
    background: var(--emergency-red-bright);
    color: #FFF;
    font-size: 0.65rem;
    font-weight: 900;
    padding: 1px 6px;
    border-radius: var(--radius-full);
    margin-left: auto;
}

/* Bottom System Status Card in Sidebar */
.sidebar-system-card {
    background: rgba(0, 0, 0, 0.35);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 10px 12px;
    margin: 10px;
    font-size: 0.72rem;
    color: var(--text-secondary);
}

.sys-status-head {
    display: flex;
    align-items: center;
    gap: 6px;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 4px;
}

.sys-pulse-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #00E676;
    box-shadow: 0 0 8px #00E676;
    animation: sysPulse 2s infinite;
}

@keyframes sysPulse {
    0% { transform: scale(0.95); opacity: 0.8; box-shadow: 0 0 4px #00E676; }
    50% { transform: scale(1.15); opacity: 1; box-shadow: 0 0 12px #00E676; }
    100% { transform: scale(0.95); opacity: 0.8; box-shadow: 0 0 4px #00E676; }
}

.sys-status-meta {
    display: flex;
    flex-direction: column;
    gap: 2px;
    font-size: 0.68rem;
    color: var(--text-muted);
}

/* ================= MAIN WRAPPER & TOP NAV ================= */
.main-wrapper {
    flex: 1;
    display: flex;
    flex-direction: column;
    height: 100vh;
    overflow: hidden;
    background: var(--bg-app);
    min-width: 0;
}

/* Top Navigation Bar */
.top-nav-bar {
    height: 56px;
    min-height: 56px;
    background: var(--bg-surface-1);
    border-bottom: 1px solid var(--border-subtle);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    z-index: 90;
    gap: 12px;
}

.top-nav-left {
    display: flex;
    align-items: center;
    gap: 12px;
}

.top-zone-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255, 109, 0, 0.12);
    border: 1px solid rgba(255, 109, 0, 0.35);
    color: #FFB74D;
    padding: 5px 12px;
    border-radius: var(--radius-full);
    font-size: 0.8rem;
    font-weight: 700;
}

.badge-icon {
    font-size: 0.9rem;
}

.top-nav-right {
    display: flex;
    align-items: center;
    gap: 10px;
}

/* Trilingual Switcher */
.lang-btn-group {
    display: inline-flex;
    background: var(--bg-surface-2);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-full);
    padding: 2px;
}

.lang-tab-btn {
    background: transparent;
    color: var(--text-muted);
    border: none;
    padding: 4px 10px;
    border-radius: var(--radius-full);
    font-size: 0.75rem;
    font-weight: 700;
    cursor: pointer;
    transition: all var(--transition-fast);
}

.lang-tab-btn:hover {
    color: #FFFFFF;
}

.lang-tab-btn.active {
    background: #FF6D00;
    color: #FFFFFF;
    box-shadow: 0 2px 6px rgba(255, 109, 0, 0.4);
}

.top-action-btn {
    background: var(--bg-surface-2);
    border: 1px solid var(--border-subtle);
    color: var(--text-primary);
    padding: 5px 12px;
    border-radius: var(--radius-sm);
    font-size: 0.78rem;
    font-weight: 700;
    cursor: pointer;
    transition: var(--transition-fast);
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.top-action-btn:hover {
    background: var(--bg-surface-hover);
    color: #FFFFFF;
}

.top-action-btn.active {
    background: rgba(0, 230, 118, 0.15);
    border-color: rgba(0, 230, 118, 0.4);
    color: #00E676;
}

.notif-bell-btn {
    position: relative;
    background: var(--bg-surface-2);
    border: 1px solid var(--border-subtle);
    color: #FFFFFF;
    width: 34px;
    height: 34px;
    border-radius: var(--radius-sm);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 0.95rem;
    transition: var(--transition-fast);
}

.notif-bell-btn:hover {
    background: var(--bg-surface-hover);
}

.notif-badge {
    position: absolute;
    top: -4px;
    right: -4px;
    background: var(--emergency-red-bright);
    color: #FFFFFF;
    font-size: 0.65rem;
    font-weight: 900;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px solid var(--bg-surface-1);
}

.user-profile-pill {
    display: flex;
    align-items: center;
    gap: 6px;
    background: var(--bg-surface-2);
    border: 1px solid var(--border-subtle);
    padding: 5px 12px;
    border-radius: var(--radius-full);
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--text-primary);
}

.user-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--safety-green-bright);
    box-shadow: 0 0 6px var(--safety-green-bright);
}

/* ================= SCROLLABLE CONTENT CANVAS ================= */
.content-canvas {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    scroll-behavior: smooth;
}

/* ================= HOME DASHBOARD GRID ================= */
.home-dashboard-grid {
    display: flex;
    flex-direction: column;
    gap: 20px;
    max-width: 1360px;
    margin: 0 auto;
}

/* Hero Section: 2 Large Side-by-Side Cards */
.home-hero-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

@media (max-width: 1024px) {
    .home-hero-grid {
        grid-template-columns: 1fr;
    }
}

.hero-card {
    background: var(--bg-surface-1);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 20px;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-md);
    display: flex;
    flex-direction: column;
}

.hero-card-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 14px;
}

.hero-card-title {
    font-family: var(--font-display);
    font-size: 1.05rem;
    font-weight: 800;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    gap: 8px;
}

.hero-card-sub {
    font-size: 0.78rem;
}

/* Emergency Assistance Card */
.emergency-assistance-card {
    background: linear-gradient(145deg, #161B22 0%, #1D1115 100%);
    border-color: rgba(255, 82, 82, 0.3);
}

.emergency-card-body {
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    flex: 1;
}

.emergency-card-bg-logo {
    position: absolute;
    right: -10px;
    bottom: -10px;
    width: 200px;
    height: 200px;
    opacity: 0.07;
    pointer-events: none;
    object-fit: contain;
    z-index: 0;
}

/* Circular Master SOS Button */
.sos-button-wrapper {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 18px 0;
    z-index: 1;
}

.sos-ring-pulse {
    position: absolute;
    width: 170px;
    height: 170px;
    border-radius: 50%;
    border: 2px solid rgba(255, 23, 68, 0.4);
    animation: ringPulse 2s infinite ease-out;
}

@keyframes ringPulse {
    0% { transform: scale(0.85); opacity: 0.9; }
    50% { transform: scale(1.15); opacity: 0.4; }
    100% { transform: scale(1.3); opacity: 0; }
}

.master-sos-circular-btn {
    width: 140px;
    height: 140px;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 35%, #FF1744, #B71C1C, #660000);
    border: 4px solid #FFA4A4;
    color: #FFFFFF;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 0 35px rgba(255, 23, 68, 0.6), inset 0 2px 10px rgba(255, 255, 255, 0.4);
    transition: all 0.15s cubic-bezier(0.16, 1, 0.3, 1);
    user-select: none;
    z-index: 2;
}

.master-sos-circular-btn:hover {
    transform: scale(1.04);
    box-shadow: 0 0 45px rgba(255, 23, 68, 0.8), inset 0 2px 12px rgba(255, 255, 255, 0.5);
}

.master-sos-circular-btn:active {
    transform: scale(0.96);
    box-shadow: 0 0 20px rgba(255, 23, 68, 0.9);
}

.sos-label-main {
    font-family: var(--font-display);
    font-size: 2.2rem;
    font-weight: 900;
    letter-spacing: 2px;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.6);
    line-height: 1;
}

.sos-label-sub {
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.4px;
    opacity: 0.9;
    text-align: center;
    max-width: 90px;
    line-height: 1.1;
    margin-top: 4px;
}

/* Quick Stats 4-Box Grid */
.quick-stats-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
    margin-top: 12px;
    z-index: 1;
}

.stat-box {
    background: rgba(0, 0, 0, 0.45);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 10px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.stat-box-icon {
    font-size: 1.3rem;
    flex-shrink: 0;
}

.stat-box-text {
    display: flex;
    flex-direction: column;
    min-width: 0;
}

.stat-box-lbl {
    font-size: 0.65rem;
    font-weight: 800;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.4px;
}

.stat-box-val {
    font-size: 0.82rem;
    font-weight: 700;
    color: #FFFFFF;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.stat-box-sub {
    font-size: 0.7rem;
    color: var(--accent-cyan);
}

/* Safety Network Card */
.safety-network-card {
    background: var(--bg-surface-1);
    display: flex;
    flex-direction: column;
}

.safety-filter-bar {
    display: flex;
    gap: 6px;
    overflow-x: auto;
    padding-bottom: 8px;
    margin-bottom: 10px;
}

.filter-pill-btn {
    background: var(--bg-surface-2);
    border: 1px solid var(--border-subtle);
    color: var(--text-secondary);
    padding: 4px 10px;
    border-radius: var(--radius-full);
    font-size: 0.74rem;
    font-weight: 700;
    cursor: pointer;
    white-space: nowrap;
    transition: all var(--transition-fast);
}

.filter-pill-btn:hover {
    background: var(--bg-surface-hover);
    color: #FFFFFF;
}

.filter-pill-btn.active {
    background: #FF6D00;
    border-color: #FFA000;
    color: #FFFFFF;
    box-shadow: 0 2px 8px rgba(255, 109, 0, 0.4);
}

.safety-map-container-box {
    flex: 1;
    min-height: 220px;
    border-radius: var(--radius-md);
    overflow: hidden;
    border: 1px solid var(--border-subtle);
    position: relative;
}

.safety-map-footer-strip {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 0.76rem;
    color: var(--text-muted);
    margin-top: 10px;
}

/* ================= 4-COLUMN OPERATIONAL DECK ================= */
.operational-deck-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
}

@media (max-width: 1200px) {
    .operational-deck-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 650px) {
    .operational-deck-grid {
        grid-template-columns: 1fr;
    }
}

.op-card {
    background: var(--bg-surface-1);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 16px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: var(--shadow-sm);
}

.op-card-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    padding-bottom: 8px;
}

.op-card-title {
    font-family: var(--font-display);
    font-size: 0.88rem;
    font-weight: 800;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    gap: 6px;
}

.op-card-status-badge {
    font-size: 0.68rem;
    font-weight: 800;
    padding: 2px 8px;
    border-radius: 6px;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: #FFFFFF;
}

.op-card-body {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 12px;
}

.op-action-btn {
    width: 100%;
    background: linear-gradient(135deg, #8B0000, #B71C1C);
    color: #FFFFFF;
    border: none;
    padding: 8px 12px;
    border-radius: var(--radius-sm);
    font-weight: 800;
    font-size: 0.8rem;
    cursor: pointer;
    transition: all var(--transition-fast);
    text-align: center;
}

.op-action-btn:hover {
    background: linear-gradient(135deg, #A00000, #D32F2F);
    box-shadow: 0 3px 12px rgba(183, 28, 28, 0.45);
}

.op-action-btn.secondary {
    background: var(--bg-surface-2);
    border: 1px solid var(--border-subtle);
    color: var(--text-secondary);
}

.op-action-btn.secondary:hover {
    background: var(--bg-surface-hover);
    color: #FFFFFF;
}

/* Stepper List */
.stepper-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.stepper-step {
    display: flex;
    flex-direction: column;
    padding-left: 16px;
    position: relative;
    font-size: 0.76rem;
}

.stepper-step::before {
    content: '';
    position: absolute;
    left: 0;
    top: 5px;
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--border-strong);
}

.stepper-step.completed::before {
    background: #00E676;
    box-shadow: 0 0 6px #00E676;
}

.stepper-step.active::before {
    background: #FFB74D;
    box-shadow: 0 0 6px #FFB74D;
}

.step-title-txt {
    font-weight: 700;
    color: #FFFFFF;
}

.step-time-txt {
    font-size: 0.68rem;
    color: var(--text-muted);
}

/* Incident Info Box in Op Cards */
.incident-info-box {
    background: rgba(0, 0, 0, 0.35);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 10px;
    display: flex;
    flex-direction: column;
    gap: 4px;
    font-size: 0.78rem;
}

.incident-head-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 4px;
}

.inc-id-tag {
    font-family: var(--font-mono);
    font-size: 0.78rem;
    font-weight: 800;
    color: var(--accent-cyan);
}

.inc-sev-badge {
    background: rgba(255, 0, 85, 0.2);
    border: 1px solid #FF0055;
    color: #FF5252;
    font-size: 0.65rem;
    font-weight: 800;
    padding: 1px 6px;
    border-radius: var(--radius-sm);
}

.inc-row-detail {
    color: var(--text-secondary);
    font-size: 0.75rem;
}

/* Hospital Capacity Pill Row */
.capacity-pill-row {
    display: flex;
    gap: 8px;
}

.cap-pill {
    flex: 1;
    background: rgba(0, 0, 0, 0.35);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 8px;
    text-align: center;
}

.cap-pill-num {
    font-size: 1.2rem;
    font-weight: 900;
    color: #00E676;
}

.cap-pill-lbl {
    font-size: 0.62rem;
    font-weight: 800;
    color: var(--text-muted);
    text-transform: uppercase;
}

/* Command Center Quad Stats */
.cmd-stats-quad {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
}

.cmd-quad-stat {
    background: rgba(0, 0, 0, 0.35);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 6px;
    text-align: center;
}

.cmd-quad-num {
    font-size: 1.15rem;
    font-weight: 900;
}

.cmd-quad-num.red { color: #FF5252; }
.cmd-quad-num.orange { color: #FFB74D; }
.cmd-quad-num.blue { color: #4FC3F7; }
.cmd-quad-num.green { color: #00E676; }

.cmd-quad-lbl {
    font-size: 0.62rem;
    font-weight: 800;
    color: var(--text-muted);
    text-transform: uppercase;
}

/* Secondary Quick Action Buttons Row */
.hero-secondary-actions {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
}

.quick-act-btn {
    background: var(--bg-surface-1);
    border: 1px solid var(--border-subtle);
    color: var(--text-primary);
    padding: 8px 16px;
    border-radius: var(--radius-md);
    font-size: 0.82rem;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    cursor: pointer;
    transition: all var(--transition-fast);
}

.quick-act-btn:hover {
    background: var(--bg-surface-hover);
    color: #FFFFFF;
    border-color: rgba(255, 255, 255, 0.2);
    transform: translateY(-1px);
}

.act-icon {
    font-size: 1rem;
}

/* ================= JOIN THE WARI SAFETY NETWORK PORTALS ================= */
.network-portals-section {
    background: var(--bg-surface-1);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 20px;
}

.section-title-row {
    margin-bottom: 16px;
}

.home-section-title {
    font-family: var(--font-display);
    font-size: 1.1rem;
    font-weight: 800;
    color: #FFFFFF;
}

.section-subtitle {
    font-size: 0.78rem;
    color: var(--text-muted);
}

.network-portals-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 16px;
}

.network-portal-card {
    background: rgba(0, 0, 0, 0.35);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 16px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.npc-icon {
    font-size: 1.8rem;
    margin-bottom: 6px;
}

.npc-title {
    font-family: var(--font-display);
    font-size: 0.95rem;
    font-weight: 800;
    color: #FFB74D;
}

.npc-desc {
    font-size: 0.78rem;
    color: var(--text-secondary);
    margin: 8px 0 14px 0;
    line-height: 1.4;
}

.npc-btn-group {
    display: flex;
    gap: 8px;
}

.npc-btn {
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 6px 12px;
    border-radius: var(--radius-sm);
    font-weight: 700;
    font-size: 0.78rem;
    cursor: pointer;
    transition: var(--transition-fast);
}

.npc-btn.primary {
    background: linear-gradient(135deg, #8B0000, #B71C1C);
    color: #FFFFFF;
}

.npc-btn.primary.green {
    background: #1E8E3E;
}

.npc-btn.secondary {
    background: var(--bg-surface-2);
    border: 1px solid var(--border-subtle);
    color: var(--text-secondary);
}

.npc-btn:hover {
    filter: brightness(1.15);
}
"""

with open('static/style.css', 'r', encoding='utf-8') as f:
    current_css = f.read()

# Replace or prepend the sidebar and dashboard CSS
updated_css = sidebar_and_dashboard_css + "\n\n" + current_css

with open('static/style.css', 'w', encoding='utf-8') as f:
    f.write(updated_css)

print("SUCCESS: Sidebar and Dashboard CSS prepended successfully!")
