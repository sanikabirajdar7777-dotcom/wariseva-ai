import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace setDemoEmergencyStage implementation
old_stage_fn_start = content.find('    function setDemoEmergencyStage(stage) {')
old_stage_fn_end = content.find('    // =========================================================================\n    // 1. EMERGENCY TRIGGER WORKFLOW', old_stage_fn_start)

if old_stage_fn_start == -1 or old_stage_fn_end == -1:
    print("Could not locate setDemoEmergencyStage bounds", old_stage_fn_start, old_stage_fn_end)
else:
    new_stage_fn = '''    function setDemoEmergencyStage(stage) {
        window.WariState.demoEmergencyStage = stage;
        const lang = window.WariState.lang || 'en';
        const dict = i18n[lang] || i18n.en;
        const statusTitle = document.getElementById('em-current-status-title');
        const emMap = window.WariState.maps.emergency;
        const markers = window.WariState.markers.emergency;
        const cmdStatusText = document.getElementById('cmd-ins-status');

        speakStep(stage);

        switch (stage) {
            case 1:
                setTimelineStep(1, true, false);
                if (statusTitle) statusTitle.textContent = lang === 'mr' ? '🚨 SOS पाठवले आणि नोंदणी झाली' : (lang === 'hi' ? '🚨 SOS भेजा गया और दर्ज किया गया' : '🚨 SOS SENT & REGISTERED');
                if (cmdStatusText) cmdStatusText.textContent = lang === 'mr' ? 'आपत्कालीन घटना' : (lang === 'hi' ? 'आपातकालीन घटना' : 'ACTIVE EMERGENCY');
                showToast(lang === 'mr' ? "🚨 पायरी १: केंद्रीय नोंदणी प्रणालीमध्ये SOS नोंदवला गेला" : (lang === 'hi' ? "🚨 चरण १: केंद्रीय रजिस्टर में SOS दर्ज हुआ" : "🚨 Step 1: SOS Sent & Registered in Central Incident Registry"), "success");
                if (emMap && markers) {
                    if (!emMap.hasLayer(markers.patient)) markers.patient.addTo(emMap);
                    if (emMap.hasLayer(markers.volunteer)) emMap.removeLayer(markers.volunteer);
                    if (emMap.hasLayer(markers.responder)) emMap.removeLayer(markers.responder);
                    if (emMap.hasLayer(markers.hospital)) emMap.removeLayer(markers.hospital);
                    if (emMap.hasLayer(markers.bypass)) emMap.removeLayer(markers.bypass);
                    markers.volunteer.setLatLng([18.3470, 74.0330]);
                    emMap.setView([18.3444, 74.0305], 16);
                }
                break;

            case 2:
                setTimelineStep(1, false, true);
                setTimelineStep(2, true, false);
                if (statusTitle) statusTitle.textContent = lang === 'mr' ? '📍 अचूक ठिकाण मिळाले' : (lang === 'hi' ? '📍 सटीक स्थान प्राप्त हुआ' : '📍 EXACT LOCATION ACQUIRED');
                if (cmdStatusText) cmdStatusText.textContent = lang === 'mr' ? 'ठिकाण मिळाले' : (lang === 'hi' ? 'स्थान प्राप्त हुआ' : 'LOCATION ACQUIRED');
                showToast(lang === 'mr' ? "📍 पायरी २: अचूक ठिकाण: 18.3444, 74.0305 (±5m precision)" : (lang === 'hi' ? "📍 चरण २: सटीक स्थान: 18.3444, 74.0305 (±5m precision)" : "📍 Step 2: Exact Location: 18.3444, 74.0305 (±5m precision)"), "info");
                if (emMap) emMap.flyTo([18.3444, 74.0305], 17);
                break;

            case 3:
                setTimelineStep(2, false, true);
                setTimelineStep(3, true, false);
                if (statusTitle) statusTitle.textContent = lang === 'mr' ? '🗺️ वारी क्षेत्र ओळखले' : (lang === 'hi' ? '🗺️ वारी क्षेत्र की पहचान हुई' : '🗺️ WARI ZONE IDENTIFIED');
                showToast(lang === 'mr' ? "🗺️ पायरी ३: वारी क्षेत्र: झोन ०४ — सासवड पालखी मैदान" : (lang === 'hi' ? "🗺️ चरण ३: वारी क्षेत्र: जोन ०४ — सासवड पालखी मैदान" : "🗺️ Step 3: Wari Zone: Zone 04 — Saswad Palkhi Maidan"), "info");
                break;

            case 4:
                setTimelineStep(3, false, true);
                setTimelineStep(4, true, false);
                if (statusTitle) statusTitle.textContent = lang === 'mr' ? '🔴 तीव्रता: गंभीर' : (lang === 'hi' ? '🔴 गंभीरता: अत्यंत गंभीर' : '🔴 SEVERITY: CRITICAL');
                showToast(lang === 'mr' ? "🔴 पायरी ४: आपत्कालीन तीव्रता निश्चित: गंभीर (Medical Priority)" : (lang === 'hi' ? "🔴 चरण ४: आपातकाल की गंभीरता: अत्यंत गंभीर (Medical Priority)" : "🔴 Step 4: Emergency Classified: CRITICAL (Medical / Triage Priority)"), "info");
                break;

            case 5:
                setTimelineStep(1, false, true);
                setTimelineStep(2, false, true);
                setTimelineStep(3, false, true);
                setTimelineStep(4, false, true);
                setTimelineStep(5, false, true);
                setTimelineStep(6, true, false);
                if (statusTitle) statusTitle.textContent = lang === 'mr' ? '⏳ स्वयंसेवकाची प्रतीक्षा' : (lang === 'hi' ? '⏳ स्वयंसेवक की प्रतीक्षा' : '⏳ WAITING FOR VOLUNTEER ACCEPTANCE');
                if (cmdStatusText) cmdStatusText.textContent = lang === 'mr' ? 'पाठवले (प्रतीक्षा)' : (lang === 'hi' ? 'भेजा गया (प्रतीक्षा)' : 'DISPATCHED (WAITING)');
                fetchAiRecommendation('EM-28471');
                showToast(lang === 'mr' ? "🔔 पायरी ५ व ६: योग्य स्वयंसेवकाची शिफारस व सूचना पाठवली!" : (lang === 'hi' ? "🔔 चरण ५ व ६: नजदीकी स्वयंसेवक की सिफारिश व सूचना भेजी गई!" : "🔔 Step 5 & 6: Nearest Volunteer Matched & Alerted! Awaiting volunteer acceptance."), "info");
                if (emMap && markers) {
                    markers.volunteer.setLatLng([18.3470, 74.0330]);
                    if (!emMap.hasLayer(markers.volunteer)) markers.volunteer.addTo(emMap);
                    emMap.fitBounds([
                        [18.3444, 74.0305],
                        [18.3470, 74.0330]
                    ], { padding: [40, 40] });
                }
                break;

            case 6:
                setTimelineStep(5, false, true);
                setTimelineStep(6, true, false);
                if (statusTitle) statusTitle.textContent = lang === 'mr' ? '⏳ स्वयंसेवकाची प्रतीक्षा' : (lang === 'hi' ? '⏳ स्वयंसेवक की प्रतीक्षा' : '⏳ WAITING FOR VOLUNTEER ACCEPTANCE');
                showToast(lang === 'mr' ? "🔔 पायरी ६: स्वयंसेवक रमेश कुलकर्णी यांना सूचना पाठवली" : (lang === 'hi' ? "🔔 चरण ६: स्वयंसेवक रमेश कुलकर्णी को सूचना भेजी गई" : "🔔 Step 6: Emergency Alert Sent to Volunteer Ramesh Kulkarni"), "info");
                break;

            case 7:
                setTimelineStep(5, false, true);
                setTimelineStep(6, false, true);
                setTimelineStep(7, false, true);
                setTimelineStep(8, true, false);
                if (statusTitle) statusTitle.textContent = lang === 'mr' ? '🦺 स्वयंसेवकाने मदत स्वीकारली' : (lang === 'hi' ? '🦺 स्वयंसेवक ने केस स्वीकार किया' : '🦺 VOLUNTEER ACCEPTED • EN ROUTE');
                if (cmdStatusText) cmdStatusText.textContent = lang === 'mr' ? 'स्वयंसेवक मार्गस्थ' : (lang === 'hi' ? 'स्वयंसेवक मार्गस्थ' : 'VOLUNTEER EN ROUTE');
                updateVolunteerDistance(320, 2, lang === 'mr' ? '🟡 प्रतिसाद देत आहे' : (lang === 'hi' ? '🟡 प्रतिक्रिया दे रहे हैं' : '🟡 Responding'), '🟡 RESPONDING');
                showToast(lang === 'mr' ? "🦺 पायरी ७: स्वयंसेवक रमेश कुलकर्णी (V-001) यांनी केस स्वीकारली" : (lang === 'hi' ? "🦺 चरण ७: स्वयंसेवक रमेश कुलकर्णी (V-001) ने केस स्वीकार किया" : "🦺 Step 7: Volunteer Ramesh Kulkarni (V-001) Accepted Dispatch"), "success");
                if (emMap && markers) {
                    if (!emMap.hasLayer(markers.volunteer)) markers.volunteer.addTo(emMap);
                }
                break;

            case 8:
                setTimelineStep(8, true, false);
                if (statusTitle) statusTitle.textContent = lang === 'mr' ? '🚶 स्वयंसेवक मार्गस्थ' : (lang === 'hi' ? '🚶 स्वयंसेवक मार्गस्थ' : '🚶 VOLUNTEER EN ROUTE');
                if (cmdStatusText) cmdStatusText.textContent = lang === 'mr' ? 'मार्गस्थ' : (lang === 'hi' ? 'मार्गस्थ' : 'EN ROUTE');
                updateVolunteerDistance(180, 1, lang === 'mr' ? '🟡 प्रतिसाद देत आहे' : (lang === 'hi' ? '🟡 प्रतिक्रिया दे रहे हैं' : '🟡 Responding'), '🟡 RESPONDING');
                break;

            case 9:
                setTimelineStep(8, false, true);
                setTimelineStep(9, false, true);
                setTimelineStep(10, true, false);
                if (statusTitle) statusTitle.textContent = lang === 'mr' ? '📍 स्वयंसेवक पोहोचला' : (lang === 'hi' ? '📍 स्वयंसेवक पहुंच गया' : '📍 VOLUNTEER WITH PATIENT');
                if (cmdStatusText) cmdStatusText.textContent = lang === 'mr' ? 'स्वयंसेवक पोहोचला' : (lang === 'hi' ? 'स्वयंसेवक पहुंच गया' : 'VOLUNTEER ARRIVED');
                updateVolunteerDistance(0, 0, lang === 'mr' ? '🟢 रुग्णाजवळ पोहोचले' : (lang === 'hi' ? '🟢 मरीज के पास पहुंचे' : '🟢 With Patient'), '🟢 VOLUNTEER ARRIVED');
                showToast(lang === 'mr' ? "📍 पायरी ९: स्वयंसेवक रुग्णाजवळ पोहोचले (0m • With Patient)" : (lang === 'hi' ? "📍 चरण ९: स्वयंसेवक मरीज के पास पहुंचे (0m • With Patient)" : "📍 Step 9: Volunteer Arrived at Emergency Location (0m • With Patient)"), "success");
                document.getElementById('reached-confirmed-banner')?.classList.remove('hidden');
                if (markers && markers.volunteer) {
                    markers.volunteer.setLatLng([18.3444, 74.0305]);
                }
                break;

            case 10:
                setTimelineStep(10, true, false);
                if (statusTitle) statusTitle.textContent = lang === 'mr' ? '🏥 वैद्यकीय केंद्राने केस स्वीकारली' : (lang === 'hi' ? '🏥 चिकित्सा केंद्र ने केस स्वीकार किया' : '🏥 AI HOSPITAL RECOMMENDATION');
                if (cmdStatusText) cmdStatusText.textContent = lang === 'mr' ? 'रुग्णालय शिफारस' : (lang === 'hi' ? 'अस्पताल सिफारिश' : 'HOSPITAL RECOMMENDED');
                break;

            case 11:
                setTimelineStep(10, false, true);
                setTimelineStep(11, false, true);
                if (statusTitle) statusTitle.textContent = lang === 'mr' ? '🚑 रुग्ण पोहोचला • बेड राखीव' : (lang === 'hi' ? '🚑 मरीज पहुंच गया • बेड आरक्षित' : '🚑 HOSPITAL ACCEPTED • BED RESERVED');
                if (cmdStatusText) cmdStatusText.textContent = lang === 'mr' ? 'रुग्णालय सज्ज' : (lang === 'hi' ? 'अस्पताल तैयार' : 'HOSPITAL READY');
                const respState = document.getElementById('resp-state-text');
                if (respState) respState.textContent = lang === 'mr' ? '🏥 वैद्यकीय केंद्र: रुग्ण स्वीकारला • बेड राखीव: १' : (lang === 'hi' ? '🏥 चिकित्सा केंद्र: मरीज स्वीकार किया • बेड आरक्षित: १' : '🏥 HOSPITAL ACCEPTED • BED RESERVED: 1');
                showToast(lang === 'mr' ? "🚑 पायरी ११: रुग्णालयाने केस स्वीकारली (बेड राखीव: १)" : (lang === 'hi' ? "🚑 चरण ११: अस्पताल ने केस स्वीकार किया (बेड आरक्षित: १)" : "🚑 Step 11: Hospital Accepted Case (Bed Reserved: 1)"), "success");
                if (emMap && markers) {
                    if (!emMap.hasLayer(markers.responder)) markers.responder.addTo(emMap);
                    emMap.fitBounds([
                        [18.3444, 74.0305],
                        [18.3390, 74.0260]
                    ], { padding: [40, 40] });
                }
                break;

            case 12:
                for (let s = 1; s <= 12; s++) {
                    setTimelineStep(s, false, true);
                }
                if (statusTitle) statusTitle.textContent = lang === 'mr' ? '✅ केस पूर्ण झाली' : (lang === 'hi' ? '✅ केस पूरा हुआ' : '✅ CASE RESOLVED');
                if (cmdStatusText) cmdStatusText.textContent = lang === 'mr' ? 'पूर्ण' : (lang === 'hi' ? 'पूर्ण' : 'RESOLVED');
                stopStopwatch();
                window.WariState.isSimulationRunning = false;
                showToast(lang === 'mr' ? "✅ पायरी १२: केस यशस्वीरित्या पूर्ण झाली! उपचार सुरू." : (lang === 'hi' ? "✅ चरण १२: केस सफलतापूर्वक पूरा हुआ! उपचार जारी." : "✅ Step 12: Case Resolved! Patient Admitted Successfully."), "success");
                if (emMap && markers) {
                    if (!emMap.hasLayer(markers.bypass)) markers.bypass.addTo(emMap);
                }
                const completeCard = document.getElementById('coordination-complete-card');
                if (completeCard) {
                    completeCard.classList.remove('hidden');
                }
                break;
        }
    }
'''
    content = content[:old_stage_fn_start] + new_stage_fn + content[old_stage_fn_end:]

# Ensure language listener is initialized in DOMContentLoaded
dom_init_pos = content.find('document.addEventListener(\'DOMContentLoaded\', () => {')
if dom_init_pos != -1:
    init_snippet = '''        // Initialize Multilingual System
        const savedLang = localStorage.getItem('wariseva_lang') || 'en';
        applyLanguage(savedLang);

        const langSelect = document.getElementById('lang-select');
        if (langSelect) {
            langSelect.value = savedLang;
            langSelect.addEventListener('change', (e) => {
                applyLanguage(e.target.value);
            });
        }
'''
    # Check if already in content
    if 'Initialize Multilingual System' not in content:
        insert_at = dom_init_pos + len('document.addEventListener(\'DOMContentLoaded\', () => {\n')
        content = content[:insert_at] + init_snippet + content[insert_at:]

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated static/script.js with full multilingual state and voice dispatch!")
