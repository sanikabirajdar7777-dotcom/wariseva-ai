secondary_css = """
/* ==========================================================================
   WARISEVA AI — SECONDARY COMPONENTS, TRIAGE, AUDIT TRAIL & INSPECTOR CSS
   ========================================================================== */

/* 1. Emergency Nearest Relationship Banner */
.emergency-nearest-relationship-banner {
    margin: 16px 0;
    padding: 16px;
    background: var(--bg-surface-1);
    border: 1px solid rgba(0, 229, 255, 0.35);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-sm);
}

.rel-nodes-row {
    display: flex;
    align-items: center;
    justify-content: space-around;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 10px;
}

.rel-node-card {
    background: var(--bg-surface-2);
    border: 1px solid var(--border-subtle);
    padding: 12px 16px;
    border-radius: var(--radius-md);
    text-align: center;
    min-width: 140px;
    flex: 1;
}

.rel-node-card.patient {
    background: rgba(211, 47, 47, 0.14);
    border-color: #FF5252;
}

.rel-node-card.volunteer {
    background: rgba(2, 136, 209, 0.14);
    border-color: #00E5FF;
}

.rel-node-card.hospital {
    background: rgba(245, 124, 0, 0.14);
    border-color: #FF851A;
}

.rel-connector {
    display: flex;
    flex-direction: column;
    align-items: center;
    color: var(--accent-cyan);
    font-weight: 800;
    font-size: 0.82rem;
}

/* 2. Transparent AI Recommendation Duo Cards */
.ai-recommendations-duo-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 16px;
    margin: 16px 0;
}

.ai-rec-box {
    background: var(--bg-surface-1);
    border: 1px solid rgba(0, 229, 255, 0.4);
    border-radius: var(--radius-lg);
    padding: 16px;
    box-shadow: var(--shadow-sm);
}

.ai-factor-bars {
    font-size: 0.78rem;
    color: var(--text-secondary);
    margin: 10px 0;
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.ai-why-reasons {
    background: rgba(0, 0, 0, 0.4);
    padding: 10px 12px;
    border-radius: var(--radius-sm);
    font-size: 0.8rem;
    color: var(--text-secondary);
    display: flex;
    flex-direction: column;
    gap: 4px;
}

/* 3. Response Clock & Emergency Audit Trail */
.response-clock-and-audit-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 16px;
    margin: 16px 0;
}

.resp-clock-card, .audit-trail-card {
    background: var(--bg-surface-1);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 16px;
    box-shadow: var(--shadow-sm);
}

.clock-milestones {
    font-size: 0.82rem;
    color: var(--text-secondary);
    display: flex;
    flex-direction: column;
    gap: 6px;
    margin-top: 10px;
}

.audit-trail-events {
    max-height: 180px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 6px;
    font-size: 0.78rem;
    font-family: var(--font-mono);
    margin-top: 10px;
}

/* 4. Triage & Severity Selection Controls */
.triage-selection-box {
    background: var(--bg-surface-1);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 16px;
    margin: 14px 0;
}

.triage-lbl-heading {
    font-size: 0.82rem;
    font-weight: 800;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
    display: block;
}

.triage-pills-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 12px;
}

.triage-pill {
    background: var(--bg-surface-2);
    border: 1px solid var(--border-subtle);
    color: var(--text-secondary);
    padding: 6px 14px;
    border-radius: var(--radius-full);
    font-size: 0.8rem;
    font-weight: 700;
    cursor: pointer;
    transition: var(--transition-fast);
}

.triage-pill:hover, .triage-pill.active {
    background: var(--brand-primary);
    color: #FFFFFF;
    border-color: #FFA000;
}

.triage-sev-row {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}

.triage-sev-btn {
    flex: 1;
    padding: 8px 12px;
    border-radius: var(--radius-sm);
    font-size: 0.78rem;
    font-weight: 800;
    cursor: pointer;
    background: var(--bg-surface-2);
    border: 1px solid var(--border-subtle);
    color: var(--text-secondary);
    transition: var(--transition-fast);
    text-align: center;
}

.triage-sev-btn.active {
    background: var(--emergency-red);
    color: #FFF;
    border-color: #FF5252;
}

/* 5. Wari Zone Safety Overview Grid */
.wari-zone-safety-overview {
    margin: 18px 0;
}

.wzso-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
}

.wzso-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 12px;
}

.wz-card {
    background: var(--bg-surface-1);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.wz-card.high-risk { border-left: 4px solid #FF5252; }
.wz-card.elevated-risk { border-left: 4px solid #FFB74D; }
.wz-card.mod-risk { border-left: 4px solid #FFD600; }
.wz-card.low-risk { border-left: 4px solid #00E676; }

/* 6. Command Center Inspector & Detail Grid */
.inspector-details-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 10px;
    margin: 12px 0;
}

.idg-row {
    display: flex;
    flex-direction: column;
    font-size: 0.78rem;
}

.ins-resolve-box {
    margin-top: 14px;
    padding-top: 12px;
    border-top: 1px solid var(--border-subtle);
}

.cmd-ai-body {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding-top: 10px;
}

.dive-banner-left, .dive-banner-right {
    display: flex;
    align-items: center;
    gap: 8px;
}

.efi-name { font-weight: 700; color: #FFF; font-size: 0.82rem; }
.efi-pts { font-weight: 800; color: #00E676; font-size: 0.82rem; }

/* 7. QR Scanner & Manual Lookup Controls */
.manual-entry-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
}

.manual-input-row {
    display: flex;
    gap: 8px;
    margin-top: 8px;
}

.manual-id-input {
    flex: 1;
    background: var(--bg-surface-2);
    border: 1px solid var(--border-subtle);
    color: #FFF;
    padding: 8px 12px;
    border-radius: var(--radius-sm);
    font-family: var(--font-mono);
    font-size: 0.88rem;
    outline: none;
}

.manual-lookup-btn {
    background: #FF6D00;
    color: #FFF;
    border: none;
    padding: 8px 16px;
    border-radius: var(--radius-sm);
    font-weight: 800;
    font-size: 0.82rem;
    cursor: pointer;
}

.scan-result-box {
    background: var(--bg-surface-1);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 18px;
    margin-top: 16px;
}

.scanner-btn-pill {
    background: var(--bg-surface-2);
    border: 1px solid var(--border-subtle);
    color: var(--text-primary);
    padding: 6px 14px;
    border-radius: var(--radius-full);
    font-size: 0.8rem;
    font-weight: 700;
    cursor: pointer;
}

.scan-bottom-reset {
    margin-top: 14px;
    text-align: center;
}

/* 8. PIN & Auth Field Groups */
.pin-entry-form {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-top: 12px;
}

.auth-field-group {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.auth-input-pill {
    background: var(--bg-surface-2);
    border: 1px solid var(--border-subtle);
    color: #FFF;
    padding: 8px 14px;
    border-radius: var(--radius-md);
    font-size: 0.85rem;
    outline: none;
}

.authorized-profile-box {
    background: rgba(0, 230, 118, 0.08);
    border: 1px solid rgba(0, 230, 118, 0.35);
    border-radius: var(--radius-md);
    padding: 14px;
    margin-top: 12px;
}

/* 9. Utility Classes & Badges */
.verified-badge {
    background: rgba(0, 230, 118, 0.15);
    color: #00E676;
    border: 1px solid rgba(0, 230, 118, 0.4);
    font-size: 0.65rem;
    font-weight: 800;
    padding: 1px 6px;
    border-radius: var(--radius-sm);
}

.top-action-badge {
    font-weight: 800;
    font-size: 0.72rem;
    padding: 3px 8px;
    border-radius: var(--radius-full);
}

.highlight-red { color: #FF5252 !important; }
.text-danger { color: #FF5252 !important; }
.text-success { color: #00E676 !important; }
.voice-icon { font-size: 1.1rem; }
.sim-desc { font-size: 0.72rem; color: var(--text-muted); }
.rip-body { padding-top: 12px; }
.rsh-right-col { display: flex; align-items: center; gap: 12px; }
.ds-head-left { display: flex; flex-direction: column; gap: 2px; }
.timeline-col { display: flex; flex-direction: column; gap: 8px; }
.timeline-header-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.stage-info { display: flex; flex-direction: column; }
.coordination-complete-card {
    background: rgba(0, 230, 118, 0.1);
    border: 1px solid #00E676;
    border-radius: var(--radius-md);
    padding: 14px;
    text-align: center;
    margin-top: 12px;
}
.empty-feed-text { font-size: 0.8rem; color: var(--text-muted); padding: 12px; text-align: center; }
.error-banner { background: rgba(255, 82, 82, 0.15); border: 1px solid #FF5252; color: #FF5252; padding: 10px; border-radius: var(--radius-sm); font-size: 0.8rem; margin: 8px 0; }
.modal-label { font-size: 0.78rem; font-weight: 700; color: var(--text-muted); }
.front-side { display: flex; width: 100%; }
.wb-nav-back, .qr-nav-back, .qr-nav-home {
    background: var(--bg-surface-2);
    border: 1px solid var(--border-subtle);
    color: var(--text-primary);
    padding: 6px 12px;
    border-radius: var(--radius-sm);
    font-size: 0.8rem;
    font-weight: 700;
    cursor: pointer;
}
"""

with open('static/style.css', 'a', encoding='utf-8') as f:
    f.write("\n\n" + secondary_css)

print("SUCCESS: Secondary component CSS appended successfully!")
