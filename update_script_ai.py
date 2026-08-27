with open('static/script.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Let's inspect stepMap replacement
old_step_map = """    function setTimelineStep(stepNumber, active = true, completed = false) {
        const stepMap = {
            1: 'step-1-sos',
            2: 'step-2-loc',
            3: 'step-3-vol-found',
            4: 'step-4-alert-sent',
            5: 'step-5-vol-enroute',
            6: 'step-6-vol-reached',
            7: 'step-7-resp-dispatched',
            8: 'step-8-hosp-escalation',
            9: 'step-9-coordinated'
        };

        for (let i = 1; i <= 9; i++) {
            const el = document.getElementById(stepMap[i]);
            if (!el) continue;
            const marker = el.querySelector('.step-marker');
            if (i < stepNumber || (i === stepNumber && completed)) {
                el.className = 'timeline-step step-done';
                if (marker) marker.textContent = '✓';
            } else if (i === stepNumber && active) {
                el.className = 'timeline-step step-active';
                if (marker) marker.textContent = i;
            } else {
                el.className = 'timeline-step';
                if (marker) marker.textContent = i;
            }
        }
    }"""

new_step_map = """    function setTimelineStep(stepNumber, active = true, completed = false) {
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
            if (i < stepNumber || (i === stepNumber && completed)) {
                el.className = 'timeline-step step-done';
                if (marker) marker.textContent = '✓';
            } else if (i === stepNumber && active) {
                el.className = 'timeline-step step-active';
                if (marker) marker.textContent = i;
            } else {
                el.className = 'timeline-step';
                if (marker) marker.textContent = i;
            }
        }
    }"""

assert old_step_map in js_content, "Could not find old_step_map in script.js"
js_content = js_content.replace(old_step_map, new_step_map)

# Let's update runFullSimulation to 12 steps
old_sim = """    // Run Smooth 25-28 Second Live Emergency Response Simulation
    function runFullSimulation() {
        if (window.WariState.isSimulationRunning) return;
        window.WariState.isSimulationRunning = true;
        clearSimulationTimers();

        // 1. Switch to Emergency View and Initialize Stopwatch
        switchView('emergency-view');
        startStopwatch();

        // 2. Ensure Emergency Record Exists on Backend with synchronized ID EM-28471
        fetch('/api/demo/create-emergency', { method: 'POST' })
            .then(res => res.json())
            .then(data => {
                const emId = data.emergency_id || 'EM-28471';
                syncEmergencyUI(emId);
            })
            .catch(() => {
                syncEmergencyUI('EM-28471');
            });

        // Initialize Map
        initEmergencyMap();

        // STAGE 0: SOS REGISTERED
        setTimelineStep(1, true, false);
        const statusTitle = document.getElementById('em-current-status-title');
        if (statusTitle) statusTitle.textContent = '🚨 SOS REGISTERED';
        speakText("Emergency SOS registered in Saswad Zone 04. Locating patient.");
        showToast("🚨 SOS Registered in Central Incident Registry", "success");

        // STAGE 1 (2s): LOCATION IDENTIFIED
        const t1 = setTimeout(() => {
            setTimelineStep(2, true, false);
            if (statusTitle) statusTitle.textContent = '📍 LOCATION & ZONE IDENTIFIED';
            speakText("Patient coordinates matched to Zone 04, Saswad Palkhi Maidan.");
            showToast("📍 Coordinates Matched: Zone 04 — Saswad Palkhi Maidan (±5m)", "info");
        }, 2000);

        // STAGE 2 (4s): NEAREST VOLUNTEER FOUND
        const t2 = setTimeout(() => {
            setTimelineStep(3, true, false);
            if (statusTitle) statusTitle.textContent = '👥 NEAREST VOLUNTEER FOUND';
            updateVolunteerDistance(320, 2, '🟡 Responding', '🟡 RESPONDING');
            speakText("Nearest volunteer Ramesh Kulkarni found, 320 metres away.");
            showToast("👥 Volunteer Found: Ramesh Kulkarni (V-001) • 320m away", "success");
        }, 4000);

        // STAGE 3 (6s): VOLUNTEER NOTIFIED
        const t3 = setTimeout(() => {
            setTimelineStep(4, true, false);
            if (statusTitle) statusTitle.textContent = '🔔 VOLUNTEER ALERT SENT';
            speakText("Emergency alert sent to volunteer device.");
            showToast("🔔 Alert Dispatched to Volunteer Ramesh Kulkarni", "info");
        }, 6000);

        // STAGE 4 (8s): VOLUNTEER EN ROUTE (320m)
        const t4 = setTimeout(() => {
            setTimelineStep(5, true, false);
            if (statusTitle) statusTitle.textContent = '🚶 VOLUNTEER EN ROUTE';
            updateVolunteerDistance(320, 2, '🟡 Responding', '🟡 RESPONDING');
            speakText("Volunteer Ramesh Kulkarni is en route to patient location.");
        }, 8000);

        // STAGE 5 (11s): VOLUNTEER APPROACHING (180m)
        const t5 = setTimeout(() => {
            updateVolunteerDistance(180, 1, '🔵 Approaching', '🔵 APPROACHING');
            showToast("🚶 Volunteer Approaching: 180m (ETA 1 min)", "info");
        }, 11000);

        // STAGE 6 (13s): VOLUNTEER CLOSE (60m)
        const t6 = setTimeout(() => {
            updateVolunteerDistance(60, 1, '🔵 Approaching', '🔵 APPROACHING');
        }, 13000);

        // STAGE 7 (15s): VOLUNTEER WITH PATIENT (0m)
        const t7 = setTimeout(() => {
            setTimelineStep(6, true, false);
            if (statusTitle) statusTitle.textContent = '🤝 VOLUNTEER WITH PATIENT';
            updateVolunteerDistance(0, 0, '🟢 With Patient', '🟢 WITH PATIENT');
            speakText("Volunteer has reached the patient.");
            showToast("🤝 Volunteer Ramesh Kulkarni is WITH THE PATIENT (0m)", "success");

            // Update volunteer view reached banner
            const reachBanner = document.getElementById('reached-confirmed-banner');
            if (reachBanner) reachBanner.classList.remove('hidden');
        }, 15000);

        // STAGE 8 (19s): MEDICAL RESPONDER DISPATCHED
        const t8 = setTimeout(() => {
            setTimelineStep(7, true, false);
            if (statusTitle) statusTitle.textContent = '🚑 MEDICAL RESPONDER EN ROUTE';
            const respState = document.getElementById('resp-state-text');
            if (respState) respState.textContent = '🔵 EN ROUTE (Ambulance 1)';
            speakText("Mobile Ambulance Unit 1 dispatched with Dr. Arvind Shinde.");
            showToast("🚑 Ambulance Dispatched: Dr. Arvind Shinde (MR-001)", "success");
        }, 19000);

        // STAGE 9 (23s): HOSPITAL ESCALATION
        const t9 = setTimeout(() => {
            setTimelineStep(8, true, false);
            if (statusTitle) statusTitle.textContent = '🏥 HOSPITAL ESCALATION';
            const hospCard = document.getElementById('hospital-escalation-card');
            if (hospCard) hospCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            speakText("Nearest trauma hospital identified: Saswad Rural Hospital, 2.8 kilometres away.");
            showToast("🏥 Hospital Escalation: Saswad Rural Hospital (2.8 km • 8 min)", "info");
        }, 23000);

        // STAGE 10 (27s): RESPONSE COORDINATED & OPEN SCORECARD
        const t10 = setTimeout(() => {
            setTimelineStep(9, false, true);
            if (statusTitle) statusTitle.textContent = '✅ RESPONSE COORDINATED';
            stopStopwatch();
            window.WariState.isSimulationRunning = false;
            speakText("Emergency response successfully coordinated. Total response time 4 minutes 18 seconds. WariSeva Score 92 out of 100.");
            showToast("✅ Emergency Response Coordinated! WariSeva Score: 92/100", "success");

            // Trigger Scorecard Modal
            const modal = document.getElementById('analytics-modal');
            if (modal) modal.classList.remove('hidden');
        }, 27000);

        window.WariState.simulationTimers.push(t1, t2, t3, t4, t5, t6, t7, t8, t9, t10);
    }"""

new_sim = """    // Run Smooth 30-Second Live Emergency Response Simulation (12 Stages)
    function runFullSimulation() {
        if (window.WariState.isSimulationRunning) return;
        window.WariState.isSimulationRunning = true;
        clearSimulationTimers();

        // 1. Switch to Emergency View and Initialize Stopwatch
        switchView('emergency-view');
        startStopwatch();

        // 2. Ensure Emergency Record Exists on Backend with synchronized ID EM-28471
        fetch('/api/demo/create-emergency', { method: 'POST' })
            .then(res => res.json())
            .then(data => {
                const emId = data.emergency_id || 'EM-28471';
                syncEmergencyUI(emId);
                fetchAiRecommendation(emId);
            })
            .catch(() => {
                syncEmergencyUI('EM-28471');
                fetchAiRecommendation('EM-28471');
            });

        // Initialize Map
        initEmergencyMap();

        // STEP 1 (0s): SOS REGISTERED
        setTimelineStep(1, true, false);
        const statusTitle = document.getElementById('em-current-status-title');
        if (statusTitle) statusTitle.textContent = '🚨 SOS REGISTERED';
        speakText("Emergency SOS registered. Locating patient.");
        showToast("🚨 SOS Sent & Registered in Central Registry", "success");

        // STEP 2 (2s): EXACT LOCATION ACQUIRED
        const t1 = setTimeout(() => {
            setTimelineStep(2, true, false);
            if (statusTitle) statusTitle.textContent = '📍 EXACT LOCATION ACQUIRED';
            showToast("📍 Exact Coordinates: 18.3444, 74.0305 (±5m)", "info");
        }, 2000);

        // STEP 3 (4s): WARI ZONE IDENTIFIED
        const t2 = setTimeout(() => {
            setTimelineStep(3, true, false);
            if (statusTitle) statusTitle.textContent = '🗺️ ZONE IDENTIFIED';
            speakText("Patient located in Zone 04, Saswad Palkhi Maidan.");
            showToast("🗺️ Zone Identified: Zone 04 — Saswad Palkhi Maidan", "info");
        }, 4000);

        // STEP 4 (6s): SEVERITY CLASSIFIED
        const t3 = setTimeout(() => {
            setTimelineStep(4, true, false);
            if (statusTitle) statusTitle.textContent = '🔴 SEVERITY: CRITICAL';
            showToast("🔴 Severity Classified: CRITICAL (Medical Triage Priority)", "info");
        }, 6000);

        // STEP 5 (8s): AI RESPONDER RECOMMENDATION
        const t4 = setTimeout(() => {
            setTimelineStep(5, true, false);
            if (statusTitle) statusTitle.textContent = '🤖 AI RESPONDER MATCHED';
            fetchAiRecommendation('EM-28471');
            speakText("AI Response Engine matched volunteer Ramesh Kulkarni with response score 94 out of 100.");
            showToast("🤖 AI Recommendation: Ramesh Kulkarni (V-001) • Score 94/100", "success");
        }, 8000);

        // STEP 6 (10s): VOLUNTEER ALERT SENT
        const t5 = setTimeout(() => {
            setTimelineStep(6, true, false);
            if (statusTitle) statusTitle.textContent = '🔔 VOLUNTEER ALERT SENT';
            showToast("🔔 Emergency Alert Sent to Volunteer Device", "info");
        }, 10000);

        // STEP 7 (12s): VOLUNTEER ACCEPTED
        const t6 = setTimeout(() => {
            setTimelineStep(7, true, false);
            if (statusTitle) statusTitle.textContent = '🤝 VOLUNTEER ACCEPTED';
            updateVolunteerDistance(320, 2, '🟡 Responding', '🟡 RESPONDING');
            speakText("Volunteer accepted dispatch.");
            showToast("🤝 Volunteer Ramesh Kulkarni Accepted Dispatch", "success");
        }, 12000);

        // STEP 8 (16s): VOLUNTEER EN ROUTE (320m -> 180m -> 60m)
        const t7 = setTimeout(() => {
            setTimelineStep(8, true, false);
            if (statusTitle) statusTitle.textContent = '🚶 VOLUNTEER EN ROUTE';
            updateVolunteerDistance(250, 2, '🟡 Responding', '🟡 RESPONDING');
            speakText("Volunteer is moving toward patient via safe bypass corridor.");
        }, 16000);

        const t7b = setTimeout(() => {
            updateVolunteerDistance(120, 1, '🔵 Approaching', '🔵 APPROACHING');
            showToast("🚶 Volunteer Approaching: 120m (ETA 1 min)", "info");
        }, 18000);

        // STEP 9 (20s): VOLUNTEER REACHED PATIENT (0m)
        const t8 = setTimeout(() => {
            setTimelineStep(9, true, false);
            if (statusTitle) statusTitle.textContent = '🤝 WITH PATIENT';
            updateVolunteerDistance(0, 0, '🟢 With Patient', '🟢 WITH PATIENT');
            speakText("Volunteer has reached the patient. First aid administered.");
            showToast("🤝 Volunteer Ramesh Kulkarni is WITH THE PATIENT (0m)", "success");
            document.getElementById('reached-confirmed-banner')?.classList.remove('hidden');
        }, 20000);

        // STEP 10 (22s): MEDICAL RESPONDER DISPATCHED
        const t9 = setTimeout(() => {
            setTimelineStep(10, true, false);
            if (statusTitle) statusTitle.textContent = '🚑 MEDICAL RESPONDER DISPATCHED';
            const respState = document.getElementById('resp-state-text');
            if (respState) respState.textContent = '🔵 EN ROUTE (Mobile Ambulance 1)';
            speakText("Dr. Arvind Shinde Mobile Ambulance Unit dispatched.");
            showToast("🚑 Medical Ambulance Dispatched: Dr. Arvind Shinde (MR-001)", "success");
        }, 22000);

        // STEP 11 (25s): HOSPITAL RECOMMENDED
        const t10 = setTimeout(() => {
            setTimelineStep(11, true, false);
            if (statusTitle) statusTitle.textContent = '🏥 HOSPITAL RECOMMENDED';
            speakText("Recommended hospital: Saswad Rural Hospital, 2.8 kilometres away.");
            showToast("🏥 Hospital Recommended: Saswad Rural Hospital (2.8 km • 8 min)", "info");
        }, 25000);

        // STEP 12 (30s): EMERGENCY RESPONSE COORDINATED
        const t11 = setTimeout(() => {
            setTimelineStep(12, false, true);
            if (statusTitle) statusTitle.textContent = '✅ RESPONSE COORDINATED';
            stopStopwatch();
            window.WariState.isSimulationRunning = false;
            speakText("Emergency response successfully coordinated. WariSeva Score 92 out of 100.");
            showToast("✅ Emergency Response Coordinated! Score: 92/100", "success");
            document.getElementById('analytics-modal')?.classList.remove('hidden');
        }, 30000);

        window.WariState.simulationTimers.push(t1, t2, t3, t4, t5, t6, t7, t7b, t8, t9, t10, t11);
    }"""

assert old_sim in js_content, "Could not find old_sim in script.js"
js_content = js_content.replace(old_sim, new_sim)

# Add AI helper functions and event handlers
helper_funcs = """
    // Fetch and Populate AI Recommendation in Emergency & Command Center Views
    function fetchAiRecommendation(emId) {
        const id = emId || 'EM-28471';
        fetch(`/api/emergency/${id}/ai-recommendation`)
            .then(res => res.json())
            .then(data => {
                if (!data.success) return;
                const rec = data.recommended_volunteer;
                if (rec) {
                    const titleEl = document.getElementById('ai-rec-title');
                    const scoreEl = document.getElementById('ai-rec-score');
                    if (titleEl) titleEl.textContent = `${rec.name} (${rec.wari_id})`;
                    if (scoreEl) scoreEl.textContent = rec.total_score;

                    // Update Command Center AI Panel
                    const cmdRec = document.getElementById('cmd-rec-vol-name');
                    if (cmdRec) cmdRec.textContent = `${rec.name} (${rec.wari_id})`;
                }

                const backups = data.backup_volunteers;
                if (backups && backups.length > 0) {
                    const b = backups[0];
                    const backupTxt = `${b.name} (${b.wari_id} • Score ${b.total_score}/100) — ${b.reason}`;
                    const aiBackup = document.getElementById('ai-backup-text');
                    const cmdBackup = document.getElementById('cmd-backup-text');
                    if (aiBackup) aiBackup.textContent = backupTxt;
                    if (cmdBackup) cmdBackup.textContent = backupTxt;
                }
            })
            .catch(() => {});
    }

    // Load Command Center Resource Metrics
    function loadCommandResourcesCount() {
        fetch('/api/command-center/resources-count')
            .then(res => res.json())
            .then(data => {
                if (!data.success) return;
                const elVols = document.getElementById('cm-avail-vols');
                const elResps = document.getElementById('cm-avail-resps');
                const elIncs = document.getElementById('cm-active-incs');
                const elHosps = document.getElementById('cm-nearby-hosps');
                const elCamps = document.getElementById('cm-active-camps');

                if (elVols) elVols.textContent = data.available_volunteers;
                if (elResps) elResps.textContent = data.available_medical_responders;
                if (elIncs) elIncs.textContent = data.active_incidents;
                if (elHosps) elHosps.textContent = data.nearby_hospitals;
                if (elCamps) elCamps.textContent = data.active_medical_camps;
            })
            .catch(() => {});
    }
"""

# Insert helper functions before document DOMContentLoaded event listener
dom_marker = "document.addEventListener('DOMContentLoaded', () => {"
assert dom_marker in js_content, "Could not find DOMContentLoaded in script.js"
js_content = js_content.replace(dom_marker, helper_funcs + "\n    " + dom_marker)

# Add event listeners for new modals & actions
event_handlers = """
        // 17. Load Command Center Resource Counts
        loadCommandResourcesCount();
        fetchAiRecommendation('EM-28471');

        // 18. Pilgrim Incident Modal Events
        document.getElementById('open-pilgrim-incident-btn')?.addEventListener('click', () => {
            document.getElementById('pilgrim-incident-modal')?.classList.remove('hidden');
        });

        document.getElementById('close-pilgrim-modal-btn')?.addEventListener('click', () => {
            document.getElementById('pilgrim-incident-modal')?.classList.add('hidden');
        });

        document.getElementById('pilgrim-incident-form')?.addEventListener('submit', (e) => {
            e.preventDefault();
            const name = document.getElementById('p-pilgrim-name')?.value || 'Elderly Pilgrim';
            const wariId = document.getElementById('p-pilgrim-wari-id')?.value || '';
            const emType = document.getElementById('p-emergency-type')?.value || 'MEDICAL';
            const severity = document.getElementById('p-severity-level')?.value || 'CRITICAL';
            const zone = document.getElementById('p-zone-select')?.value || 'Zone 04 — Saswad Palkhi Maidan';
            const notes = document.getElementById('p-notes')?.value || '';

            fetch('/api/incident/create-for-pilgrim', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    patient_name: name,
                    wari_id: wariId,
                    emergency_type: emType,
                    severity: severity,
                    zone: zone,
                    notes: notes,
                    latitude: 18.3444,
                    longitude: 74.0305
                })
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById('pilgrim-incident-modal')?.classList.add('hidden');
                showToast(`🚨 Incident ${data.emergency_id} created for ${name}!`, "success");
                syncEmergencyUI(data.emergency_id);
                switchView('emergency-view');
                runFullSimulation();
            })
            .catch(() => {
                document.getElementById('pilgrim-incident-modal')?.classList.add('hidden');
                showToast("Incident created in prototype mode.", "info");
                switchView('emergency-view');
            });
        });

        // 19. Volunteer Registration Modal Events
        document.getElementById('open-register-vol-btn')?.addEventListener('click', () => {
            document.getElementById('volunteer-reg-modal')?.classList.remove('hidden');
        });

        document.getElementById('close-volunteer-modal-btn')?.addEventListener('click', () => {
            document.getElementById('volunteer-reg-modal')?.classList.add('hidden');
        });

        document.getElementById('volunteer-reg-form')?.addEventListener('submit', (e) => {
            e.preventDefault();
            const name = document.getElementById('v-reg-name')?.value || 'Volunteer';
            const phone = document.getElementById('v-reg-phone')?.value || '9820099999';
            const zone = document.getElementById('v-reg-zone')?.value || 'Zone 04 — Saswad Palkhi Maidan';
            const skills = document.getElementById('v-reg-skills')?.value || 'First Aid, CPR';
            const cert = document.getElementById('v-reg-cert')?.value || 'First Aid Certified';
            const org = document.getElementById('v-reg-org')?.value || 'Warkari Seva Mandal';

            fetch('/api/volunteer/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: name,
                    phone: phone,
                    zone: zone,
                    skills: skills,
                    certification: cert,
                    organization: org
                })
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById('volunteer-reg-modal')?.classList.add('hidden');
                showToast(`✓ Volunteer ${name} (${data.volunteer_id}) Verified & Registered!`, "success");
                loadVolunteerFeed();
                loadCommandResourcesCount();
            })
            .catch(() => {
                document.getElementById('volunteer-reg-modal')?.classList.add('hidden');
                showToast("Volunteer registered in prototype mode.", "info");
            });
        });

        // 20. Volunteer Availability Toggle
        document.getElementById('vol-avail-toggle-btn')?.addEventListener('click', () => {
            const btn = document.getElementById('vol-avail-toggle-btn');
            fetch('/api/volunteer/toggle-availability', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ volunteer_id: 'V-001' })
            })
            .then(res => res.json())
            .then(data => {
                if (btn) {
                    if (data.status === 'AVAILABLE') {
                        btn.textContent = '🟢 STATUS: AVAILABLE';
                        btn.classList.remove('offline');
                        showToast("Volunteer status: 🟢 AVAILABLE for Dispatch", "success");
                    } else {
                        btn.textContent = '⚫ STATUS: OFFLINE';
                        btn.classList.add('offline');
                        showToast("Volunteer status: ⚫ OFFLINE (Excluded from AI Dispatch)", "info");
                    }
                }
                loadCommandResourcesCount();
            })
            .catch(() => {
                if (btn) {
                    btn.classList.toggle('offline');
                    btn.textContent = btn.classList.contains('offline') ? '⚫ STATUS: OFFLINE' : '🟢 STATUS: AVAILABLE';
                }
            });
        });

        // 21. Volunteer Accept & Reached Buttons
        document.getElementById('vol-accept-em-btn')?.addEventListener('click', () => {
            const emId = window.WariState.currentEmergencyId || 'EM-28471';
            fetch(`/api/emergency/${emId}/volunteer/accept`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ volunteer_id: 'V-001' })
            })
            .then(() => {
                showToast("Volunteer Ramesh Kulkarni Accepted Dispatch", "success");
                setTimelineStep(7, true, false);
            })
            .catch(() => {
                showToast("Volunteer accepted in prototype mode.", "info");
            });
        });
"""

end_marker = "initEmergencyMap();\n        loadServicesCards('WATER');"
assert end_marker in js_content, "Could not find end_marker in script.js"
js_content = js_content.replace(end_marker, event_handlers + "\n        " + end_marker)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Updated static/script.js with full 12-step timeline simulation, AI recommendation, and modal event handlers!")
