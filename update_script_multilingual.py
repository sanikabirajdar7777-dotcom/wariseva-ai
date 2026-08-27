import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Replace applyLanguage and setTimelineStep with the enhanced version
enhanced_lang_js = '''    function speakStep(stage) {
        if (!window.WariState.voiceEnabled) return;
        const lang = window.WariState.lang || 'en';
        const dict = i18n[lang] || i18n.en;
        const text = (dict.timeline_narrations && dict.timeline_narrations[stage]) || (i18n.en.timeline_narrations && i18n.en.timeline_narrations[stage]);
        if (text) {
            speakText(text);
        }
    }

    // Multilingual Translation Engine
    function applyLanguage(lang) {
        const selectedLang = (lang === 'mr' || lang === 'hi') ? lang : 'en';
        window.WariState.lang = selectedLang;
        try { localStorage.setItem('wariseva_lang', selectedLang); } catch (e) {}

        const dict = i18n[selectedLang] || i18n.en;

        // 1. Data-i18n Attribute Translations
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (dict[key]) {
                if (el.tagName === 'INPUT' && (el.type === 'button' || el.type === 'submit')) {
                    el.value = dict[key];
                } else {
                    el.textContent = dict[key];
                }
            }
        });

        // 2. Main SOS Button Translations
        const sosMainBtn = document.getElementById('home-sos-btn') || document.getElementById('sos-button-main');
        if (sosMainBtn) {
            const titleEl = sosMainBtn.querySelector('.sos-btn-text') || sosMainBtn.querySelector('.sos-text-main');
            const subEl = sosMainBtn.querySelector('.sos-btn-sub') || sosMainBtn.querySelector('.sos-text-sub');
            if (titleEl) titleEl.textContent = dict.sos_btn_text.replace('🚨 ', '');
            if (subEl) subEl.textContent = dict.sos_btn_sub;
        }

        // 3. Emergency Timeline Steps (Titles & Descriptions)
        const stepMap = {
            1: 'step-1-sos',
            2: 'step-2-loc',
            3: 'step-3-zone',
            4: 'step-4-severity',
            5: 'step-5-ai-match',
            6: 'step-6-vol-alert',
            7: 'step-7-vol-accept',
            8: 'step-8-vol-enroute',
            9: 'step-9-vol-reached',
            10: 'step-10-resp-dispatched',
            11: 'step-11-hosp-recommended',
            12: 'step-12-coordinated'
        };

        for (let i = 1; i <= 12; i++) {
            const stepEl = document.getElementById(stepMap[i]);
            if (stepEl && dict.timeline_steps && dict.timeline_steps[i]) {
                const titleNode = stepEl.querySelector('.step-title');
                const descNode = stepEl.querySelector('.step-desc');
                if (titleNode) titleNode.textContent = dict.timeline_steps[i].title;
                if (descNode) descNode.textContent = dict.timeline_steps[i].desc;
            }
        }

        // 4. Update Volunteer Dashboard Controls
        const volAcceptBtn = document.getElementById('vol-accept-case-btn');
        if (volAcceptBtn) volAcceptBtn.textContent = dict.vol_accept_btn;

        const volEnrouteBtn = document.getElementById('vol-start-response-btn');
        if (volEnrouteBtn) volEnrouteBtn.textContent = dict.vol_enroute_btn;

        const volArrivedBtn = document.getElementById('vol-mark-arrived-btn');
        if (volArrivedBtn) volArrivedBtn.textContent = dict.vol_arrived_btn;

        const volScanBtn = document.getElementById('vol-scan-wristband-btn');
        if (volScanBtn) volScanBtn.textContent = dict.vol_scan_wb_btn;

        const volEscalateBtn = document.getElementById('vol-escalate-btn');
        if (volEscalateBtn) volEscalateBtn.textContent = dict.vol_escalate_btn;

        const volSpaLoginBtn = document.getElementById('vol-spa-login-btn');
        if (volSpaLoginBtn) volSpaLoginBtn.textContent = dict.vol_login_btn;

        const volSpaLogoutBtn = document.getElementById('vol-spa-logout-btn');
        if (volSpaLogoutBtn) volSpaLogoutBtn.textContent = dict.vol_logout_btn;

        const volOpenScannerBtn = document.getElementById('vol-open-scanner-btn');
        if (volOpenScannerBtn) volOpenScannerBtn.textContent = dict.vol_open_scanner;

        const volQuickFillBtn = document.getElementById('vol-quick-fill-btn');
        if (volQuickFillBtn) volQuickFillBtn.textContent = dict.vol_quick_fill;

        // 5. Update Hospital Dashboard Controls
        const hospAcceptBtn = document.getElementById('hosp-accept-case-btn');
        if (hospAcceptBtn) hospAcceptBtn.textContent = dict.hosp_accept_btn;

        const hospPatientArrivedBtn = document.getElementById('hosp-patient-arrived-btn');
        if (hospPatientArrivedBtn) hospPatientArrivedBtn.textContent = dict.hosp_arrived_btn;

        const hospTreatmentBtn = document.getElementById('hosp-treatment-started-btn');
        if (hospTreatmentBtn) hospTreatmentBtn.textContent = dict.hosp_treatment_btn;

        const hospTransferBtn = document.getElementById('hosp-transfer-btn');
        if (hospTransferBtn) hospTransferBtn.textContent = dict.hosp_transfer_btn;

        const hospResolveBtn = document.getElementById('hosp-mark-admitted-btn');
        if (hospResolveBtn) hospResolveBtn.textContent = dict.hosp_resolve_btn;

        const hospSpaLoginBtn = document.getElementById('hosp-spa-login-btn');
        if (hospSpaLoginBtn) hospSpaLoginBtn.textContent = dict.hosp_login_btn;

        const hospSpaLogoutBtn = document.getElementById('hosp-spa-logout-btn');
        if (hospSpaLogoutBtn) hospSpaLogoutBtn.textContent = dict.hosp_logout_btn;

        const hospQuickFillBtn = document.getElementById('hosp-quick-fill-btn');
        if (hospQuickFillBtn) hospQuickFillBtn.textContent = dict.hosp_quick_fill;

        const hospBedStatus = document.getElementById('hosp-bed-status');
        if (hospBedStatus) {
            const isReserved = hospBedStatus.textContent.includes('RESERVED') || hospBedStatus.textContent.includes('राखीव') || hospBedStatus.textContent.includes('आरक्षित');
            hospBedStatus.textContent = isReserved ? dict.hosp_bed_reserved : dict.hosp_bed_avail;
        }

        const hospStatusChip = document.getElementById('responder-status-chip');
        if (hospStatusChip) hospStatusChip.textContent = dict.hosp_accepting_chip;

        // 6. Update AI Recommendation Card
        const aiRecTitle = document.getElementById('ai-rec-title');
        if (aiRecTitle) aiRecTitle.textContent = dict.ai_rec_title;
        const aiWhyHeading = document.getElementById('ai-why-heading');
        if (aiWhyHeading) aiWhyHeading.textContent = dict.ai_why_heading;
        const aiR1 = document.getElementById('ai-reason-1');
        if (aiR1) aiR1.textContent = dict.ai_reason_1;
        const aiR2 = document.getElementById('ai-reason-2');
        if (aiR2) aiR2.textContent = dict.ai_reason_2;
        const aiR3 = document.getElementById('ai-reason-3');
        if (aiR3) aiR3.textContent = dict.ai_reason_3;
        const aiR4 = document.getElementById('ai-reason-4');
        if (aiR4) aiR4.textContent = dict.ai_reason_4;
        const aiKicker = document.getElementById('ai-kicker');
        if (aiKicker) aiKicker.textContent = dict.ai_kicker;

        // 7. Update Command Center Tabs
        const cmdOpsTab = document.getElementById('cmd-tab-operations');
        if (cmdOpsTab) cmdOpsTab.textContent = dict.cmd_tab_ops;
        const cmdVolsTab = document.getElementById('cmd-tab-volunteers');
        if (cmdVolsTab) cmdVolsTab.innerHTML = `${dict.cmd_tab_vols} (<span id="tab-pending-vols-count">17</span>)`;
        const cmdHospsTab = document.getElementById('cmd-tab-hospitals');
        if (cmdHospsTab) cmdHospsTab.innerHTML = `${dict.cmd_tab_hosps} (<span id="tab-pending-hosps-count">4</span>)`;
        const cmdDiveTab = document.getElementById('cmd-tab-incident-dive');
        if (cmdDiveTab) cmdDiveTab.textContent = dict.cmd_tab_dive;

        // 8. Sync Dropdown Value
        const langDropdown = document.getElementById('lang-select');
        if (langDropdown && langDropdown.value !== selectedLang) {
            langDropdown.value = selectedLang;
        }

        // 9. Re-apply current timeline step tags in selected language
        if (window.WariState.currentEmergencyStage !== undefined && window.WariState.currentEmergencyStage !== null) {
            setTimelineStep(window.WariState.currentEmergencyStage, true, window.WariState.currentEmergencyStage === 12);
        }
    }

    // Set Timeline Step with Localized Status Tags & Sequential Progression
    function setTimelineStep(stepNumber, active = true, completed = false) {
        window.WariState.currentEmergencyStage = stepNumber;
        const lang = window.WariState.lang || 'en';
        const dict = i18n[lang] || i18n.en;

        const stepMap = {
            1: 'step-1-sos',
            2: 'step-2-loc',
            3: 'step-3-zone',
            4: 'step-4-severity',
            5: 'step-5-ai-match',
            6: 'step-6-vol-alert',
            7: 'step-7-vol-accept',
            8: 'step-8-vol-enroute',
            9: 'step-9-vol-reached',
            10: 'step-10-resp-dispatched',
            11: 'step-11-hosp-recommended',
            12: 'step-12-coordinated'
        };

        for (let i = 1; i <= 12; i++) {
            const el = document.getElementById(stepMap[i]);
            if (!el) continue;
            const marker = el.querySelector('.step-marker');
            let statusTag = el.querySelector('.step-status-tag');
            if (!statusTag) {
                statusTag = document.createElement('span');
                statusTag.className = 'step-status-tag';
                el.appendChild(statusTag);
            }

            if (stepNumber === 0) {
                el.className = 'timeline-step step-pending';
                if (marker) marker.textContent = i;
                statusTag.className = 'step-status-tag pending';
                statusTag.textContent = dict.tag_pending || '○ PENDING';
            } else if (i < stepNumber || (i === stepNumber && completed)) {
                el.className = 'timeline-step step-done';
                if (marker) marker.textContent = '✓';
                statusTag.className = 'step-status-tag done';
                statusTag.textContent = dict.tag_completed || '✓ COMPLETED';
            } else if (i === stepNumber && active) {
                el.className = 'timeline-step step-active';
                if (marker) marker.textContent = i;
                if (i === 6) {
                    statusTag.className = 'step-status-tag waiting';
                    statusTag.textContent = dict.tag_waiting_vol || '⏳ WAITING FOR VOLUNTEER';
                } else if (i === 10) {
                    statusTag.className = 'step-status-tag waiting';
                    statusTag.textContent = dict.tag_waiting_hosp || '⏳ WAITING FOR HOSPITAL';
                } else {
                    statusTag.className = 'step-status-tag active';
                    statusTag.innerHTML = `<span class="proc-spinner"></span> ${dict.tag_processing || '🔵 PROCESSING...'}`;
                }
            } else {
                el.className = 'timeline-step step-pending';
                if (marker) marker.textContent = i;
                statusTag.className = 'step-status-tag locked';
                statusTag.textContent = dict.tag_locked || '🔒 LOCKED';
            }
        }
    }
'''

# Find the start of function applyLanguage in js_content
pos_apply_lang = js_content.find('    // Multilingual Translation Update')
if pos_apply_lang == -1:
    pos_apply_lang = js_content.find('    function applyLanguage(')

# Find the end of function setTimelineStep
pos_sync_ui = js_content.find('    // Synchronize Emergency Details Across All Screens')

if pos_apply_lang != -1 and pos_sync_ui != -1:
    new_js = js_content[:pos_apply_lang] + enhanced_lang_js + '\n' + js_content[pos_sync_ui:]
    with open('static/script.js', 'w', encoding='utf-8') as f:
        f.write(new_js)
    print("Successfully replaced applyLanguage and setTimelineStep in static/script.js")
else:
    print("Could not find slice indices for applyLanguage and setTimelineStep", pos_apply_lang, pos_sync_ui)
