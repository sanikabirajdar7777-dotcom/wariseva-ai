import os

js_content = """// =========================================================================
// WARISEVA AI — MASTER CONTROLLER & SIMULATED LIVE RESPONSE ENGINE
// Sant Dnyaneshwar & Sant Tukaram Palkhi Emergency Response Prototype
// =========================================================================

(function () {
    'use strict';

    // Global Application State Object
    window.WariState = {
        lang: 'en',
        voiceEnabled: true,
        elderMode: false,
        currentView: 'home-view',
        currentWariId: 'WS-28471',
        currentUserName: 'Tukaram Shinde',
        currentPhone: '9822128471',
        currentEmergencyId: null,
        emergencyStatus: null,
        stopwatchInterval: null,
        stopwatchSeconds: 0,
        simulationTimers: [],
        isSimulationRunning: false,
        gpsCoords: { lat: 18.3444, lon: 74.0305, accuracy: 5.0 },
        zone: 'Zone 04 — Saswad Palkhi Maidan',
        landmark: 'Saswad Central Palkhi Maidan Ground',
        volunteer: {
            id: 'V-001',
            name: 'Ramesh Kulkarni',
            sector: 'Zone 04 — Saswad Palkhi Maidan',
            distance: 320,
            eta: 2,
            status: 'AVAILABLE'
        },
        responder: {
            id: 'MR-001',
            name: 'Dr. Arvind Shinde',
            unit: 'Mobile Ambulance Unit 1',
            status: 'AVAILABLE',
            eta: 4
        },
        hospital: {
            id: 'HOSP-001',
            name: 'Saswad Rural Hospital',
            distance: '2.8 km',
            eta: '8 min',
            status: 'Available'
        },
        maps: {
            emergency: null,
            safety: null,
            responder: null,
            command: null
        },
        markers: {
            emergency: {},
            safety: [],
            responder: {},
            command: {}
        },
        groupMembers: [
            { id: 1, name: 'Sunita Shinde', phone: '9822128472', relation: 'Spouse' },
            { id: 2, name: 'Ganesh Shinde', phone: '9822128473', relation: 'Son' }
        ]
    };

    // Multilingual Translation Dictionaries
    const i18n = {
        en: {
            tagline: "Your safety, one tap away.",
            value_prop: "\\"We don't just report an emergency — we coordinate the response behind the SOS.\\"",
            demo_desc: "DEMO DATA • SIMULATED RESPONSE",
            reset_demo: "🔄 RESET",
            elder_mode: "Elder Mode",
            nav_home: "Home",
            nav_emergency: "Emergency",
            nav_map: "Safety Map",
            nav_services: "Services",
            nav_volunteer: "Volunteer",
            nav_responder: "Responder",
            nav_command: "Command",
            palkhi_safety: "🚩 Palkhi Safety Coordination",
            hero_tagline: "\\"Your safety, one tap away.\\"",
            hero_subtext: "Emergency coordination and safety assistance for the Sant Dnyaneshwar & Sant Tukaram Palkhi Wari.",
            sos_btn_text: "EMERGENCY",
            sos_btn_sub: "PRESS FOR HELP • मदत",
            current_zone: "Zone 04 — Saswad Palkhi Maidan",
            act_where_am_i: "Where am I?",
            act_medical_help: "Medical Help",
            act_safety_map: "Safety Map",
            quick_services_title: "🛡️ Quick Safety Services / सुविधा",
            see_all: "See All 13 Facilities →",
            svc_water: "Water",
            svc_water_sub: "पिण्याचे पाणी",
            svc_toilets: "Toilets",
            svc_toilets_sub: "स्वच्छतागृह",
            svc_rest: "Rest",
            svc_rest_sub: "विश्रांती मंडप",
            svc_medical: "Medical",
            svc_medical_sub: "आरोग्य केंद्र",
            svc_food: "Food / Prasad",
            svc_hospitals: "Hospitals",
            safety_id_title: "WariSeva Safety ID / सुरक्षा ओळखपत्र",
            safety_id_sub: "Register demo profile for quick identification and instant SOS dispatch.",
            label_full_name: "Full Name / पूर्ण नाव",
            label_phone: "Mobile Number / फोन नंबर",
            btn_create_id: "CREATE SAFETY ID",
            id_active_badge: "Safety ID Active & Registered",
            btn_change_profile: "Change / Register Another Profile",
            em_kicker: "HELP IS ON THE WAY • मदत येत आहे",
            em_help_requested: "HELP REQUESTED",
            palkhi_zone: "Wari Palkhi Zone",
            nearest_landmark: "Nearest Landmark",
            gps_precision: "GPS Precision",
            response_timeline: "📊 Emergency Response Timeline",
            btn_open_tactical_map: "🗺️ VIEW TACTICAL MAP",
            btn_report_another: "REPORT ANOTHER EMERGENCY",
            filter_label: "Filters:",
            map_pin_prompt: "Select Any Map Pin",
            map_pin_prompt_sub: "Click any service marker or emergency incident to view distance, route, and details.",
            btn_focus_pin: "🎯 FOCUS ON MAP",
            services_page_title: "Wari Safety Directory",
            services_page_sub: "Find verified essential facilities across all 12 pilgrimage route sectors.",
            select_zone: "Select Sector / झोन निवडा:",
            modal_sos_title: "Trigger Emergency SOS?",
            modal_sos_msg: "This will capture your exact coordinates and immediately alert the nearest Palkhi route volunteer and medical responder unit.",
            modal_using_id: "Using Safety ID:",
            btn_cancel: "CANCEL",
            btn_confirm_sos: "DISPATCH SOS",
            acquiring_gps: "Acquiring GPS Position...",
            mapping_checkpoint: "Mapping to nearest Palkhi route checkpoint",
            active_em_title: "ACTIVE EMERGENCY IN PROGRESS",
            view_live_response: "VIEW LIVE RESPONSE →",
            elder_screen_title: "ज्येष्ठ नागरिक सुरक्षा मोड • ELDER MODE",
            elder_screen_sub: "सोपी व मोठी बटणे • तात्काळ मदत एका स्पर्शात",
            exit_elder_mode: "✕ सामान्य मोड",
            elder_sos_title: "🆘 तातडीची मदत (EMERGENCY)",
            elder_sos_desc: "दाबा — मदत त्वरित आपल्याकडे येईल",
            elder_where_title: "📍 मी कुठे आहे? (WHERE AM I?)",
            elder_med_title: "🏥 डॉक्टर / औषधोपचार (MEDICAL)",
            elder_med_desc: "जवळचे आरोग्य शिबिर (१८० मीटर)",
            elder_water_title: "💧 पिण्याचे पाणी (WATER)",
            elder_water_desc: "सासवड पालखी मैदान जल केंद्र (५५ मीटर)",
            elder_toilet_title: "🚻 स्वच्छतागृह (TOILETS)",
            elder_toilet_desc: "स्वच्छ मोबाईल टॉयलेट (९० मीटर)"
        },
        mr: {
            tagline: "आपली सुरक्षा, एका स्पर्शात.",
            value_prop: "\\"आम्ही केवळ आपत्कालीन नोंद करत नाही — मदतीची संपूर्ण यंत्रणा समन्वयित करतो.\\"",
            demo_desc: "डेमो डेटा • सिम्युलेटेड प्रतिसाद",
            reset_demo: "🔄 रिसेट",
            elder_mode: "ज्येष्ठ नागरिक मोड",
            nav_home: "मुख्य पान",
            nav_emergency: "आपत्कालीन",
            nav_map: "सुरक्षा नकाशा",
            nav_services: "सुविधा",
            nav_volunteer: "स्वयंसेवक",
            nav_responder: "आरोग्य पथक",
            nav_command: "नियंत्रण कक्ष",
            palkhi_safety: "🚩 पालखी सुरक्षा समन्वय",
            hero_tagline: "\\"आपली सुरक्षा, एका स्पर्शात.\\"",
            hero_subtext: "संत ज्ञानेश्वर व संत तुकाराम पालखी वारीसाठी डिजिटल आरोग्य व सुरक्षा यंत्रणा.",
            sos_btn_text: "तातडीची मदत",
            sos_btn_sub: "मदतीसाठी दाबा • SOS",
            current_zone: "झोन ०४ — सासवड पालखी मैदान",
            act_where_am_i: "मी कुठे आहे?",
            act_medical_help: "वैद्यकीय मदत",
            act_safety_map: "सुरक्षा नकाशा",
            quick_services_title: "🛡️ तातडीच्या वारी सुविधा",
            see_all: "सर्व १३ सुविधा पहा →",
            svc_water: "पिण्याचे पाणी",
            svc_water_sub: "शुद्ध जल केंद्र",
            svc_toilets: "स्वच्छतागृह",
            svc_toilets_sub: "मोबाईल टॉयलेट",
            svc_rest: "विश्रांती",
            svc_rest_sub: "विश्रांती मंडप",
            svc_medical: "आरोग्य केंद्र",
            svc_medical_sub: "प्रथमोपचार तंबू",
            svc_food: "अन्नछत्र / प्रसाद",
            svc_hospitals: "रुग्णालये",
            safety_id_title: "वारीसेवा सुरक्षा ओळखपत्र",
            safety_id_sub: "तातडीच्या मदतीसाठी आपली माहिती नोंदवा.",
            label_full_name: "पूर्ण नाव",
            label_phone: "मोबाईल नंबर",
            btn_create_id: "सुरक्षा आयडी तयार करा",
            id_active_badge: "सुरक्षा ओळखपत्र सक्रिय आहे",
            btn_change_profile: "दुसरे ओळखपत्र नोंदवा",
            em_kicker: "मदत येत आहे • घाबरू नका",
            em_help_requested: "मदत मागितली आहे",
            palkhi_zone: "पालखी झोन",
            nearest_landmark: "जवळची खूण",
            gps_precision: "GPS अचूकता",
            response_timeline: "📊 आपत्कालीन प्रतिसाद कालरेषा",
            btn_open_tactical_map: "🗺️ संपूर्ण नकाशा पहा",
            btn_report_another: "दुसरी मदत नोंदवा",
            filter_label: "फिल्टर:",
            map_pin_prompt: "नकाशावरील पिन निवडा",
            map_pin_prompt_sub: "तपशील, अंतर आणि मार्ग पाहण्यासाठी कोणत्याही पिनवर क्लिक करा.",
            btn_focus_pin: "🎯 नकाशावर पहा",
            services_page_title: "वारी सुरक्षा सुविधा डिरेक्टरी",
            services_page_sub: "सर्व १२ पालखी टप्प्यांवरील सत्यापित सुविधा.",
            select_zone: "झोन निवडा:",
            modal_sos_title: "तातडीची मदत मागवायची का?",
            modal_sos_msg: "आपले थेट लोकेशन नोंदवून सर्वात जवळच्या वारी स्वयंसेवकाला तात्काळ पाठवले जाईल.",
            modal_using_id: "वापरत असलेला आयडी:",
            btn_cancel: "रद्द करा",
            btn_confirm_sos: "मदत पाठवा (SOS)",
            acquiring_gps: "GPS लोकेशन मिळवत आहे...",
            mapping_checkpoint: "जवळच्या पालखी चेकपॉईंटशी जोडत आहे",
            active_em_title: "आपत्कालीन मदत सक्रिय आहे",
            view_live_response: "प्रतिसाद पहा →",
            elder_screen_title: "ज्येष्ठ नागरिक सुरक्षा मोड",
            elder_screen_sub: "सोपी व मोठी बटणे • तात्काळ मदत एका स्पर्शात",
            exit_elder_mode: "✕ सामान्य मोड",
            elder_sos_title: "🆘 तातडीची मदत (EMERGENCY)",
            elder_sos_desc: "दाबा — मदत त्वरित आपल्याकडे येईल",
            elder_where_title: "📍 मी कुठे आहे? (WHERE AM I?)",
            elder_med_title: "🏥 डॉक्टर / औषधोपचार",
            elder_med_desc: "जवळचे आरोग्य शिबिर (१८० मीटर)",
            elder_water_title: "💧 पिण्याचे पाणी",
            elder_water_desc: "सासवड पालखी मैदान जल केंद्र (५५ मीटर)",
            elder_toilet_title: "🚻 स्वच्छतागृह",
            elder_toilet_desc: "स्वच्छ मोबाईल टॉयलेट (९० मीटर)"
        },
        hi: {
            tagline: "आपकी सुरक्षा, एक स्पर्श में.",
            value_prop: "\\"हम सिर्फ आपातकाल दर्ज नहीं करते — पूरी राहत प्रणाली का समन्वय करते हैं.\\"",
            demo_desc: "डेमो डेटा • सिम्युलेटेड प्रतिक्रिया",
            reset_demo: "🔄 रीसेट",
            elder_mode: "वरिष्ठ नागरिक मोड",
            nav_home: "होम",
            nav_emergency: "आपातकाल",
            nav_map: "सुरक्षा नक्शा",
            nav_services: "सुविधाएं",
            nav_volunteer: "स्वयंसेवक",
            nav_responder: "चिकित्सा दल",
            nav_command: "कंट्रोल रूम",
            palkhi_safety: "🚩 पालखी सुरक्षा समन्वय",
            hero_tagline: "\\"आपकी सुरक्षा, एक स्पर्श में.\\"",
            hero_subtext: "संत ज्ञानेश्वर एवं संत तुकाराम पालखी वारी के लिए डिजिटल स्वास्थ्य और सुरक्षा प्रणाली.",
            sos_btn_text: "आपातकालीन मदद",
            sos_btn_sub: "सहायता के लिए दबाएं • SOS",
            current_zone: "जोन ०४ — सासवड पालखी मैदान",
            act_where_am_i: "मैं कहाँ हूँ?",
            act_medical_help: "चिकित्सा सहायता",
            act_safety_map: "सुरक्षा नक्शा",
            quick_services_title: "🛡️ त्वरित सुरक्षा सेवाएं",
            see_all: "सभी १३ सुविधाएं देखें →",
            svc_water: "पीने का पानी",
            svc_water_sub: "शुद्ध जल केंद्र",
            svc_toilets: "शौचालय",
            svc_toilets_sub: "मोबाइल शौचालय",
            svc_rest: "विश्राम",
            svc_rest_sub: "विश्राम पंडाल",
            svc_medical: "चिकित्सा केंद्र",
            svc_medical_sub: "प्राथमिक उपचार",
            svc_food: "भोजन / प्रसाद",
            svc_hospitals: "अस्पताल",
            safety_id_title: "वारीसेवा सुरक्षा पहचान पत्र",
            safety_id_sub: "त्वरित सहायता के लिए अपनी जानकारी दर्ज करें.",
            label_full_name: "पूरा नाम",
            label_phone: "मोबाइल नंबर",
            btn_create_id: "सुरक्षा आईडी बनाएं",
            id_active_badge: "सुरक्षा आईडी सक्रिय है",
            btn_change_profile: "अन्य प्रोफाइल दर्ज करें",
            em_kicker: "मदद आ रही है • निश्चिंत रहें",
            em_help_requested: "मदद का अनुरोध किया गया",
            palkhi_zone: "पालखी जोन",
            nearest_landmark: "निकटतम स्थान",
            gps_precision: "जीपीएस सटीकता",
            response_timeline: "📊 आपातकालीन प्रतिक्रिया समयरेखा",
            btn_open_tactical_map: "🗺️ संपूर्ण नक्शा देखें",
            btn_report_another: "अन्य मदद दर्ज करें",
            filter_label: "फ़िल्टर:",
            map_pin_prompt: "नक्शे पर कोई पिन चुनें",
            map_pin_prompt_sub: "दूरी, मार्ग और विवरण देखने के लिए किसी भी पिन पर क्लिक करें.",
            btn_focus_pin: "🎯 नक्शे पर देखें",
            services_page_title: "वारी सुरक्षा सुविधा सूची",
            services_page_sub: "सभी १२ पालखी चरणों पर सत्यापित सुविधाएं.",
            select_zone: "जोन चुनें:",
            modal_sos_title: "आपातकालीन मदद का अनुरोध करें?",
            modal_sos_msg: "आपका सटीक स्थान दर्ज करके निकटतम वारी स्वयंसेवक को तुरंत भेजा जाएगा.",
            modal_using_id: "उपयोग की जा रही आईडी:",
            btn_cancel: "रद्द करें",
            btn_confirm_sos: "मदद भेजें (SOS)",
            acquiring_gps: "जीपीएस स्थान प्राप्त कर रहे हैं...",
            mapping_checkpoint: "निकटतम पालखी चेकपॉइंट से जोड़ रहे हैं",
            active_em_title: "आपातकालीन प्रतिक्रिया जारी है",
            view_live_response: "प्रतिक्रिया देखें →",
            elder_screen_title: "वरिष्ठ नागरिक सुरक्षा मोड",
            elder_screen_sub: "सरल और बड़े बटन • एक स्पर्श में सहायता",
            exit_elder_mode: "✕ सामान्य मोड",
            elder_sos_title: "🆘 आपातकालीन मदद (EMERGENCY)",
            elder_sos_desc: "दबाएं — मदद तुरंत पहुंचेगी",
            elder_where_title: "📍 मैं कहाँ हूँ? (WHERE AM I?)",
            elder_med_title: "🏥 डॉक्टर / दवाएं",
            elder_med_desc: "निकटतम चिकित्सा शिविर (१८० मीटर)",
            elder_water_title: "💧 पीने का पानी",
            elder_water_desc: "सासवड पालखी मैदान जल केंद्र (५५ मीटर)",
            elder_toilet_title: "🚻 शौचालय",
            elder_toilet_desc: "स्वच्छ मोबाइल शौचालय (९० मीटर)"
        }
    };

    // Spoken Audio Synthesis Helper
    function speakText(text) {
        if (!window.WariState.voiceEnabled) return;
        if (!('speechSynthesis' in window)) return;
        try {
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 0.95;
            utterance.pitch = 1.0;
            if (window.WariState.lang === 'mr') utterance.lang = 'mr-IN';
            else if (window.WariState.lang === 'hi') utterance.lang = 'hi-IN';
            else utterance.lang = 'en-IN';
            window.speechSynthesis.speak(utterance);
        } catch (e) {
            console.warn('Voice synthesis error:', e);
        }
    }

    // Toast Notification System
    function showToast(message, type = 'info') {
        const container = document.getElementById('toast-container');
        if (!container) return;
        const toast = document.createElement('div');
        toast.className = `toast-item toast-${type}`;
        toast.innerHTML = `<span class="toast-icon">${type === 'success' ? '✓' : type === 'error' ? '⚠️' : 'ℹ️'}</span> <span>${message}</span>`;
        container.appendChild(toast);
        setTimeout(() => {
            toast.classList.add('toast-fade-out');
            setTimeout(() => toast.remove(), 400);
        }, 3500);
    }

    // Stopwatch Management
    function startStopwatch() {
        clearInterval(window.WariState.stopwatchInterval);
        window.WariState.stopwatchSeconds = 0;
        const timerEl = document.getElementById('em-stopwatch-timer');
        if (timerEl) timerEl.textContent = '00:00';
        window.WariState.stopwatchInterval = setInterval(() => {
            window.WariState.stopwatchSeconds++;
            const mins = String(Math.floor(window.WariState.stopwatchSeconds / 60)).padStart(2, '0');
            const secs = String(window.WariState.stopwatchSeconds % 60).padStart(2, '0');
            if (timerEl) timerEl.textContent = `${mins}:${secs}`;
        }, 1000);
    }

    function stopStopwatch() {
        clearInterval(window.WariState.stopwatchInterval);
    }

    // Navigation Switcher
    function switchView(viewId) {
        document.querySelectorAll('.content-view').forEach(v => v.classList.add('hidden'));
        document.querySelectorAll('.content-view').forEach(v => v.classList.remove('active'));
        const target = document.getElementById(viewId);
        if (target) {
            target.classList.remove('hidden');
            target.classList.add('active');
            window.WariState.currentView = viewId;
        }

        // Update Desktop & Mobile Nav active states
        document.querySelectorAll('.desktop-nav .nav-link-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.view === viewId);
        });
        document.querySelectorAll('.mobile-bottom-nav .mob-nav-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.view === viewId);
        });

        // Invalidate Leaflet maps upon view display
        setTimeout(() => {
            if (viewId === 'emergency-view') {
                initEmergencyMap();
                if (window.WariState.maps.emergency) window.WariState.maps.emergency.invalidateSize();
            } else if (viewId === 'safety-map-view') {
                initSafetyMap();
                if (window.WariState.maps.safety) window.WariState.maps.safety.invalidateSize();
            } else if (viewId === 'responder-view') {
                initResponderMap();
                loadResponderEmergencyFeed();
                if (window.WariState.maps.responder) window.WariState.maps.responder.invalidateSize();
            } else if (viewId === 'volunteer-view') {
                loadVolunteerEmergencyFeed();
            } else if (viewId === 'command-view') {
                initCommandMap();
                loadCommandIncidentsList();
                if (window.WariState.maps.command) window.WariState.maps.command.invalidateSize();
            }
        }, 200);
    }

    // Multilingual Translation Update
    function applyLanguage(lang) {
        window.WariState.lang = lang;
        const dict = i18n[lang] || i18n.en;
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (dict[key]) {
                if (el.tagName === 'INPUT' && el.type === 'button') {
                    el.value = dict[key];
                } else {
                    el.textContent = dict[key];
                }
            }
        });
        const langDropdown = document.getElementById('lang-select');
        if (langDropdown) langDropdown.value = lang;
    }

    // Set Timeline Step
    function setTimelineStep(stepNumber, active = true, completed = false) {
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
    }

    // Synchronize Emergency Details Across All Screens
    function syncEmergencyUI(emId) {
        const em = emId || 'EM-28471';
        window.WariState.currentEmergencyId = em;

        // Emergency Page
        const idDisplays = ['em-id-display', 'vol-response-em-id', 'resp-active-em-id', 'cmd-ins-id', 'modal-active-wari-id'];
        idDisplays.forEach(id => {
            const el = document.getElementById(id);
            if (el) el.textContent = em;
        });

        // Header Badges
        const headerBadge = document.getElementById('header-em-badge');
        if (headerBadge) headerBadge.classList.remove('hidden');

        // Home View Banner
        const homeBanner = document.getElementById('home-active-emergency-banner');
        if (homeBanner) homeBanner.classList.remove('hidden');

        // Volunteer Box
        const volBox = document.getElementById('volunteer-active-response-box');
        if (volBox) volBox.classList.remove('hidden');

        // Responder Box
        const respBox = document.getElementById('responder-active-box');
        if (respBox) respBox.classList.remove('hidden');

        // Command Center Count & List
        const cmdTotal = document.getElementById('command-total-count');
        const cmdCount = document.getElementById('cmd-incident-count');
        if (cmdTotal) cmdTotal.textContent = 'TOTAL: 1 INCIDENTS';
        if (cmdCount) cmdCount.textContent = '1';

        loadCommandIncidentsList();
    }

    // Update Simulated Volunteer Location & Distance
    function updateVolunteerDistance(distM, etaMin, statusText, statusState) {
        const ripDist = document.getElementById('rip-dist-val');
        const ripEta = document.getElementById('rip-eta-val');
        const ripStatus = document.getElementById('rip-status-text');
        const ripPill = document.getElementById('rip-status-pill');
        const volDist = document.getElementById('vol-distance-val');
        const step5Dist = document.getElementById('step-5-dist-tag');
        const step5Eta = document.getElementById('step-5-eta-tag');

        if (ripDist) ripDist.textContent = `${distM}m`;
        if (ripEta) ripEta.textContent = `${etaMin} min`;
        if (ripStatus) ripStatus.textContent = statusText;
        if (ripPill) {
            ripPill.textContent = statusState;
            ripPill.className = `rip-status-pill ${statusState === '🟢 WITH PATIENT' ? 'with-patient' : ''}`;
        }
        if (volDist) volDist.textContent = `${distM}m`;
        if (step5Dist) step5Dist.textContent = `${distM}m`;
        if (step5Eta) step5Eta.textContent = `${etaMin} min`;

        // Update leaflet volunteer marker position if exists
        if (window.WariState.markers.emergency && window.WariState.markers.emergency.volunteer) {
            const frac = Math.max(0, Math.min(1, 1 - (distM / 320)));
            const newLat = 18.3470 - ((18.3470 - 18.3444) * frac);
            const newLon = 74.0330 - ((74.0330 - 74.0305) * frac);
            window.WariState.markers.emergency.volunteer.setLatLng([newLat, newLon]);
        }
    }

    // Run Smooth 25-28 Second Live Emergency Response Simulation
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
    }

    function clearSimulationTimers() {
        window.WariState.simulationTimers.forEach(t => clearTimeout(t));
        window.WariState.simulationTimers = [];
        window.WariState.isSimulationRunning = false;
    }

    // Reset Demo State
    function resetDemo() {
        clearSimulationTimers();
        stopStopwatch();
        window.WariState.currentEmergencyId = null;
        window.WariState.emergencyStatus = null;

        fetch('/api/demo/reset', { method: 'POST' })
            .catch(() => {});

        // Reset UI Elements
        const timerEl = document.getElementById('em-stopwatch-timer');
        if (timerEl) timerEl.textContent = '00:00';

        const headerBadge = document.getElementById('header-em-badge');
        if (headerBadge) headerBadge.classList.add('hidden');

        const homeBanner = document.getElementById('home-active-emergency-banner');
        if (homeBanner) homeBanner.classList.add('hidden');

        const reachBanner = document.getElementById('reached-confirmed-banner');
        if (reachBanner) reachBanner.classList.add('hidden');

        const hospBanner = document.getElementById('hospital-selected-banner');
        if (hospBanner) hospBanner.classList.add('hidden');

        const respArrived = document.getElementById('resp-arrived-banner');
        if (respArrived) respArrived.classList.add('hidden');

        // Reset Timeline
        for (let i = 1; i <= 9; i++) {
            setTimelineStep(i, false, false);
        }
        setTimelineStep(1, false, false);

        // Reset Status Banner
        const statusTitle = document.getElementById('em-current-status-title');
        if (statusTitle) statusTitle.textContent = '🟡 VOLUNTEER RESPONDING';

        // Reset Volunteer metrics
        updateVolunteerDistance(320, 2, '🟡 Responding', '🟡 RESPONDING');

        // Reset Command Center
        const cmdTotal = document.getElementById('command-total-count');
        const cmdCount = document.getElementById('cmd-incident-count');
        if (cmdTotal) cmdTotal.textContent = 'TOTAL: 0 INCIDENTS';
        if (cmdCount) cmdCount.textContent = '0';

        const cmdList = document.getElementById('command-emergency-list');
        if (cmdList) {
            cmdList.innerHTML = '<p class="empty-feed-text">No active emergencies in registry.</p>';
        }

        const volFeed = document.getElementById('volunteer-emergency-feed');
        if (volFeed) {
            volFeed.innerHTML = '<p class="empty-feed-text">No active emergency alerts in your radius.</p>';
        }

        const respFeed = document.getElementById('responder-emergency-feed');
        if (respFeed) {
            respFeed.innerHTML = '<p class="empty-feed-text">No incoming medical emergencies.</p>';
        }

        showToast("🔄 Demo System Reset to Initial Clean State", "info");
        switchView('home-view');
    }

    // Leaflet Emergency Map Initialization
    function initEmergencyMap() {
        const container = document.getElementById('emergency-live-map');
        if (!container) return;
        if (window.WariState.maps.emergency) {
            window.WariState.maps.emergency.invalidateSize();
            return;
        }

        const map = L.map('emergency-live-map').setView([18.3444, 74.0305], 16);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        // Custom Leaflet Icons
        const patientIcon = L.divIcon({
            className: 'custom-map-icon patient-icon',
            html: '<div style="background:#D32F2F; color:#fff; border-radius:50%; width:32px; height:32px; display:flex; align-items:center; justify-content:center; border:2px solid #fff; box-shadow:0 0 10px rgba(211,47,47,0.8); font-size:16px;">📍</div>',
            iconSize: [32, 32],
            iconAnchor: [16, 16]
        });

        const volunteerIcon = L.divIcon({
            className: 'custom-map-icon volunteer-icon',
            html: '<div style="background:#0288D1; color:#fff; border-radius:50%; width:32px; height:32px; display:flex; align-items:center; justify-content:center; border:2px solid #fff; box-shadow:0 0 10px rgba(2,136,209,0.8); font-size:16px;">🔵</div>',
            iconSize: [32, 32],
            iconAnchor: [16, 16]
        });

        const responderIcon = L.divIcon({
            className: 'custom-map-icon responder-icon',
            html: '<div style="background:#00897B; color:#fff; border-radius:50%; width:32px; height:32px; display:flex; align-items:center; justify-content:center; border:2px solid #fff; box-shadow:0 0 10px rgba(0,137,123,0.8); font-size:16px;">🚑</div>',
            iconSize: [32, 32],
            iconAnchor: [16, 16]
        });

        // Add Markers
        const patientMarker = L.marker([18.3444, 74.0305], { icon: patientIcon }).addTo(map)
            .bindPopup('<b>📍 Patient: Tukaram Shinde</b><br>Zone 04 — Saswad Palkhi Maidan');

        const volunteerMarker = L.marker([18.3470, 74.0330], { icon: volunteerIcon }).addTo(map)
            .bindPopup('<b>🔵 Volunteer: Ramesh Kulkarni (V-001)</b><br>En Route • 320m');

        const responderMarker = L.marker([18.3390, 74.0260], { icon: responderIcon }).addTo(map)
            .bindPopup('<b>🚑 Medical Responder: Dr. Arvind Shinde</b><br>Mobile Ambulance Unit 1');

        // Add Safe Bypass Corridor Polyline (Green)
        const bypassLine = L.polyline([
            [18.3470, 74.0330],
            [18.3458, 74.0322],
            [18.3444, 74.0305]
        ], {
            color: '#00E676',
            weight: 5,
            opacity: 0.85,
            dashArray: '8, 8'
        }).addTo(map);

        window.WariState.maps.emergency = map;
        window.WariState.markers.emergency = {
            patient: patientMarker,
            volunteer: volunteerMarker,
            responder: responderMarker,
            bypass: bypassLine
        };

        // Camera Button Handlers
        document.getElementById('em-cam-patient')?.addEventListener('click', () => {
            map.flyTo([18.3444, 74.0305], 17);
        });
        document.getElementById('em-cam-volunteer')?.addEventListener('click', () => {
            map.flyTo(volunteerMarker.getLatLng(), 17);
        });
        document.getElementById('em-cam-responder')?.addEventListener('click', () => {
            map.flyTo([18.3390, 74.0260], 17);
        });
        document.getElementById('em-cam-fit-all')?.addEventListener('click', () => {
            map.fitBounds([
                [18.3444, 74.0305],
                [18.3470, 74.0330],
                [18.3390, 74.0260]
            ], { padding: [40, 40] });
        });
    }

    // Leaflet Safety Map Initialization
    function initSafetyMap() {
        const container = document.getElementById('main-safety-map');
        if (!container) return;
        if (window.WariState.maps.safety) {
            window.WariState.maps.safety.invalidateSize();
            return;
        }

        const map = L.map('main-safety-map').setView([18.3444, 74.0305], 15);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        window.WariState.maps.safety = map;
        loadSafetyMapMarkers('ALL');
    }

    function loadSafetyMapMarkers(category = 'ALL') {
        const map = window.WariState.maps.safety;
        if (!map) return;

        // Clear existing markers
        window.WariState.markers.safety.forEach(m => map.removeLayer(m));
        window.WariState.markers.safety = [];

        fetch(`/api/safety-services?category=${category}&lat=18.3444&lon=74.0305`)
            .then(res => res.json())
            .then(data => {
                if (!data.success || !data.services) return;
                data.services.forEach(svc => {
                    const iconEmoji = svc.category === 'WATER' ? '💧' :
                                      svc.category === 'TOILET' ? '🚻' :
                                      svc.category === 'MEDICAL_CAMP' ? '🏥' :
                                      svc.category === 'REST_AREA' ? '🛏️' :
                                      svc.category === 'FOOD' ? '🍛' : '🚑';

                    const markerIcon = L.divIcon({
                        className: 'service-pin-icon',
                        html: `<div style="background:#1E2638; color:#fff; border-radius:50%; width:28px; height:28px; display:flex; align-items:center; justify-content:center; border:2px solid #00BCD4; font-size:14px;">${iconEmoji}</div>`,
                        iconSize: [28, 28],
                        iconAnchor: [14, 14]
                    });

                    const marker = L.marker([svc.latitude, svc.longitude], { icon: markerIcon }).addTo(map);
                    marker.on('click', () => {
                        showSidebarDetail(svc);
                    });
                    window.WariState.markers.safety.push(marker);
                });
            })
            .catch(() => {});
    }

    function showSidebarDetail(svc) {
        const emptyState = document.getElementById('sidebar-empty-state');
        const detailCard = document.getElementById('sidebar-detail-card');
        if (emptyState) emptyState.classList.add('hidden');
        if (detailCard) detailCard.classList.remove('hidden');

        const catBadge = document.getElementById('sb-category-badge');
        const distBadge = document.getElementById('sb-dist-badge');
        const nameEl = document.getElementById('sb-name');
        const zoneEl = document.getElementById('sb-zone');
        const addrEl = document.getElementById('sb-address');
        const noteEl = document.getElementById('sb-note');

        if (catBadge) catBadge.textContent = `${svc.category}`;
        if (distBadge) distBadge.textContent = svc.distance_text || `${svc.distance_m || 250}m away`;
        if (nameEl) nameEl.textContent = svc.name;
        if (zoneEl) zoneEl.textContent = `📍 ${svc.zone}`;
        if (addrEl) addrEl.textContent = svc.address;
        if (noteEl) noteEl.textContent = `ℹ️ ${svc.special_note || 'Available 24/7 during Palkhi procession.'}`;

        const actBtn = document.getElementById('sb-action-btn');
        if (actBtn) {
            actBtn.onclick = () => {
                if (window.WariState.maps.safety) {
                    window.WariState.maps.safety.flyTo([svc.latitude, svc.longitude], 17);
                }
            };
        }
    }

    // Tactical Map for Medical Responder
    function initResponderMap() {
        const container = document.getElementById('responder-map');
        if (!container) return;
        if (window.WariState.maps.responder) {
            window.WariState.maps.responder.invalidateSize();
            return;
        }

        const map = L.map('responder-map').setView([18.3444, 74.0305], 15);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        // Safe Bypass Polyline (Green)
        L.polyline([
            [18.3390, 74.0260],
            [18.3415, 74.0275],
            [18.3444, 74.0305]
        ], { color: '#00E676', weight: 6, opacity: 0.9 }).addTo(map)
        .bindPopup('<b>🟢 Safe Bypass Corridor (3 min)</b><br>Low crowd congestion');

        // Congested Direct Line (Red Dashed)
        L.polyline([
            [18.3390, 74.0260],
            [18.3430, 74.0290],
            [18.3444, 74.0305]
        ], { color: '#FF5252', weight: 4, opacity: 0.6, dashArray: '6, 6' }).addTo(map)
        .bindPopup('<b>🔴 Direct Procession Route (10 min)</b><br>High bottleneck delay');

        window.WariState.maps.responder = map;
    }

    // Command Center Map
    function initCommandMap() {
        const container = document.getElementById('command-map');
        if (!container) return;
        if (window.WariState.maps.command) {
            window.WariState.maps.command.invalidateSize();
            return;
        }

        const map = L.map('command-map').setView([18.3444, 74.0305], 15);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        const patientMarker = L.marker([18.3444, 74.0305]).addTo(map)
            .bindPopup('<b>🔴 Incident EM-28471</b><br>Tukaram Shinde (URGENT)');

        const volMarker = L.marker([18.3470, 74.0330]).addTo(map)
            .bindPopup('<b>🔵 Volunteer V-001</b><br>Ramesh Kulkarni');

        const respMarker = L.marker([18.3390, 74.0260]).addTo(map)
            .bindPopup('<b>🚑 Responder MR-001</b><br>Ambulance 1');

        window.WariState.maps.command = map;
        window.WariState.markers.command = {
            patient: patientMarker,
            volunteer: volMarker,
            responder: respMarker
        };

        // Command Map Camera Controls
        document.getElementById('cmd-cam-patient')?.addEventListener('click', () => {
            map.flyTo([18.3444, 74.0305], 17);
        });
        document.getElementById('cmd-cam-vol')?.addEventListener('click', () => {
            map.flyTo([18.3470, 74.0330], 17);
        });
        document.getElementById('cmd-cam-resp')?.addEventListener('click', () => {
            map.flyTo([18.3390, 74.0260], 17);
        });
    }

    // Load Services Cards on Services View
    function loadServicesCards(category = 'WATER') {
        const container = document.getElementById('services-cards-list');
        if (!container) return;

        fetch(`/api/safety-services?category=${category}&lat=18.3444&lon=74.0305`)
            .then(res => res.json())
            .then(data => {
                if (!data.success || !data.services || data.services.length === 0) {
                    container.innerHTML = '<p class="empty-feed-text">No facilities found for this category.</p>';
                    return;
                }
                const countBadge = document.getElementById('services-count-badge');
                if (countBadge) countBadge.textContent = `${data.services.length} facilities`;

                container.innerHTML = data.services.map(s => `
                    <div class="service-detail-card">
                        <div class="sdc-top">
                            <span class="sdc-cat-badge">${s.category}</span>
                            <span class="sdc-dist-badge">${s.distance_text || '250m away'}</span>
                        </div>
                        <h4 class="sdc-name">${s.name}</h4>
                        <div class="sdc-zone">📍 ${s.zone}</div>
                        <div class="sdc-address">${s.address}</div>
                        <div class="sdc-note">ℹ️ ${s.special_note || 'Available 24/7 for Warkaris.'}</div>
                    </div>
                `).join('');
            })
            .catch(() => {
                container.innerHTML = '<p class="empty-feed-text">Error loading service facilities.</p>';
            });
    }

    // Load Command Center Active Incidents
    function loadCommandIncidentsList() {
        const container = document.getElementById('command-emergency-list');
        if (!container) return;

        fetch('/api/command-center/emergencies')
            .then(res => res.json())
            .then(data => {
                if (!data.success || !data.emergencies || data.emergencies.length === 0) {
                    container.innerHTML = '<p class="empty-feed-text">No active emergencies in registry.</p>';
                    return;
                }
                container.innerHTML = data.emergencies.map(e => `
                    <div class="cmd-incident-card active" data-em-id="${e.emergency_id}">
                        <div class="cic-head">
                            <span class="cic-id">${e.emergency_id}</span>
                            <span class="cic-priority">${e.priority || 'URGENT'}</span>
                        </div>
                        <div class="cic-patient">${e.reported_by} (${e.wari_id})</div>
                        <div class="cic-zone">${e.wari_zone}</div>
                        <div class="cic-status">Status: <strong>${e.status}</strong></div>
                    </div>
                `).join('');
            })
            .catch(() => {
                container.innerHTML = '<p class="empty-feed-text">Error fetching incident registry.</p>';
            });
    }

    // Load Volunteer Emergency Feed
    function loadVolunteerEmergencyFeed() {
        const container = document.getElementById('volunteer-emergency-feed');
        if (!container) return;

        fetch('/api/volunteer/dashboard-data')
            .then(res => res.json())
            .then(data => {
                if (!data.success || !data.emergencies || data.emergencies.length === 0) {
                    container.innerHTML = '<p class="empty-feed-text">No active emergency alerts in your radius.</p>';
                    return;
                }
                container.innerHTML = data.emergencies.map(e => `
                    <div class="emergency-feed-card">
                        <div class="efc-top">
                            <span class="efc-id">${e.emergency_id}</span>
                            <span class="efc-priority">${e.priority || 'URGENT'}</span>
                        </div>
                        <div class="efc-name">Patient: <strong>${e.reported_by}</strong></div>
                        <div class="efc-zone">📍 ${e.wari_zone}</div>
                        <div class="efc-time">Status: <strong>${e.status}</strong></div>
                    </div>
                `).join('');
            })
            .catch(() => {
                container.innerHTML = '<p class="empty-feed-text">Error loading volunteer feed.</p>';
            });
    }

    // Load Responder Emergency Feed
    function loadResponderEmergencyFeed() {
        const container = document.getElementById('responder-emergency-feed');
        if (!container) return;

        fetch('/api/responder/dashboard-data')
            .then(res => res.json())
            .then(data => {
                if (!data.success || !data.emergencies || data.emergencies.length === 0) {
                    container.innerHTML = '<p class="empty-feed-text">No incoming medical emergencies.</p>';
                    return;
                }
                container.innerHTML = data.emergencies.map(e => `
                    <div class="emergency-feed-card">
                        <div class="efc-top">
                            <span class="efc-id">${e.emergency_id}</span>
                            <span class="efc-priority">${e.priority || 'URGENT'}</span>
                        </div>
                        <div class="efc-name">Patient: <strong>${e.reported_by}</strong></div>
                        <div class="efc-zone">📍 ${e.wari_zone}</div>
                        <div class="efc-time">Status: <strong>${e.status}</strong></div>
                    </div>
                `).join('');
            })
            .catch(() => {
                container.innerHTML = '<p class="empty-feed-text">Error loading responder feed.</p>';
            });
    }

    // Load Companion Group Members
    function loadGroupMembers() {
        const container = document.getElementById('group-members-list');
        if (!container) return;

        fetch(`/api/group/members?wari_id=${window.WariState.currentWariId}`)
            .then(res => res.json())
            .then(data => {
                if (!data.success || !data.members || data.members.length === 0) {
                    container.innerHTML = '<p class="empty-feed-text">No companion members linked yet.</p>';
                    return;
                }
                container.innerHTML = data.members.map(m => `
                    <div class="group-member-item">
                        <div class="gm-info">
                            <strong class="gm-name">${m.name}</strong>
                            <span class="gm-phone">📞 ${m.phone}</span>
                        </div>
                        <span class="gm-role">${m.relation || 'Companion'}</span>
                    </div>
                `).join('');
            })
            .catch(() => {
                container.innerHTML = '<p class="empty-feed-text">Error loading group members.</p>';
            });
    }

    // Load Nearby Hospitals for Modal
    function loadNearbyHospitals() {
        const list = document.getElementById('nearby-hospitals-list');
        if (!list) return;

        const emId = window.WariState.currentEmergencyId || 'EM-28471';
        fetch(`/api/emergency/${emId}/nearby-hospitals`)
            .then(res => res.json())
            .then(data => {
                if (!data.success || !data.hospitals) return;
                list.innerHTML = data.hospitals.map(h => `
                    <div class="hospital-list-item">
                        <div class="hli-info">
                            <strong>${h.name}</strong>
                            <div class="hli-meta">${h.distance_km} km • ETA ${h.eta_min} min • ${h.capabilities.join(', ')}</div>
                        </div>
                        <button type="button" class="select-hosp-btn" data-hosp-id="${h.hospital_id}" data-hosp-name="${h.name}">
                            SELECT
                        </button>
                    </div>
                `).join('');

                // Attach hospital selection listeners
                list.querySelectorAll('.select-hosp-btn').forEach(btn => {
                    btn.addEventListener('click', (e) => {
                        const hId = e.target.dataset.hospId;
                        const hName = e.target.dataset.hospName;
                        selectHospital(emId, hId, hName);
                    });
                });
            })
            .catch(() => {
                list.innerHTML = '<p class="empty-feed-text">Error fetching nearby hospitals.</p>';
            });
    }

    function selectHospital(emId, hospId, hospName) {
        fetch(`/api/emergency/${emId}/hospital/select`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ hospital_id: hospId })
        })
        .then(res => res.json())
        .then(data => {
            showToast(`🏥 Selected: ${hospName}`, 'success');
            document.getElementById('hospital-selection-card')?.classList.add('hidden');
            const confBanner = document.getElementById('hospital-selected-banner');
            if (confBanner) {
                confBanner.classList.remove('hidden');
                const hospNameEl = document.getElementById('selected-hospital-name');
                if (hospNameEl) hospNameEl.textContent = hospName;
            }
        })
        .catch(() => {
            showToast('Hospital selected in prototype mode.', 'info');
        });
    }

    // DOM Ready Event Initialization
    document.addEventListener('DOMContentLoaded', () => {
        
        // 1. Navigation Button Listeners (Desktop & Mobile)
        document.querySelectorAll('.desktop-nav .nav-link-btn, .mobile-bottom-nav .mob-nav-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const targetView = btn.dataset.view;
                if (targetView) switchView(targetView);
            });
        });

        // Direct Nav ID Listeners for Extra Reliability
        document.getElementById('nav-home')?.addEventListener('click', () => switchView('home-view'));
        document.getElementById('nav-emergency')?.addEventListener('click', () => switchView('emergency-view'));
        document.getElementById('nav-safety-map')?.addEventListener('click', () => switchView('safety-map-view'));
        document.getElementById('nav-services')?.addEventListener('click', () => switchView('services-view'));
        document.getElementById('nav-volunteer')?.addEventListener('click', () => switchView('volunteer-view'));
        document.getElementById('nav-responder')?.addEventListener('click', () => switchView('responder-view'));
        document.getElementById('nav-command')?.addEventListener('click', () => switchView('command-view'));

        document.getElementById('mob-nav-home')?.addEventListener('click', () => switchView('home-view'));
        document.getElementById('mob-nav-map')?.addEventListener('click', () => switchView('safety-map-view'));
        document.getElementById('mob-nav-sos')?.addEventListener('click', () => switchView('emergency-view'));
        document.getElementById('mob-nav-services')?.addEventListener('click', () => switchView('services-view'));
        document.getElementById('mob-nav-command')?.addEventListener('click', () => switchView('command-view'));

        // Refresh Feed Button Handlers
        document.getElementById('refresh-volunteer-btn')?.addEventListener('click', () => {
            loadVolunteerEmergencyFeed();
            showToast("Volunteer feed refreshed", "info");
        });
        document.getElementById('refresh-responder-btn')?.addEventListener('click', () => {
            loadResponderEmergencyFeed();
            showToast("Responder feed refreshed", "info");
        });
        document.getElementById('refresh-command-btn')?.addEventListener('click', () => {
            loadCommandIncidentsList();
            showToast("Command incidents refreshed", "info");
        });

        // Brand click -> Home
        document.getElementById('nav-brand-home')?.addEventListener('click', () => {
            switchView('home-view');
        });

        // 2. Language Selector
        const langDropdown = document.getElementById('lang-select');
        if (langDropdown) {
            langDropdown.addEventListener('change', (e) => {
                applyLanguage(e.target.value);
            });
        }

        // 3. Voice Toggle
        const voiceBtn = document.getElementById('voice-toggle-btn');
        if (voiceBtn) {
            voiceBtn.addEventListener('click', () => {
                window.WariState.voiceEnabled = !window.WariState.voiceEnabled;
                voiceBtn.textContent = window.WariState.voiceEnabled ? '🔊 Voice: ON' : '🔇 Voice: OFF';
                showToast(`Voice assistance ${window.WariState.voiceEnabled ? 'Enabled' : 'Muted'}`, 'info');
            });
        }

        // 4. Elder Mode Toggle
        const elderToggle = document.getElementById('elder-mode-toggle');
        const elderContainer = document.getElementById('elder-mode-container');
        const exitElder = document.getElementById('exit-elder-mode-btn');

        if (elderToggle && elderContainer) {
            elderToggle.addEventListener('click', () => {
                window.WariState.elderMode = true;
                elderContainer.classList.remove('hidden');
                speakText("ज्येष्ठ नागरिक सुरक्षा मोड सुरू केला आहे. मदतीसाठी लाल बटण दाबा.");
            });
        }
        if (exitElder && elderContainer) {
            exitElder.addEventListener('click', () => {
                window.WariState.elderMode = false;
                elderContainer.classList.add('hidden');
            });
        }

        // Elder Action Buttons
        document.getElementById('elder-sos-action-btn')?.addEventListener('click', () => {
            elderContainer.classList.add('hidden');
            runFullSimulation();
        });
        document.getElementById('elder-where-am-i-btn')?.addEventListener('click', () => {
            speakText("आपण सासवड पालखी मैदान, झोन चार मध्ये आहात. जवळचे आरोग्य केंद्र १८० मीटर अंतरावर आहे.");
            showToast("📍 आपण सासवड पालखी मैदान, झोन ०४ मध्ये आहात.", "info");
        });
        document.getElementById('elder-medical-btn')?.addEventListener('click', () => {
            elderContainer.classList.add('hidden');
            switchView('services-view');
            loadServicesCards('MEDICAL_CAMP');
        });
        document.getElementById('elder-water-btn')?.addEventListener('click', () => {
            elderContainer.classList.add('hidden');
            switchView('services-view');
            loadServicesCards('WATER');
        });
        document.getElementById('elder-toilet-btn')?.addEventListener('click', () => {
            elderContainer.classList.add('hidden');
            switchView('services-view');
            loadServicesCards('TOILET');
        });

        // Elder Language Switchers
        document.querySelectorAll('.elder-lang-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                applyLanguage(btn.dataset.lang);
            });
        });

        // 5. Main SOS Button & Confirmation Modal
        const mainSosBtn = document.getElementById('main-sos-button');
        const sosModal = document.getElementById('sos-modal');
        const cancelSosBtn = document.getElementById('cancel-sos-btn');
        const confirmSosBtn = document.getElementById('confirm-sos-btn');

        if (mainSosBtn && sosModal) {
            mainSosBtn.addEventListener('click', () => {
                sosModal.classList.remove('hidden');
            });
        }
        if (cancelSosBtn && sosModal) {
            cancelSosBtn.addEventListener('click', () => {
                sosModal.classList.add('hidden');
            });
        }
        if (confirmSosBtn && sosModal) {
            confirmSosBtn.addEventListener('click', () => {
                sosModal.classList.add('hidden');
                runFullSimulation();
            });
        }

        // 6. Demo Mode Toolbar Actions
        document.getElementById('run-simulation-demo-btn')?.addEventListener('click', () => {
            runFullSimulation();
        });
        document.getElementById('create-demo-em-btn')?.addEventListener('click', () => {
            runFullSimulation();
        });
        document.getElementById('reset-demo-btn')?.addEventListener('click', () => {
            resetDemo();
        });

        // 7. Simulation Quick Bar on Emergency Page
        document.getElementById('em-simulate-btn')?.addEventListener('click', () => {
            runFullSimulation();
        });

        // 8. Secondary Quick Actions on Home View
        document.getElementById('home-where-am-i-btn')?.addEventListener('click', () => {
            const modal = document.getElementById('where-modal');
            if (modal) modal.classList.remove('hidden');
            speakText("You are at Saswad Central Palkhi Maidan Ground, Zone 04.");
        });
        document.getElementById('close-where-modal-btn')?.addEventListener('click', () => {
            document.getElementById('where-modal')?.classList.add('hidden');
        });

        document.getElementById('home-find-medical-btn')?.addEventListener('click', () => {
            switchView('services-view');
            loadServicesCards('MEDICAL_CAMP');
        });

        document.getElementById('home-open-safety-map-btn')?.addEventListener('click', () => {
            switchView('safety-map-view');
            initSafetyMap();
        });

        document.getElementById('home-group-btn')?.addEventListener('click', () => {
            const modal = document.getElementById('group-modal');
            if (modal) {
                modal.classList.remove('hidden');
                loadGroupMembers();
            }
        });
        document.getElementById('close-group-modal-btn')?.addEventListener('click', () => {
            document.getElementById('group-modal')?.classList.add('hidden');
        });

        // Add Group Member Form Handler
        const addGroupForm = document.getElementById('add-group-member-form');
        if (addGroupForm) {
            addGroupForm.addEventListener('submit', (e) => {
                e.preventDefault();
                const name = document.getElementById('new-member-name').value.trim();
                const phone = document.getElementById('new-member-phone').value.trim();

                fetch('/api/group/add-member', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        wari_id: window.WariState.currentWariId,
                        member_name: name,
                        member_phone: phone,
                        relation: 'Companion'
                    })
                })
                .then(res => res.json())
                .then(data => {
                    showToast(`Companion ${name} added to your safety group!`, 'success');
                    addGroupForm.reset();
                    loadGroupMembers();
                })
                .catch(() => {
                    showToast('Companion added in prototype mode.', 'info');
                });
            });
        }

        document.getElementById('home-jump-to-emergency-btn')?.addEventListener('click', () => {
            switchView('emergency-view');
            initEmergencyMap();
        });

        document.getElementById('home-see-all-services-btn')?.addEventListener('click', () => {
            switchView('services-view');
            loadServicesCards('WATER');
        });

        // Home Service Tiles Click
        document.querySelectorAll('.service-tile-home').forEach(tile => {
            tile.addEventListener('click', () => {
                const type = tile.dataset.serviceType;
                switchView('services-view');
                loadServicesCards(type);
            });
        });

        // 9. Safety ID Form Submission
        const safetyForm = document.getElementById('safety-id-form');
        if (safetyForm) {
            safetyForm.addEventListener('submit', (e) => {
                e.preventDefault();
                const name = document.getElementById('user-name').value.trim();
                const phone = document.getElementById('user-phone').value.trim();

                fetch('/safety-id/create', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, phone })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        window.WariState.currentWariId = data.wari_id;
                        window.WariState.currentUserName = data.name;
                        document.getElementById('display-user-name').textContent = data.name;
                        document.getElementById('display-wari-id').textContent = data.wari_id;
                        document.getElementById('qr-id-caption').textContent = data.wari_id;
                        document.getElementById('header-wari-id').textContent = data.wari_id;
                        document.getElementById('modal-active-wari-id').textContent = data.wari_id;

                        safetyForm.classList.add('hidden');
                        document.getElementById('safety-id-result').classList.remove('hidden');
                        showToast(`Safety ID ${data.wari_id} Active!`, 'success');
                    } else {
                        const err = document.getElementById('form-error');
                        if (err) {
                            err.textContent = data.error || 'Failed to create Safety ID.';
                            err.classList.remove('hidden');
                        }
                    }
                })
                .catch(() => {
                    showToast('Safety ID registered in offline demo mode.', 'info');
                });
            });
        }

        document.getElementById('create-another-btn')?.addEventListener('click', () => {
            document.getElementById('safety-id-result')?.classList.add('hidden');
            safetyForm?.classList.remove('hidden');
        });

        // 10. Safety Map Filter Pills
        document.querySelectorAll('#map-filter-group .filter-pill').forEach(pill => {
            pill.addEventListener('click', () => {
                document.querySelectorAll('#map-filter-group .filter-pill').forEach(p => p.classList.remove('active'));
                pill.classList.add('active');
                loadSafetyMapMarkers(pill.dataset.filter);
            });
        });

        // 11. Services Page Category Tiles
        document.querySelectorAll('.category-tiles-carousel .cat-tile-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.category-tiles-carousel .cat-tile-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                loadServicesCards(btn.dataset.category);
            });
        });

        // Services Zone Dropdown
        document.getElementById('services-zone-dropdown')?.addEventListener('change', () => {
            const activeCat = document.querySelector('.category-tiles-carousel .cat-tile-btn.active')?.dataset.category || 'WATER';
            loadServicesCards(activeCat);
        });

        // 12. Volunteer Page Actions
        document.getElementById('vol-accept-em-btn')?.addEventListener('click', () => {
            const emId = window.WariState.currentEmergencyId || 'EM-28471';
            fetch(`/api/emergency/${emId}/volunteer/accept`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ volunteer_id: 'V-001' })
            })
            .then(res => res.json())
            .then(data => {
                showToast("Volunteer Ramesh Kulkarni Accepted Dispatch!", "success");
                setTimelineStep(5, true, false);
            })
            .catch(() => {
                showToast("Volunteer accepted dispatch in prototype mode.", "info");
            });
        });

        document.getElementById('reached-patient-btn')?.addEventListener('click', () => {
            const emId = window.WariState.currentEmergencyId || 'EM-28471';
            fetch('/api/volunteer/reached', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ emergency_id: emId, volunteer_id: 'V-001' })
            })
            .then(res => res.json())
            .then(data => {
                updateVolunteerDistance(0, 0, '🟢 With Patient', '🟢 WITH PATIENT');
                setTimelineStep(6, true, false);
                document.getElementById('reached-confirmed-banner')?.classList.remove('hidden');
                showToast("Volunteer reached patient (0m)", "success");
            })
            .catch(() => {
                updateVolunteerDistance(0, 0, '🟢 With Patient', '🟢 WITH PATIENT');
                document.getElementById('reached-confirmed-banner')?.classList.remove('hidden');
            });
        });

        // 13. Responder Page Actions
        document.getElementById('escalate-hospital-btn')?.addEventListener('click', () => {
            const picker = document.getElementById('hospital-selection-card');
            if (picker) {
                picker.classList.toggle('hidden');
                if (!picker.classList.contains('hidden')) {
                    loadNearbyHospitals();
                }
            }
        });

        document.getElementById('hec-view-btn')?.addEventListener('click', () => {
            switchView('responder-view');
            initResponderMap();
            document.getElementById('hospital-selection-card')?.classList.remove('hidden');
            loadNearbyHospitals();
        });

        document.getElementById('cmd-escalate-quick-btn')?.addEventListener('click', () => {
            switchView('responder-view');
            initResponderMap();
            document.getElementById('hospital-selection-card')?.classList.remove('hidden');
            loadNearbyHospitals();
        });

        document.getElementById('resp-start-response-btn')?.addEventListener('click', () => {
            const emId = window.WariState.currentEmergencyId || 'EM-28471';
            fetch(`/api/emergency/${emId}/responder/status`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ responder_id: 'MR-001', status: 'EN_ROUTE' })
            })
            .then(() => {
                showToast("Medical Responder Ambulance EN ROUTE", "success");
                setTimelineStep(7, true, false);
            })
            .catch(() => {
                showToast("Responder en route in prototype mode.", "info");
            });
        });

        document.getElementById('resp-mark-arrived-btn')?.addEventListener('click', () => {
            const emId = window.WariState.currentEmergencyId || 'EM-28471';
            fetch(`/api/emergency/${emId}/responder/status`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ responder_id: 'MR-001', status: 'ARRIVED' })
            })
            .then(() => {
                document.getElementById('resp-arrived-banner')?.classList.remove('hidden');
                showToast("Medical Responder Arrived On Scene", "success");
            })
            .catch(() => {
                document.getElementById('resp-arrived-banner')?.classList.remove('hidden');
            });
        });

        // 14. Command Center Sub-Tabs
        document.getElementById('cmd-tab-operations')?.addEventListener('click', () => {
            document.querySelectorAll('.cmd-tab-btn').forEach(b => b.classList.remove('active'));
            document.getElementById('cmd-tab-operations').classList.add('active');
            document.getElementById('cmd-operations-subview').classList.remove('hidden');
            document.getElementById('cmd-heatmap-subview').classList.add('hidden');
            document.getElementById('cmd-readiness-subview').classList.add('hidden');
            initCommandMap();
        });

        document.getElementById('cmd-tab-heatmap')?.addEventListener('click', () => {
            document.querySelectorAll('.cmd-tab-btn').forEach(b => b.classList.remove('active'));
            document.getElementById('cmd-tab-heatmap').classList.add('active');
            document.getElementById('cmd-operations-subview').classList.add('hidden');
            document.getElementById('cmd-heatmap-subview').classList.remove('hidden');
            document.getElementById('cmd-readiness-subview').classList.add('hidden');
            loadCommandHeatmap();
        });

        document.getElementById('cmd-tab-readiness')?.addEventListener('click', () => {
            document.querySelectorAll('.cmd-tab-btn').forEach(b => b.classList.remove('active'));
            document.getElementById('cmd-tab-readiness').classList.add('active');
            document.getElementById('cmd-operations-subview').classList.add('hidden');
            document.getElementById('cmd-heatmap-subview').classList.add('hidden');
            document.getElementById('cmd-readiness-subview').classList.remove('hidden');
            loadCommandReadiness();
        });

        document.getElementById('cmd-resolve-current-btn')?.addEventListener('click', () => {
            const emId = window.WariState.currentEmergencyId || 'EM-28471';
            fetch(`/api/emergency/${emId}/resolve`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ emergency_id: emId })
            })
            .then(() => {
                showToast("Incident Resolved & Archived", "success");
                resetDemo();
            })
            .catch(() => {
                resetDemo();
            });
        });

        // 15. Analytics Modal Close
        document.getElementById('close-analytics-modal-btn')?.addEventListener('click', () => {
            document.getElementById('analytics-modal')?.classList.add('hidden');
        });

        // 16. Sharing & Tactical Navigation Buttons
        document.getElementById('em-share-details-btn')?.addEventListener('click', () => {
            const shareData = {
                title: 'WariSeva AI Emergency Alert',
                text: `Active Emergency EM-28471 at Zone 04 — Saswad Palkhi Maidan (18.3444, 74.0305). Response coordinated by WariSeva AI.`,
                url: window.location.href
            };
            if (navigator.share) {
                navigator.share(shareData).catch(() => {});
            } else {
                navigator.clipboard.writeText(`${shareData.title}: ${shareData.text}`)
                    .then(() => showToast("Emergency details copied to clipboard!", "success"))
                    .catch(() => showToast("Emergency telemetry ready to share.", "info"));
            }
        });

        document.getElementById('em-view-tactical-map-btn')?.addEventListener('click', () => {
            switchView('safety-map-view');
            initSafetyMap();
        });

        document.getElementById('em-new-sos-btn')?.addEventListener('click', () => {
            resetDemo();
        });

        // Initial View Initialization
        initEmergencyMap();
        loadServicesCards('WATER');
    });

    function loadCommandHeatmap() {
        const grid = document.getElementById('cmd-heatmap-grid');
        if (!grid) return;

        fetch('/api/command-center/heatmap')
            .then(res => res.json())
            .then(data => {
                if (!data.success || !data.zones) return;
                grid.innerHTML = data.zones.map(z => `
                    <div class="heatmap-zone-card ${z.density_level.toLowerCase()}">
                        <div class="hz-head">
                            <strong>${z.zone_name}</strong>
                            <span class="hz-tag">${z.density_level}</span>
                        </div>
                        <div class="hz-index">Crowd Congestion Index: <strong>${z.crowd_index}%</strong></div>
                        <div class="hz-emergencies">Active Incidents: <strong>${z.active_emergencies}</strong></div>
                    </div>
                `).join('');
            })
            .catch(() => {});
    }

    function loadCommandReadiness() {
        const grid = document.getElementById('cmd-readiness-grid');
        if (!grid) return;

        fetch('/api/command-center/resources')
            .then(res => res.json())
            .then(data => {
                if (!data.success || !data.camps) return;
                grid.innerHTML = data.camps.map(c => `
                    <div class="readiness-camp-card">
                        <div class="rc-head">
                            <strong>${c.name}</strong>
                            <span class="rc-status ${c.load_status.toLowerCase()}">${c.load_status}</span>
                        </div>
                        <div class="rc-zone">📍 ${c.zone}</div>
                        <div class="rc-stat">Staff / Medics: <strong>${c.staff_count}</strong></div>
                        <div class="rc-stat">Available Volunteers: <strong>${c.available_volunteers}</strong></div>
                        <div class="rc-stat">Ambulance Units: <strong>${c.responders_on_standby}</strong></div>
                    </div>
                `).join('');
            })
            .catch(() => {});
    }

})();
"""

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Successfully generated clean master static/script.js ({len(js_content)} characters)!")
