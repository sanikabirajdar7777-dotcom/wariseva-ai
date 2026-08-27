with open('static/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

extra_css = """
/* =========================================================================
   SOS RESPONSE FLOW & SYNCHRONIZED EMERGENCY UPGRADE STYLES
   ========================================================================= */

.response-status-header-banner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: linear-gradient(135deg, rgba(255, 109, 0, 0.18), rgba(211, 47, 47, 0.18));
    border: 1px solid rgba(255, 109, 0, 0.35);
    border-radius: var(--radius-lg);
    padding: var(--space-4) var(--space-5);
    margin-bottom: var(--space-4);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.rsh-top {
    display: flex;
    align-items: center;
    gap: var(--space-3);
}

.rsh-pulse-badge {
    font-size: 1.8rem;
    animation: pulse 1.5s infinite ease-in-out;
}

.rsh-kicker {
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 1px;
    color: var(--accent-orange);
    text-transform: uppercase;
    display: block;
}

.rsh-title {
    font-size: 1.25rem;
    font-weight: 800;
    color: var(--text-primary);
    margin: 0;
}

.rsh-id-tag {
    background: rgba(0, 0, 0, 0.4);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: var(--space-2) var(--space-3);
    font-size: 0.82rem;
    color: var(--text-secondary);
}

.rsh-id-tag strong {
    color: var(--accent-cyan);
    font-family: 'JetBrains Mono', monospace;
    margin-left: 4px;
}

/* RESPONSE IN PROGRESS CARD */
.response-in-progress-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: var(--space-5);
    margin-bottom: var(--space-4);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
}

.rip-card-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--space-4);
    border-bottom: 1px solid var(--border-color);
    padding-bottom: var(--space-3);
}

.rip-head-left {
    display: flex;
    align-items: center;
    gap: var(--space-3);
}

.rip-icon {
    font-size: 1.5rem;
}

.rip-title {
    font-size: 1.05rem;
    font-weight: 800;
    color: var(--accent-orange);
    margin: 0;
    letter-spacing: 0.5px;
}

.rip-sub {
    font-size: 0.78rem;
    color: var(--text-muted);
}

.rip-status-pill {
    padding: var(--space-1) var(--space-3);
    border-radius: var(--radius-full);
    font-size: 0.78rem;
    font-weight: 800;
    background: rgba(255, 179, 0, 0.15);
    color: var(--accent-orange);
    border: 1px solid var(--accent-orange);
}

.rip-volunteer-profile {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    margin-bottom: var(--space-4);
}

.rip-avatar {
    font-size: 2rem;
    background: rgba(2, 136, 209, 0.15);
    border-radius: var(--radius-full);
    padding: var(--space-2);
    border: 1px solid rgba(2, 136, 209, 0.3);
}

.rip-vol-name {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0;
}

.rip-vol-id {
    font-size: 0.8rem;
    color: var(--accent-cyan);
    font-family: 'JetBrains Mono', monospace;
    display: block;
}

.rip-sector {
    font-size: 0.8rem;
    color: var(--text-muted);
    margin: 2px 0 0 0;
}

.rip-metrics-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--space-3);
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: var(--space-3);
    margin-bottom: var(--space-3);
}

.rip-metric-box {
    display: flex;
    flex-direction: column;
}

.rip-m-lbl {
    font-size: 0.72rem;
    color: var(--text-muted);
    text-transform: uppercase;
    font-weight: 700;
}

.rip-m-val {
    font-size: 1rem;
    font-weight: 800;
    margin-top: 2px;
}

.rip-sim-notice {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.72rem;
    color: var(--text-muted);
    background: rgba(0, 0, 0, 0.2);
    padding: var(--space-2) var(--space-3);
    border-radius: var(--radius-sm);
}

.rip-sim-notice .sim-badge {
    background: rgba(156, 39, 176, 0.15);
    color: #ce93d8;
    border: 1px solid rgba(156, 39, 176, 0.3);
    border-radius: 4px;
    padding: 2px 6px;
    font-weight: 700;
}

/* SIMULATION TRIGGER BAR */
.simulation-quick-bar {
    margin-bottom: var(--space-4);
}

.sim-trigger-btn {
    width: 100%;
    background: linear-gradient(135deg, #FF6D00, #E65100);
    color: #FFFFFF;
    font-size: 0.92rem;
    font-weight: 800;
    padding: var(--space-3);
    border-radius: var(--radius-md);
    border: none;
    cursor: pointer;
    box-shadow: 0 4px 14px rgba(255, 109, 0, 0.35);
    transition: all var(--transition-fast);
}

.sim-trigger-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(255, 109, 0, 0.5);
}

/* HOSPITAL ESCALATION CARD */
.hospital-escalation-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: var(--space-4);
    margin-top: var(--space-4);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
}

.hec-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--space-3);
    border-bottom: 1px solid var(--border-color);
    padding-bottom: var(--space-2);
}

.hec-head-left {
    display: flex;
    align-items: center;
    gap: var(--space-2);
}

.hec-icon {
    font-size: 1.4rem;
}

.hec-title {
    font-size: 0.95rem;
    font-weight: 800;
    color: var(--accent-cyan);
    margin: 0;
    letter-spacing: 0.5px;
}

.hec-sub {
    font-size: 0.75rem;
    color: var(--text-muted);
}

.hec-status-pill {
    font-size: 0.75rem;
    font-weight: 700;
    background: rgba(0, 230, 118, 0.15);
    color: var(--success);
    border: 1px solid var(--success);
    border-radius: var(--radius-full);
    padding: 2px 8px;
}

.hec-hosp-name {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 var(--space-2) 0;
}

.hec-metrics {
    display: flex;
    gap: var(--space-4);
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-bottom: var(--space-3);
}

.hec-view-btn {
    width: 100%;
    background: rgba(0, 188, 212, 0.15);
    border: 1px solid var(--accent-cyan);
    color: var(--accent-cyan);
    font-weight: 700;
    padding: var(--space-2) var(--space-3);
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all var(--transition-fast);
}

.hec-view-btn:hover {
    background: var(--accent-cyan);
    color: #000;
}

/* NEAREST SERVICES SUMMARY STRIP ON SERVICES PAGE */
.nearest-services-summary-strip {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: var(--space-4);
    margin-bottom: var(--space-5);
}

.nss-title {
    font-size: 0.85rem;
    font-weight: 800;
    color: var(--accent-orange);
    margin: 0 0 var(--space-3) 0;
    letter-spacing: 0.5px;
}

.nss-chips-grid {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-2);
}

.nss-chip {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: var(--space-2) var(--space-3);
    font-size: 0.82rem;
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    gap: 4px;
}

.nss-chip strong {
    color: var(--accent-cyan);
    font-weight: 800;
}

.nss-glyph {
    font-size: 1rem;
}
"""

if '.response-status-header-banner' not in css:
    css = css + extra_css
    with open('static/style.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("Appended new response flow CSS styles to static/style.css!")
else:
    print("Response flow CSS styles already present.")
