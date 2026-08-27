new_css_rules = """
/* ==========================================================================
   INTELLIGENT RESPONSE & EXPLAINABLE AI DESIGN COMPONENTS
   ========================================================================== */

.decision-support-card {
    background: linear-gradient(135deg, rgba(22, 27, 34, 0.95), rgba(13, 17, 23, 0.98));
    border: 1px solid rgba(0, 230, 118, 0.35);
    border-radius: var(--radius-lg);
    padding: var(--space-4);
    margin-bottom: var(--space-4);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}

.ds-card-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border-subtle);
    padding-bottom: var(--space-3);
    margin-bottom: var(--space-3);
}

.ds-star-badge {
    display: inline-block;
    background: rgba(0, 230, 118, 0.15);
    color: #00E676;
    font-size: 0.78rem;
    font-weight: 800;
    padding: 3px 8px;
    border-radius: var(--radius-full);
    border: 1px solid rgba(0, 230, 118, 0.3);
    margin-bottom: 4px;
}

.ds-vol-title {
    font-size: 1.15rem;
    font-weight: 800;
    color: var(--text-primary);
    margin: 0;
}

.ds-score-badge {
    background: rgba(0, 230, 118, 0.2);
    border: 1px solid #00E676;
    padding: 6px 14px;
    border-radius: var(--radius-md);
    text-align: center;
}

.ds-score-badge .score-num {
    font-family: 'Outfit', sans-serif;
    font-size: 1.5rem;
    font-weight: 900;
    color: #00E676;
}

.ds-score-badge .score-denom {
    font-size: 0.85rem;
    color: var(--text-muted);
}

.ds-checklist-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 8px;
    margin-bottom: var(--space-3);
}

.ds-check-item {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    padding: 8px 12px;
    border-radius: var(--radius-sm);
    font-size: 0.85rem;
    color: var(--text-secondary);
}

.ds-backup-row {
    background: rgba(255, 109, 0, 0.08);
    border-left: 3px solid #FF6D00;
    padding: 8px 12px;
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    font-size: 0.82rem;
    margin-bottom: 8px;
}

.ds-backup-row .backup-label {
    color: #FFB74D;
    font-weight: 700;
    margin-right: 6px;
}

.ds-backup-row .backup-val {
    color: var(--text-secondary);
}

.ds-disclaimer-text {
    font-size: 0.75rem;
    color: var(--text-muted);
}

/* Command Center Resources Metric Strip */
.command-resources-metric-strip {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 12px;
    margin-bottom: var(--space-4);
}

.cmd-metric-card {
    background: var(--bg-surface-1);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 12px 16px;
    display: flex;
    flex-direction: column;
    box-shadow: var(--shadow-sm);
}

.cmd-metric-card .cm-val {
    font-family: 'Outfit', sans-serif;
    font-size: 1.8rem;
    font-weight: 900;
    line-height: 1.1;
}

.cmd-metric-card .cm-lbl {
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.05em;
    color: var(--text-secondary);
    margin-top: 4px;
}

.cmd-metric-card .cm-sub {
    font-size: 0.65rem;
    color: var(--text-muted);
    font-weight: 600;
}

/* Command AI Recommendation Card */
.command-ai-panel-card {
    background: linear-gradient(135deg, rgba(22, 27, 34, 0.95), rgba(13, 17, 23, 0.98));
    border: 1px solid rgba(0, 230, 118, 0.3);
    border-radius: var(--radius-md);
    padding: 12px 16px;
    margin-top: 12px;
}

.cmd-ai-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.cmd-ai-head-left {
    display: flex;
    align-items: center;
    gap: 8px;
}

.cmd-ai-icon {
    font-size: 1.4rem;
}

.cmd-ai-title {
    font-size: 0.88rem;
    font-weight: 800;
    color: var(--text-primary);
    margin: 0;
}

.cmd-ai-sub {
    font-size: 0.72rem;
    color: var(--text-muted);
}

.cmd-ai-badge {
    background: rgba(0, 230, 118, 0.15);
    color: #00E676;
    border: 1px solid #00E676;
    font-size: 0.75rem;
    font-weight: 800;
    padding: 3px 8px;
    border-radius: var(--radius-sm);
}

.cmd-ai-rec-row {
    font-size: 0.85rem;
    color: var(--text-primary);
    margin-bottom: 8px;
}

.cmd-ai-reasons-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-bottom: 8px;
}

.ai-chip {
    background: rgba(0, 230, 118, 0.08);
    border: 1px solid rgba(0, 230, 118, 0.25);
    color: #00E676;
    font-size: 0.75rem;
    padding: 2px 8px;
    border-radius: var(--radius-full);
}

.cmd-ai-backup-row {
    font-size: 0.78rem;
    color: var(--text-muted);
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    padding-top: 6px;
}

.cmd-ai-backup-row .backup-lbl {
    color: #FFB74D;
    font-weight: 700;
}

.cmd-ai-backup-row .backup-txt {
    color: var(--text-secondary);
}

/* Nearest To Me Summary Strip */
.nearest-services-summary-strip {
    background: var(--bg-surface-1);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 12px 16px;
    margin-bottom: var(--space-4);
}

.nss-title {
    font-size: 0.82rem;
    font-weight: 800;
    color: var(--brand-primary);
    letter-spacing: 0.05em;
    margin: 0 0 8px 0;
}

.nss-chips-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.nss-chip {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-sm);
    padding: 6px 12px;
    font-size: 0.82rem;
    color: var(--text-secondary);
}

.nss-chip strong {
    color: var(--text-primary);
}

/* Custom Buttons & Verified Badges */
.verified-pill {
    background: rgba(0, 230, 118, 0.15);
    color: #00E676;
    border: 1px solid rgba(0, 230, 118, 0.3);
    font-size: 0.68rem;
    font-weight: 800;
    padding: 2px 6px;
    border-radius: var(--radius-full);
    margin-left: 6px;
}

.cmd-assisted-btn {
    background: linear-gradient(135deg, #FF6D00, #E65100);
    color: #FFFFFF;
    border: none;
    font-weight: 800;
    font-size: 0.78rem;
    padding: 6px 12px;
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: transform 0.15s ease;
}

.cmd-assisted-btn:hover {
    transform: translateY(-1px);
    box-shadow: var(--glow-orange);
}

.reg-vol-btn {
    background: rgba(2, 136, 209, 0.2);
    border: 1px solid #0288D1;
    color: #4FC3F7;
    font-weight: 700;
    font-size: 0.78rem;
    padding: 6px 12px;
    border-radius: var(--radius-sm);
    cursor: pointer;
}

.reg-vol-btn:hover {
    background: rgba(2, 136, 209, 0.35);
}

.avail-toggle-btn {
    background: rgba(0, 230, 118, 0.15);
    border: 1px solid #00E676;
    color: #00E676;
    font-weight: 700;
    font-size: 0.78rem;
    padding: 6px 12px;
    border-radius: var(--radius-sm);
    cursor: pointer;
}

.avail-toggle-btn.offline {
    background: rgba(139, 148, 158, 0.15);
    border-color: #8B949E;
    color: #8B949E;
}

.ai-rec-banner-small {
    background: rgba(0, 230, 118, 0.1);
    border: 1px solid rgba(0, 230, 118, 0.3);
    color: var(--text-primary);
    padding: 8px 12px;
    border-radius: var(--radius-sm);
    font-size: 0.82rem;
    margin: 8px 0;
}
"""

with open('static/style.css', 'a', encoding='utf-8') as f:
    f.write(new_css_rules)

print("Appended new AI styling rules to static/style.css!")
