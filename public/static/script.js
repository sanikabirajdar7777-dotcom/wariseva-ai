// =========================================================================
// WARISEVA AI — MASTER CONTROLLER & SIMULATED LIVE RESPONSE ENGINE
// Sant Dnyaneshwar & Sant Tukaram Palkhi Emergency Response Prototype
// =========================================================================

(function () {
    'use strict';

    // Global Application State Object
    window.WariState = {
        lang: 'en',
        voiceEnabled: true,
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
            volunteer: null,
            command: null,
            homeSafety: null
        },
        markers: {
            emergency: {},
            safety: [],
            responder: {},
            volunteer: {},
            command: {},
            homeSafety: []
        },
        groupMembers: [
            { id: 1, name: 'Sunita Shinde', phone: '9822128472', relation: 'Spouse' },
            { id: 2, name: 'Ganesh Shinde', phone: '9822128473', relation: 'Son' }
        ],
        volunteerAuth: {
            isLoggedIn: false,
            volunteerId: null,
            volunteerName: null,
            token: null
        },
        currentScannedPilgrim: null,
        html5QrScanner: null
    };

    // Comprehensive Multilingual Translation Dictionaries (English, Marathi, Hindi)
    const i18n = {
        en: {
            lang_code: "en-IN",
            tagline: "Your safety, one tap away.",
            value_prop: "\"We don't just report an emergency — we coordinate the response behind the SOS.\"",
            value_flow: "QR Wristband → Exact Identification → Protected Medical Profile → AI Emergency Coordination",
            demo_desc: "DEMO DATA • SIMULATED RESPONSE",
            reset_demo: "🔄 RESET DEMO",
            nav_home: "Home",
            nav_emergency: "Emergency",
            nav_volunteer: "Volunteer",
            nav_responder: "Medical Facility",
            nav_map: "Safety Network",
            nav_qr_scanner: "Wristband / QR",
            nav_command: "Command Center",
            wristband_id_btn: "Wristband ID",
            palkhi_safety: "🚩 Palkhi Safety Coordination",
            hero_tagline: "\"Your safety, one tap away.\"",
            hero_subtext: "Emergency coordination and safety assistance for the Sant Dnyaneshwar & Sant Tukaram Palkhi Wari.",
            sos_btn_text: "🚨 EMERGENCY / SOS",
            sos_btn_sub: "PRESS FOR HELP • SOS",
            current_zone: "Zone 04 — Saswad Palkhi Maidan",
            act_where_am_i: "Where am I?",
            act_medical_help: "Medical Help",
            act_safety_map: "Safety Map",
            quick_services_title: "🛡️ Quick Safety Services",
            see_all: "See All 13 Facilities →",
            svc_water: "Water",
            svc_water_sub: "Drinking Water Station",
            svc_toilets: "Toilets",
            svc_toilets_sub: "Mobile Sanitation Units",
            svc_rest: "Rest Area",
            svc_rest_sub: "Pilgrim Rest Camp",
            svc_medical: "Medical Center",
            svc_medical_sub: "First Aid & Clinic",
            svc_food: "Food / Prasad",
            svc_food_sub: "Annachhatra & Meals",
            svc_hospitals: "Hospitals",
            svc_hospitals_sub: "Trauma & Emergency Care",
            safety_id_title: "WariSeva Safety ID",
            safety_id_sub: "Register demo profile for quick identification and instant SOS dispatch.",
            label_full_name: "Full Name",
            label_phone: "Mobile Number",
            btn_create_id: "CREATE SAFETY ID",
            id_active_badge: "Safety ID Active & Registered",
            btn_change_profile: "Change / Register Another Profile",
            em_kicker: "HELP IS ON THE WAY • KEEP CALM",
            em_help_requested: "EMERGENCY HELP REQUESTED",
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
            select_zone: "Select Sector:",
            modal_sos_title: "Trigger Emergency SOS?",
            modal_sos_msg: "This will capture your exact coordinates and immediately alert the nearest Palkhi route volunteer and medical responder unit.",
            modal_using_id: "Using Safety ID:",
            btn_cancel: "CANCEL",
            btn_confirm_sos: "DISPATCH SOS",
            acquiring_gps: "Acquiring GPS Position...",
            mapping_checkpoint: "Mapping to nearest Palkhi route checkpoint",
            active_em_title: "ACTIVE EMERGENCY IN PROGRESS",
            view_live_response: "VIEW LIVE RESPONSE →",
            
            // Volunteer Dashboard Strings
            vol_login_title: "VOLUNTEER LOGIN",
            vol_login_sub: "Official Wari Emergency Response Portal",
            vol_demo_badge: "DEMO ACCOUNT",
            vol_demo_creds: "Demo ID: V-001 • Password: demo123 (Ramesh Kulkarni • Zone 04 • First Aid Certified)",
            vol_quick_fill: "⚡ AUTO-FILL DEMO CREDENTIALS",
            vol_id_label: "Volunteer ID",
            vol_pass_label: "Password",
            vol_login_btn: "🔐 LOGIN AS VOLUNTEER",
            vol_logout_btn: "🚪 LOGOUT",
            vol_network_kicker: "WARISEVA VERIFIED VOLUNTEER NETWORK",
            vol_sector_info: "Assigned: Zone 04 — Saswad Palkhi Maidan • Skills: First Aid Certified, CPR",
            vol_status_avail: "🟢 STATUS: AVAILABLE",
            vol_open_scanner: "📸 OPEN QR SCANNER",
            vol_inc_dispatch: "🚨 INCOMING EMERGENCY DISPATCH",
            vol_accept_btn: "🦺 ACCEPT CASE",
            vol_enroute_btn: "🚶 START RESPONSE (EN ROUTE)",
            vol_arrived_btn: "🤝 I'M WITH PATIENT",
            vol_scan_wb_btn: "📸 SCAN PATIENT WRISTBAND",
            vol_escalate_btn: "🏥 ESCALATE TO HOSPITAL",
            vol_status_responding: "🟡 RESPONDING",
            vol_status_verified: "✓ VERIFIED",

            // Hospital Dashboard Strings
            hosp_login_title: "MEDICAL FACILITY LOGIN",
            hosp_login_sub: "Hospital & Trauma Center Coordination Portal",
            hosp_demo_badge: "DEMO FACILITY",
            hosp_demo_creds: "Facility ID: H-001 • Password: demo123 (WariSeva Medical Camp — Zone 04 • 1 Bed Available)",
            hosp_quick_fill: "⚡ AUTO-FILL DEMO CREDENTIALS",
            hosp_id_label: "Facility ID",
            hosp_pass_label: "Password",
            hosp_login_btn: "🔐 LOGIN AS MEDICAL FACILITY",
            hosp_logout_btn: "🚪 LOGOUT",
            hosp_network_kicker: "WARISEVA MEDICAL FACILITY NETWORK",
            hosp_bed_avail: "1 AVAILABLE",
            hosp_bed_reserved: "1 RESERVED",
            hosp_accepting_chip: "ACCEPTING EMERGENCIES",
            hosp_inc_intake: "🏥 INCOMING PATIENT INTAKE",
            hosp_accept_btn: "🏥 ACCEPT PATIENT (RESERVE BED)",
            hosp_arrived_btn: "📍 PATIENT ARRIVED",
            hosp_treatment_btn: "🩺 TREATMENT STARTED",
            hosp_transfer_btn: "🚑 MARK TRANSFERRED",
            hosp_resolve_btn: "✅ CASE RESOLVED",
            hosp_resolved_banner: "✅ STATUS: EMERGENCY RESOLVED. Treatment successfully administered.",

            // Command Center Strings
            cmd_title: "🛰️ TACTICAL COMMAND CENTER",
            cmd_sub: "Wari Emergency Operations, Dispatch & Verification Hub",
            cmd_tab_ops: "📊 Operations",
            cmd_tab_vols: "🦺 Volunteers",
            cmd_tab_hosps: "🏥 Medical Network",
            cmd_tab_dive: "🚨 Live Incident Deep Dive",
            cmd_stat_registered: "Total Registered",
            cmd_stat_verified: "Verified",
            cmd_stat_available: "Available",
            cmd_stat_responding: "Responding",
            cmd_stat_pending: "Pending Verification",
            cmd_stat_accepting: "Accepting Emergencies",
            cmd_stat_critical: "Critical",
            cmd_stat_high: "High",
            cmd_stat_resolved: "Resolved",

            // AI Recommendation
            ai_rec_title: "🤖 AI RESPONDER RECOMMENDATION",
            ai_why_heading: "Why this responder?",
            ai_reason_1: "✓ First-aid certified",
            ai_reason_2: "✓ 350m from patient",
            ai_reason_3: "✓ Inside Zone 04",
            ai_reason_4: "✓ Available on route",
            ai_kicker: "AI-assisted responder recommendation",

            // Timeline Steps Translation (Title & Description)
            timeline_steps: {
                1: { title: "🚨 Step 1: SOS Sent & Registered", desc: "Emergency registered in central incident registry." },
                2: { title: "📍 Step 2: Exact Location Acquired", desc: "GPS telemetry coordinates acquired: 18.3444, 74.0305 (±5m precision)." },
                3: { title: "🗺️ Step 3: Wari Zone Identified", desc: "Location matched to Zone 04 — Saswad Palkhi Maidan." },
                4: { title: "🔴 Step 4: Emergency Severity Classified", desc: "Severity: Critical • Type: Medical Emergency / Triage Priority." },
                5: { title: "🤖 Step 5: AI Responder Recommendation", desc: "Matched: Ramesh Kulkarni (V-001) • Score: 94/100 (First Aid Certified + Available + Nearby + Same Wari Zone)." },
                6: { title: "🔔 Step 6: Volunteer Alert Sent", desc: "Emergency dispatch notification sent to nearest volunteer device." },
                7: { title: "🦺 Step 7: Volunteer Accepted", desc: "Volunteer Ramesh Kulkarni confirmed and accepted dispatch." },
                8: { title: "🚶 Step 8: Volunteer En Route", desc: "Moving toward emergency location (320m • ETA 2 min)." },
                9: { title: "📍 Step 9: Volunteer Arrived", desc: "Volunteer arrived at emergency location (0m • With Patient). First aid in progress." },
                10: { title: "🏥 Step 10: Hospital Accepted", desc: "Medical facility accepted case. Emergency Bed Reserved: 1." },
                11: { title: "🚑 Step 11: Patient Expected / Arrived", desc: "Patient arrived at medical facility. Clinical triage and assessment started." },
                12: { title: "✅ Step 12: Case Resolved", desc: "Case Resolved. Patient admitted / emergency assistance completed successfully." }
            },

            // Exact Spoken Audio Narration Sentences
            timeline_narrations: {
                1: "SOS received. Emergency registered.",
                2: "Exact location acquired.",
                3: "Wari zone identified. Saswad Palkhi Maidan.",
                4: "Emergency classified as critical.",
                5: "Nearest suitable volunteer identified.",
                6: "Emergency alert sent to the nearest volunteer.",
                7: "Volunteer has accepted the emergency.",
                8: "Volunteer is on the way.",
                9: "Volunteer has arrived at the emergency location.",
                10: "Suitable medical facility identified.",
                11: "Hospital has accepted the case. Patient transfer initiated.",
                12: "Emergency response completed successfully."
            },

            // Status Tags
            tag_pending: "○ PENDING",
            tag_completed: "✓ COMPLETED",
            tag_waiting_vol: "⏳ WAITING FOR VOLUNTEER",
            tag_waiting_hosp: "⏳ WAITING FOR HOSPITAL",
            tag_processing: "🔵 PROCESSING...",
            tag_locked: "🔒 LOCKED",

            // Emergency notification
            notif_title: "🚨 NEW EMERGENCY",
            notif_msg: "Critical medical emergency reported in Zone 04. Volunteer action required."
        },
        mr: {
            lang_code: "mr-IN",
            tagline: "आपली सुरक्षा, एका स्पर्शात.",
            value_prop: "\"आम्ही केवळ आपत्कालीन नोंद करत नाही — मदतीची संपूर्ण यंत्रणा समन्वयित करतो.\"",
            value_flow: "QR रिस्टबँड → अचूक ओळख → सुरक्षित वैद्यकीय माहिती → AI आपत्कालीन समन्वय",
            demo_desc: "डेमो डेटा • सिम्युलेटेड प्रतिसाद",
            reset_demo: "🔄 रिसेट डेमो",
            nav_home: "मुख्य पान",
            nav_emergency: "आपत्कालीन",
            nav_volunteer: "स्वयंसेवक",
            nav_responder: "वैद्यकीय केंद्र",
            nav_map: "सुरक्षा नकाशा",
            nav_qr_scanner: "रिस्टबँड / QR",
            nav_command: "नियंत्रण कक्ष",
            wristband_id_btn: "रिस्टबँड ID",
            palkhi_safety: "🚩 पालखी सुरक्षा समन्वय",
            hero_tagline: "\"आपली सुरक्षा, एका स्पर्शात.\"",
            hero_subtext: "संत ज्ञानेश्वर व संत तुकाराम पालखी वारीसाठी डिजिटल आरोग्य व सुरक्षा यंत्रणा.",
            sos_btn_text: "🚨 आपत्कालीन मदत / SOS",
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
            svc_food_sub: "अन्नदान व भोजन",
            svc_hospitals: "रुग्णालये",
            svc_hospitals_sub: "ट्रॉमा व आपत्कालीन कक्ष",
            safety_id_title: "वारीसेवा सुरक्षा ओळखपत्र",
            safety_id_sub: "तातडीच्या मदतीसाठी आपली माहिती नोंदवा.",
            label_full_name: "पूर्ण नाव",
            label_phone: "मोबाईल नंबर",
            btn_create_id: "सुरक्षा आयडी तयार करा",
            id_active_badge: "सुरक्षा ओळखपत्र सक्रिय आहे",
            btn_change_profile: "दुसरे ओळखपत्र नोंदवा",
            em_kicker: "मदत येत आहे • घाबरू नका",
            em_help_requested: "आपत्कालीन मदत मागितली आहे",
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

            // Volunteer Dashboard Strings
            vol_login_title: "स्वयंसेवक लॉगिन",
            vol_login_sub: "अधिकृत वारी आपत्कालीन प्रतिसाद पोर्टल",
            vol_demo_badge: "डेमो खाते",
            vol_demo_creds: "डेमो ID: V-001 • पासवर्ड: demo123 (रमेश कुलकर्णी • झोन ०४ • प्रथमोपचार प्रमाणित)",
            vol_quick_fill: "⚡ डेमो माहिती भरा",
            vol_id_label: "स्वयंसेवक ID",
            vol_pass_label: "पासवर्ड",
            vol_login_btn: "🔐 स्वयंसेवक लॉगिन करा",
            vol_logout_btn: "🚪 लॉगआउट",
            vol_network_kicker: "वारीसेवा सत्यापित स्वयंसेवक नेटवर्क",
            vol_sector_info: "नेमणूक: झोन ०४ — सासवड पालखी मैदान • कौशल्ये: प्रथमोपचार प्रमाणित, CPR",
            vol_status_avail: "🟢 स्थिती: उपलब्ध",
            vol_open_scanner: "📸 QR स्कॅनर उघडा",
            vol_inc_dispatch: "🚨 नवीन आपत्कालीन मदत सूचना",
            vol_accept_btn: "🦺 केस स्वीकारा",
            vol_enroute_btn: "🚶 मदतीसाठी निघा (मार्गस्थ)",
            vol_arrived_btn: "🤝 मी रुग्णाजवळ पोहोचलो",
            vol_scan_wb_btn: "📸 रुग्णाचा रिस्टबँड स्कॅन करा",
            vol_escalate_btn: "🏥 रुग्णालयाकडे संदर्भ द्या",
            vol_status_responding: "🟡 प्रतिसाद देत आहे",
            vol_status_verified: "✓ सत्यापित",

            // Hospital Dashboard Strings
            hosp_login_title: "वैद्यकीय केंद्र लॉगिन",
            hosp_login_sub: "रुग्णालय व ट्रॉमा केंद्र समन्वय पोर्टल",
            hosp_demo_badge: "डेमो केंद्र",
            hosp_demo_creds: "केंद्र ID: H-001 • पासवर्ड: demo123 (वारीसेवा मेडिकल कॅम्प — झोन ०४ • १ बेड उपलब्ध)",
            hosp_quick_fill: "⚡ डेमो माहिती भरा",
            hosp_id_label: "केंद्र ID",
            hosp_pass_label: "पासवर्ड",
            hosp_login_btn: "🔐 वैद्यकीय केंद्र लॉगिन करा",
            hosp_logout_btn: "🚪 लॉगआउट",
            hosp_network_kicker: "वारीसेवा वैद्यकीय केंद्र नेटवर्क",
            hosp_bed_avail: "१ उपलब्ध",
            hosp_bed_reserved: "१ राखीव",
            hosp_accepting_chip: "रुग्ण स्वीकारत आहे",
            hosp_inc_intake: "🏥 नवीन रुग्ण आगमन",
            hosp_accept_btn: "🏥 रुग्ण स्वीकारा (बेड राखीव)",
            hosp_arrived_btn: "📍 रुग्ण पोहोचला",
            hosp_treatment_btn: "🩺 उपचार सुरू झाले",
            hosp_transfer_btn: "🚑 रुग्ण हस्तांतरित झाला",
            hosp_resolve_btn: "✅ केस पूर्ण झाली",
            hosp_resolved_banner: "✅ स्थिती: आपत्कालीन केस यशस्वीरित्या पूर्ण झाली. उपचार यशस्वीरित्या दिले गेले.",

            // Command Center Strings
            cmd_title: "🛰️ नियंत्रण कक्ष",
            cmd_sub: "वारी आपत्कालीन ऑपरेशन्स, पाठपुरावा व पडताळणी केंद्र",
            cmd_tab_ops: "📊 कार्यप्रणाली",
            cmd_tab_vols: "🦺 स्वयंसेवक",
            cmd_tab_hosps: "🏥 आरोग्य यंत्रणा",
            cmd_tab_dive: "🚨 थेट घटना विश्लेषण",
            cmd_stat_registered: "एकूण नोंदणीकृत",
            cmd_stat_verified: "सत्यापित",
            cmd_stat_available: "उपलब्ध",
            cmd_stat_responding: "प्रतिसाद देत आहेत",
            cmd_stat_pending: "पडताळणी प्रलंबित",
            cmd_stat_accepting: "मदत स्वीकारत आहेत",
            cmd_stat_critical: "गंभीर",
            cmd_stat_high: "उच्च",
            cmd_stat_resolved: "पूर्ण झालेल्या केसेस",

            // AI Recommendation
            ai_rec_title: "🤖 AI-सहाय्यित प्रतिसादकाची शिफारस",
            ai_why_heading: "निवडण्याची कारणे:",
            ai_reason_1: "✓ प्रथमोपचार प्रमाणित",
            ai_reason_2: "✓ ३५० मी अंतर (२ मिनिटे)",
            ai_reason_3: "✓ त्याच वारी क्षेत्रात (झोन ०४)",
            ai_reason_4: "✓ मार्गावर उपलब्ध",
            ai_kicker: "AI-सहाय्यित प्रतिसादकाची शिफारस",

            // Timeline Steps Translation (Exact Marathi as requested)
            timeline_steps: {
                1: { title: "🚨 पायरी १: SOS पाठवले आणि नोंदणी झाली", desc: "आपत्कालीन घटना केंद्रीय नोंदणी प्रणालीमध्ये नोंदवली गेली." },
                2: { title: "📍 पायरी २: अचूक ठिकाण मिळाले", desc: "GPS द्वारे अचूक ठिकाण मिळाले." },
                3: { title: "🗺️ पायरी ३: वारी क्षेत्र ओळखले", desc: "ठिकाण संबंधित वारी क्षेत्राशी जुळवले गेले." },
                4: { title: "🔴 पायरी ४: आपत्कालीन परिस्थितीची तीव्रता निश्चित केली", desc: "तीव्रता: गंभीर." },
                5: { title: "🤖 पायरी ५: AI प्रतिसादकाची शिफारस", desc: "सर्वात योग्य जवळील प्रतिसादकाची शिफारस केली." },
                6: { title: "🔔 पायरी ६: स्वयंसेवकाला सूचना पाठवली", desc: "स्वयंसेवकाला आपत्कालीन मदतीची सूचना पाठवली गेली." },
                7: { title: "🦺 पायरी ७: स्वयंसेवकाने मदत स्वीकारली", desc: "स्वयंसेवकाने केस स्वीकारली असून मदतीसाठी तयारी दर्शवली आहे." },
                8: { title: "🚶 पायरी ८: स्वयंसेवक घटनास्थळी येत आहे", desc: "स्वयंसेवक घटनास्थळी येत आहे (३२० मी • अंदाजे २ मिनिटे)." },
                9: { title: "📍 पायरी ९: स्वयंसेवक पोहोचला", desc: "स्वयंसेवक रुग्णाजवळ पोहोचला असून प्रथमोपचार सुरू केले आहेत." },
                10: { title: "🏥 पायरी १०: वैद्यकीय केंद्राने केस स्वीकारली", desc: "वैद्यकीय केंद्राने केस स्वीकारली असून १ आपत्कालीन बेड राखीव केला आहे." },
                11: { title: "🚑 पायरी ११: रुग्ण येण्याची माहिती दिली", desc: "रुग्ण पोहोचला असून उपचार सुरू झाले आहेत." },
                12: { title: "✅ पायरी १२: केस पूर्ण झाली", desc: "केस पूर्ण झाली. रुग्णावर योग्य उपचार यशस्वीरित्या झाले." }
            },

            // Exact Spoken Audio Narration Sentences in Marathi
            timeline_narrations: {
                1: "SOS पाठवले आणि नोंदणी झाली.",
                2: "GPS द्वारे अचूक ठिकाण मिळाले.",
                3: "वारी क्षेत्र ओळखले. सासवड पालखी मैदान.",
                4: "आपत्कालीन परिस्थितीची तीव्रता गंभीर निश्चित केली.",
                5: "सर्वात योग्य जवळील स्वयंसेवकाची शिफारस केली.",
                6: "स्वयंसेवकाला सूचना पाठवली आहे.",
                7: "स्वयंसेवकाने मदत स्वीकारली आहे.",
                8: "स्वयंसेवक घटनास्थळी येत आहे.",
                9: "स्वयंसेवक रुग्णाजवळ पोहोचला आहे.",
                10: "वैद्यकीय केंद्राने केस स्वीकारली आहे आणि बेड राखीव केला आहे.",
                11: "रुग्ण वैद्यकीय केंद्रात पोहोचला आहे.",
                12: "आपत्कालीन केस यशस्वीरित्या पूर्ण झाली आहे."
            },

            // Status Tags
            tag_pending: "○ प्रलंबित",
            tag_completed: "✓ पूर्ण",
            tag_waiting_vol: "⏳ स्वयंसेवकाची प्रतीक्षा",
            tag_waiting_hosp: "⏳ रुग्णालयाची प्रतीक्षा",
            tag_processing: "🔵 प्रक्रिया सुरू...",
            tag_locked: "🔒 बंद",

            // Emergency notification
            notif_title: "🚨 नवीन आपत्कालीन घटना",
            notif_msg: "झोन ०४ मध्ये गंभीर वैद्यकीय आपत्कालीन घटना नोंदवली आहे. स्वयंसेवकाची मदत आवश्यक आहे."
        },
        hi: {
            lang_code: "hi-IN",
            tagline: "आपकी सुरक्षा, एक स्पर्श में.",
            value_prop: "\"हम सिर्फ आपातकाल दर्ज नहीं करते — पूरी राहत प्रणाली का समन्वय करते हैं.\"",
            value_flow: "QR रिस्टबैंड → सटीक पहचान → सुरक्षित चिकित्सा प्रोफ़ाइल → AI आपातकालीन समन्वय",
            demo_desc: "डेमो डेटा • सिम्युलेटेड प्रतिक्रिया",
            reset_demo: "🔄 रीसेट डेमो",
            nav_home: "होम",
            nav_emergency: "आपातकाल",
            nav_volunteer: "स्वयंसेवक",
            nav_responder: "चिकित्सा केंद्र",
            nav_map: "सुरक्षा नक्शा",
            nav_qr_scanner: "रिस्टबैंड / QR",
            nav_command: "कंट्रोल रूम",
            wristband_id_btn: "रिस्टबैंड ID",
            palkhi_safety: "🚩 पालखी सुरक्षा समन्वय",
            hero_tagline: "\"आपकी सुरक्षा, एक स्पर्श में.\"",
            hero_subtext: "संत ज्ञानेश्वर एवं संत तुकाराम पालखी वारी के लिए डिजिटल स्वास्थ्य और सुरक्षा प्रणाली.",
            sos_btn_text: "🚨 आपातकालीन सहायता / SOS",
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
            svc_food_sub: "अन्नदान व भोजन",
            svc_hospitals: "अस्पताल",
            svc_hospitals_sub: "ट्रॉमा व आपातकालीन कक्ष",
            safety_id_title: "वारीसेवा सुरक्षा पहचान पत्र",
            safety_id_sub: "त्वरित सहायता के लिए अपनी जानकारी दर्ज करें.",
            label_full_name: "पूरा नाम",
            label_phone: "मोबाइल नंबर",
            btn_create_id: "सुरक्षा आईडी बनाएं",
            id_active_badge: "सुरक्षा आईडी सक्रिय है",
            btn_change_profile: "अन्य प्रोफाइल दर्ज करें",
            em_kicker: "मदद आ रही है • निश्चिंत रहें",
            em_help_requested: "आपातकालीन सहायता का अनुरोध किया गया",
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

            // Volunteer Dashboard Strings
            vol_login_title: "स्वयंसेवक लॉगिन",
            vol_login_sub: "आधिकारिक वारी आपातकालीन सहायता पोर्टल",
            vol_demo_badge: "डेमो खाता",
            vol_demo_creds: "डेमो ID: V-001 • पासवर्ड: demo123 (रमेश कुलकर्णी • जोन ०४ • प्राथमिक उपचार प्रमाणित)",
            vol_quick_fill: "⚡ डेमो जानकारी भरें",
            vol_id_label: "स्वयंसेवक ID",
            vol_pass_label: "पासवर्ड",
            vol_login_btn: "🔐 स्वयंसेवक लॉगिन करें",
            vol_logout_btn: "🚪 लॉगआउट",
            vol_network_kicker: "वारीसेवा सत्यापित स्वयंसेवक नेटवर्क",
            vol_sector_info: "नियुक्त: जोन ०४ — सासवड पालखी मैदान • कौशल्य: प्राथमिक उपचार प्रमाणित, CPR",
            vol_status_avail: "🟢 स्थिति: उपलब्ध",
            vol_open_scanner: "📸 QR स्कैनर खोलें",
            vol_inc_dispatch: "🚨 नई आपातकालीन सहायता सूचना",
            vol_accept_btn: "🦺 केस स्वीकारें",
            vol_enroute_btn: "🚶 मदद के लिए निकलें (मार्गस्थ)",
            vol_arrived_btn: "🤝 मैं मरीज के पास पहुँचा",
            vol_scan_wb_btn: "📸 मरीज का रिस्टबैंड स्कैन करें",
            vol_escalate_btn: "🏥 अस्पताल को रेफर करें",
            vol_status_responding: "🟡 प्रतिक्रिया दे रहे हैं",
            vol_status_verified: "✓ सत्यापित",

            // Hospital Dashboard Strings
            hosp_login_title: "चिकित्सा केंद्र लॉगिन",
            hosp_login_sub: "अस्पताल एवं ट्रॉमा केंद्र समन्वय पोर्टल",
            hosp_demo_badge: "डेमो केंद्र",
            hosp_demo_creds: "केंद्र ID: H-001 • पासवर्ड: demo123 (वारीसेवा मेडिकल कैम्प — जोन ०४ • १ बेड उपलब्ध)",
            hosp_quick_fill: "⚡ डेमो जानकारी भरें",
            hosp_id_label: "केंद्र ID",
            hosp_pass_label: "पासवर्ड",
            hosp_login_btn: "🔐 चिकित्सा केंद्र लॉगिन करें",
            hosp_logout_btn: "🚪 लॉगआउट",
            hosp_network_kicker: "वारीसेवा चिकित्सा केंद्र नेटवर्क",
            hosp_bed_avail: "१ उपलब्ध",
            hosp_bed_reserved: "१ आरक्षित",
            hosp_accepting_chip: "मरीज स्वीकार कर रहे हैं",
            hosp_inc_intake: "🏥 नया मरीज आगमन",
            hosp_accept_btn: "🏥 मरीज स्वीकारें (बेड आरक्षित)",
            hosp_arrived_btn: "📍 मरीज पहुंच गया",
            hosp_treatment_btn: "🩺 उपचार शुरू हुआ",
            hosp_transfer_btn: "🚑 मरीज ट्रांसफर हुआ",
            hosp_resolve_btn: "✅ केस पूरा हुआ",
            hosp_resolved_banner: "✅ स्थिति: आपातकालीन केस सफलतापूर्वक पूरा हुआ। उपचार सफलतापूर्वक दिया गया।",

            // Command Center Strings
            cmd_title: "🛰️ कंट्रोल रूम",
            cmd_sub: "वारी आपातकालीन ऑपरेशन्स, नियंत्रण एवं सत्यापन केंद्र",
            cmd_tab_ops: "📊 ऑपरेशन्स",
            cmd_tab_vols: "🦺 स्वयंसेवक",
            cmd_tab_hosps: "🏥 चिकित्सा नेटवर्क",
            cmd_tab_dive: "🚨 लाइव घटना विश्लेषण",
            cmd_stat_registered: "कुल पंजीकृत",
            cmd_stat_verified: "सत्यापित",
            cmd_stat_available: "उपलब्ध",
            cmd_stat_responding: "प्रतिक्रिया दे रहे हैं",
            cmd_stat_pending: "सत्यापन लंबित",
            cmd_stat_accepting: "सहायता स्वीकार रहे हैं",
            cmd_stat_critical: "अत्यंत गंभीर",
            cmd_stat_high: "गंभीर",
            cmd_stat_resolved: "सुलझाई गई घटनाएं",

            // AI Recommendation
            ai_rec_title: "🤖 AI-सहायता प्राप्त रिस्पॉन्डर की सिफारिश",
            ai_why_heading: "चयन के कारण:",
            ai_reason_1: "✓ प्राथमिक उपचार प्रमाणित",
            ai_reason_2: "✓ ३५० मी दूरी (२ मिनट)",
            ai_reason_3: "✓ उसी वारी क्षेत्र में (जोन ०४)",
            ai_reason_4: "✓ मार्ग पर उपलब्ध",
            ai_kicker: "AI-सहायता प्राप्त रिस्पॉन्डर की सिफारिश",

            // Timeline Steps Translation (Exact Hindi as requested)
            timeline_steps: {
                1: { title: "🚨 चरण १: SOS भेजा गया और दर्ज किया गया", desc: "आपातकालीन घटना केंद्रीय रजिस्टर में दर्ज की गई।" },
                2: { title: "📍 चरण २: सटीक स्थान प्राप्त हुआ", desc: "GPS के माध्यम से सटीक स्थान प्राप्त हुआ।" },
                3: { title: "🗺️ चरण ३: वारी क्षेत्र की पहचान हुई", desc: "स्थान को संबंधित वारी क्षेत्र से जोड़ा गया।" },
                4: { title: "🔴 चरण ४: आपातकाल की गंभीरता निर्धारित की गई", desc: "गंभीरता: अत्यंत गंभीर।" },
                5: { title: "🤖 चरण ५: AI रिस्पॉन्डर की सिफारिश", desc: "सबसे उपयुक्त नजदीकी रिस्पॉन्डर की सिफारिश की गई।" },
                6: { title: "🔔 चरण ६: स्वयंसेवक को सूचना भेजी गई", desc: "स्वयंसेवक को आपातकालीन सहायता की सूचना भेजी गई।" },
                7: { title: "🦺 चरण ७: स्वयंसेवक ने केस स्वीकार किया", desc: "स्वयंसेवक ने केस स्वीकार कर लिया और सहायता के लिए तैयार है।" },
                8: { title: "🚶 चरण ८: स्वयंसेवक घटनास्थल की ओर जा रहा है", desc: "स्वयंसेवक घटनास्थल की ओर जा रहा है (३२० मी • लगभग २ मिनट)।" },
                9: { title: "📍 चरण ९: स्वयंसेवक पहुंच गया", desc: "स्वयंसेवक मरीज के पास पहुंच गया और प्राथमिक उपचार शुरू किया।" },
                10: { title: "🏥 चरण १०: चिकित्सा केंद्र ने केस स्वीकार किया", desc: "चिकित्सा केंद्र ने केस स्वीकार किया और १ आपातकालीन बेड आरक्षित किया।" },
                11: { title: "🚑 चरण ११: मरीज के आने की सूचना दी गई", desc: "मरीज पहुंच गया और उपचार शुरू हुआ।" },
                12: { title: "✅ चरण १२: केस पूरा हुआ", desc: "केस पूरा हुआ। मरीज को उचित चिकित्सा सहायता सफलतापूर्वक मिली।" }
            },

            // Exact Spoken Audio Narration Sentences in Hindi
            timeline_narrations: {
                1: "SOS भेजा गया और दर्ज किया गया.",
                2: "GPS के माध्यम से सटीक स्थान प्राप्त हुआ.",
                3: "वारी क्षेत्र की पहचान हुई. सासवड पालखी मैदान.",
                4: "आपातकाल की गंभीरता अत्यंत गंभीर निर्धारित की गई.",
                5: "सबसे उपयुक्त नजदीकी स्वयंसेवक की सिफारिश की गई.",
                6: "स्वयंसेवक को सूचना भेजी गई है.",
                7: "स्वयंसेवक ने केस स्वीकार किया है.",
                8: "स्वयंसेवक घटनास्थल की ओर जा रहा है.",
                9: "स्वयंसेवक मरीज के पास पहुंच गया है.",
                10: "चिकित्सा केंद्र ने केस स्वीकार किया और बेड आरक्षित किया.",
                11: "मरीज चिकित्सा केंद्र पर पहुंच गया है.",
                12: "आपातकालीन केस सफलतापूर्वक पूरा हुआ."
            },

            // Status Tags
            tag_pending: "○ लंबित",
            tag_completed: "✓ पूर्ण",
            tag_waiting_vol: "⏳ स्वयंसेवक की प्रतीक्षा",
            tag_waiting_hosp: "⏳ अस्पताल की प्रतीक्षा",
            tag_processing: "🔵 प्रक्रिया जारी...",
            tag_locked: "🔒 बंद",

            // Emergency notification
            notif_title: "🚨 नई आपातकालीन घटना",
            notif_msg: "ज़ोन ०४ में गंभीर चिकित्सा आपातकाल दर्ज की गई है। स्वयंसेवक की सहायता आवश्यक है।"
        }
    };

    // Spoken Audio Synthesis Helper
    function getPreferredVoice(targetLang = 'en-IN') {
        if (!('speechSynthesis' in window)) return null;
        const voices = window.speechSynthesis.getVoices() || [];
        return voices.find(v => v.lang === targetLang || v.lang.replace('_', '-') === targetLang) ||
               voices.find(v => v.lang.startsWith(targetLang.split('-')[0])) || null;
    }

    function speakText(text) {
        if (!window.WariState.voiceEnabled) return;
        if (!('speechSynthesis' in window)) return;
        try {
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 0.95;
            utterance.pitch = 1.0;
            const targetLang = window.WariState.lang === 'mr' ? 'mr-IN' : (window.WariState.lang === 'hi' ? 'hi-IN' : 'en-IN');
            utterance.lang = targetLang;
            const voice = getPreferredVoice(targetLang);
            if (voice) utterance.voice = voice;
            window.speechSynthesis.speak(utterance);
        } catch (e) {
            console.warn('Voice synthesis error:', e);
        }
    }

    function speakVoice(text) {
        speakText(text);
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

        // Update Desktop, Sidebar & Mobile Nav active states
        document.querySelectorAll('.sidebar-panel .nav-link-btn, .desktop-nav .nav-link-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.view === viewId);
        });
        document.querySelectorAll('.mobile-bottom-nav .mob-nav-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.view === viewId);
        });

        // Auto-close mobile drawer if open
        const sidebar = document.querySelector('.sidebar-panel');
        const backdrop = document.getElementById('sidebar-backdrop');
        if (sidebar && sidebar.classList.contains('mobile-open')) {
            sidebar.classList.remove('mobile-open');
            if (backdrop) backdrop.classList.add('hidden');
        }

        // Invalidate Leaflet maps upon view display
        setTimeout(() => {
            if (viewId === 'home-view') {
                initHomeSafetyMap();
                if (window.WariState.maps.homeSafety) window.WariState.maps.homeSafety.invalidateSize();
            } else if (viewId === 'emergency-view') {
                initEmergencyMap();
                if (window.WariState.maps.emergency) window.WariState.maps.emergency.invalidateSize();
            } else if (viewId === 'safety-map-view') {
                initSafetyMap();
                if (window.WariState.maps.safety) window.WariState.maps.safety.invalidateSize();
            } else if (viewId === 'responder-view') {
                checkHospAuth();
                if (sessionStorage.getItem('wariseva_hospital_auth')) {
                    initResponderMap();
                    loadResponderEmergencyFeed();
                }
                if (window.WariState.maps.responder) {
                    scheduleMapInvalidate(window.WariState.maps.responder, document.getElementById('responder-map'));
                }
            } else if (viewId === 'volunteer-view') {
                checkVolAuth();
                if (sessionStorage.getItem('wariseva_volunteer_auth')) {
                    initVolunteerMap();
                    loadVolunteerEmergencyFeed();
                }
                if (window.WariState.maps.volunteer) {
                    scheduleMapInvalidate(window.WariState.maps.volunteer, document.getElementById('volunteer-map'));
                }
            } else if (viewId === 'command-view') {
                if (typeof checkCommandAuth === 'function') {
                    checkCommandAuth();
                }
                if (sessionStorage.getItem('wariseva_command_auth')) {
                    initCommandMap();
                    loadCommandIncidentsList();
                    if (window.WariState.maps.command) {
                        scheduleMapInvalidate(window.WariState.maps.command, document.getElementById('command-map'));
                    }
                }
            }
        }, 150);
    }

    function speakStep(stage) {
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
        const sosMainBtn = document.getElementById('main-sos-button');
        if (sosMainBtn) {
            const titleEl = sosMainBtn.querySelector('.sos-label-main') || sosMainBtn.querySelector('.sos-btn-text');
            const subEl = sosMainBtn.querySelector('.sos-label-sub') || sosMainBtn.querySelector('.sos-btn-sub');
            if (titleEl) titleEl.textContent = dict.sos_btn_text ? dict.sos_btn_text.replace('🚨 ', '') : 'SOS';
            if (subEl) subEl.textContent = dict.sos_btn_sub || dict.sos_touch_text || 'TAP FOR EMERGENCY';
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
        const volAcceptBtn = document.getElementById('vol-accept-em-btn');
        if (volAcceptBtn) volAcceptBtn.textContent = dict.vol_accept_btn;

        const volEnrouteBtn = document.getElementById('vol-start-response-btn');
        if (volEnrouteBtn) volEnrouteBtn.textContent = dict.vol_enroute_btn;

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
        const step8Dist = document.getElementById('step-8-dist-tag');
        const step8Eta = document.getElementById('step-8-eta-tag');

        if (ripDist) ripDist.textContent = `${distM}m`;
        if (ripEta) ripEta.textContent = `${etaMin} min`;
        if (ripStatus) ripStatus.textContent = statusText;
        if (ripPill) {
            ripPill.className = `status-pill ${statusState.toLowerCase()}`;
            ripPill.textContent = `STATUS: ${statusState}`;
        }
        if (volDist) volDist.textContent = `${distM}m`;
        if (step8Dist) step8Dist.textContent = `${distM}m`;
        if (step8Eta) step8Eta.textContent = `${etaMin} min`;

        // Update leaflet volunteer marker position if exists
        if (window.WariState.markers.emergency && window.WariState.markers.emergency.volunteer) {
            const frac = Math.max(0, Math.min(1, 1 - (distM / 320)));
            const newLat = 18.3470 - ((18.3470 - 18.3444) * frac);
            const newLon = 74.0330 - ((74.0330 - 74.0305) * frac);
            window.WariState.markers.emergency.volunteer.setLatLng([newLat, newLon]);
        }
    }

    // =========================================================================
    // CENTRALIZED DEMO EMERGENCY STATE ENGINE (MASTER WORKFLOW)
    // =========================================================================

    // Audit Trail Logger Helper
    function addAuditLogEntry(text) {
        const list = document.getElementById('audit-trail-events-list');
        if (!list) return;
        const now = new Date();
        const timeStr = [
            String(now.getHours()).padStart(2, '0'),
            String(now.getMinutes()).padStart(2, '0'),
            String(now.getSeconds()).padStart(2, '0')
        ].join(':');

        const entry = document.createElement('div');
        entry.style.color = '#C9D1D9';
        entry.innerHTML = `<span style="color: var(--accent-cyan);">${timeStr}</span> ${text}`;
        list.appendChild(entry);
        list.scrollTop = list.scrollHeight;
    }

    // Response Clock Milestone Recorder
    function recordClockMilestone(milestoneKey, customLabel) {
        const secs = window.WariState.stopwatchSeconds || 0;
        const minsStr = String(Math.floor(secs / 60)).padStart(2, '0');
        const secsStr = String(secs % 60).padStart(2, '0');
        const timeStr = `${minsStr}:${secsStr}`;

        const elMap = {
            'sos': 'clock-ms-sos',
            'vol_accept': 'clock-ms-vol-accept',
            'vol_enroute': 'clock-ms-vol-enroute',
            'vol_arrived': 'clock-ms-vol-arrived',
            'hosp_accept': 'clock-ms-hosp-accept',
            'transferred': 'clock-ms-transferred',
            'resolved': 'clock-ms-resolved'
        };

        if (elMap[milestoneKey]) {
            const node = document.getElementById(elMap[milestoneKey]);
            if (node) node.textContent = timeStr;
        }

        if (milestoneKey === 'vol_accept') {
            const sosVolEl = document.getElementById('clock-sos-vol');
            if (sosVolEl) sosVolEl.textContent = `${secs} sec`;
        } else if (milestoneKey === 'hosp_accept') {
            const sosHospEl = document.getElementById('clock-sos-hosp');
            if (sosHospEl) sosHospEl.textContent = `${Math.floor(secs / 60)} min ${secs % 60} sec`;
        } else if (milestoneKey === 'resolved') {
            const totalEl = document.getElementById('clock-total-time');
            if (totalEl) totalEl.textContent = `${Math.floor(secs / 60)} min ${secs % 60} sec`;
        }
    }

    function setDemoEmergencyStage(stage) {
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
                addAuditLogEntry("✓ SOS Registered (WS-28471 • Tukaram Shinde)");
                recordClockMilestone('sos');
                syncEmergencyStatusAcrossConsoles('EM-28471', 'CREATED', 'SOS SENT & REGISTERED');
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
                addAuditLogEntry("✓ GPS Telemetry Acquired: 18.3444, 74.0305 (±5m)");
                if (emMap) emMap.flyTo([18.3444, 74.0305], 17);
                break;

            case 3:
                setTimelineStep(2, false, true);
                setTimelineStep(3, true, false);
                if (statusTitle) statusTitle.textContent = lang === 'mr' ? '🗺️ वारी क्षेत्र ओळखले' : (lang === 'hi' ? '🗺️ वारी क्षेत्र की पहचान हुई' : '🗺️ WARI ZONE IDENTIFIED');
                showToast(lang === 'mr' ? "🗺️ पायरी ३: वारी क्षेत्र: झोन ०४ — सासवड पालखी मैदान" : (lang === 'hi' ? "🗺️ चरण ३: वारी क्षेत्र: जोन ०४ — सासवड पालखी मैदान" : "🗺️ Step 3: Wari Zone: Zone 04 — Saswad Palkhi Maidan"), "info");
                addAuditLogEntry("✓ Wari Sector Verified: Zone 04 — Saswad Palkhi Maidan");
                break;

            case 4:
                setTimelineStep(3, false, true);
                setTimelineStep(4, true, false);
                const curSev = (window.WariState.selectedTriageSeverity || 'CRITICAL').toUpperCase();
                const curType = window.WariState.selectedTriageType || 'Medical / Chest Pain';
                if (statusTitle) statusTitle.textContent = `🔴 SEVERITY: ${curSev} (${curType})`;
                showToast(`🔴 Step 4: Emergency Classified: ${curSev} (${curType})`, "info");
                addAuditLogEntry(`✓ Emergency Classified: ${curSev} • ${curType}`);
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
                addAuditLogEntry("✓ AI Matched Volunteer: Ramesh Kulkarni (V-001) Score 94/100");
                addAuditLogEntry("🔔 Volunteer Alert Dispatched to V-001 Device");
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
                syncEmergencyStatusAcrossConsoles('EM-28471', 'VOLUNTEER ACCEPTED', 'VOLUNTEER ACCEPTED • EN ROUTE');
                showToast(lang === 'mr' ? "🦺 पायरी ७: स्वयंसेवक रमेश कुलकर्णी (V-001) यांनी केस स्वीकारली" : (lang === 'hi' ? "🦺 चरण ७: स्वयंसेवक रमेश कुलकर्णी (V-001) ने केस स्वीकार किया" : "🦺 Step 7: Volunteer Ramesh Kulkarni (V-001) Accepted Dispatch"), "success");
                addAuditLogEntry("✓ Volunteer Ramesh Kulkarni (V-001) Accepted Dispatch");
                recordClockMilestone('vol_accept');
                if (emMap && markers) {
                    if (!emMap.hasLayer(markers.volunteer)) markers.volunteer.addTo(emMap);
                }
                break;

            case 8:
                setTimelineStep(8, true, false);
                if (statusTitle) statusTitle.textContent = lang === 'mr' ? '🚶 स्वयंसेवक मार्गस्थ' : (lang === 'hi' ? '🚶 स्वयंसेवक मार्गस्थ' : '🚶 VOLUNTEER EN ROUTE');
                if (cmdStatusText) cmdStatusText.textContent = lang === 'mr' ? 'मार्गस्थ' : (lang === 'hi' ? 'मार्गस्थ' : 'EN ROUTE');
                updateVolunteerDistance(180, 1, lang === 'mr' ? '🟡 प्रतिसाद देत आहे' : (lang === 'hi' ? '🟡 प्रतिक्रिया दे रहे हैं' : '🟡 Responding'), '🟡 RESPONDING');
                syncEmergencyStatusAcrossConsoles('EM-28471', 'VOLUNTEER RESPONDING', 'VOLUNTEER EN ROUTE (180m)');
                addAuditLogEntry("✓ Volunteer En Route (180m • Safe Corridor)");
                recordClockMilestone('vol_enroute');
                break;

            case 9:
                setTimelineStep(8, false, true);
                setTimelineStep(9, false, true);
                setTimelineStep(10, true, false);
                if (statusTitle) statusTitle.textContent = lang === 'mr' ? '📍 स्वयंसेवक पोहोचला' : (lang === 'hi' ? '📍 स्वयंसेवक पहुंच गया' : '📍 VOLUNTEER WITH PATIENT');
                if (cmdStatusText) cmdStatusText.textContent = lang === 'mr' ? 'स्वयंसेवक पोहोचला' : (lang === 'hi' ? 'स्वयंसेवक पहुंच गया' : 'VOLUNTEER ARRIVED');
                updateVolunteerDistance(0, 0, lang === 'mr' ? '🟢 रुग्णाजवळ पोहोचले' : (lang === 'hi' ? '🟢 मरीज के पास पहुंचे' : '🟢 With Patient'), '🟢 VOLUNTEER ARRIVED');
                syncEmergencyStatusAcrossConsoles('EM-28471', 'WITH PATIENT', 'ARRIVED • FIRST AID ADMINISTERED');
                showToast(lang === 'mr' ? "📍 पायरी ९: स्वयंसेवक रुग्णाजवळ पोहोचले (0m • With Patient)" : (lang === 'hi' ? "📍 चरण ९: स्वयंसेवक मरीज के पास पहुंचे (0m • With Patient)" : "📍 Step 9: Volunteer Arrived at Emergency Location (0m • With Patient)"), "success");
                addAuditLogEntry("✓ Volunteer Arrived with Patient (0m • First Aid Active)");
                recordClockMilestone('vol_arrived');
                document.getElementById('reached-confirmed-banner')?.classList.remove('hidden');
                if (markers && markers.volunteer) {
                    markers.volunteer.setLatLng([18.3444, 74.0305]);
                }
                break;

            case 10:
                setTimelineStep(10, true, false);
                if (statusTitle) statusTitle.textContent = lang === 'mr' ? '🏥 वैद्यकीय केंद्राने केस स्वीकारली' : (lang === 'hi' ? '🏥 चिकित्सा केंद्र ने केस स्वीकार किया' : '🏥 AI HOSPITAL RECOMMENDATION');
                if (cmdStatusText) cmdStatusText.textContent = lang === 'mr' ? 'रुग्णालय शिफारस' : (lang === 'hi' ? 'अस्पताल सिफारिश' : 'HOSPITAL RECOMMENDED');
                syncEmergencyStatusAcrossConsoles('EM-28471', 'HOSPITAL RECOMMENDED', 'AI HOSPITAL RECOMMENDED');
                addAuditLogEntry("✓ AI Hospital Recommended: Saswad Rural Hospital (H-001)");
                break;

            case 11:
                setTimelineStep(10, false, true);
                setTimelineStep(11, false, true);
                if (statusTitle) statusTitle.textContent = lang === 'mr' ? '🚑 रुग्ण पोहोचला • बेड राखीव' : (lang === 'hi' ? '🚑 मरीज पहुंच गया • बेड आरक्षित' : '🚑 HOSPITAL ACCEPTED • BED RESERVED');
                if (cmdStatusText) cmdStatusText.textContent = lang === 'mr' ? 'रुग्णालय सज्ज' : (lang === 'hi' ? 'अस्पताल तैयार' : 'HOSPITAL READY');
                const respState = document.getElementById('resp-state-text');
                if (respState) respState.textContent = lang === 'mr' ? '🏥 वैद्यकीय केंद्र: रुग्ण स्वीकारला • बेड राखीव: १' : (lang === 'hi' ? '🏥 चिकित्सा केंद्र: मरीज स्वीकार किया • बेड आरक्षित: १' : '🏥 HOSPITAL ACCEPTED • BED RESERVED: 1');
                syncEmergencyStatusAcrossConsoles('EM-28471', 'HOSPITAL ACCEPTED', 'BED CONFIRMED RESERVED (H-001)');
                showToast(lang === 'mr' ? "🚑 पायरी ११: रुग्णालयाने केस स्वीकारली (बेड राखीव: १)" : (lang === 'hi' ? "🚑 चरण ११: अस्पताल ने केस स्वीकार किया (बेड आरक्षित: १)" : "🚑 Step 11: Hospital Accepted Case (Bed Reserved: 1)"), "success");
                addAuditLogEntry("✓ Hospital H-001 Accepted Case (Emergency Bed Reserved: 1)");
                recordClockMilestone('hosp_accept');
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
                syncEmergencyStatusAcrossConsoles('EM-28471', 'RESOLVED', 'CASE RESOLVED');
                stopStopwatch();
                window.WariState.isSimulationRunning = false;
                showToast(lang === 'mr' ? "✅ पायरी १२: केस यशस्वीरित्या पूर्ण झाली! उपचार सुरू." : (lang === 'hi' ? "✅ चरण १२: केस सफलतापूर्वक पूरा हुआ! उपचार जारी." : "✅ Step 12: Case Resolved! Patient Admitted Successfully."), "success");
                addAuditLogEntry("✓ Patient Admitted to Emergency Ward");
                addAuditLogEntry("✓ Case Resolved & Telemetry Archived");
                recordClockMilestone('resolved');
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

    // =========================================================================
    // TRIAGE EMERGENCY TYPE & SEVERITY STATE MANAGERS
    // =========================================================================
    function updateTriageTypeUI(selectedType) {
        const typeButtons = document.querySelectorAll('#triage-type-selector .triage-pill');
        typeButtons.forEach(btn => {
            const btnType = btn.dataset.type || btn.textContent.trim();
            const isMatch = (btnType === selectedType) || (selectedType && btn.textContent.trim().toLowerCase().includes(selectedType.toLowerCase()));
            if (isMatch) {
                btn.classList.add('active');
                btn.style.setProperty('background', 'rgba(255, 82, 82, 0.22)', 'important');
                btn.style.setProperty('border-color', '#FF5252', 'important');
                btn.style.setProperty('color', '#FFFFFF', 'important');
            } else {
                btn.classList.remove('active');
                btn.style.setProperty('background', 'rgba(22, 27, 34, 0.85)', 'important');
                btn.style.setProperty('border-color', '#30363D', 'important');
                btn.style.setProperty('color', '#C9D1D9', 'important');
            }
        });
    }

    function updateTriageSeverityUI(selectedSev) {
        const sevButtons = document.querySelectorAll('#triage-sev-selector .triage-sev-btn');
        const sevUpper = (selectedSev || 'CRITICAL').toUpperCase();
        sevButtons.forEach(btn => {
            const btnSev = (btn.dataset.sev || btn.textContent.trim()).toUpperCase();
            if (btnSev === sevUpper || (btnSev.includes(sevUpper) || sevUpper.includes(btnSev))) {
                btn.classList.add('active');
                if (btnSev.includes('CRITICAL')) {
                    btn.style.setProperty('background', '#D32F2F', 'important');
                    btn.style.setProperty('border-color', '#FF5252', 'important');
                    btn.style.setProperty('color', '#FFFFFF', 'important');
                } else if (btnSev.includes('HIGH')) {
                    btn.style.setProperty('background', '#E65100', 'important');
                    btn.style.setProperty('border-color', '#FF9800', 'important');
                    btn.style.setProperty('color', '#FFFFFF', 'important');
                } else if (btnSev.includes('MODERATE')) {
                    btn.style.setProperty('background', '#F57F17', 'important');
                    btn.style.setProperty('border-color', '#FFD54F', 'important');
                    btn.style.setProperty('color', '#000000', 'important');
                } else if (btnSev.includes('LOW')) {
                    btn.style.setProperty('background', '#2E7D32', 'important');
                    btn.style.setProperty('border-color', '#4CAF50', 'important');
                    btn.style.setProperty('color', '#FFFFFF', 'important');
                }
            } else {
                btn.classList.remove('active');
                btn.style.setProperty('background', 'rgba(22, 27, 34, 0.85)', 'important');
                btn.style.setProperty('border-color', '#30363D', 'important');
                btn.style.setProperty('color', '#C9D1D9', 'important');
            }
        });
    }

    function initTriageSelectionHandlers() {
        if (!window.WariState.selectedTriageType) {
            window.WariState.selectedTriageType = 'Medical / Chest Pain';
        }
        if (!window.WariState.selectedTriageSeverity) {
            window.WariState.selectedTriageSeverity = 'CRITICAL';
        }

        const typeButtons = document.querySelectorAll('#triage-type-selector .triage-pill');
        typeButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                const chosenType = btn.dataset.type || btn.textContent.trim();
                window.WariState.selectedTriageType = chosenType;
                updateTriageTypeUI(chosenType);
            });
        });

        const sevButtons = document.querySelectorAll('#triage-sev-selector .triage-sev-btn');
        sevButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                const chosenSev = (btn.dataset.sev || btn.textContent.trim()).toUpperCase();
                window.WariState.selectedTriageSeverity = chosenSev;
                updateTriageSeverityUI(chosenSev);
            });
        });

        updateTriageTypeUI(window.WariState.selectedTriageType);
        updateTriageSeverityUI(window.WariState.selectedTriageSeverity);
    }

    window.updateTriageTypeUI = updateTriageTypeUI;
    window.updateTriageSeverityUI = updateTriageSeverityUI;
    window.initTriageSelectionHandlers = initTriageSelectionHandlers;

    // =========================================================================
    // PRIMARY CENTRAL SOS DISPATCH HANDLER (STEPS 1-4 AUTO, THEN HALTS)
    // =========================================================================
    function handleSOS() {
        clearSimulationTimers();
        window.WariState.isSimulationRunning = true;
        window.WariState.currentEmergencyId = 'EM-28471';
        window.WariState.demoEmergencyStage = 1;

        const chosenSource = window.WariState.currentEmergencySource || "MAIN SOS";
        const wariId = window.WariState.currentWariId || "WS-28471";
        const patientName = window.WariState.currentUserName || "Tukaram Shinde";
        const chosenType = window.WariState.selectedTriageType || "Medical / Chest Pain";
        const chosenSeverity = (window.WariState.selectedTriageSeverity || "CRITICAL").toUpperCase();

        const activeEmergency = {
            id: "EM-28471",
            emergency_id: "EM-28471",
            wristbandId: "WS-28471",
            wari_id: wariId,
            patientName: patientName,
            patient_name: patientName,
            phone: "+91 98221 28471",
            emergencyContact: "+91 98220 99881",
            emergency_contact: "+91 98220 99881",
            bloodGroup: "B+",
            blood_group: "B+",
            emergencyType: chosenType,
            emergency_type: chosenType,
            severity: chosenSeverity,
            source: chosenSource,
            source_type: chosenSource,
            latitude: 18.3444,
            longitude: 74.0305,
            zone: "Zone 04 — Saswad Palkhi Maidan",
            wari_zone: "Zone 04 — Saswad Palkhi Maidan",
            status: "CREATED",
            currentStage: 1,
            assignedVolunteerId: null,
            assigned_volunteer_id: null,
            volunteerStatus: "WAITING",
            volunteer_status: "WAITING",
            assignedHospitalId: null,
            assigned_hospital_id: null,
            hospitalStatus: "WAITING",
            hospital_status: "WAITING",
            currentStage: 4,
            timestamp: Date.now()
        };

        window.WariState.activeEmergency = activeEmergency;
        try {
            localStorage.setItem('wariseva_shared_emergency_state', JSON.stringify(activeEmergency));
            if (typeof BroadcastChannel !== 'undefined') {
                const bc = new BroadcastChannel('wariseva_emergency_channel');
                bc.postMessage({ type: 'SOS_CREATED', emergency: activeEmergency });
                bc.close();
            }
        } catch (e) {}

        // Switch to Emergency View immediately & start stopwatch
        switchView('emergency-view');
        startStopwatch();

        initEmergencyMap();
        syncEmergencyUI('EM-28471');
        document.getElementById('coordination-complete-card')?.classList.add('hidden');
        document.getElementById('reached-confirmed-banner')?.classList.add('hidden');
        document.getElementById('hosp-resolved-banner')?.classList.add('hidden');

        // Reset Volunteer and Hospital button states
        const volAcceptBtn = document.getElementById('vol-accept-em-btn');
        if (volAcceptBtn) {
            volAcceptBtn.textContent = '[ ACCEPT CASE ]';
            volAcceptBtn.disabled = false;
            volAcceptBtn.style.opacity = '1';
        }
        const hospAcceptBtn = document.getElementById('hosp-accept-case-btn');
        if (hospAcceptBtn) {
            hospAcceptBtn.textContent = '🏥 ACCEPT CASE (RESERVE BED)';
            hospAcceptBtn.disabled = false;
            hospAcceptBtn.style.opacity = '1';
        }
        const hospAdmitBtn = document.getElementById('hosp-mark-admitted-btn');
        if (hospAdmitBtn) {
            hospAdmitBtn.textContent = '✅ MARK PATIENT ADMITTED';
            hospAdmitBtn.disabled = false;
            hospAdmitBtn.style.opacity = '1';
        }

        fetch('/api/demo/create-emergency', { method: 'POST' }).catch(() => {});

        // Step 1: Immediately ACTIVE
        setDemoEmergencyStage(1);

        // Step 2: After 1.2s
        const t1 = setTimeout(() => {
            if (window.WariState.activeEmergency) window.WariState.activeEmergency.currentStage = 2;
            setDemoEmergencyStage(2);
        }, 1200);

        // Step 3: After 2.4s
        const t2 = setTimeout(() => {
            if (window.WariState.activeEmergency) window.WariState.activeEmergency.currentStage = 3;
            setDemoEmergencyStage(3);
        }, 2400);

        // Step 4: After 3.6s
        const t3 = setTimeout(() => {
            if (window.WariState.activeEmergency) window.WariState.activeEmergency.currentStage = 4;
            setDemoEmergencyStage(4);
        }, 3600);

        // Step 5: At 4.8s -> WAITING FOR HUMAN ACTION! (NO AUTO-ADVANCE)
        const t4 = setTimeout(() => {
            setDemoEmergencyStage(5);
            if (window.WariState.activeEmergency) {
                window.WariState.activeEmergency.currentStage = 5;
                window.WariState.activeEmergency.status = 'WAITING_FOR_VOLUNTEER';
            }
        }, 4800);

        window.WariState.simulationTimers.push(t1, t2, t3, t4);
    }

    // =========================================================================
    // VOLUNTEER & HOSPITAL HUMAN ACTIONS (REAL BUTTONS, NO TIMERS)
    // =========================================================================
    function handleVolunteerAccept() {
        if (!window.WariState.activeEmergency) {
            handleSOS();
        }
        clearSimulationTimers();

        if (window.WariState.activeEmergency) {
            window.WariState.activeEmergency.assignedVolunteerId = 'V-001';
            window.WariState.activeEmergency.assigned_volunteer_id = 'V-001';
            window.WariState.activeEmergency.volunteerStatus = 'ACCEPTED';
            window.WariState.activeEmergency.volunteer_status = 'ACCEPTED';
            window.WariState.activeEmergency.status = 'VOLUNTEER_ACCEPTED';
            window.WariState.activeEmergency.currentStage = 7;
            try {
                localStorage.setItem('wariseva_shared_emergency_state', JSON.stringify(window.WariState.activeEmergency));
                if (typeof BroadcastChannel !== 'undefined') {
                    const bc = new BroadcastChannel('wariseva_emergency_channel');
                    bc.postMessage({ type: 'VOLUNTEER_ACCEPTED', emergency: window.WariState.activeEmergency });
                    bc.close();
                }
            } catch(e) {}
        }

        fetch('/api/emergency/EM-28471/volunteer/accept', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ volunteer_id: 'V-001' })
        }).catch(() => {});

        setDemoEmergencyStage(7);

        const volAcceptBtn = document.getElementById('vol-accept-em-btn');
        if (volAcceptBtn) {
            volAcceptBtn.textContent = '✓ CASE ACCEPTED';
            volAcceptBtn.disabled = true;
            volAcceptBtn.style.opacity = '0.6';
        }
        const volBadge = document.getElementById('vol-response-badge');
        if (volBadge) {
            volBadge.textContent = '🟢 STATUS: EN ROUTE';
        }
    }

    function handleVolunteerEnRoute() {
        if (!window.WariState.activeEmergency) return;
        clearSimulationTimers();

        window.WariState.activeEmergency.volunteerStatus = 'EN_ROUTE';
        window.WariState.activeEmergency.volunteer_status = 'EN_ROUTE';
        window.WariState.activeEmergency.status = 'EN_ROUTE';
        window.WariState.activeEmergency.currentStage = 8;
        try {
            localStorage.setItem('wariseva_shared_emergency_state', JSON.stringify(window.WariState.activeEmergency));
            if (typeof BroadcastChannel !== 'undefined') {
                const bc = new BroadcastChannel('wariseva_emergency_channel');
                bc.postMessage({ type: 'VOLUNTEER_ENROUTE', emergency: window.WariState.activeEmergency });
                bc.close();
            }
        } catch(e) {}

        fetch('/api/emergency/EM-28471/volunteer-enroute', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ volunteer_id: 'V-001' })
        }).catch(() => {});

        setDemoEmergencyStage(8);
        const respBtn = document.getElementById('resp-start-response-btn');
        if (respBtn) {
            respBtn.textContent = '✓ EN ROUTE';
            respBtn.disabled = true;
            respBtn.style.opacity = '0.6';
        }
        const volRespBtn = document.getElementById('vol-start-response-btn');
        if (volRespBtn) {
            volRespBtn.textContent = '✓ EN ROUTE';
            volRespBtn.disabled = true;
            volRespBtn.style.opacity = '0.6';
        }
    }

    function handleVolunteerArrived() {
        if (!window.WariState.activeEmergency) return;
        clearSimulationTimers();

        window.WariState.activeEmergency.volunteerStatus = 'ARRIVED';
        window.WariState.activeEmergency.volunteer_status = 'ARRIVED';
        window.WariState.activeEmergency.status = 'VOLUNTEER_ARRIVED';
        window.WariState.activeEmergency.currentStage = 9;
        try {
            localStorage.setItem('wariseva_shared_emergency_state', JSON.stringify(window.WariState.activeEmergency));
            if (typeof BroadcastChannel !== 'undefined') {
                const bc = new BroadcastChannel('wariseva_emergency_channel');
                bc.postMessage({ type: 'VOLUNTEER_ARRIVED', emergency: window.WariState.activeEmergency });
                bc.close();
            }
        } catch(e) {}

        fetch('/api/volunteer/reached', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ volunteer_id: 'V-001', emergency_id: 'EM-28471' })
        }).catch(() => {});

        setDemoEmergencyStage(9);
        const reachBtn = document.getElementById('reached-patient-btn');
        if (reachBtn) {
            reachBtn.textContent = '✓ WITH PATIENT';
            reachBtn.disabled = true;
            reachBtn.style.opacity = '0.6';
        }
        document.getElementById('reached-confirmed-banner')?.classList.remove('hidden');
    }

    function handleHospitalAccept() {
        if (!window.WariState.activeEmergency) {
            handleSOS();
        }
        clearSimulationTimers();

        if (window.WariState.activeEmergency) {
            window.WariState.activeEmergency.assignedHospitalId = 'H-001';
            window.WariState.activeEmergency.assigned_hospital_id = 'H-001';
            window.WariState.activeEmergency.hospitalStatus = 'ACCEPTED';
            window.WariState.activeEmergency.hospital_status = 'ACCEPTED';
            window.WariState.activeEmergency.status = 'HOSPITAL_ACCEPTED';
            window.WariState.activeEmergency.currentStage = 11;
            try {
                localStorage.setItem('wariseva_shared_emergency_state', JSON.stringify(window.WariState.activeEmergency));
                if (typeof BroadcastChannel !== 'undefined') {
                    const bc = new BroadcastChannel('wariseva_emergency_channel');
                    bc.postMessage({ type: 'HOSPITAL_ACCEPTED', emergency: window.WariState.activeEmergency });
                    bc.close();
                }
            } catch(e) {}
        }

        fetch('/api/emergency/EM-28471/responder/accept', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ hospital_id: 'H-001', responder_id: 'H-001' })
        }).catch(() => {});

        setDemoEmergencyStage(11);

        const hospBtn = document.getElementById('hosp-accept-case-btn');
        if (hospBtn) {
            hospBtn.textContent = '✓ BED RESERVED (H-001)';
            hospBtn.disabled = true;
            hospBtn.style.opacity = '0.6';
        }
    }

    function handleHospitalTransfer() {
        if (!window.WariState.activeEmergency) return;
        clearSimulationTimers();

        window.WariState.activeEmergency.hospitalStatus = 'TRANSFERRED';
        window.WariState.activeEmergency.hospital_status = 'TRANSFERRED';
        window.WariState.activeEmergency.status = 'HOSPITAL_TRANSFER';
        window.WariState.activeEmergency.currentStage = 11;
        try {
            localStorage.setItem('wariseva_shared_emergency_state', JSON.stringify(window.WariState.activeEmergency));
            if (typeof BroadcastChannel !== 'undefined') {
                const bc = new BroadcastChannel('wariseva_emergency_channel');
                bc.postMessage({ type: 'HOSPITAL_TRANSFER', emergency: window.WariState.activeEmergency });
                bc.close();
            }
        } catch(e) {}

        fetch('/api/emergency/EM-28471/transfer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        }).catch(() => {});

        setDemoEmergencyStage(11);
    }

    function handleHospitalAdmit() {
        if (!window.WariState.activeEmergency) return;
        clearSimulationTimers();

        window.WariState.activeEmergency.status = 'RESOLVED';
        window.WariState.activeEmergency.currentStage = 12;
        try {
            localStorage.setItem('wariseva_shared_emergency_state', JSON.stringify(window.WariState.activeEmergency));
            if (typeof BroadcastChannel !== 'undefined') {
                const bc = new BroadcastChannel('wariseva_emergency_channel');
                bc.postMessage({ type: 'EMERGENCY_RESOLVED', emergency: window.WariState.activeEmergency });
                bc.close();
            }
        } catch(e) {}

        fetch('/api/emergency/EM-28471/resolve', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ responder_id: 'H-001', notes: 'Patient admitted to trauma center' })
        }).catch(() => {});

        setDemoEmergencyStage(12);

        document.getElementById('hosp-resolved-banner')?.classList.remove('hidden');
        const admitBtn = document.getElementById('hosp-mark-admitted-btn');
        if (admitBtn) {
            admitBtn.textContent = '✓ CASE RESOLVED';
            admitBtn.disabled = true;
            admitBtn.style.opacity = '0.6';
        }
    }

    function handleHospitalPatientArrived() {
        if (!window.WariState.activeEmergency) return;
        clearSimulationTimers();

        window.WariState.activeEmergency.status = 'PATIENT_ARRIVED';
        window.WariState.activeEmergency.currentStage = 11;
        try {
            localStorage.setItem('wariseva_shared_emergency_state', JSON.stringify(window.WariState.activeEmergency));
            if (typeof BroadcastChannel !== 'undefined') {
                const bc = new BroadcastChannel('wariseva_emergency_channel');
                bc.postMessage({ type: 'PATIENT_ARRIVED', emergency: window.WariState.activeEmergency });
                bc.close();
            }
        } catch(e) {}

        fetch('/api/emergency/EM-28471/transfer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ hospital_id: 'H-001' })
        }).catch(() => {});

        setDemoEmergencyStage(11);
        document.getElementById('resp-arrived-banner')?.classList.remove('hidden');
        const arrivedBtn = document.getElementById('hosp-patient-arrived-btn');
        if (arrivedBtn) {
            arrivedBtn.textContent = '✓ PATIENT ARRIVED';
            arrivedBtn.disabled = true;
            arrivedBtn.style.opacity = '0.6';
        }
        showToast("📍 Hospital: Patient Arrived at Medical Facility.", "success");
    }

    function handleHospitalTreatmentStarted() {
        if (!window.WariState.activeEmergency) return;
        clearSimulationTimers();

        window.WariState.activeEmergency.status = 'TREATMENT_STARTED';
        window.WariState.activeEmergency.currentStage = 11;
        try {
            localStorage.setItem('wariseva_shared_emergency_state', JSON.stringify(window.WariState.activeEmergency));
            if (typeof BroadcastChannel !== 'undefined') {
                const bc = new BroadcastChannel('wariseva_emergency_channel');
                bc.postMessage({ type: 'TREATMENT_STARTED', emergency: window.WariState.activeEmergency });
                bc.close();
            }
        } catch(e) {}

        const banner = document.getElementById('resp-arrived-banner');
        if (banner) {
            banner.textContent = '🩺 Clinical triage & treatment actively in progress. Vital signs stabilizing.';
            banner.classList.remove('hidden');
        }
        const treatBtn = document.getElementById('hosp-treatment-started-btn');
        if (treatBtn) {
            treatBtn.textContent = '✓ TREATMENT IN PROGRESS';
            treatBtn.disabled = true;
            treatBtn.style.opacity = '0.6';
        }
        showToast("🩺 Hospital: Treatment Started — Inhaler & Oxygen Administered.", "success");
    }

    function applySharedEmergencyState(em) {
        if (!em) return;
        const status = (em.status || '').toUpperCase();
        const stage = em.currentStage || em.stage || 1;
        const volStatus = (em.volunteer_status || em.volunteerStatus || '').toUpperCase();
        const hospStatus = (em.hospital_status || em.hospitalStatus || '').toUpperCase();

        if (status === 'RESOLVED' || stage === 12) {
            setDemoEmergencyStage(12);
            return;
        }

        if (hospStatus === 'ACCEPTED' || status === 'HOSPITAL_ACCEPTED' || stage === 11 || stage === 10) {
            setDemoEmergencyStage(10);
            const hospBtn = document.getElementById('hosp-accept-case-btn');
            if (hospBtn) {
                hospBtn.textContent = '✓ PATIENT ACCEPTED (BED RESERVED)';
                hospBtn.disabled = true;
                hospBtn.style.opacity = '0.6';
            }
            const bedStatus = document.getElementById('hosp-bed-status');
            if (bedStatus) {
                bedStatus.textContent = '1 RESERVED';
                bedStatus.style.color = '#FFD600';
            }
            return;
        }

        if (volStatus === 'ARRIVED' || status === 'VOLUNTEER_ARRIVED' || stage === 9) {
            setDemoEmergencyStage(9);
            return;
        }

        if (volStatus === 'EN_ROUTE' || status === 'EN_ROUTE' || stage === 8) {
            setDemoEmergencyStage(8);
            const respBtn = document.getElementById('vol-start-response-btn');
            if (respBtn) {
                respBtn.textContent = '✓ EN ROUTE';
                respBtn.disabled = true;
                respBtn.style.opacity = '0.6';
            }
            return;
        }

        if (volStatus === 'ACCEPTED' || status === 'VOLUNTEER_ACCEPTED' || stage === 7) {
            setDemoEmergencyStage(7);
            const volAcceptBtn = document.getElementById('vol-accept-em-btn');
            if (volAcceptBtn) {
                volAcceptBtn.textContent = '✓ CASE ACCEPTED';
                volAcceptBtn.disabled = true;
                volAcceptBtn.style.opacity = '0.6';
            }
            return;
        }

        if (status === 'CREATED' || status === 'ACTIVE' || stage >= 1) {
            setDemoEmergencyStage(Math.min(stage, 6));
        }
    }

    function initAuthGates() {
        // 1. Volunteer Auth State
        const checkVolAuth = () => {
            const auth = sessionStorage.getItem('wariseva_volunteer_auth');
            const gate = document.getElementById('vol-auth-gate-card');
            const dash = document.getElementById('volunteer-dashboard-content');
            if (auth) {
                try {
                    const parsed = JSON.parse(auth);
                    if (gate) gate.classList.add('hidden');
                    if (dash) dash.classList.remove('hidden');
                    const nameEl = document.getElementById('vol-dash-name');
                    if (nameEl && parsed.name) {
                        nameEl.innerHTML = `${parsed.name} (${parsed.id || 'V-001'}) <span class="verified-pill">✓ VERIFIED</span>`;
                    }
                    initVolunteerMap();
                } catch(e) {}
            } else {
                if (gate) gate.classList.remove('hidden');
                if (dash) dash.classList.add('hidden');
            }
        };

        // 2. Hospital Auth State
        const checkHospAuth = () => {
            const auth = sessionStorage.getItem('wariseva_hospital_auth');
            const gate = document.getElementById('hosp-auth-gate-card');
            const dash = document.getElementById('hospital-dashboard-content');
            if (auth) {
                if (gate) gate.classList.add('hidden');
                if (dash) dash.classList.remove('hidden');
                initResponderMap();
            } else {
                if (gate) gate.classList.remove('hidden');
                if (dash) dash.classList.add('hidden');
            }
        };

        // 3. Command Center Auth State
        const checkCommandAuth = () => {
            const auth = sessionStorage.getItem('wariseva_command_auth');
            const gate = document.getElementById('cmd-auth-gate-card');
            const dash = document.getElementById('command-dashboard-content');
            if (auth) {
                if (gate) gate.classList.add('hidden');
                if (dash) dash.classList.remove('hidden');
                initCommandMap();
                loadCommandIncidentsList();
            } else {
                if (gate) gate.classList.remove('hidden');
                if (dash) dash.classList.add('hidden');
            }
        };
        window.checkCommandAuth = checkCommandAuth;

        checkVolAuth();
        checkHospAuth();
        checkCommandAuth();

        // 4. Quick-fill buttons
        document.getElementById('vol-quick-fill-btn')?.addEventListener('click', () => {
            const idInput = document.getElementById('vol-spa-login-id');
            const passInput = document.getElementById('vol-spa-login-pass');
            if (idInput) idInput.value = 'V-001';
            if (passInput) passInput.value = '1234';
        });

        document.getElementById('hosp-quick-fill-btn')?.addEventListener('click', () => {
            const idInput = document.getElementById('hosp-spa-login-id');
            const passInput = document.getElementById('hosp-spa-login-pass');
            if (idInput) idInput.value = 'MF-001';
            if (passInput) passInput.value = '1234';
        });

        document.getElementById('cmd-quick-fill-btn')?.addEventListener('click', () => {
            const userInput = document.getElementById('cmd-spa-login-user');
            const passInput = document.getElementById('cmd-spa-login-pass');
            if (userInput) userInput.value = 'admin';
            if (passInput) passInput.value = 'admin123';
        });

        // 4. Volunteer In-App Login
        const performVolunteerLogin = () => {
            const id = (document.getElementById('vol-spa-login-id')?.value || '').trim();
            const password = (document.getElementById('vol-spa-login-pass')?.value || '').trim();
            const errEl = document.getElementById('vol-spa-login-error');
            const succEl = document.getElementById('vol-spa-login-success');

            if (succEl) succEl.classList.add('hidden');
            if (errEl) errEl.classList.add('hidden');

            if (!id || !password) {
                if (errEl) {
                    errEl.textContent = '❌ Invalid Volunteer ID or Password';
                    errEl.classList.remove('hidden');
                }
                return;
            }

            fetch('/api/auth/volunteer/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ volunteer_id: id, password: password })
            })
            .then(res => res.json().then(data => ({ status: res.status, body: data })))
            .then(({ status, body }) => {
                if (status === 200 && body.success) {
                    if (errEl) errEl.classList.add('hidden');
                    if (succEl) {
                        succEl.textContent = '✓ Authentication Successful';
                        succEl.classList.remove('hidden');
                    }
                    sessionStorage.setItem('wariseva_volunteer_auth', JSON.stringify(body.volunteer || { id: id || 'V-001', name: 'Ramesh Kulkarni' }));
                    window.WariState.volunteerAuth.isLoggedIn = true;
                    setTimeout(() => {
                        checkVolAuth();
                        initVolunteerMap();
                        loadVolunteerEmergencyFeed();
                        showToast(`✓ Authentication Successful — Welcome, ${body.volunteer ? body.volunteer.name : 'Ramesh Kulkarni'}!`, 'success');
                    }, 350);
                } else {
                    if (succEl) succEl.classList.add('hidden');
                    if (errEl) {
                        errEl.textContent = '❌ Invalid Volunteer ID or Password';
                        errEl.classList.remove('hidden');
                    }
                    showToast('❌ Invalid Volunteer ID or Password', 'error');
                }
            })
            .catch(() => {
                if (succEl) succEl.classList.add('hidden');
                if (errEl) {
                    errEl.textContent = '❌ Invalid Volunteer ID or Password';
                    errEl.classList.remove('hidden');
                }
                showToast('❌ Invalid Volunteer ID or Password', 'error');
            });
        };

        document.getElementById('vol-spa-login-btn')?.addEventListener('click', performVolunteerLogin);
        document.getElementById('vol-spa-login-form')?.addEventListener('submit', (e) => {
            e.preventDefault();
            performVolunteerLogin();
        });

        // 5. Volunteer In-App Logout
        document.getElementById('vol-spa-logout-btn')?.addEventListener('click', () => {
            sessionStorage.removeItem('wariseva_volunteer_auth');
            checkVolAuth();
            showToast('🚪 Volunteer logged out.', 'info');
        });

        // 6. Hospital In-App Login
        const performHospitalLogin = () => {
            const id = (document.getElementById('hosp-spa-login-id')?.value || '').trim();
            const password = (document.getElementById('hosp-spa-login-pass')?.value || '').trim();
            const errEl = document.getElementById('hosp-spa-login-error');
            const succEl = document.getElementById('hosp-spa-login-success');

            if (succEl) succEl.classList.add('hidden');
            if (errEl) errEl.classList.add('hidden');

            if (!id || !password) {
                if (errEl) {
                    errEl.textContent = '❌ Invalid Facility ID or Password';
                    errEl.classList.remove('hidden');
                }
                return;
            }

            fetch('/api/auth/hospital/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ facility_id: id, password: password })
            })
            .then(res => res.json().then(data => ({ status: res.status, body: data })))
            .then(({ status, body }) => {
                if (status === 200 && body.success) {
                    if (errEl) errEl.classList.add('hidden');
                    if (succEl) {
                        succEl.textContent = '✓ Authentication Successful';
                        succEl.classList.remove('hidden');
                    }
                    sessionStorage.setItem('wariseva_hospital_auth', JSON.stringify(body.hospital || { id: id || 'MF-001', name: 'WariSeva Medical Camp — Zone 04' }));
                    setTimeout(() => {
                        checkHospAuth();
                        loadResponderEmergencyFeed();
                        initResponderMap();
                        showToast(`✓ Authentication Successful — Welcome, ${body.hospital ? body.hospital.name : 'Medical Facility'}!`, 'success');
                    }, 350);
                } else {
                    if (succEl) succEl.classList.add('hidden');
                    if (errEl) {
                        errEl.textContent = '❌ Invalid Facility ID or Password';
                        errEl.classList.remove('hidden');
                    }
                    showToast('❌ Invalid Facility ID or Password', 'error');
                }
            })
            .catch(() => {
                if (succEl) succEl.classList.add('hidden');
                if (errEl) {
                    errEl.textContent = '❌ Invalid Facility ID or Password';
                    errEl.classList.remove('hidden');
                }
                showToast('❌ Invalid Facility ID or Password', 'error');
            });
        };

        document.getElementById('hosp-spa-login-btn')?.addEventListener('click', performHospitalLogin);
        document.getElementById('hosp-spa-login-form')?.addEventListener('submit', (e) => {
            e.preventDefault();
            performHospitalLogin();
        });

        // 7. Hospital In-App Logout
        document.getElementById('hosp-spa-logout-btn')?.addEventListener('click', () => {
            sessionStorage.removeItem('wariseva_hospital_auth');
            checkHospAuth();
            showToast('🚪 Medical Facility logged out.', 'info');
        });

        // 8. Command Center In-App Login
        const performCommandLogin = () => {
            const user = (document.getElementById('cmd-spa-login-user')?.value || '').trim();
            const password = (document.getElementById('cmd-spa-login-pass')?.value || '').trim();
            const errEl = document.getElementById('cmd-spa-login-error');
            const succEl = document.getElementById('cmd-spa-login-success');

            if (succEl) succEl.classList.add('hidden');
            if (errEl) errEl.classList.add('hidden');

            if (!user || !password) {
                if (errEl) {
                    errEl.innerHTML = '❌ Invalid username or password<br><span style="font-size: 0.8rem; opacity: 0.9;">Please try again.</span>';
                    errEl.classList.remove('hidden');
                }
                showToast('❌ Invalid username or password', 'error');
                return;
            }

            fetch('/api/auth/command/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: user, password: password })
            })
            .then(res => res.json().then(data => ({ status: res.status, body: data })))
            .then(({ status, body }) => {
                if (status === 200 && body.success) {
                    if (errEl) errEl.classList.add('hidden');
                    if (succEl) {
                        succEl.textContent = '✓ Login Successful';
                        succEl.classList.remove('hidden');
                    }
                    sessionStorage.setItem('wariseva_command_auth', JSON.stringify(body.user || { username: 'admin', role: 'COMMAND_OPERATOR' }));
                    setTimeout(() => {
                        checkCommandAuth();
                        if (window.WariState.maps.command) {
                            scheduleMapInvalidate(window.WariState.maps.command, document.getElementById('command-map'));
                        }
                        showToast('✓ Login Successful — Welcome to Command Center!', 'success');
                    }, 300);
                } else {
                    if (succEl) succEl.classList.add('hidden');
                    if (errEl) {
                        errEl.innerHTML = '❌ Invalid username or password<br><span style="font-size: 0.8rem; opacity: 0.9;">Please try again.</span>';
                        errEl.classList.remove('hidden');
                    }
                    showToast('❌ Invalid username or password', 'error');
                }
            })
            .catch(() => {
                // Client-side fallback check
                if (user.toLowerCase() === 'admin' && password === 'admin123') {
                    if (errEl) errEl.classList.add('hidden');
                    if (succEl) {
                        succEl.textContent = '✓ Login Successful';
                        succEl.classList.remove('hidden');
                    }
                    sessionStorage.setItem('wariseva_command_auth', JSON.stringify({ username: 'admin', role: 'COMMAND_OPERATOR' }));
                    setTimeout(() => {
                        checkCommandAuth();
                        if (window.WariState.maps.command) {
                            scheduleMapInvalidate(window.WariState.maps.command, document.getElementById('command-map'));
                        }
                        showToast('✓ Login Successful', 'success');
                    }, 300);
                } else {
                    if (succEl) succEl.classList.add('hidden');
                    if (errEl) {
                        errEl.innerHTML = '❌ Invalid username or password<br><span style="font-size: 0.8rem; opacity: 0.9;">Please try again.</span>';
                        errEl.classList.remove('hidden');
                    }
                    showToast('❌ Invalid username or password', 'error');
                }
            });
        };

        document.getElementById('cmd-spa-login-btn')?.addEventListener('click', performCommandLogin);
        document.getElementById('cmd-spa-login-form')?.addEventListener('submit', (e) => {
            e.preventDefault();
            performCommandLogin();
        });

        // 9. Command Center In-App Logout
        document.getElementById('cmd-spa-logout-btn')?.addEventListener('click', () => {
            sessionStorage.removeItem('wariseva_command_auth');
            fetch('/api/auth/command/logout', { method: 'POST' }).catch(() => {});
            checkCommandAuth();
            const userInput = document.getElementById('cmd-spa-login-user');
            const passInput = document.getElementById('cmd-spa-login-pass');
            if (userInput) userInput.value = '';
            if (passInput) passInput.value = '';
            const errEl = document.getElementById('cmd-spa-login-error');
            const succEl = document.getElementById('cmd-spa-login-success');
            if (errEl) errEl.classList.add('hidden');
            if (succEl) succEl.classList.add('hidden');
            showToast('🚪 Command Center logged out. Session secured.', 'info');
        });
    }

    window.handleVolunteerAccept = handleVolunteerAccept;
    window.handleVolunteerEnRoute = handleVolunteerEnRoute;
    window.handleVolunteerArrived = handleVolunteerArrived;
    window.handleHospitalAccept = handleHospitalAccept;
    window.handleHospitalTransfer = handleHospitalTransfer;
    window.handleHospitalPatientArrived = handleHospitalPatientArrived;
    window.handleHospitalTreatmentStarted = handleHospitalTreatmentStarted;
    window.handleHospitalAdmit = handleHospitalAdmit;
    window.initAuthGates = initAuthGates;
    window.initVolunteerMap = initVolunteerMap;
    window.initResponderMap = initResponderMap;
    window.renderLiveCrowdAwareNavigationMap = renderLiveCrowdAwareNavigationMap;
    window.syncEmergencyStatusAcrossConsoles = syncEmergencyStatusAcrossConsoles;
    window.initHomeSafetyMap = initHomeSafetyMap;
    window.loadSafetyMapMarkers = loadSafetyMapMarkers;

    // Explainable AI & Inspector Modals
    function closeAllModals() {
        document.querySelectorAll('.modal-overlay').forEach(m => m.classList.add('hidden'));
    }

    function openWhyResponderModal(volId) {
        const modal = document.getElementById('why-responder-modal');
        if (!modal) return;
        if (volId === 'V-001') {
            const nameEl = document.getElementById('wr-name');
            if (nameEl) nameEl.textContent = 'Ramesh Kulkarni (V-001)';
            const scoreEl = document.getElementById('wr-score');
            if (scoreEl) scoreEl.textContent = '94';
        }
        modal.classList.remove('hidden');
    }

    function openWhyFacilityModal(facilityId) {
        const modal = document.getElementById('why-facility-modal');
        if (!modal) return;
        if (facilityId === 'H-001') {
            const nameEl = document.getElementById('wf-name');
            if (nameEl) nameEl.textContent = 'Saswad Rural Sub-District Hospital (H-001)';
            const scoreEl = document.getElementById('wf-score');
            if (scoreEl) scoreEl.textContent = '92';
        }
        modal.classList.remove('hidden');
    }

    function openVolunteerInspector(volId) {
        const modal = document.getElementById('vol-detail-modal');
        if (!modal) return;
        modal.classList.remove('hidden');
    }

    function openHospitalInspector(hospId) {
        const modal = document.getElementById('hosp-detail-modal');
        if (!modal) return;
        modal.classList.remove('hidden');
    }

    function suspendVolunteerFromModal() {
        showToast('Volunteer status updated to STANDBY', 'info');
        closeAllModals();
    }

    function suspendHospitalFromModal() {
        showToast('Hospital status updated', 'info');
        closeAllModals();
    }

    window.closeAllModals = closeAllModals;
    window.openWhyResponderModal = openWhyResponderModal;
    window.openWhyFacilityModal = openWhyFacilityModal;
    window.openVolunteerInspector = openVolunteerInspector;
    window.openHospitalInspector = openHospitalInspector;
    window.suspendVolunteerFromModal = suspendVolunteerFromModal;
    window.suspendHospitalFromModal = suspendHospitalFromModal;

    // Demo Mode Role Switcher
    function setupDemoRoleSwitcher() {
        const roles = [
            { id: 'role-btn-warkari', view: 'home-view' },
            { id: 'role-btn-volunteer', view: 'volunteer-view' },
            { id: 'role-btn-hospital', view: 'responder-view' },
            { id: 'role-btn-command', view: 'command-view' }
        ];

        roles.forEach(r => {
            const btn = document.getElementById(r.id);
            if (!btn) return;
            btn.addEventListener('click', () => {
                document.querySelectorAll('.demo-role-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                if (r.id === 'role-btn-warkari') {
                    if (window.WariState.activeEmergency && window.WariState.activeEmergency.status !== 'RESOLVED') {
                        switchView('emergency-view');
                    } else {
                        switchView('home-view');
                    }
                } else {
                    switchView(r.view);
                }
            });
        });
    }

    // =========================================================================
    // RESET DEMO TO CLEAN INITIAL STANDBY
    // =========================================================================
    function resetDemo() {
        clearSimulationTimers();
        window.WariState.isSimulationRunning = false;
        window.WariState.currentEmergencyId = null;
        window.WariState.demoEmergencyStage = 0;
        window.WariState.activeEmergency = null;
        window.WariState.selectedTriageType = 'Medical / Chest Pain';
        window.WariState.selectedTriageSeverity = 'CRITICAL';
        updateTriageTypeUI('Medical / Chest Pain');
        updateTriageSeverityUI('CRITICAL');
        stopStopwatch();

        try {
            localStorage.removeItem('wariseva_shared_emergency_state');
            if (typeof BroadcastChannel !== 'undefined') {
                const bc = new BroadcastChannel('wariseva_emergency_channel');
                bc.postMessage({ type: 'DEMO_RESET' });
                bc.close();
            }
        } catch(e) {}

        fetch('/api/demo/reset', { method: 'POST' }).catch(() => {});

        for (let i = 1; i <= 12; i++) {
            setTimelineStep(i, false, false);
        }

        document.getElementById('home-active-emergency-banner')?.classList.add('hidden');
        document.getElementById('header-em-badge')?.classList.add('hidden');
        document.getElementById('coordination-complete-card')?.classList.add('hidden');
        document.getElementById('reached-confirmed-banner')?.classList.add('hidden');
        document.getElementById('hosp-resolved-banner')?.classList.add('hidden');

        const volAcceptBtn = document.getElementById('vol-accept-em-btn');
        if (volAcceptBtn) {
            volAcceptBtn.textContent = '[ ACCEPT CASE ]';
            volAcceptBtn.disabled = false;
            volAcceptBtn.style.opacity = '1';
        }
        const hospBtn = document.getElementById('hosp-accept-case-btn');
        if (hospBtn) {
            hospBtn.textContent = '🏥 ACCEPT CASE (RESERVE BED)';
            hospBtn.disabled = false;
            hospBtn.style.opacity = '1';
        }
        const admitBtn = document.getElementById('hosp-mark-admitted-btn');
        if (admitBtn) {
            admitBtn.textContent = '✅ MARK PATIENT ADMITTED';
            admitBtn.disabled = false;
            admitBtn.style.opacity = '1';
        }

        const emStatusTitle = document.getElementById('em-current-status-title');
        if (emStatusTitle) emStatusTitle.textContent = 'STANDBY';

        document.querySelectorAll('.demo-role-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('role-btn-warkari')?.classList.add('active');

        switchView('home-view');
        showToast("🔄 Demo reset cleanly.", "info");
    }

    function runFullSimulation() {
        handleSOS();
    }

    function initSharedEmergencySync() {
        // 1. Cross-tab BroadcastChannel
        try {
            if (typeof BroadcastChannel !== 'undefined') {
                emergencyChannel = new BroadcastChannel('wariseva_emergency_channel');
                emergencyChannel.onmessage = (event) => {
                    if (event.data && event.data.emergency) {
                        applySharedEmergencyState(event.data.emergency);
                    } else if (event.data && event.data.type === 'RESET') {
                        resetDemo();
                    }
                };
            }
        } catch (e) {}

        // 2. localStorage StorageEvent for cross-tab sync
        window.addEventListener('storage', (e) => {
            if (e.key === 'wariseva_shared_emergency_state' && e.newValue) {
                try {
                    const parsed = JSON.parse(e.newValue);
                    applySharedEmergencyState(parsed);
                } catch (err) {}
            } else if (e.key === 'wariseva_shared_emergency_state' && !e.newValue) {
                resetDemo();
            }
        });

        // 3. Short polling loop for backend sync (every 800ms)
        if (sharedStateSyncTimer) clearInterval(sharedStateSyncTimer);
        sharedStateSyncTimer = setInterval(() => {
            const emId = window.WariState.currentEmergencyId || 'EM-28471';
            fetch(`/api/public/emergency-status/${emId}`)
                .then(res => res.json())
                .then(data => {
                    if (data.success && data.status) {
                        applySharedEmergencyState({
                            id: data.emergency_id,
                            status: data.status,
                            volunteerId: data.assigned_volunteer,
                            hospital_status: data.hospital_status,
                            stage: data.stage
                        });
                    }
                })
                .catch(() => {});
        }, 800);

        // 4. On initial load, restore any active state from localStorage
        try {
            const savedState = localStorage.getItem('wariseva_shared_emergency_state');
            if (savedState) {
                const parsed = JSON.parse(savedState);
                if (parsed && parsed.status && parsed.status !== 'RESOLVED') {
                    applySharedEmergencyState(parsed);
                }
            }
        } catch (e) {}
    }

    function clearSimulationTimers() {
        if ('speechSynthesis' in window) {
            try { window.speechSynthesis.cancel(); } catch (e) {}
        }
        window.WariState.simulationTimers.forEach(t => clearTimeout(t));
        window.WariState.simulationTimers = [];
        window.WariState.isSimulationRunning = false;
    }



    // Leaflet Emergency Map Initialization
    function initEmergencyMap() {
        const container = document.getElementById('emergency-live-map');
        if (!container || typeof L === 'undefined') return;
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

    // Leaflet Safety Map Initialization (Tactical Page)
    function initSafetyMap() {
        const container = document.getElementById('main-safety-map');
        if (!container || typeof L === 'undefined') return;
        if (window.WariState.maps.safety) {
            window.WariState.maps.safety.invalidateSize();
            return;
        }

        if (container._leaflet_id) {
            container._leaflet_id = null;
        }

        const map = L.map('main-safety-map').setView([18.3444, 74.0305], 15);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        window.WariState.maps.safety = map;
        if (!window.WariState.markers) window.WariState.markers = {};
        window.WariState.markers.safety = [];

        if (window.ResizeObserver) {
            new ResizeObserver(() => {
                if (map && map.invalidateSize) map.invalidateSize();
            }).observe(container);
        }

        loadSafetyMapMarkers('ALL', 'safety');
    }

    // Leaflet Home Safety Map Initialization (Home Dashboard)
    function initHomeSafetyMap() {
        const container = document.getElementById('home-safety-map');
        if (!container || typeof L === 'undefined') return;
        if (window.WariState.maps.homeSafety) {
            window.WariState.maps.homeSafety.invalidateSize();
            return;
        }

        if (container._leaflet_id) {
            container._leaflet_id = null;
        }

        try {
            const map = L.map('home-safety-map', {
                zoomControl: true
            }).setView([18.3444, 74.0305], 15);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
                attribution: '© OpenStreetMap contributors'
            }).addTo(map);

            window.WariState.maps.homeSafety = map;
            if (!window.WariState.markers) window.WariState.markers = {};
            window.WariState.markers.homeSafety = [];

            if (window.ResizeObserver) {
                new ResizeObserver(() => {
                    if (map && map.invalidateSize) map.invalidateSize();
                }).observe(container);
            }

            loadSafetyMapMarkers('ALL', 'homeSafety');

            setTimeout(() => { map.invalidateSize(); }, 200);
            setTimeout(() => { map.invalidateSize(); }, 600);
        } catch (e) {
            console.warn('initHomeSafetyMap caught:', e);
        }
    }

    function loadSafetyMapMarkers(category = 'ALL', specificMapKey = null) {
        if (!window.WariState || !window.WariState.maps) return;

        // Category normalization
        let rawCat = (category || 'ALL').toString().trim().toUpperCase();
        let apiCat = rawCat;
        if (rawCat === 'WASHROOM' || rawCat === 'WASHROOMS' || rawCat === 'RESTROOM' || rawCat === 'RESTROOMS') {
            apiCat = 'TOILET';
        } else if (rawCat === 'MEDICAL' || rawCat === 'MEDICALS' || rawCat === 'DOCTOR' || rawCat === 'MEDIC') {
            apiCat = 'MEDICAL_CAMP';
        } else if (rawCat === 'VOLUNTEER') {
            apiCat = 'VOLUNTEERS';
        } else if (rawCat === 'HOSPITAL') {
            apiCat = 'HOSPITALS';
        } else if (rawCat === 'EMERGENCY') {
            apiCat = 'EMERGENCIES';
        }

        const targetKeys = specificMapKey ? [specificMapKey] : ['homeSafety', 'safety'];
        const activeEntries = [];
        targetKeys.forEach(k => {
            const m = window.WariState.maps[k];
            if (m) activeEntries.push({ key: k, map: m });
        });

        if (activeEntries.length === 0) return;

        // Clear existing markers
        activeEntries.forEach(entry => {
            if (!window.WariState.markers) window.WariState.markers = {};
            if (window.WariState.markers[entry.key]) {
                window.WariState.markers[entry.key].forEach(m => {
                    try { entry.map.removeLayer(m); } catch (e) {}
                });
            }
            window.WariState.markers[entry.key] = [];
        });

        fetch(`/api/safety-services?type=${apiCat}&lat=18.3444&lon=74.0305`)
            .then(res => res.json())
            .then(data => {
                if (!data.success || !data.services) return;
                const services = data.services;

                activeEntries.forEach(entry => {
                    const map = entry.map;
                    const mapKey = entry.key;
                    const latLngs = [];

                    services.forEach(svc => {
                        const cat = (svc.category || svc.type || '').toUpperCase();
                        let iconEmoji = '📍';
                        let bgCol = '#1E2638';
                        let borderCol = '#00BCD4';
                        let catTitle = 'Facility';

                        if (cat === 'WATER') {
                            iconEmoji = '💧';
                            borderCol = '#00BCD4';
                            bgCol = '#006064';
                            catTitle = 'Water Point';
                        } else if (cat === 'TOILET' || cat === 'WASHROOM') {
                            iconEmoji = '🚻';
                            borderCol = '#80D8FF';
                            bgCol = '#01579B';
                            catTitle = 'Washroom / Sanitation';
                        } else if (cat === 'MEDICAL_CAMP' || cat === 'MEDICAL') {
                            iconEmoji = '🏥';
                            borderCol = '#FF5252';
                            bgCol = '#B71C1C';
                            catTitle = 'Medical Camp';
                        } else if (cat === 'HOSPITAL' || cat === 'HOSPITALS') {
                            iconEmoji = '🚑';
                            borderCol = '#FF9100';
                            bgCol = '#E65100';
                            catTitle = 'Hospital';
                        } else if (cat === 'VOLUNTEER' || cat === 'VOLUNTEERS') {
                            iconEmoji = '🦺';
                            borderCol = '#00E5FF';
                            bgCol = '#00695C';
                            catTitle = 'Volunteer Responder';
                        } else if (cat === 'EMERGENCY' || cat === 'EMERGENCIES') {
                            iconEmoji = '🚨';
                            borderCol = '#FF0055';
                            bgCol = '#D32F2F';
                            catTitle = 'Active Emergency';
                        } else if (cat === 'CROWD_RISK') {
                            iconEmoji = '👥';
                            borderCol = '#FFD600';
                            bgCol = '#FF6F00';
                            catTitle = 'Crowd Risk Zone';
                        } else if (cat === 'FOOD') {
                            iconEmoji = '🍛';
                            borderCol = '#FFB74D';
                            bgCol = '#BF360C';
                            catTitle = 'Annachhatra / Food';
                        } else if (cat === 'REST_AREA') {
                            iconEmoji = '🛏️';
                            borderCol = '#81C784';
                            bgCol = '#1B5E20';
                            catTitle = 'Rest Area';
                        }

                        const markerIcon = L.divIcon({
                            className: 'service-pin-icon',
                            html: `<div style="background:${bgCol}; color:#fff; border-radius:50%; width:32px; height:32px; display:flex; align-items:center; justify-content:center; border:2px solid ${borderCol}; font-size:15px; box-shadow:0 0 10px ${borderCol}88; cursor:pointer;" title="${svc.name}">${iconEmoji}</div>`,
                            iconSize: [32, 32],
                            iconAnchor: [16, 16]
                        });

                        const marker = L.marker([svc.latitude, svc.longitude], { icon: markerIcon, title: svc.name }).addTo(map);

                        const popupHtml = `
                            <div class="facility-map-popup" style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; min-width:210px; max-width:280px; padding:3px; color:#1C1D21;">
                                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                                    <span style="font-size:0.72rem; font-weight:800; color:${borderCol}; text-transform:uppercase; letter-spacing:0.5px;">
                                        ${iconEmoji} ${catTitle}
                                    </span>
                                    <span style="font-size:0.68rem; background:#E8F5E9; color:#1B5E20; padding:2px 6px; border-radius:8px; font-weight:700;">
                                        ${svc.status || 'AVAILABLE'}
                                    </span>
                                </div>
                                <div style="font-size:0.92rem; font-weight:800; color:#1C1D21; margin-bottom:4px; line-height:1.25;">
                                    ${svc.name}
                                </div>
                                <div style="font-size:0.76rem; color:#5F6368; margin-bottom:3px;">
                                    📍 ${svc.address || svc.zone || 'Saswad Palkhi Corridor'}
                                </div>
                                <div style="font-size:0.76rem; color:#333; margin-bottom:2px;">
                                    <strong>Distance:</strong> ${svc.distance_text || (svc.distance_m ? svc.distance_m + 'm away' : 'Nearby')}
                                </div>
                                ${svc.special_note || svc.note ? `
                                <div style="font-size:0.72rem; color:#444; background:#F8F9FA; border-left:3px solid ${borderCol}; padding:4px 6px; border-radius:4px; margin-top:4px;">
                                    ℹ️ ${svc.special_note || svc.note}
                                </div>` : ''}
                            </div>
                        `;
                        marker.bindPopup(popupHtml, { maxWidth: 290 });

                        marker.on('click', () => {
                            if (typeof showSidebarDetail === 'function') {
                                showSidebarDetail(svc);
                            }
                        });

                        window.WariState.markers[mapKey].push(marker);
                        latLngs.push([svc.latitude, svc.longitude]);
                    });

                    // Auto-fit bounds as required in Part 7
                    if (latLngs.length > 1) {
                        try {
                            const bounds = L.latLngBounds(latLngs);
                            map.fitBounds(bounds, { padding: [30, 30], maxZoom: 16 });
                        } catch (e) {}
                    } else if (latLngs.length === 1) {
                        map.setView(latLngs[0], 15);
                    } else {
                        map.setView([18.3444, 74.0305], 15);
                    }

                    setTimeout(() => { if (map.invalidateSize) map.invalidateSize(); }, 150);
                });
            })
            .catch(err => {
                console.warn('loadSafetyMapMarkers fetch failed:', err);
            });
    }

    function showSidebarDetail(svc) {
        const emptyState = document.getElementById('sidebar-empty-state');
        const detailCard = document.getElementById('sidebar-detail-card');
        if (emptyState) emptyState.classList.add('hidden');
        if (detailCard) detailCard.classList.remove('hidden');

        const cat = (svc.category || svc.type || 'FACILITY').toUpperCase();
        const catBadge = document.getElementById('sb-category-badge');
        const distBadge = document.getElementById('sb-dist-badge');
        const nameEl = document.getElementById('sb-name');
        const zoneEl = document.getElementById('sb-zone');
        const addrEl = document.getElementById('sb-address');
        const noteEl = document.getElementById('sb-note');

        if (catBadge) catBadge.textContent = cat;
        if (distBadge) distBadge.textContent = svc.distance_text || `${svc.distance_m || 250}m away`;
        if (nameEl) nameEl.textContent = svc.name;
        if (zoneEl) zoneEl.textContent = `📍 ${svc.zone || 'Zone 04 — Saswad Palkhi Maidan'}`;
        if (addrEl) addrEl.textContent = svc.address || 'Saswad Palkhi Route';
        
        let compactInfo = `Status: ${svc.status || 'OPEN'}`;
        if (cat === 'MEDICAL_CAMP') {
            compactInfo = `Camp ID: ${svc.service_id || 'MC-004'} • Status: ${svc.status || 'OPEN'} • First Aid: ${svc.first_aid || 'AVAILABLE'} • Emergency Support: ${svc.emergency_support || 'YES'}`;
        } else if (cat === 'WATER') {
            compactInfo = `Status: ${svc.status || 'AVAILABLE'} • Free Drinking Water & Electrolytes`;
        } else if (cat === 'TOILET' || cat === 'WASHROOM') {
            compactInfo = `Status: ${svc.status || 'OPEN'} • Sanitation & Hygiene Checked`;
        } else if (cat === 'CROWD_RISK') {
            compactInfo = `Risk Level: ${svc.status || 'HIGH'} • Reason: High crowd density + procession choke bottleneck. Safe bypass active.`;
        } else if (cat === 'HOSPITAL') {
            compactInfo = `Status: ${svc.status || 'ACCEPTING'} • Trauma & Emergency Unit • 24x7 Ambulance Bay`;
        } else if (cat === 'VOLUNTEER') {
            compactInfo = `Status: ${svc.status || 'AVAILABLE'} • Certified First Aid & CPR • On-Foot Mobility`;
        }

        if (noteEl) noteEl.textContent = `ℹ️ ${compactInfo}`;

        const actBtn = document.getElementById('sb-action-btn');
        if (actBtn) {
            actBtn.onclick = () => {
                if (window.WariState.maps.safety) {
                    window.WariState.maps.safety.flyTo([svc.latitude, svc.longitude], 17);
                }
            };
        }
    }
    // =========================================================================
    // REUSABLE LIVE CROWD-AWARE NAVIGATION MAP COMPONENT
    // =========================================================================

    // Shared Map Data Structure from Active Emergency
    function getEmergencyMapData(roleType) {
        const em = window.WariState.activeEmergency || {};
        const emergencyId = em.id || em.emergency_id || 'EM-28471';
        const patientName = em.patientName || em.reported_by || 'Tukaram Shinde';
        const zoneName = em.zone || em.wari_zone || 'Zone 04 — Saswad Palkhi Maidan';
        
        // Exact emergency location: [18.3444, 74.0305]
        const emergencyLocation = (em.latitude && em.longitude) 
            ? [Number(em.latitude), Number(em.longitude)] 
            : (em.location || [18.3444, 74.0305]);

        const volunteerLocation = [18.3470, 74.0330]; // Ramesh Kulkarni (V-001)
        const medicalFacilityLocation = [18.3390, 74.0260]; // Saswad Rural Hospital (H-001)

        let originLocation = volunteerLocation;
        let originPopup = '<b>🔵 Your Location (V-001)</b><br>Ramesh Kulkarni (Assigned Responder)';
        let patientPopup = `<b>🔴 Patient: ${patientName}</b><br>Incident ${emergencyId} • ${zoneName} (350m)`;
        let safeRoute = [
            [18.3470, 74.0330],
            [18.3458, 74.0315],
            [18.3444, 74.0305]
        ];
        let congestedRoute = [
            [18.3470, 74.0330],
            [18.3460, 74.0320],
            [18.3444, 74.0305]
        ];

        if (roleType === 'hospital' || roleType === 'responder') {
            originLocation = medicalFacilityLocation;
            originPopup = '<b>🏥 Saswad Rural Sub-District Hospital (H-001)</b><br>Trauma Center • Beds Reserved: 1';
            patientPopup = `<b>🔴 Incoming Patient: ${patientName}</b><br>Incident ${emergencyId} • ${zoneName}`;
            safeRoute = [
                [18.3390, 74.0260],
                [18.3415, 74.0275],
                [18.3444, 74.0305]
            ];
            congestedRoute = [
                [18.3390, 74.0260],
                [18.3430, 74.0290],
                [18.3444, 74.0305]
            ];
        }

        return {
            emergencyId,
            patient: patientName,
            zone: zoneName,
            emergencyLocation,
            volunteerLocation,
            medicalFacilityLocation,
            originLocation,
            originPopup,
            patientPopup,
            safeRoute,
            congestedRoute
        };
    }

    // Helper: Safely schedule invalidateSize across render cycles
    function scheduleMapInvalidate(map, container) {
        if (!map) return;
        map.invalidateSize();
        if (typeof requestAnimationFrame !== 'undefined') {
            requestAnimationFrame(() => {
                if (map) map.invalidateSize();
            });
        }
        setTimeout(() => {
            if (map) map.invalidateSize();
        }, 100);
        setTimeout(() => {
            if (map) map.invalidateSize();
        }, 300);
    }

    // One Reusable Map Component for Both Volunteer Console and Medical Facility Console
    function renderLiveCrowdAwareNavigationMap(containerId, roleType) {
        const container = document.getElementById(containerId);
        if (!container || typeof L === 'undefined') return null;

        const mapKey = (roleType === 'hospital' || roleType === 'responder') ? 'responder' : 'volunteer';
        const mapData = getEmergencyMapData(roleType);

        window.WariState.mapLayers = window.WariState.mapLayers || {};
        window.WariState.mapLayers[mapKey] = window.WariState.mapLayers[mapKey] || [];

        let map = window.WariState.maps[mapKey];

        // If map exists on this container, REUSE IT
        if (map && map.getContainer && map.getContainer() === container) {
            // Remove previous route layers and markers to prevent duplicate lines/markers on update
            window.WariState.mapLayers[mapKey].forEach(layer => {
                try { map.removeLayer(layer); } catch(e) {}
            });
            window.WariState.mapLayers[mapKey] = [];
        } else {
            // Check if DOM container already has a leaflet instance to avoid "Map container is already initialized"
            if (container._leaflet_id && typeof L !== 'undefined') {
                container._leaflet_id = null;
            }

            // Create the single Leaflet instance
            map = L.map(containerId, {
                zoomControl: true,
                attributionControl: true
            }).setView(mapData.emergencyLocation, 15);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
                attribution: '© OpenStreetMap contributors'
            }).addTo(map);

            window.WariState.maps[mapKey] = map;

            // Attach ResizeObserver to container if available
            if (typeof ResizeObserver !== 'undefined' && !container._wariResizeObserved) {
                container._wariResizeObserved = true;
                const ro = new ResizeObserver(() => {
                    if (container.offsetWidth > 0 && container.offsetHeight > 0) {
                        map.invalidateSize();
                    }
                });
                ro.observe(container);
            }
        }

        // Render Safe Bypass Polyline (Green)
        const safeBypass = L.polyline(mapData.safeRoute, {
            color: '#00E676',
            weight: 6,
            opacity: 0.9
        }).addTo(map).bindPopup('<b>🟢 Safe Bypass Corridor (3 min)</b><br>Low crowd congestion • Recommended');

        // Render Congested Direct Polyline (Red Dashed)
        const congestedDirect = L.polyline(mapData.congestedRoute, {
            color: '#FF5252',
            weight: 4,
            opacity: 0.6,
            dashArray: '6, 6'
        }).addTo(map).bindPopup('<b>🔴 Direct Procession Route (10 min)</b><br>High bottleneck delay');

        // Render Emergency / Patient Marker
        const patientMarker = L.marker(mapData.emergencyLocation).addTo(map)
            .bindPopup(mapData.patientPopup);

        // Render Origin Marker (Volunteer or Medical Facility)
        const originMarker = L.marker(mapData.originLocation).addTo(map)
            .bindPopup(mapData.originPopup);

        // Track layers for clean re-rendering
        window.WariState.mapLayers[mapKey] = [safeBypass, congestedDirect, patientMarker, originMarker];
        window.WariState.markers[mapKey] = {
            patient: patientMarker,
            origin: originMarker,
            safeRoute: safeBypass,
            congestedRoute: congestedDirect
        };

        // Auto-fit bounds so both origin and destination are clearly visible
        if (mapData.originLocation && mapData.emergencyLocation) {
            const bounds = L.latLngBounds([mapData.originLocation, mapData.emergencyLocation]);
            map.fitBounds(bounds, { padding: [40, 40] });
        } else if (mapData.emergencyLocation) {
            map.setView(mapData.emergencyLocation, 15);
        }

        // Explicitly invalidate size after visibility transitions
        scheduleMapInvalidate(map, container);

        return map;
    }

    // Volunteer Console uses the shared reusable component
    function initVolunteerMap() {
        return renderLiveCrowdAwareNavigationMap('volunteer-map', 'volunteer');
    }

    // Medical Facility Console uses the exact same shared reusable component
    function initResponderMap() {
        return renderLiveCrowdAwareNavigationMap('responder-map', 'hospital');
    }

    // Command Center Map
    function initCommandMap() {
        const container = document.getElementById('command-map');
        if (!container || typeof L === 'undefined') return;
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

    // Central Synchronizer for Emergency Status Across All Consoles
    function syncEmergencyStatusAcrossConsoles(emId, newStatus, stageLabel) {
        if (!emId) emId = 'EM-28471';

        // 1. Volunteer Active Box
        const volBadge = document.getElementById('vol-response-badge');
        if (volBadge) volBadge.textContent = newStatus;
        const volStatusText = document.getElementById('vol-status-text');
        if (volStatusText) volStatusText.textContent = newStatus;
        const volStageInd = document.getElementById('vol-stage-indicator');
        if (volStageInd && stageLabel) volStageInd.textContent = stageLabel;
        const volBadgeChip = document.getElementById('vol-status-badge-chip');
        if (volBadgeChip) volBadgeChip.textContent = newStatus;

        // 2. Volunteer Feed Card (update in place - deduplicated)
        const volCard = document.getElementById(`vol-feed-card-${emId}`);
        if (volCard) {
            const statusEl = volCard.querySelector('.efc-status-val');
            if (statusEl) statusEl.textContent = newStatus;
        }

        // 3. Responder / Medical Facility Active Box & Feed Card
        const respState = document.getElementById('resp-state-text');
        if (respState) respState.textContent = newStatus;
        const respBadge = document.getElementById('resp-status-badge');
        if (respBadge) respBadge.textContent = `🏥 INCOMING: ${newStatus}`;
        const respCard = document.getElementById(`resp-feed-card-${emId}`);
        if (respCard) {
            const statusEl = respCard.querySelector('.efc-status-val');
            if (statusEl) statusEl.textContent = newStatus;
        }

        // 4. Command Center
        const cmdStatusText = document.getElementById('cmd-ins-status');
        if (cmdStatusText) cmdStatusText.textContent = newStatus;
        const cmdCard = document.querySelector(`.cmd-incident-card[data-em-id="${emId}"]`);
        if (cmdCard) {
            const cmdStatusVal = cmdCard.querySelector('.cic-status strong');
            if (cmdStatusVal) cmdStatusVal.textContent = newStatus;
        }
    }

    // Load Volunteer Emergency Feed (Strict Deduplication by emergency_id)
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

                // Strict deduplication by emergency_id
                const uniqueMap = new Map();
                data.emergencies.forEach(e => {
                    if (e && e.emergency_id && !uniqueMap.has(e.emergency_id)) {
                        uniqueMap.set(e.emergency_id, e);
                    }
                });
                const uniqueList = Array.from(uniqueMap.values());

                const emptyPlaceholder = container.querySelector('.empty-feed-text');
                if (emptyPlaceholder) emptyPlaceholder.remove();

                uniqueList.forEach(e => {
                    const emId = e.emergency_id;
                    let card = document.getElementById(`vol-feed-card-${emId}`);
                    const priorityText = e.priority || e.severity || 'CRITICAL';
                    const patientName = e.reported_by || e.patient_name || 'Tukaram Shinde';
                    const zoneText = e.wari_zone || e.zone || 'Zone 04 — Saswad Palkhi Maidan';
                    const statusText = e.status || 'CREATED';

                    if (card) {
                        // UPDATE EXISTING CARD IN-PLACE
                        const prioEl = card.querySelector('.efc-priority');
                        if (prioEl) prioEl.textContent = priorityText;
                        const nameEl = card.querySelector('.efc-name strong');
                        if (nameEl) nameEl.textContent = patientName;
                        const zoneEl = card.querySelector('.efc-zone');
                        if (zoneEl) zoneEl.textContent = `📍 ${zoneText}`;
                        const statusEl = card.querySelector('.efc-status-val');
                        if (statusEl) statusEl.textContent = statusText;
                    } else {
                        // Create unique card
                        card = document.createElement('div');
                        card.className = 'emergency-feed-card';
                        card.id = `vol-feed-card-${emId}`;
                        card.dataset.emId = emId;
                        card.innerHTML = `
                            <div class="efc-top">
                                <span class="efc-id">${emId}</span>
                                <span class="efc-priority">${priorityText}</span>
                            </div>
                            <div class="efc-name">Patient: <strong>${patientName}</strong></div>
                            <div class="efc-zone">📍 ${zoneText}</div>
                            <div class="efc-time">Status: <strong class="efc-status-val">${statusText}</strong></div>
                        `;
                        container.appendChild(card);
                    }
                });
            })
            .catch(() => {
                if (!container.querySelector('.emergency-feed-card')) {
                    container.innerHTML = '<p class="empty-feed-text">Error loading volunteer feed.</p>';
                }
            });
    }

    // Load Responder Emergency Feed (Strict Deduplication by emergency_id)
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

                // Strict deduplication by emergency_id
                const uniqueMap = new Map();
                data.emergencies.forEach(e => {
                    if (e && e.emergency_id && !uniqueMap.has(e.emergency_id)) {
                        uniqueMap.set(e.emergency_id, e);
                    }
                });
                const uniqueList = Array.from(uniqueMap.values());

                const emptyPlaceholder = container.querySelector('.empty-feed-text');
                if (emptyPlaceholder) emptyPlaceholder.remove();

                uniqueList.forEach(e => {
                    const emId = e.emergency_id;
                    let card = document.getElementById(`resp-feed-card-${emId}`);
                    const priorityText = e.priority || e.severity || 'CRITICAL';
                    const patientName = e.reported_by || e.patient_name || 'Tukaram Shinde';
                    const zoneText = e.wari_zone || e.zone || 'Zone 04 — Saswad Palkhi Maidan';
                    const statusText = e.status || 'CREATED';

                    if (card) {
                        // UPDATE EXISTING CARD IN-PLACE
                        const prioEl = card.querySelector('.efc-priority');
                        if (prioEl) prioEl.textContent = priorityText;
                        const nameEl = card.querySelector('.efc-name strong');
                        if (nameEl) nameEl.textContent = patientName;
                        const zoneEl = card.querySelector('.efc-zone');
                        if (zoneEl) zoneEl.textContent = `📍 ${zoneText}`;
                        const statusEl = card.querySelector('.efc-status-val');
                        if (statusEl) statusEl.textContent = statusText;
                    } else {
                        // Create unique card
                        card = document.createElement('div');
                        card.className = 'emergency-feed-card';
                        card.id = `resp-feed-card-${emId}`;
                        card.dataset.emId = emId;
                        card.innerHTML = `
                            <div class="efc-top">
                                <span class="efc-id">${emId}</span>
                                <span class="efc-priority">${priorityText}</span>
                            </div>
                            <div class="efc-name">Patient: <strong>${patientName}</strong></div>
                            <div class="efc-zone">📍 ${zoneText}</div>
                            <div class="efc-time">Status: <strong class="efc-status-val">${statusText}</strong></div>
                        `;
                        container.appendChild(card);
                    }
                });
            })
            .catch(() => {
                if (!container.querySelector('.emergency-feed-card')) {
                    container.innerHTML = '<p class="empty-feed-text">Error loading responder feed.</p>';
                }
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

    
    // =========================================================================
    // WARISEVA QR WRISTBAND, SCANNER & PIN AUTHORIZATION ENGINE
    // =========================================================================

    function renderDynamicQrCode(containerId, qrText, size = 260) {
        const container = document.getElementById(containerId);
        if (!container) return;
        container.innerHTML = '';

        // Ensure payload is complete valid public pilgrim URL
        let payload = qrText;
        if (!payload.startsWith('http://') && !payload.startsWith('https://')) {
            const wariId = payload.startsWith('WS-') ? payload : 'WS-28471';
            payload = `${window.location.origin}/public/pilgrim/${wariId}`;
        }

        console.log(`[WariSeva QR Engine] Rendering QR Code for container: #${containerId} | Payload: ${payload}`);

        // 1. Primary: Standard High-Resolution Scannable QR Code Image (Python official qrcode engine, Level H, 4-module quiet zone)
        const qrImg = document.createElement('img');
        const encodedUrl = encodeURIComponent(payload);
        qrImg.src = `/api/qr/image?url=${encodedUrl}&cb=${Date.now()}`;
        qrImg.alt = `WariSeva QR Code for ${payload}`;
        qrImg.width = size;
        qrImg.height = size;
        qrImg.style.display = 'block';
        qrImg.style.width = '100%';
        qrImg.style.height = '100%';
        qrImg.style.aspectRatio = '1 / 1';
        qrImg.style.imageRendering = 'pixelated';
        qrImg.style.background = '#FFFFFF';
        qrImg.style.borderRadius = '4px';

        // 2. Fallback: Client-side QRCode generator if network fails
        qrImg.onerror = function() {
            console.warn('[WariSeva QR Engine] Server image load fallback to client-side QRCode canvas');
            if (typeof QRCode !== 'undefined') {
                container.innerHTML = '';
                try {
                    new QRCode(container, {
                        text: payload,
                        width: size,
                        height: size,
                        colorDark: "#000000",
                        colorLight: "#ffffff",
                        correctLevel: QRCode.CorrectLevel.H
                    });
                } catch(e) {
                    console.error("[WariSeva QR Engine] QRCode library error:", e);
                }
            }
        };

        container.appendChild(qrImg);
    }

    function triggerWristbandAuthModal() {
        const authModal = document.getElementById('wristband-auth-modal');
        const passInput = document.getElementById('wb-password-input');
        const errEl = document.getElementById('wb-password-error');
        if (errEl) errEl.classList.add('hidden');
        if (passInput) {
            passInput.value = '';
        }
        if (authModal) {
            authModal.classList.remove('hidden');
            if (passInput) passInput.focus();
        }
        speakVoice("Please enter demo password WARI2026 to preview pilgrim wristband.");
    }

    function closeWristbandAuthModal() {
        const authModal = document.getElementById('wristband-auth-modal');
        if (authModal) authModal.classList.add('hidden');
    }

    function handleWristbandPasswordSubmit(enteredPassword) {
        const errEl = document.getElementById('wb-password-error');
        if (errEl) errEl.classList.add('hidden');

        fetch('/api/demo/verify-wristband-password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password: enteredPassword })
        })
        .then(res => res.json().then(data => ({ status: res.status, body: data })))
        .then(({ status, body }) => {
            if (status === 200 && body.success) {
                closeWristbandAuthModal();
                showPhysicalWristbandModal();
            } else {
                if (errEl) {
                    errEl.textContent = body.error || "❌ Incorrect demo password. Enter WARI2026.";
                    errEl.classList.remove('hidden');
                }
                showToast(body.error || "Incorrect demo password", "error");
                speakVoice("Incorrect demo password.");
            }
        })
        .catch(() => {
            // Fallback for prototype stability
            if (enteredPassword.toUpperCase() === 'WARI2026') {
                closeWristbandAuthModal();
                showPhysicalWristbandModal();
            } else {
                if (errEl) {
                    errEl.textContent = "❌ Incorrect demo password. Enter WARI2026.";
                    errEl.classList.remove('hidden');
                }
            }
        });
    }

    let currentLanQrUrl = `${window.location.origin}/public/pilgrim/WS-28471`;

    function setWristbandViewMode(mode) {
        const tabFront = document.getElementById('tab-wb-front');
        const tabBack = document.getElementById('tab-wb-back');
        const tabBoth = document.getElementById('tab-wb-both');
        const bandFront = document.getElementById('wb-band-front');
        const bandBack = document.getElementById('wb-band-back');

        [tabFront, tabBack, tabBoth].forEach(t => t?.classList.remove('active'));

        if (mode === 'front') {
            if (tabFront) tabFront.classList.add('active');
            if (bandFront) bandFront.classList.remove('hidden');
            if (bandBack) bandBack.classList.add('hidden');
        } else if (mode === 'back') {
            if (tabBack) tabBack.classList.add('active');
            if (bandFront) bandFront.classList.add('hidden');
            if (bandBack) bandBack.classList.remove('hidden');
        } else if (mode === 'both') {
            if (tabBoth) tabBoth.classList.add('active');
            if (bandFront) bandFront.classList.remove('hidden');
            if (bandBack) bandBack.classList.remove('hidden');
        }
    }

    function showPhysicalWristbandModal() {
        const modal = document.getElementById('wristband-modal');
        if (!modal) return;
        modal.classList.remove('hidden');
        setWristbandViewMode('front');

        // Fetch machine's real LAN IP dynamically from the backend for physical phone scanning
        fetch('/api/network-info')
        .then(res => res.json())
        .then(data => {
            if (data.success && data.lan_ip) {
                const lanIp = data.lan_ip;
                const port = data.port || 5000;
                currentLanQrUrl = data.qr_target_url || `http://${lanIp}:${port}/public/pilgrim/WS-28471`;

                const lanIpEl = document.getElementById('wb-lan-ip-display');
                if (lanIpEl) lanIpEl.textContent = `${lanIp}:${port}`;

                const diagLanEl = document.getElementById('diag-lan-ip');
                if (diagLanEl) diagLanEl.textContent = `${lanIp}:${port}`;

                const urlTextEl = document.getElementById('wb-qr-url-text');
                if (urlTextEl) urlTextEl.textContent = currentLanQrUrl;

                const openLinkEl = document.getElementById('open-public-profile-link');
                if (openLinkEl) openLinkEl.href = currentLanQrUrl;

                // Render high-contrast 220x220px machine-readable QR code
                renderDynamicQrCode('wristband-qr-target', currentLanQrUrl, 220);
            }
        })
        .catch(() => {
            currentLanQrUrl = `${window.location.origin}/public/pilgrim/WS-28471`;
            renderDynamicQrCode('wristband-qr-target', currentLanQrUrl, 220);
        });

        showToast("✓ Physical WariSeva QR Wristband Preview Unlocked", "success");
        speakVoice("Demo access verified. Physical wristband preview unlocked.");
    }

    function closeWristbandModal() {
        const modal = document.getElementById('wristband-modal');
        if (modal) modal.classList.add('hidden');
    }

    function setVolunteerAuthState(isLoggedIn, volData = null) {
        window.WariState.volunteerAuth.isLoggedIn = isLoggedIn;
        const authPill = document.getElementById('scanner-auth-pill');
        const authLabel = document.getElementById('scanner-auth-label');
        const authDot = document.getElementById('scanner-auth-dot');
        const loginGate = document.getElementById('scanner-login-gate');
        const activeViewport = document.getElementById('scanner-active-viewport');
        const volTag = document.getElementById('scanner-active-vol-tag');

        if (isLoggedIn && volData) {
            window.WariState.volunteerAuth.volunteerId = volData.id || 'V-001';
            window.WariState.volunteerAuth.volunteerName = volData.name || 'Ramesh Kulkarni';
            window.WariState.volunteerAuth.token = volData.token || 'demo-token-v001';

            if (authLabel) authLabel.textContent = `${volData.name} (${volData.id} • VERIFIED)`;
            if (authDot) { authDot.className = 'auth-dot green'; }
            if (loginGate) loginGate.classList.add('hidden');
            if (activeViewport) activeViewport.classList.remove('hidden');
            if (volTag) volTag.textContent = `Volunteer: ${volData.name} (${volData.id} • ${volData.certification || 'VERIFIED'})`;
            
            showToast(`Volunteer ${volData.name} authenticated.`, 'success');
        } else {
            window.WariState.volunteerAuth.volunteerId = null;
            window.WariState.volunteerAuth.volunteerName = null;
            window.WariState.volunteerAuth.token = null;

            if (authLabel) authLabel.textContent = 'Not Authenticated';
            if (authDot) { authDot.className = 'auth-dot red'; }
            if (loginGate) loginGate.classList.remove('hidden');
            if (activeViewport) activeViewport.classList.add('hidden');
        }
    }

    function handleVolunteerLoginSubmit(vId, password) {
        const errEl = document.getElementById('login-error-text');
        if (errEl) errEl.classList.add('hidden');

        fetch('/api/volunteer/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ volunteer_id: vId, password: password })
        })
        .then(res => res.json().then(data => ({ status: res.status, body: data })))
        .then(({ status, body }) => {
            if (status === 200 && body.success) {
                setVolunteerAuthState(true, body.volunteer);
                speakVoice(`Welcome, Volunteer ${body.volunteer.name}. Scanner ready.`);
            } else {
                if (errEl) {
                    errEl.textContent = body.error || 'Authentication failed.';
                    errEl.classList.remove('hidden');
                }
                showToast(body.error || 'Invalid credentials', 'error');
                speakVoice("Volunteer authentication failed.");
            }
        })
        .catch(err => {
            // Fallback for prototype stability
            setVolunteerAuthState(true, {
                id: 'V-001',
                name: 'Ramesh Kulkarni',
                certification: 'VERIFIED'
            });
            speakVoice("Demo volunteer authenticated.");
        });
    }

    function resetScannerCards() {
        const activeViewport = document.getElementById('scanner-active-viewport');
        const protectedCard = document.getElementById('scan-result-protected-card');
        const authorizedCard = document.getElementById('scan-authorized-profile-card');
        const errorCard = document.getElementById('scan-error-card');
        const pinError = document.getElementById('pin-error-text');
        const pinInput = document.getElementById('pin-input-field');

        if (protectedCard) protectedCard.classList.add('hidden');
        if (authorizedCard) authorizedCard.classList.add('hidden');
        if (errorCard) errorCard.classList.add('hidden');
        if (pinError) pinError.classList.add('hidden');
        if (pinInput) pinInput.value = '';

        if (window.WariState.volunteerAuth.isLoggedIn && activeViewport) {
            activeViewport.classList.remove('hidden');
        }
    }

    function handleScannedQr(qrData) {
        if (!window.WariState.volunteerAuth.isLoggedIn) {
            setVolunteerAuthState(true, {
                id: 'V-001',
                name: 'Ramesh Kulkarni',
                role: 'Medical First Responder',
                status: 'AVAILABLE',
                verified: true
            });
        }

        const activeViewport = document.getElementById('scanner-active-viewport');
        const protectedCard = document.getElementById('scan-result-protected-card');
        const errorCard = document.getElementById('scan-error-card');
        const authorizedCard = document.getElementById('scan-authorized-profile-card');
        const pinError = document.getElementById('pin-error-text');

        if (authorizedCard) authorizedCard.classList.add('hidden');
        if (pinError) pinError.classList.add('hidden');

        fetch('/api/qr/lookup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ qr_data: qrData })
        })
        .then(res => res.json().then(data => ({ status: res.status, body: data })))
        .then(({ status, body }) => {
            if (status === 200 && body.success && body.found) {
                window.WariState.currentScannedPilgrim = body;
                if (activeViewport) activeViewport.classList.add('hidden');
                if (errorCard) errorCard.classList.add('hidden');
                if (authorizedCard) authorizedCard.classList.add('hidden'); // Medical details stay locked!
                
                if (protectedCard) {
                    protectedCard.classList.remove('hidden'); // Show limited identification & PIN prompt!
                    const srId = document.getElementById('sr-wari-id');
                    if (srId) srId.textContent = body.wari_id;
                    const srPilgrimId = document.getElementById('sr-pilgrim-wari-id');
                    if (srPilgrimId) srPilgrimId.textContent = body.wari_id;
                    const srName = document.getElementById('sr-pilgrim-name');
                    if (srName) srName.textContent = body.name;
                    const srDindi = document.getElementById('sr-pilgrim-dindi');
                    if (srDindi) srDindi.textContent = `Dindi ${body.dindi || '27'}`;
                    
                    const pinInput = document.getElementById('pin-input-field');
                    if (pinInput) pinInput.value = '';
                    const pinError = document.getElementById('pin-error-text');
                    if (pinError) pinError.classList.add('hidden');
                }

                speakVoice(`Wristband detected. ${body.name}, ${body.wari_id}.`);
                showToast(`🪪 Wristband Detected: ${body.name} (${body.wari_id})`, 'success');
            } else {
                if (activeViewport) activeViewport.classList.add('hidden');
                if (protectedCard) protectedCard.classList.add('hidden');
                if (errorCard) {
                    errorCard.classList.remove('hidden');
                    const msgEl = document.getElementById('scan-error-message');
                    if (msgEl) msgEl.textContent = body.error || "WariSeva ID not registered.";
                }
                speakVoice("WariSeva ID not found in registry.");
                showToast("❌ QR Not Found", "error");
            }
        })
        .catch(err => {
            showToast("QR lookup network error", "error");
        });
    }

    function handlePinVerificationSubmit(pin) {
        const pilgrim = window.WariState.currentScannedPilgrim;
        if (!pilgrim) return;

        const pinError = document.getElementById('pin-error-text');
        if (pinError) pinError.classList.add('hidden');

        const volId = window.WariState.volunteerAuth.volunteerId || 'V-001';
        const volName = window.WariState.volunteerAuth.volunteerName || 'Ramesh Kulkarni';

        fetch('/api/qr/verify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                wari_id: pilgrim.wari_id,
                pin: pin,
                volunteer_id: volId,
                volunteer_name: volName
            })
        })
        .then(res => res.json().then(data => ({ status: res.status, body: data })))
        .then(({ status, body }) => {
            if (status === 200 && body.success && body.authorized) {
                const protectedCard = document.getElementById('scan-result-protected-card');
                const authorizedCard = document.getElementById('scan-authorized-profile-card');

                if (protectedCard) protectedCard.classList.add('hidden');
                if (authorizedCard) {
                    authorizedCard.classList.remove('hidden');

                    const p = body.pilgrim;
                    const apName = document.getElementById('ap-name');
                    if (apName) apName.textContent = p.name;
                    const apId = document.getElementById('ap-wari-id');
                    if (apId) apId.textContent = p.wari_id;
                    const apDindi = document.getElementById('ap-dindi');
                    if (apDindi) apDindi.textContent = p.dindi || '27';
                    const apBlood = document.getElementById('ap-blood');
                    if (apBlood) apBlood.textContent = p.blood_group || 'B+';
                    const apContact = document.getElementById('ap-contact');
                    if (apContact) apContact.textContent = p.emergency_contact || '+91 98221 28542';
                    const apAlert = document.getElementById('ap-alert');
                    if (apAlert) apAlert.textContent = p.medical_alert || '⚠️ None Listed';

                    if (body.access_audit) {
                        const audVol = document.getElementById('audit-volunteer');
                        if (audVol) audVol.textContent = body.access_audit.accessed_by;
                        const audTime = document.getElementById('audit-time');
                        if (audTime) audTime.textContent = body.access_audit.access_time;
                    }
                }
                speakVoice("Identity verified. Authorized emergency medical profile unlocked.");
                showToast("✓ Verification Successful", "success");
            } else {
                if (pinError) {
                    pinError.innerHTML = "❌ Incorrect PIN<br>Please try again.";
                    pinError.classList.remove('hidden');
                }
                speakVoice("Incorrect PIN. Please try again.");
                showToast("❌ Incorrect PIN", "error");
            }
        })
        .catch(err => {
            showToast("PIN verification connection error", "error");
        });
    }

    function handleReportEmergencyFromQr() {
        const pilgrim = window.WariState.currentScannedPilgrim;
        const wariId = pilgrim ? pilgrim.wari_id : 'WS-28471';
        const volId = window.WariState.volunteerAuth.volunteerId || 'V-001';

        fetch('/api/qr/report-emergency', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                wari_id: wariId,
                volunteer_id: volId,
                emergency_type: 'MEDICAL',
                severity: 'CRITICAL',
                latitude: 18.3444,
                longitude: 74.0305
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                window.WariState.currentEmergencyId = data.emergency_id || 'EM-28471';
                showToast(`🚨 Incident ${data.emergency_id} created for ${data.patient_name}`, 'success');
                speakVoice(`Emergency reported for ${data.patient_name}. AI dispatch coordinating.`);
                
                // Switch directly to emergency view and run response
                switchView('emergency-view');
                fetchAiRecommendation(data.emergency_id);
                handleSOS();
            }
        })
        .catch(() => {
            switchView('emergency-view');
            handleSOS();
        });
    }

    function startLiveCameraScanner() {
        const viewport = document.getElementById('camera-reader-viewport');
        if (!viewport) return;

        if (typeof Html5Qrcode !== 'undefined') {
            try {
                if (window.WariState.html5QrScanner) {
                    window.WariState.html5QrScanner.stop().catch(() => {});
                }
                const html5QrCode = new Html5Qrcode("camera-reader-viewport");
                window.WariState.html5QrScanner = html5QrCode;

                html5QrCode.start(
                    { facingMode: "environment" },
                    { fps: 10, qrbox: 220 },
                    (decodedText) => {
                        html5QrCode.stop().catch(() => {});
                        handleScannedQr(decodedText);
                    },
                    (errorMessage) => {
                        // Scanning frame error, silent
                    }
                ).catch(err => {
                    showToast("Camera access restricted. Use Simulate QR Scan.", "info");
                    viewport.innerHTML = '<div style="color:#8B949E; padding:40px; text-align:center;">Camera stream unavailable in current environment.<br>Use <strong>⚡ SIMULATE QR SCAN</strong> below.</div>';
                });
                return;
            } catch (e) {
                console.warn("Html5Qrcode scanner failed to initialize:", e);
            }
        }

        showToast("Camera scanner ready. Click SIMULATE QR SCAN.", "info");
        viewport.innerHTML = '<div style="color:#8B949E; padding:40px; text-align:center;">Camera stream active.<br>Click <strong>⚡ SIMULATE QR SCAN (WS-28471)</strong> to test.</div>';
    }

    document.addEventListener('DOMContentLoaded', () => {
        // Initialize Multilingual System
        const savedLang = localStorage.getItem('wariseva_lang') || 'en';
        applyLanguage(savedLang);

        const langSelect = document.getElementById('lang-select');
        if (langSelect) {
            langSelect.value = savedLang;
            langSelect.addEventListener('change', (e) => {
                applyLanguage(e.target.value);
            });
        }
        
        // 1. Navigation Button Listeners (Desktop, Sidebar & Mobile)
        document.querySelectorAll('.desktop-nav .nav-link-btn, .sidebar-panel .nav-link-btn, .mobile-bottom-nav .mob-nav-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const targetView = btn.dataset.view;
                if (targetView) switchView(targetView);
            });
        });

        // Mobile Sidebar Drawer Toggle & Backdrop Handlers
        const mobileMenuBtn = document.getElementById('mobile-menu-toggle-btn');
        const sidebarCloseBtn = document.getElementById('sidebar-close-btn');
        const sidebarBackdrop = document.getElementById('sidebar-backdrop');
        const sidebarPanel = document.querySelector('.sidebar-panel');

        if (mobileMenuBtn && sidebarPanel) {
            mobileMenuBtn.addEventListener('click', () => {
                sidebarPanel.classList.add('mobile-open');
                if (sidebarBackdrop) sidebarBackdrop.classList.remove('hidden');
            });
        }

        const closeMobileSidebar = () => {
            if (sidebarPanel) sidebarPanel.classList.remove('mobile-open');
            if (sidebarBackdrop) sidebarBackdrop.classList.add('hidden');
        };

        sidebarCloseBtn?.addEventListener('click', closeMobileSidebar);
        sidebarBackdrop?.addEventListener('click', closeMobileSidebar);

        // Direct Nav ID Listeners for Extra Reliability
        document.getElementById('nav-home')?.addEventListener('click', () => switchView('home-view'));
        document.getElementById('nav-emergency')?.addEventListener('click', () => switchView('emergency-view'));
        document.getElementById('nav-emergency-status')?.addEventListener('click', () => switchView('emergency-view'));
        document.getElementById('nav-volunteer')?.addEventListener('click', () => switchView('volunteer-view'));
        document.getElementById('nav-responder')?.addEventListener('click', () => switchView('responder-view'));
        document.getElementById('nav-safety-map')?.addEventListener('click', () => switchView('safety-map-view'));
        document.getElementById('nav-qr-scanner')?.addEventListener('click', () => switchView('qr-scanner-view'));
        document.getElementById('nav-command')?.addEventListener('click', () => switchView('command-view'));

        document.getElementById('mob-nav-home')?.addEventListener('click', () => switchView('home-view'));
        document.getElementById('mob-nav-map')?.addEventListener('click', () => switchView('safety-map-view'));
        document.getElementById('mob-nav-sos')?.addEventListener('click', () => switchView('emergency-view'));
        document.getElementById('mob-nav-qr')?.addEventListener('click', () => switchView('qr-scanner-view'));
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
        document.getElementById('sidebar-brand-home')?.addEventListener('click', () => {
            switchView('home-view');
        });
        document.getElementById('nav-home')?.addEventListener('click', () => {
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



        // 5. Main SOS Button & Confirmation Modal
        const mainSosBtn = document.getElementById('main-sos-button');
        const sosModal = document.getElementById('sos-modal');
        const cancelSosBtn = document.getElementById('cancel-sos-btn');
        const confirmSosBtn = document.getElementById('confirm-sos-btn');

        // Initialize triage selection event listeners on page load
        initTriageSelectionHandlers();

        function openSosConfirmation() {
            if (sosModal) {
                sosModal.classList.remove('hidden');
                const modalId = document.getElementById('modal-active-wari-id');
                if (modalId) modalId.textContent = window.WariState.currentWariId || 'WS-28471';
                updateTriageTypeUI(window.WariState.selectedTriageType || 'Medical / Chest Pain');
                updateTriageSeverityUI(window.WariState.selectedTriageSeverity || 'CRITICAL');
            }
        }

        function closeSosConfirmation() {
            if (sosModal) {
                sosModal.classList.add('hidden');
            }
        }

        window.openSosModal = openSosConfirmation;
        window.closeSosModal = closeSosConfirmation;

        if (mainSosBtn) {
            mainSosBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                window.WariState.currentEmergencySource = 'MAIN SOS';
                openSosConfirmation();
            });
        }

        if (cancelSosBtn) {
            cancelSosBtn.addEventListener('click', (e) => {
                e.preventDefault();
                closeSosConfirmation();
            });
        }

        if (confirmSosBtn) {
            confirmSosBtn.addEventListener('click', (e) => {
                e.preventDefault();
                closeSosConfirmation();
                handleSOS();
            });
        }

        if (sosModal) {
            sosModal.addEventListener('click', (e) => {
                if (e.target === sosModal) {
                    closeSosConfirmation();
                }
            });
        }

        // 6. Demo Mode Toolbar Actions
        document.getElementById('create-demo-em-btn')?.addEventListener('click', () => {
            handleSOS();
        });
        document.getElementById('reset-demo-btn')?.addEventListener('click', () => {
            resetDemo();
        });

        // 7. Simulation Quick Bar on Emergency Page
        document.getElementById('em-simulate-btn')?.addEventListener('click', () => {
            handleSOS();
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



        // Home Service Tiles Click
        document.querySelectorAll('.service-tile-home').forEach(tile => {
            tile.addEventListener('click', () => {
                const type = tile.dataset.serviceType;
                switchView('services-view');
                loadServicesCards(type);
            });
        });



        // 10. Safety Map Filter Pills (Tactical Map)
        document.querySelectorAll('#map-filter-group .filter-pill').forEach(pill => {
            pill.addEventListener('click', () => {
                document.querySelectorAll('#map-filter-group .filter-pill').forEach(p => p.classList.remove('active'));
                pill.classList.add('active');
                loadSafetyMapMarkers(pill.dataset.filter, 'safety');
            });
        });

        // Home Safety Map Filter Pills
        document.querySelectorAll('#map-filter-group-home .filter-pill-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('#map-filter-group-home .filter-pill-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                const filterCategory = btn.dataset.filter || 'ALL';
                loadSafetyMapMarkers(filterCategory, 'homeSafety');
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
        // --- QR Scanner & Wristband Event Bindings ---
        // --- Physical Wristband Preview Event Bindings ---
        document.getElementById('open-wristband-modal-btn')?.addEventListener('click', showPhysicalWristbandModal);
        document.getElementById('btn-view-demo-wristband')?.addEventListener('click', showPhysicalWristbandModal);
        
        document.getElementById('cancel-wb-pass-btn')?.addEventListener('click', closeWristbandAuthModal);
        document.getElementById('wristband-auth-modal')?.addEventListener('click', (e) => {
            if (e.target.id === 'wristband-auth-modal') closeWristbandAuthModal();
        });

        // Submit Wristband Password Form
        document.getElementById('wristband-pass-form')?.addEventListener('submit', (e) => {
            e.preventDefault();
            const passVal = document.getElementById('wb-password-input')?.value || '';
            handleWristbandPasswordSubmit(passVal);
        });

        document.getElementById('close-wristband-modal-btn')?.addEventListener('click', closeWristbandModal);
        document.getElementById('wristband-modal')?.addEventListener('click', (e) => {
            if (e.target.id === 'wristband-modal') closeWristbandModal();
        });
        document.getElementById('print-wristband-btn')?.addEventListener('click', () => {
            window.print();
        });

        // --- Wristband Tab Switcher ---
        document.getElementById('tab-wb-front')?.addEventListener('click', () => setWristbandViewMode('front'));
        document.getElementById('tab-wb-back')?.addEventListener('click', () => setWristbandViewMode('back'));
        document.getElementById('tab-wb-both')?.addEventListener('click', () => setWristbandViewMode('both'));

        // --- Wristband Modal Top Navigation Links ---
        document.getElementById('wb-modal-home-btn')?.addEventListener('click', () => {
            closeWristbandModal();
            switchView('home-view');
        });
        document.getElementById('wb-modal-nav-em')?.addEventListener('click', () => {
            closeWristbandModal();
            switchView('emergency-view');
        });
        document.getElementById('wb-modal-nav-map')?.addEventListener('click', () => {
            closeWristbandModal();
            switchView('safety-map-view');
        });
        document.getElementById('wb-modal-nav-svc')?.addEventListener('click', () => {
            closeWristbandModal();
            switchView('services-view');
        });
        document.getElementById('wb-modal-nav-vol')?.addEventListener('click', () => {
            closeWristbandModal();
            switchView('volunteer-view');
        });
        document.getElementById('wb-modal-nav-resp')?.addEventListener('click', () => {
            closeWristbandModal();
            switchView('responder-view');
        });
        document.getElementById('wb-modal-nav-cmd')?.addEventListener('click', () => {
            closeWristbandModal();
            switchView('command-view');
        });
        document.getElementById('wb-modal-back-btn')?.addEventListener('click', closeWristbandModal);

        // Copy QR Link Button (Copies real LAN URL)
        document.getElementById('copy-qr-link-btn')?.addEventListener('click', () => {
            navigator.clipboard.writeText(currentLanQrUrl).then(() => {
                showToast("✓ Real LAN QR link copied to clipboard!", "success");
            }).catch(() => {
                showToast(`Link: ${currentLanQrUrl}`, "info");
            });
        });

        // Copy Diagnostic Phone Test URL Button
        document.getElementById('copy-diag-url-btn')?.addEventListener('click', () => {
            navigator.clipboard.writeText(currentLanQrUrl).then(() => {
                showToast("✓ Phone test URL copied to clipboard!", "success");
            }).catch(() => {
                showToast(`Link: ${currentLanQrUrl}`, "info");
            });
        });

        // Test QR Scan Toolbar Button (Opens LAN URL in new tab)
        document.getElementById('btn-test-qr-scan')?.addEventListener('click', () => {
            window.open(currentLanQrUrl, '_blank');
            showToast("Opened LAN emergency profile in new tab", "info");
        });

        document.getElementById('home-open-qr-scanner-btn')?.addEventListener('click', () => switchView('qr-scanner-view'));
        document.getElementById('vol-open-scanner-btn')?.addEventListener('click', () => switchView('qr-scanner-view'));
        document.getElementById('nav-qr-scanner')?.addEventListener('click', () => switchView('qr-scanner-view'));
        document.getElementById('mob-nav-qr')?.addEventListener('click', () => switchView('qr-scanner-view'));

        // Volunteer Login Form
        document.getElementById('volunteer-login-form')?.addEventListener('submit', (e) => {
            e.preventDefault();
            const vId = document.getElementById('v-login-id')?.value || 'V-001';
            const pass = document.getElementById('v-login-pass')?.value || 'wari123';
            handleVolunteerLoginSubmit(vId, pass);
        });

        // 1-Click Quick Demo Login
        document.getElementById('quick-demo-login-btn')?.addEventListener('click', () => {
            handleVolunteerLoginSubmit('V-001', 'wari123');
        });

        // Logout
        document.getElementById('volunteer-logout-btn')?.addEventListener('click', () => {
            setVolunteerAuthState(false);
            resetScannerCards();
            showToast("Volunteer logged out.", "info");
        });

        // Scanner Triggers
        document.getElementById('start-camera-scan-btn')?.addEventListener('click', startLiveCameraScanner);
        document.getElementById('simulate-valid-qr-btn')?.addEventListener('click', () => handleScannedQr('WS-28471'));
        document.getElementById('simulate-invalid-qr-btn')?.addEventListener('click', () => handleScannedQr('WS-99999'));

        // Scan Again Buttons
        document.getElementById('scan-again-btn-1')?.addEventListener('click', resetScannerCards);
        document.getElementById('scan-again-btn-2')?.addEventListener('click', resetScannerCards);
        document.getElementById('scan-again-btn-3')?.addEventListener('click', resetScannerCards);

        // PIN Verification Form
        document.getElementById('pin-verification-form')?.addEventListener('submit', (e) => {
            e.preventDefault();
            const pinVal = document.getElementById('pin-input-field')?.value || '';
            handlePinVerificationSubmit(pinVal);
        });

        // 1. Report Emergency for Scanned Warkari (No PIN required -> Existing SOS Triage)
        document.getElementById('btn-qr-report-warkari')?.addEventListener('click', (e) => {
            e.preventDefault();
            window.WariState.currentEmergencySource = 'QR REPORT';
            const pilgrim = window.WariState.currentScannedPilgrim;
            if (pilgrim) {
                window.WariState.currentWariId = pilgrim.wari_id || 'WS-28471';
                window.WariState.currentUserName = pilgrim.name || 'Tukaram Shinde';
            }
            openSosConfirmation();
        });

        // 2. Report Emergency from Unlocked Medical Profile
        document.getElementById('qr-report-emergency-btn')?.addEventListener('click', (e) => {
            e.preventDefault();
            window.WariState.currentEmergencySource = 'QR REPORT';
            const pilgrim = window.WariState.currentScannedPilgrim;
            if (pilgrim) {
                window.WariState.currentWariId = pilgrim.wari_id || 'WS-28471';
                window.WariState.currentUserName = pilgrim.name || 'Tukaram Shinde';
            }
            openSosConfirmation();
        });

        // ================= WARKARI SAFETY REPORT MODAL =================
        let selectedWarkariReportReason = "Medical Assistance";

        function openWarkariReportModal() {
            const pilgrim = window.WariState.currentScannedPilgrim || {
                wari_id: 'WS-28471',
                name: 'Tukaram Shinde',
                zone: 'Zone 04 — Saswad Palkhi Maidan'
            };

            const modal = document.getElementById('warkari-report-modal');
            const formView = document.getElementById('warkari-report-form-view');
            const succView = document.getElementById('warkari-report-success-view');
            const nameEl = document.getElementById('rep-modal-name');
            const idEl = document.getElementById('rep-modal-wari-id');
            const zoneEl = document.getElementById('rep-modal-zone');

            if (nameEl) nameEl.textContent = pilgrim.name || 'Tukaram Shinde';
            if (idEl) idEl.textContent = pilgrim.wari_id || 'WS-28471';
            if (zoneEl) zoneEl.textContent = pilgrim.zone || 'Zone 04 — Saswad Palkhi Maidan';

            if (formView) formView.classList.remove('hidden');
            if (succView) succView.classList.add('hidden');
            if (modal) modal.classList.remove('hidden');
        }

        function closeWarkariReportModal() {
            const modal = document.getElementById('warkari-report-modal');
            if (modal) modal.classList.add('hidden');
        }

        document.getElementById('btn-report-this-warkari')?.addEventListener('click', openWarkariReportModal);
        document.getElementById('btn-report-this-warkari-scan')?.addEventListener('click', openWarkariReportModal);
        document.getElementById('close-warkari-report-modal-btn')?.addEventListener('click', closeWarkariReportModal);
        document.getElementById('cancel-warkari-report-btn')?.addEventListener('click', closeWarkariReportModal);
        document.getElementById('close-rep-success-btn')?.addEventListener('click', closeWarkariReportModal);
        document.getElementById('warkari-report-modal')?.addEventListener('click', (e) => {
            if (e.target.id === 'warkari-report-modal') closeWarkariReportModal();
        });

        // Reason Buttons Selection
        document.querySelectorAll('#warkari-report-reasons .report-reason-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('#warkari-report-reasons .report-reason-btn').forEach(b => {
                    b.classList.remove('active');
                    b.style.border = '1px solid var(--border-color)';
                    b.style.background = 'rgba(48, 54, 61, 0.4)';
                    b.style.color = 'var(--text-primary)';
                });
                btn.classList.add('active');
                btn.style.border = '1.5px solid #FF5252';
                btn.style.background = 'rgba(255, 82, 82, 0.15)';
                btn.style.color = '#FFF';
                selectedWarkariReportReason = btn.dataset.reason || btn.textContent.trim();
            });
        });

        // Submit Warkari Report
        document.getElementById('submit-warkari-report-btn')?.addEventListener('click', () => {
            const pilgrim = window.WariState.currentScannedPilgrim || {
                wari_id: 'WS-28471',
                name: 'Tukaram Shinde'
            };
            const wariId = pilgrim.wari_id || 'WS-28471';
            const name = pilgrim.name || 'Tukaram Shinde';
            const notes = document.getElementById('rep-additional-notes')?.value || '';

            fetch('/api/warkari/report', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    wari_id: wariId,
                    name: name,
                    reason: selectedWarkariReportReason,
                    notes: notes,
                    zone: 'Zone 04 — Saswad Palkhi Maidan'
                })
            })
            .then(res => res.json())
            .then(data => {
                const formView = document.getElementById('warkari-report-form-view');
                const succView = document.getElementById('warkari-report-success-view');
                const succName = document.getElementById('succ-rep-name');
                const succId = document.getElementById('succ-rep-id');
                const succReason = document.getElementById('succ-rep-reason');

                if (succName) succName.textContent = name;
                if (succId) succId.textContent = wariId;
                if (succReason) succReason.textContent = selectedWarkariReportReason;

                if (formView) formView.classList.add('hidden');
                if (succView) succView.classList.remove('hidden');

                speakVoice(`Report submitted for ${name}. The Wari Safety Network has been notified.`);
                showToast(`✓ Report Submitted: ${name} (${selectedWarkariReportReason})`, 'success');
            })
            .catch(() => {
                const formView = document.getElementById('warkari-report-form-view');
                const succView = document.getElementById('warkari-report-success-view');
                if (formView) formView.classList.add('hidden');
                if (succView) succView.classList.remove('hidden');
                showToast(`✓ Report Submitted for ${name}`, 'success');
            });
        });

        // Render Home QR initial badge with full verified URL
        fetch('/api/network-info')
            .then(res => res.json())
            .then(data => {
                const targetUrl = data.qr_target_url || `${window.location.origin}/public/pilgrim/WS-28471`;
                renderDynamicQrCode('home-qrcode-target', targetUrl, 110);
            })
            .catch(() => {
                renderDynamicQrCode('home-qrcode-target', `${window.location.origin}/public/pilgrim/WS-28471`, 110);
            });

        // Master Integrated Emergency Workflow Controls
        document.getElementById('vol-accept-em-btn')?.addEventListener('click', handleVolunteerAccept);
        document.getElementById('vol-start-response-btn')?.addEventListener('click', handleVolunteerEnRoute);
        document.getElementById('reached-patient-btn')?.addEventListener('click', handleVolunteerArrived);
        document.getElementById('resp-start-response-btn')?.addEventListener('click', handleVolunteerEnRoute);
        document.getElementById('resp-mark-arrived-btn')?.addEventListener('click', handleVolunteerArrived);
        document.getElementById('hosp-accept-case-btn')?.addEventListener('click', handleHospitalAccept);
        document.getElementById('hosp-patient-arrived-btn')?.addEventListener('click', handleHospitalPatientArrived);
        document.getElementById('hosp-treatment-started-btn')?.addEventListener('click', handleHospitalTreatmentStarted);
        document.getElementById('hosp-transfer-btn')?.addEventListener('click', handleHospitalTransfer);
        document.getElementById('hosp-mark-admitted-btn')?.addEventListener('click', handleHospitalAdmit);

        // Initialize In-App Authentication Gates
        initAuthGates();

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
                handleSOS();
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
                loadVolunteerEmergencyFeed();
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

        // 21. Additional UI and Secondary Navigation Bindings
        document.getElementById('header-notif-btn')?.addEventListener('click', () => {
            showToast("🔔 Active Alert: Emergency response coordinated in Zone 04 — Saswad Palkhi Maidan.", "info");
        });
        document.getElementById('sidebar-reports-btn')?.addEventListener('click', () => {
            switchView('command-center-view');
        });
        document.getElementById('qr-global-back-btn')?.addEventListener('click', () => {
            switchView('home-view');
        });
        document.getElementById('qr-global-home-btn')?.addEventListener('click', () => {
            switchView('home-view');
        });
        document.getElementById('wb-auth-back-btn')?.addEventListener('click', () => {
            closeWristbandAuthModal();
        });
        document.getElementById('wb-auth-home-btn')?.addEventListener('click', () => {
            closeWristbandAuthModal();
            switchView('home-view');
        });

        // Manual Wristband Lookup
        const manualWbBtn = document.getElementById('lookup-manual-wristband-btn');
        const manualWbInput = document.getElementById('manual-wristband-id-input');
        if (manualWbBtn && manualWbInput) {
            manualWbBtn.addEventListener('click', () => {
                const val = manualWbInput.value.trim();
                if (val) {
                    handleQrCodeDetected(val);
                } else {
                    showToast("Please enter a valid Wristband ID", "warning");
                }
            });
            manualWbInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    manualWbBtn.click();
                }
            });
        }

        // Emergency Action Shortcuts
        document.getElementById('coord-view-map-btn')?.addEventListener('click', () => {
            document.getElementById('em-view-tactical-map-btn')?.click();
        });
        document.getElementById('coord-share-btn')?.addEventListener('click', () => {
            document.getElementById('em-share-details-btn')?.click();
        });
        document.getElementById('coord-view-details-btn')?.addEventListener('click', () => {
            document.getElementById('step-1-sos')?.scrollIntoView({ behavior: 'smooth' });
        });

        // Command Center Controls
        document.getElementById('cmd-run-demo-btn')?.addEventListener('click', () => {
            handleSOS();
            document.getElementById('cmd-run-demo-btn')?.classList.add('hidden');
            document.getElementById('cmd-pause-demo-btn')?.classList.remove('hidden');
            document.getElementById('cmd-reset-demo-btn')?.classList.remove('hidden');
        });
        document.getElementById('cmd-pause-demo-btn')?.addEventListener('click', () => {
            clearSimulationTimers();
            showToast("Simulation paused.", "info");
            document.getElementById('cmd-pause-demo-btn')?.classList.add('hidden');
            document.getElementById('cmd-run-demo-btn')?.classList.remove('hidden');
        });
        document.getElementById('cmd-reset-demo-btn')?.addEventListener('click', () => {
            resetDemo();
            document.getElementById('cmd-pause-demo-btn')?.classList.add('hidden');
            document.getElementById('cmd-reset-demo-btn')?.classList.add('hidden');
            document.getElementById('cmd-run-demo-btn')?.classList.remove('hidden');
        });
        document.getElementById('cmd-tab-alerts')?.addEventListener('click', () => {
            document.querySelectorAll('.cmd-tab-btn').forEach(b => b.classList.remove('active'));
            document.getElementById('cmd-tab-alerts')?.classList.add('active');
            document.getElementById('cmd-operations-subview')?.classList.remove('hidden');
            document.getElementById('cmd-heatmap-subview')?.classList.add('hidden');
            document.getElementById('cmd-readiness-subview')?.classList.add('hidden');
            showToast("Active Alerts: Critical triage assigned in Zone 04.", "info");
        });

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

// =========================================================================
// SIDEBAR & TOP BAR NAVIGATION HOOKS (LIGHT THEME)
// =========================================================================
document.addEventListener('DOMContentLoaded', () => {
    // 1. Sidebar Nav View Switcher
    document.querySelectorAll('.sidebar-nav-list .nav-link-btn[data-view]').forEach(btn => {
        btn.addEventListener('click', () => {
            const v = btn.dataset.view;
            if (v) {
                document.querySelectorAll('.content-view').forEach(el => el.classList.add('hidden'));
                document.querySelectorAll('.content-view').forEach(el => el.classList.remove('active'));
                const target = document.getElementById(v);
                if (target) {
                    target.classList.remove('hidden');
                    target.classList.add('active');
                    window.WariState.currentView = v;
                }
                document.querySelectorAll('.sidebar-nav-list .nav-link-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            }
        });
    });

    // 2. Language Switcher Buttons (en, mr, hi)
    ['en', 'mr', 'hi'].forEach(lang => {
        document.getElementById(`lang-btn-${lang}`)?.addEventListener('click', () => {
            document.querySelectorAll('#top-lang-btn-group .lang-tab-btn').forEach(b => b.classList.remove('active'));
            document.getElementById(`lang-btn-${lang}`)?.classList.add('active');
            const selectEl = document.getElementById('lang-select');
            if (selectEl) {
                selectEl.value = lang;
                selectEl.dispatchEvent(new Event('change'));
            }
        });
    });

    // 3. Initialize Home Safety Map
    setTimeout(() => {
        initHomeSafetyMap();
    }, 300);

    // Global Window Resize Listener for Responsive Map Invalidation
    window.addEventListener('resize', () => {
        ['volunteer', 'responder', 'emergency', 'safety', 'command', 'homeSafety'].forEach(k => {
            const m = window.WariState && window.WariState.maps && window.WariState.maps[k];
            if (m && typeof m.invalidateSize === 'function') {
                try { m.invalidateSize(); } catch(e) {}
            }
        });
    });
});
