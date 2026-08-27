tertiary_css = """
/* ==========================================================================
   WARISEVA AI — MODAL & COMPONENT UTILITY HELPERS
   ========================================================================== */

.btn-feed-accept {
    background: linear-gradient(135deg, #8B0000, #B71C1C);
    color: #FFFFFF;
    border: none;
    padding: 4px 10px;
    border-radius: var(--radius-sm);
    font-size: 0.75rem;
    font-weight: 800;
    cursor: pointer;
}

.center-col, .dossier-col {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.head-left {
    display: flex;
    align-items: center;
    gap: 10px;
}

.hec-body {
    padding-top: 10px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.info-group {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.info-label {
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--text-muted);
}

.mc-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 14px;
}

.mc-head-title {
    font-family: var(--font-display);
    font-size: 1.15rem;
    font-weight: 800;
    color: #FFFFFF;
}

.mc-close-btn {
    background: var(--bg-surface-2);
    border: 1px solid var(--border-subtle);
    color: var(--text-secondary);
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 0.85rem;
}

.mc-body {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.mc-action-btn {
    background: #FF6D00;
    color: #FFFFFF;
    border: none;
    padding: 8px 16px;
    border-radius: var(--radius-sm);
    font-weight: 800;
    font-size: 0.82rem;
    cursor: pointer;
}

.me-icon { font-size: 1.4rem; }
.me-title { font-weight: 800; font-size: 0.9rem; color: #FFFFFF; }
.me-sub { font-size: 0.76rem; color: var(--text-secondary); }
.mob-label { font-size: 0.7rem; font-weight: 700; }
.nav-arrow { font-size: 0.8rem; margin-left: auto; color: var(--text-muted); }
.nav-label { font-size: 0.85rem; }
.share-btn {
    background: var(--bg-surface-2);
    border: 1px solid var(--border-subtle);
    color: var(--text-primary);
    padding: 6px 12px;
    border-radius: var(--radius-sm);
    font-size: 0.78rem;
    font-weight: 700;
    cursor: pointer;
}

.pulse, .pulsing {
    animation: pulse 1.8s infinite;
}
"""

with open('static/style.css', 'a', encoding='utf-8') as f:
    f.write("\n\n" + tertiary_css)

print("SUCCESS: Tertiary component CSS appended successfully!")
