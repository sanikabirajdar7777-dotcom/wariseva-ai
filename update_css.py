new_css_additions = """
/* ==========================================================================
   WINNING PROTOTYPE UPGRADE STYLES
   ========================================================================== */

/* 1. Connectivity Status & Voice Button */
.conn-status-pill {
    padding: 2px 8px;
    border-radius: var(--radius-full);
    font-size: 0.72rem;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: rgba(0, 230, 118, 0.15);
    border: 1px solid rgba(0, 230, 118, 0.35);
    color: #00E676;
}

.conn-status-pill.weak {
    background: rgba(255, 183, 77, 0.15);
    border-color: rgba(255, 183, 77, 0.35);
    color: #FFB74D;
}

.conn-status-pill.offline {
    background: rgba(255, 82, 82, 0.15);
    border-color: rgba(255, 82, 82, 0.35);
    color: #FF5252;
}

.voice-btn {
    background: rgba(255, 255, 255, 0.12);
    border: 1px solid rgba(255, 255, 255, 0.25);
    color: #FFF;
    font-weight: 600;
}

.voice-btn:hover {
    background: rgba(255, 255, 255, 0.2);
}

/* 2. Elder-Friendly Mode Overlay */
.elder-mode-screen {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: #000000;
    z-index: 99999;
    padding: 20px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.elder-screen-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #161B22;
    padding: 16px 20px;
    border-radius: var(--radius-lg);
    border: 2px solid #FFD600;
    flex-wrap: wrap;
    gap: 12px;
}

.elder-banner-icon {
    font-size: 2.2rem;
    margin-right: 12px;
}

.elder-screen-title {
    font-size: 1.4rem;
    color: #FFD600;
    font-weight: 900;
}

.elder-screen-sub {
    font-size: 0.95rem;
    color: #FFFFFF;
}

.elder-header-actions {
    display: flex;
    align-items: center;
    gap: 8px;
}

.elder-lang-btn {
    background: #21262D;
    color: #FFF;
    border: 2px solid #484F58;
    padding: 8px 14px;
    border-radius: var(--radius-md);
    font-weight: 800;
    font-size: 1rem;
}

.elder-lang-btn:hover, .elder-lang-btn.active {
    border-color: #FFD600;
    background: #FFD600;
    color: #000;
}

.elder-exit-btn {
    background: #D32F2F;
    color: #FFF;
    padding: 10px 18px;
    border-radius: var(--radius-md);
    font-weight: 800;
    font-size: 1rem;
}

.elder-mega-buttons-grid {
    display: flex;
    flex-direction: column;
    gap: 14px;
    max-width: 800px;
    margin: 0 auto;
    width: 100%;
}

.elder-btn {
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 20px 24px;
    border-radius: var(--radius-xl);
    border: 3px solid transparent;
    text-align: left;
    transition: transform var(--transition-fast);
    min-height: 95px;
}

.elder-btn:active {
    transform: scale(0.98);
}

.elder-btn-icon {
    font-size: 3rem;
    flex-shrink: 0;
}

.elder-btn-text-col {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.elder-btn-title {
    font-size: 1.4rem;
    font-weight: 900;
    letter-spacing: -0.01em;
}

.elder-btn-desc {
    font-size: 1rem;
    font-weight: 600;
    opacity: 0.95;
}

.elder-sos-btn {
    background: linear-gradient(135deg, #D32F2F, #B71C1C);
    color: #FFFFFF;
    border-color: #FF8A80;
    box-shadow: 0 0 24px rgba(211, 47, 47, 0.6);
}

.elder-loc-btn {
    background: #0D47A1;
    color: #FFFFFF;
    border-color: #82B1FF;
}

.elder-med-btn {
    background: #00695C;
    color: #FFFFFF;
    border-color: #64FFDA;
}

.elder-water-btn {
    background: #0277BD;
    color: #FFFFFF;
    border-color: #80D8FF;
}

.elder-toilet-btn {
    background: #4527A0;
    color: #FFFFFF;
    border-color: #B388FF;
}

/* 3. Live Stopwatch Card */
.stopwatch-display-box {
    background: #000000;
    border: 2px solid #FF6D00;
    border-radius: var(--radius-md);
    padding: 6px 14px;
    display: flex;
    flex-direction: column;
    align-items: center;
    box-shadow: 0 0 12px rgba(255, 109, 0, 0.35);
}

.stopwatch-label {
    font-size: 0.68rem;
    font-weight: 800;
    color: #FF9800;
    letter-spacing: 0.05em;
}

.stopwatch-time {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.3rem;
    font-weight: 900;
    color: #00E676;
}

.em-hero-id-col {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 6px;
}

/* 4. Decision Support & Recommended Responder */
.decision-support-card {
    background: linear-gradient(135deg, rgba(255, 109, 0, 0.12), rgba(22, 27, 34, 0.95));
    border: 1px solid rgba(255, 109, 0, 0.4);
    border-radius: var(--radius-lg);
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.ds-card-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 8px;
}

.ds-star-badge {
    background: #FF6D00;
    color: #000;
    font-weight: 900;
    font-size: 0.72rem;
    padding: 3px 8px;
    border-radius: var(--radius-sm);
    display: inline-block;
    letter-spacing: 0.04em;
}

.ds-vol-title {
    font-size: 1.15rem;
    font-weight: 800;
    color: var(--text-primary);
    margin-top: 4px;
}

.ds-status-badge {
    background: rgba(0, 230, 118, 0.15);
    color: #00E676;
    border: 1px solid rgba(0, 230, 118, 0.4);
    padding: 3px 10px;
    border-radius: var(--radius-full);
    font-size: 0.75rem;
    font-weight: 800;
}

.ds-metrics-bar {
    display: flex;
    gap: 16px;
    background: var(--bg-surface-2);
    padding: 8px 12px;
    border-radius: var(--radius-md);
    font-size: 0.85rem;
    flex-wrap: wrap;
}

.ds-m-lbl {
    color: var(--text-muted);
}

.ds-reason-box {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    background: rgba(0, 0, 0, 0.25);
    border-left: 3px solid #FF6D00;
    padding: 8px 12px;
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    font-size: 0.88rem;
    line-height: 1.4;
}

.ds-disclaimer-text {
    font-size: 0.75rem;
    color: var(--text-muted);
}

/* 5. Nearest Help 4-Card Grid */
.nearest-help-section {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.nearest-help-title {
    font-size: 1rem;
    color: var(--text-secondary);
    font-weight: 700;
}

.nearest-help-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 10px;
}

.help-mini-card {
    background: var(--bg-surface-1);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.help-mini-head {
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
}

.help-mini-name {
    font-size: 0.92rem;
    color: var(--text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.help-mini-meta {
    font-size: 0.82rem;
    color: var(--text-secondary);
}

.help-mini-status {
    font-size: 0.72rem;
    font-weight: 800;
    margin-top: 2px;
}

/* 6. Companion Group Alert Strip */
.companion-alert-strip {
    background: rgba(2, 136, 209, 0.12);
    border: 1px solid rgba(2, 136, 209, 0.35);
    border-radius: var(--radius-md);
    padding: 10px 14px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 0.86rem;
}

.comp-icon {
    font-size: 1.4rem;
}

.comp-text strong {
    color: #4FC3F7;
}

/* 7. Command Center Tabs & Subviews */
.cmd-tabs-group {
    display: flex;
    align-items: center;
    gap: 6px;
}

.cmd-tab-btn {
    background: var(--bg-surface-2);
    border: 1px solid var(--border-subtle);
    color: var(--text-secondary);
    padding: 6px 14px;
    border-radius: var(--radius-full);
    font-size: 0.82rem;
    font-weight: 700;
    transition: all var(--transition-fast);
}

.cmd-tab-btn:hover, .cmd-tab-btn.active {
    background: #FF6D00;
    color: #000;
    border-color: #FF6D00;
}

.command-heatmap-subview, .command-readiness-subview {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.heatmap-header-card, .readiness-header-card {
    background: var(--bg-surface-1);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 10px;
}

.proto-tag {
    background: #6200EA;
    color: #FFF;
    padding: 3px 10px;
    border-radius: var(--radius-full);
    font-size: 0.72rem;
    font-weight: 800;
}

.heatmap-zones-grid, .readiness-camps-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 12px;
}

.zone-heatmap-card, .camp-readiness-card {
    background: var(--bg-surface-1);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 14px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.zone-heatmap-card.critical {
    border-color: rgba(211, 47, 47, 0.6);
    background: linear-gradient(135deg, rgba(211, 47, 47, 0.12), var(--bg-surface-1));
}

.zone-heatmap-card.high {
    border-color: rgba(245, 124, 0, 0.5);
    background: linear-gradient(135deg, rgba(245, 124, 0, 0.1), var(--bg-surface-1));
}

.card-top-tag {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.density-badge {
    padding: 2px 8px;
    border-radius: var(--radius-sm);
    font-size: 0.72rem;
    font-weight: 800;
}

.density-badge.critical { background: #D32F2F; color: #FFF; }
.density-badge.high { background: #F57C00; color: #FFF; }
.density-badge.moderate { background: #FBC02D; color: #000; }
.density-badge.low { background: #2E7D32; color: #FFF; }

.readiness-pill {
    padding: 2px 8px;
    border-radius: var(--radius-sm);
    font-size: 0.72rem;
    font-weight: 800;
}

.readiness-pill.ready { background: rgba(0, 230, 118, 0.2); color: #00E676; border: 1px solid #00E676; }
.readiness-pill.moderate { background: rgba(255, 183, 77, 0.2); color: #FFB74D; border: 1px solid #FFB74D; }
.readiness-pill.high { background: rgba(255, 82, 82, 0.2); color: #FF5252; border: 1px solid #FF5252; }

/* 8. Analytics & WariSeva Score Modal */
.analytics-card {
    max-width: 500px;
}

.analytics-metrics-deck {
    display: flex;
    flex-direction: column;
    gap: 8px;
    background: var(--bg-surface-2);
    border-radius: var(--radius-md);
    padding: 14px;
}

.analytics-stat-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 0.9rem;
}

.score-display-card {
    background: linear-gradient(135deg, #1A237E, #0D1117);
    border: 2px solid #FFD600;
    border-radius: var(--radius-lg);
    padding: 16px;
    text-align: center;
    margin-top: 12px;
    box-shadow: 0 0 20px rgba(255, 214, 0, 0.25);
}

.score-kicker {
    font-size: 0.75rem;
    font-weight: 800;
    color: #FFD600;
    letter-spacing: 0.08em;
}

.score-number-row {
    display: flex;
    align-items: baseline;
    justify-content: center;
    gap: 4px;
    margin: 8px 0;
}

.score-big {
    font-size: 3.2rem;
    font-weight: 900;
    color: #00E676;
    font-family: 'Outfit', sans-serif;
    line-height: 1;
}

.score-denom {
    font-size: 1.2rem;
    color: var(--text-muted);
}

.score-rating-badge {
    display: inline-block;
    background: rgba(0, 230, 118, 0.2);
    border: 1px solid #00E676;
    color: #00E676;
    padding: 4px 14px;
    border-radius: var(--radius-full);
    font-weight: 800;
    font-size: 0.8rem;
    letter-spacing: 0.04em;
}

.score-disclaimer {
    font-size: 0.72rem;
    color: var(--text-muted);
    margin-top: 8px;
}

/* 9. Where Am I Modal */
.where-data-box {
    background: var(--bg-surface-2);
    border-radius: var(--radius-md);
    padding: 14px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-top: 10px;
}

.where-row {
    display: flex;
    justify-content: space-between;
    font-size: 0.88rem;
}

.w-lbl {
    color: var(--text-muted);
}

.group-members-list {
    display: flex;
    flex-direction: column;
    gap: 6px;
    margin: 10px 0;
}

.group-member-item {
    background: var(--bg-surface-2);
    padding: 8px 12px;
    border-radius: var(--radius-sm);
    display: flex;
    justify-content: space-between;
    font-size: 0.86rem;
}

.group-add-form {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-top: 10px;
}
"""

with open('static/style.css', 'r', encoding='utf-8') as f:
    existing_css = f.read()

if 'WINNING PROTOTYPE UPGRADE STYLES' not in existing_css:
    with open('static/style.css', 'a', encoding='utf-8') as f:
        f.write("\n" + new_css_additions)
    print("Successfully appended winning prototype styles to static/style.css!")
else:
    print("Styles already present in static/style.css")
