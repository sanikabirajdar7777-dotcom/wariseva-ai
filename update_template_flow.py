new_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>WariSeva AI — Emergency Coordination & Wari Safety Network</title>
    <!-- Modern High-Legibility Typography -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Outfit:wght@500;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    <!-- SVG Favicon -->
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220%22%200%20100%20100%22><text y=%22.9em%22 font-size=%2290%22>🛡️</text></svg>">
    <!-- Leaflet OpenStreetMap CSS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div id="app" class="app-wrapper">
        
        <!-- ================= 1. PROTOTYPE DEMO MODE TOP BAR ================= -->
        <div class="demo-mode-bar" id="demo-mode-toolbar">
            <div class="demo-bar-left">
                <span class="demo-badge">🟣 DEMO MODE</span>
                <span class="demo-desc" data-i18n="demo_desc">DEMO DATA • SIMULATED RESPONSE</span>
                <span class="conn-status-pill online" id="conn-status-pill">🟢 CONNECTED</span>
            </div>
            <div class="demo-bar-actions">
                <button type="button" id="voice-toggle-btn" class="demo-pill-btn voice-btn" title="Toggle Spoken Voice Assistance">
                    🔊 Voice: ON
                </button>
                <button type="button" id="run-simulation-demo-btn" class="demo-action-btn pulse-orange" title="Auto-advance complete emergency response lifecycle">
                    ▶ SIMULATE RESPONSE
                </button>
                <button type="button" id="create-demo-em-btn" class="demo-action-btn primary">
                    ⚡ CREATE DEMO EMERGENCY
                </button>
                <button type="button" id="reset-demo-btn" class="demo-action-btn secondary" data-i18n="reset_demo">
                    🔄 RESET
                </button>
            </div>
        </div>

        <!-- ================= 2. GLOBAL DESKTOP & MOBILE HEADER ================= -->
        <header class="global-header">
            <div class="header-container">
                <!-- Brand Emblem & Identity -->
                <div class="brand-block" id="nav-brand-home">
                    <div class="brand-emblem">
                        <span class="emblem-shield">🛡️</span>
                        <span class="emblem-pin">📍</span>
                    </div>
                    <div class="brand-text-col">
                        <h1 class="brand-title">WariSeva <span class="ai-badge">AI</span></h1>
                        <p class="brand-tagline" data-i18n="tagline">Your safety, one tap away.</p>
                    </div>
                </div>

                <!-- Desktop Main Navigation -->
                <nav class="desktop-nav" role="navigation" aria-label="Main Navigation">
                    <button class="nav-link-btn active" data-view="home-view" id="nav-home">
                        <span class="nav-icon">🏠</span>
                        <span data-i18n="nav_home">Home</span>
                    </button>
                    <button class="nav-link-btn" data-view="emergency-view" id="nav-emergency">
                        <span class="nav-icon">🚨</span>
                        <span data-i18n="nav_emergency">Emergency</span>
                        <span id="header-em-badge" class="header-badge hidden">1</span>
                    </button>
                    <button class="nav-link-btn" data-view="safety-map-view" id="nav-safety-map">
                        <span class="nav-icon">🗺️</span>
                        <span data-i18n="nav_map">Safety Map</span>
                    </button>
                    <button class="nav-link-btn" data-view="services-view" id="nav-services">
                        <span class="nav-icon">🛡️</span>
                        <span data-i18n="nav_services">Services</span>
                    </button>
                    <button class="nav-link-btn" data-view="volunteer-view" id="nav-volunteer">
                        <span class="nav-icon">🙋</span>
                        <span data-i18n="nav_volunteer">Volunteer</span>
                    </button>
                    <button class="nav-link-btn" data-view="responder-view" id="nav-responder">
                        <span class="nav-icon">🚑</span>
                        <span data-i18n="nav_responder">Responder</span>
                    </button>
                    <button class="nav-link-btn" data-view="command-view" id="nav-command">
                        <span class="nav-icon">🛰️</span>
                        <span data-i18n="nav_command">Command</span>
                    </button>
                </nav>

                <!-- Header Utility Controls (Elderly Toggle + Language Selector) -->
                <div class="header-controls">
                    <!-- Elder-Friendly Mode Switch -->
                    <button type="button" id="elder-mode-toggle" class="elder-mode-btn" title="Toggle Elder-Friendly Large Text & Simple Layout" aria-label="Toggle Elder-Friendly Mode">
                        <span class="elder-icon">👴</span>
                        <span class="elder-text" data-i18n="elder_mode">Elder Mode</span>
                    </button>

                    <!-- Language Switcher -->
                    <div class="lang-selector-group">
                        <select id="lang-select" class="lang-dropdown" aria-label="Select Language">
                            <option value="en" selected>English</option>
                            <option value="mr">मराठी</option>
                            <option value="hi">हिन्दी</option>
                        </select>
                    </div>

                    <!-- User / Safety ID Quick Pill -->
                    <div class="user-id-pill" id="user-header-pill" title="Active WariSeva ID">
                        <span class="pill-dot"></span>
                        <span id="header-wari-id">WS-28471</span>
                    </div>
                </div>
            </div>

            <!-- Value Proposition Banner Strip -->
            <div class="value-prop-strip">
                <div class="value-prop-content">
                    <span class="prop-highlight" data-i18n="value_prop">"We don't just report an emergency — we coordinate the response behind the SOS."</span>
                    <span class="prop-flow">One SOS → Right Responder → Right Location → Fastest Safe Response</span>
                </div>
            </div>
        </header>

        <!-- ================= ELDER-FRIENDLY SIMPLIFIED VIEW OVERLAY ================= -->
        <div id="elder-mode-container" class="elder-mode-screen hidden" role="region" aria-label="Elder-Friendly Simplified Mode">
            <div class="elder-screen-header">
                <div class="elder-header-left">
                    <span class="elder-banner-icon">👴</span>
                    <div>
                        <h2 class="elder-screen-title" data-i18n="elder_screen_title">ज्येष्ठ नागरिक सुरक्षा मोड • ELDER MODE</h2>
                        <p class="elder-screen-sub" data-i18n="elder_screen_sub">सोपी व मोठी बटणे • तात्काळ मदत एका स्पर्शात</p>
                    </div>
                </div>
                <div class="elder-header-actions">
                    <button type="button" class="elder-lang-btn" data-lang="mr">मराठी</button>
                    <button type="button" class="elder-lang-btn" data-lang="hi">हिन्दी</button>
                    <button type="button" class="elder-lang-btn" data-lang="en">EN</button>
                    <button type="button" id="exit-elder-mode-btn" class="elder-exit-btn" data-i18n="exit_elder_mode">✕ सामान्य मोड</button>
                </div>
            </div>

            <!-- Elder 5 Mega Action Buttons -->
            <div class="elder-mega-buttons-grid">
                <!-- 1. EMERGENCY SOS -->
                <button type="button" class="elder-btn elder-sos-btn" id="elder-sos-action-btn">
                    <span class="elder-btn-icon">🚨</span>
                    <div class="elder-btn-text-col">
                        <span class="elder-btn-title" data-i18n="elder_sos_title">🆘 तातडीची मदत (EMERGENCY)</span>
                        <span class="elder-btn-desc" data-i18n="elder_sos_desc">दाबा — मदत त्वरित आपल्याकडे येईल</span>
                    </div>
                </button>

                <!-- 2. WHERE AM I? -->
                <button type="button" class="elder-btn elder-loc-btn" id="elder-where-am-i-btn">
                    <span class="elder-btn-icon">📍</span>
                    <div class="elder-btn-text-col">
                        <span class="elder-btn-title" data-i18n="elder_where_title">📍 मी कुठे आहे? (WHERE AM I?)</span>
                        <span class="elder-btn-desc" id="elder-location-spoken-text">सासवड पालखी मैदान • झोन ०४</span>
                    </div>
                </button>

                <!-- 3. MEDICAL HELP -->
                <button type="button" class="elder-btn elder-med-btn" id="elder-medical-btn">
                    <span class="elder-btn-icon">🏥</span>
                    <div class="elder-btn-text-col">
                        <span class="elder-btn-title" data-i18n="elder_med_title">🏥 डॉक्टर / औषधोपचार (MEDICAL)</span>
                        <span class="elder-btn-desc" data-i18n="elder_med_desc">जवळचे आरोग्य शिबिर (१८० मीटर)</span>
                    </div>
                </button>

                <!-- 4. WATER -->
                <button type="button" class="elder-btn elder-water-btn" id="elder-water-btn">
                    <span class="elder-btn-icon">💧</span>
                    <div class="elder-btn-text-col">
                        <span class="elder-btn-title" data-i18n="elder_water_title">💧 पिण्याचे पाणी (WATER)</span>
                        <span class="elder-btn-desc" data-i18n="elder_water_desc">सासवड पालखी मैदान जल केंद्र (५५ मीटर)</span>
                    </div>
                </button>

                <!-- 5. TOILET -->
                <button type="button" class="elder-btn elder-toilet-btn" id="elder-toilet-btn">
                    <span class="elder-btn-icon">🚻</span>
                    <div class="elder-btn-text-col">
                        <span class="elder-btn-title" data-i18n="elder_toilet_title">🚻 स्वच्छतागृह (TOILETS)</span>
                        <span class="elder-btn-desc" data-i18n="elder_toilet_desc">स्वच्छ मोबाईल टॉयलेट (९० मीटर)</span>
                    </div>
                </button>
            </div>
        </div>

        <!-- ================= 3. MAIN APPLICATION VIEWS ================= -->
        <main class="main-body">

            <!-- ================= VIEW 1: HOME (REDESIGNED) ================= -->
            <section id="home-view" class="content-view active" role="region" aria-label="Home Dashboard">
                <div class="home-container">
                    
                    <!-- Active Emergency Notice Banner (Appears if emergency exists) -->
                    <div id="home-active-emergency-banner" class="active-emergency-alert-card hidden">
                        <div class="alert-card-left">
                            <span class="pulsing-em-icon">🚨</span>
                            <div>
                                <h3 class="alert-em-title" data-i18n="active_em_title">ACTIVE EMERGENCY IN PROGRESS</h3>
                                <p class="alert-em-sub" id="home-em-status-summary">Incident EM-28471 • Dispatched to Volunteer V-001</p>
                            </div>
                        </div>
                        <button type="button" class="view-emergency-btn" id="home-jump-to-emergency-btn" data-i18n="view_live_response">
                            VIEW LIVE RESPONSE →
                        </button>
                    </div>

                    <!-- Hero Section -->
                    <div class="home-hero-card">
                        <div class="hero-header-text">
                            <span class="hero-badge" data-i18n="palkhi_safety">🚩 Palkhi Safety Coordination</span>
                            <h2 class="hero-main-title">WARISEVA AI</h2>
                            <p class="hero-tagline" data-i18n="hero_tagline">"Your safety, one tap away."</p>
                            <p class="hero-subtext" data-i18n="hero_subtext">Emergency coordination and safety assistance for the Sant Dnyaneshwar & Sant Tukaram Palkhi Wari.</p>
                        </div>

                        <!-- Primary Massive SOS Component -->
                        <div class="hero-sos-stage">
                            <div class="sos-ripple-ring"></div>
                            <div class="sos-ripple-ring outer"></div>
                            <button type="button" id="main-sos-button" class="master-sos-button" aria-label="Press for Emergency SOS">
                                <div class="sos-content-wrap">
                                    <span class="sos-mega-icon">🚨</span>
                                    <span class="sos-mega-text" data-i18n="sos_btn_text">EMERGENCY</span>
                                    <span class="sos-mega-sub" data-i18n="sos_btn_sub">PRESS FOR HELP • मदत</span>
                                </div>
                            </button>
                        </div>

                        <!-- GPS & Zone Status Pill -->
                        <div class="current-location-pill">
                            <span class="loc-pin-icon">📍</span>
                            <div class="loc-text-col">
                                <span class="loc-zone-label" id="home-current-zone" data-i18n="current_zone">Zone 04 — Saswad Palkhi Maidan</span>
                                <span class="loc-coords-sub" id="home-current-coords">18.3444, 74.0305 (GPS Active • ±5m)</span>
                            </div>
                        </div>

                        <!-- Secondary Quick Action Buttons -->
                        <div class="hero-secondary-actions">
                            <button type="button" class="quick-act-btn" id="home-where-am-i-btn">
                                <span class="act-icon">📍</span>
                                <span data-i18n="act_where_am_i">Where am I?</span>
                            </button>
                            <button type="button" class="quick-act-btn" id="home-find-medical-btn">
                                <span class="act-icon">🏥</span>
                                <span data-i18n="act_medical_help">Medical Help</span>
                            </button>
                            <button type="button" class="quick-act-btn" id="home-open-safety-map-btn">
                                <span class="act-icon">🗺️</span>
                                <span data-i18n="act_safety_map">Safety Map</span>
                            </button>
                            <button type="button" class="quick-act-btn" id="home-group-btn">
                                <span class="act-icon">👥</span>
                                <span>My Group</span>
                            </button>
                        </div>
                    </div>

                    <!-- Quick Safety Services Grid -->
                    <div class="home-services-section">
                        <div class="section-title-row">
                            <h3 class="home-section-title" data-i18n="quick_services_title">🛡️ Quick Safety Services / सुविधा</h3>
                            <button type="button" class="text-link-btn" id="home-see-all-services-btn" data-i18n="see_all">See All 13 Facilities →</button>
                        </div>
                        <div class="home-services-tiles-grid">
                            <button type="button" class="service-tile-home" data-service-type="WATER">
                                <span class="tile-glyph">💧</span>
                                <span class="tile-head" data-i18n="svc_water">Water</span>
                                <span class="tile-foot" data-i18n="svc_water_sub">पिण्याचे पाणी</span>
                            </button>
                            <button type="button" class="service-tile-home" data-service-type="TOILET">
                                <span class="tile-glyph">🚻</span>
                                <span class="tile-head" data-i18n="svc_toilets">Toilets</span>
                                <span class="tile-foot" data-i18n="svc_toilets_sub">स्वच्छतागृह</span>
                            </button>
                            <button type="button" class="service-tile-home" data-service-type="REST_AREA">
                                <span class="tile-glyph">🛏️</span>
                                <span class="tile-head" data-i18n="svc_rest">Rest</span>
                                <span class="tile-foot" data-i18n="svc_rest_sub">विश्रांती मंडप</span>
                            </button>
                            <button type="button" class="service-tile-home" data-service-type="MEDICAL_CAMP">
                                <span class="tile-glyph">🏥</span>
                                <span class="tile-head" data-i18n="svc_medical">Medical</span>
                                <span class="tile-foot" data-i18n="svc_medical_sub">आरोग्य केंद्र</span>
                            </button>
                        </div>
                    </div>

                    <!-- Safety ID Creation Card Section -->
                    <div class="home-safety-id-card" id="home-safety-id-card">
                        <div class="card-top-header">
                            <div>
                                <h3 class="card-head-title" data-i18n="safety_id_title">WariSeva Safety ID / सुरक्षा ओळखपत्र</h3>
                                <p class="card-head-sub" data-i18n="safety_id_sub">Register demo profile for quick identification and instant SOS dispatch.</p>
                            </div>
                            <span class="card-top-icon">🪪</span>
                        </div>

                        <form id="safety-id-form" class="safety-form-grid">
                            <div class="form-field">
                                <label for="user-name" class="field-label" data-i18n="label_full_name">Full Name / पूर्ण नाव</label>
                                <input type="text" id="user-name" class="field-input" placeholder="e.g. Tukaram Shinde" required autocomplete="name">
                            </div>
                            <div class="form-field">
                                <label for="user-phone" class="field-label" data-i18n="label_phone">Mobile Number / फोन नंबर</label>
                                <input type="tel" id="user-phone" class="field-input" placeholder="10-digit mobile number" required pattern="[0-9]{10}">
                            </div>
                            <div id="form-error" class="form-error-text hidden" role="alert"></div>
                            <button type="submit" id="create-id-btn" class="form-submit-btn" data-i18n="btn_create_id">
                                CREATE SAFETY ID
                            </button>
                        </form>

                        <!-- Created Safety ID Card -->
                        <div id="safety-id-result" class="safety-result-box hidden">
                            <div class="id-badge-banner">
                                <span class="badge-check">✓</span>
                                <span data-i18n="id_active_badge">Safety ID Active & Registered</span>
                            </div>
                            <div class="id-profile-summary">
                                <div>
                                    <div class="profile-name" id="display-user-name">Tukaram Shinde</div>
                                    <div class="profile-role">WARKARI • वारकरी</div>
                                </div>
                                <div class="profile-wari-id" id="display-wari-id">WS-28471</div>
                            </div>
                            <div class="qr-code-holder">
                                <div class="qr-mock-box">
                                    <div class="qr-dots-pattern">
                                        <span></span><span></span><span></span><span></span>
                                        <span></span><span></span><span></span><span></span>
                                        <span></span><span></span><span></span><span></span>
                                        <span></span><span></span><span></span><span></span>
                                    </div>
                                    <span class="qr-caption" id="qr-id-caption">WS-28471</span>
                                </div>
                            </div>
                            <button type="button" id="create-another-btn" class="text-secondary-btn" data-i18n="btn_change_profile">
                                Change / Register Another Profile
                            </button>
                        </div>
                    </div>
                </div>
            </section>

            <!-- ================= VIEW 2: ACTIVE EMERGENCY & LIVE TIMELINE ================= -->
            <section id="emergency-view" class="content-view hidden" role="region" aria-label="Active Emergency Screen">
                <div class="emergency-container">
                    
                    <!-- Response Status Header (Section 9) -->
                    <div class="response-status-header-banner" id="em-status-header-banner">
                        <div class="rsh-top">
                            <span class="rsh-pulse-badge">🚨</span>
                            <div>
                                <span class="rsh-kicker">EMERGENCY COORDINATION ACTIVE</span>
                                <h2 class="rsh-title" id="em-current-status-title">🟡 VOLUNTEER RESPONDING</h2>
                            </div>
                        </div>
                        <div class="rsh-id-tag">
                            <span>Incident:</span>
                            <strong id="em-id-display">EM-28471</strong>
                        </div>
                    </div>

                    <!-- Clear "RESPONSE IN PROGRESS" Card (Section 4) -->
                    <div class="response-in-progress-card" id="response-in-progress-card">
                        <div class="rip-card-head">
                            <div class="rip-head-left">
                                <span class="rip-icon">🚨</span>
                                <div>
                                    <h3 class="rip-title">RESPONSE IN PROGRESS</h3>
                                    <span class="rip-sub">Nearest Volunteer Coordination</span>
                                </div>
                            </div>
                            <span class="rip-status-pill" id="rip-status-pill">🟡 RESPONDING</span>
                        </div>
                        <div class="rip-body">
                            <div class="rip-volunteer-profile">
                                <span class="rip-avatar">👤</span>
                                <div>
                                    <h4 class="rip-vol-name" id="rip-vol-name">Ramesh Kulkarni</h4>
                                    <span class="rip-vol-id" id="rip-vol-id">Volunteer V-001</span>
                                    <p class="rip-sector" id="rip-vol-sector">Assigned Sector: Zone 04 — Saswad Palkhi Maidan</p>
                                </div>
                            </div>
                            <div class="rip-metrics-row">
                                <div class="rip-metric-box">
                                    <span class="rip-m-lbl">Distance:</span>
                                    <strong class="rip-m-val highlight-cyan" id="rip-dist-val">320m</strong>
                                </div>
                                <div class="rip-metric-box">
                                    <span class="rip-m-lbl">ETA:</span>
                                    <strong class="rip-m-val highlight-orange" id="rip-eta-val">2 min</strong>
                                </div>
                                <div class="rip-metric-box">
                                    <span class="rip-m-lbl">Status:</span>
                                    <strong class="rip-m-val highlight-green" id="rip-status-text">🟡 Responding</strong>
                                </div>
                            </div>
                            <div class="rip-sim-notice">
                                <span class="sim-badge">DEMO • SIMULATED LIVE LOCATION</span>
                                <span class="sim-desc">Auto-updating distance countdown to patient arrival</span>
                            </div>
                        </div>
                    </div>

                    <!-- Simulation Control Action Bar (Section 8) -->
                    <div class="simulation-quick-bar">
                        <button type="button" class="sim-trigger-btn" id="em-simulate-btn">
                            ▶ SIMULATE RESPONSE (Auto-Advance Timeline)
                        </button>
                    </div>

                    <!-- Incident Location Summary Bar -->
                    <div class="em-location-bar">
                        <div class="em-loc-item">
                            <span class="em-loc-icon">🗺️</span>
                            <div>
                                <span class="em-loc-label" data-i18n="palkhi_zone">Wari Palkhi Zone</span>
                                <span class="em-loc-val" id="em-zone-display">Zone 04 — Saswad Palkhi Maidan</span>
                            </div>
                        </div>
                        <div class="em-loc-item">
                            <span class="em-loc-icon">📍</span>
                            <div>
                                <span class="em-loc-label" data-i18n="nearest_landmark">Nearest Landmark</span>
                                <span class="em-loc-val" id="em-landmark-display">Saswad Central Palkhi Maidan Ground</span>
                            </div>
                        </div>
                        <div class="em-loc-item">
                            <span class="em-loc-icon">🎯</span>
                            <div>
                                <span class="em-loc-label" data-i18n="gps_precision">GPS Precision</span>
                                <span class="em-loc-val" id="em-coords-display">18.3444, 74.0305 (±5 m)</span>
                            </div>
                        </div>
                    </div>

                    <!-- Interactive Live Emergency Map Section -->
                    <div class="em-interactive-map-card">
                        <div class="em-map-card-head">
                            <div class="head-left">
                                <span class="em-map-title">📍 Live Multi-Party Response Map</span>
                                <span class="em-map-sub">Real-time GPS coordinates of Patient, Volunteer, and Medical Responder</span>
                            </div>
                            <div class="em-map-camera-controls">
                                <button type="button" class="cam-btn" id="em-cam-patient" title="Center on Patient">
                                    📍 Patient
                                </button>
                                <button type="button" class="cam-btn" id="em-cam-volunteer" title="Center on Volunteer">
                                    🔵 Volunteer
                                </button>
                                <button type="button" class="cam-btn" id="em-cam-responder" title="Center on Responder">
                                    🚑 Responder
                                </button>
                                <button type="button" class="cam-btn active" id="em-cam-fit-all" title="Fit all on map">
                                    🗺️ Fit All
                                </button>
                            </div>
                        </div>

                        <!-- Live Leaflet Map Container -->
                        <div id="emergency-live-map" class="emergency-leaflet-map" style="height: 380px; width: 100%; border-radius: 12px; background: #161B22;"></div>

                        <!-- Map Legend Strip -->
                        <div class="em-map-legend-strip">
                            <div class="legend-item"><span class="legend-dot red"></span> 📍 Patient (You)</div>
                            <div class="legend-item"><span class="legend-dot blue"></span> 🔵 Volunteer (First Contact)</div>
                            <div class="legend-item"><span class="legend-dot orange"></span> 🚑 Medical Responder (Ambulance)</div>
                            <div class="legend-item"><span class="legend-line green"></span> 🟢 Safe Bypass Corridor</div>
                        </div>
                    </div>

                    <!-- Complete 9-Step Visual Timeline (Section 2) -->
                    <div class="timeline-card">
                        <h3 class="timeline-header" data-i18n="response_timeline">📊 Emergency Response Timeline</h3>
                        
                        <div class="timeline-stepper">
                            <!-- STEP 1: SOS Sent & Registered -->
                            <div class="timeline-step step-done" id="step-1-sos">
                                <div class="step-marker">✓</div>
                                <div class="step-body">
                                    <div class="step-title">🚨 Step 1: SOS Sent & Registered</div>
                                    <div class="step-desc">Emergency registered in central incident registry.</div>
                                </div>
                            </div>

                            <!-- STEP 2: Location & Wari Zone Identified -->
                            <div class="timeline-step step-done" id="step-2-loc">
                                <div class="step-marker">✓</div>
                                <div class="step-body">
                                    <div class="step-title">📍 Step 2: Location & Wari Zone Identified</div>
                                    <div class="step-desc">Location matched to Zone 04 — Saswad Palkhi Maidan.</div>
                                </div>
                            </div>

                            <!-- STEP 3: Nearest Volunteer Found -->
                            <div class="timeline-step" id="step-3-vol-found">
                                <div class="step-marker">3</div>
                                <div class="step-body">
                                    <div class="step-title">👥 Step 3: Nearest Volunteer Found</div>
                                    <div class="step-desc" id="step-3-vol-desc">Ramesh Kulkarni (V-001) • 320m away</div>
                                </div>
                            </div>

                            <!-- STEP 4: Volunteer Alert Sent -->
                            <div class="timeline-step" id="step-4-alert-sent">
                                <div class="step-marker">4</div>
                                <div class="step-body">
                                    <div class="step-title">🔔 Step 4: Volunteer Alert Sent</div>
                                    <div class="step-desc">Emergency alert sent to nearest available volunteer.</div>
                                </div>
                            </div>

                            <!-- STEP 5: Volunteer En Route -->
                            <div class="timeline-step" id="step-5-vol-enroute">
                                <div class="step-marker">5</div>
                                <div class="step-body">
                                    <div class="step-title">🚶 Step 5: Volunteer En Route</div>
                                    <div class="step-desc" id="step-5-enroute-desc">Ramesh Kulkarni is moving toward the patient (<span id="step-5-dist-tag">320m</span> • ETA <span id="step-5-eta-tag">2 min</span>).</div>
                                </div>
                            </div>

                            <!-- STEP 6: Volunteer Reached Patient -->
                            <div class="timeline-step" id="step-6-vol-reached">
                                <div class="step-marker">6</div>
                                <div class="step-body">
                                    <div class="step-title">🤝 Step 6: Volunteer Reached Patient</div>
                                    <div class="step-desc">Volunteer reached the patient (0m • With Patient).</div>
                                </div>
                            </div>

                            <!-- STEP 7: Medical Responder Dispatched -->
                            <div class="timeline-step" id="step-7-resp-dispatched">
                                <div class="step-marker">7</div>
                                <div class="step-body">
                                    <div class="step-title">🚑 Step 7: Medical Responder Dispatched</div>
                                    <div class="step-desc">Dr. Arvind Shinde (MR-001) Mobile Ambulance Unit 1.</div>
                                </div>
                            </div>

                            <!-- STEP 8: Hospital Escalation -->
                            <div class="timeline-step" id="step-8-hosp-escalation">
                                <div class="step-marker">8</div>
                                <div class="step-body">
                                    <div class="step-title">🏥 Step 8: Hospital Escalation</div>
                                    <div class="step-desc" id="step-8-hosp-desc">Saswad Rural Hospital (2.8 km • 8 min • Available).</div>
                                </div>
                            </div>

                            <!-- STEP 9: Emergency Response Coordinated -->
                            <div class="timeline-step" id="step-9-coordinated">
                                <div class="step-marker">9</div>
                                <div class="step-body">
                                    <div class="step-title">✅ Step 9: Emergency Response Coordinated</div>
                                    <div class="step-desc">Patient connected with emergency medical response.</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Hospital Escalation Card (Section 10) -->
                    <div class="hospital-escalation-card" id="hospital-escalation-card">
                        <div class="hec-head">
                            <div class="hec-head-left">
                                <span class="hec-icon">🏥</span>
                                <div>
                                    <h3 class="hec-title">MEDICAL ESCALATION</h3>
                                    <span class="hec-sub">Nearest Suitable Hospital</span>
                                </div>
                            </div>
                            <span class="hec-status-pill">🟢 Available</span>
                        </div>
                        <div class="hec-body">
                            <h4 class="hec-hosp-name" id="hec-hospital-name">Saswad Rural Hospital</h4>
                            <div class="hec-metrics">
                                <span>Distance: <strong id="hec-hosp-dist">2.8 km</strong></span>
                                <span>ETA: <strong id="hec-hosp-eta">8 min</strong></span>
                                <span>Status: <strong class="text-success">🟢 Available</strong></span>
                            </div>
                            <button type="button" class="hec-view-btn" id="hec-view-btn">
                                🏥 VIEW HOSPITAL & ESCALATION DETAILS
                            </button>
                        </div>
                    </div>

                    <!-- Emergency Actions Footer & Sharing -->
                    <div class="em-bottom-actions">
                        <button type="button" class="em-action-btn share-btn" id="em-share-details-btn">
                            📱 SHARE EMERGENCY
                        </button>
                        <button type="button" class="em-action-btn secondary" id="em-view-tactical-map-btn" data-i18n="btn_open_tactical_map">
                            🗺️ VIEW TACTICAL MAP
                        </button>
                        <button type="button" class="em-action-btn primary" id="em-new-sos-btn" data-i18n="btn_report_another">
                            REPORT ANOTHER EMERGENCY
                        </button>
                    </div>
                </div>
            </section>

            <!-- ================= VIEW 3: INTERACTIVE SAFETY MAP ================= -->
            <section id="safety-map-view" class="content-view hidden" role="region" aria-label="Interactive Safety Map">
                <div class="safety-map-container">
                    <div class="map-filter-toolbar">
                        <span class="filter-label" data-i18n="filter_label">Filters:</span>
                        <div class="filter-pills-row" id="map-filter-group">
                            <button type="button" class="filter-pill active" data-filter="ALL">ALL (13)</button>
                            <button type="button" class="filter-pill" data-filter="WATER">💧 Water</button>
                            <button type="button" class="filter-pill" data-filter="TOILET">🚻 Toilets</button>
                            <button type="button" class="filter-pill" data-filter="MEDICAL_CAMP">🏥 Medical Camps</button>
                            <button type="button" class="filter-pill" data-filter="REST_AREA">🛏️ Rest Areas</button>
                            <button type="button" class="filter-pill" data-filter="FOOD">🍛 Food / Prasad</button>
                            <button type="button" class="filter-pill" data-filter="HOSPITAL">🚑 Hospitals</button>
                            <button type="button" class="filter-pill" data-filter="EMERGENCIES">🚨 Incidents</button>
                        </div>
                    </div>

                    <div class="map-and-sidebar-layout">
                        <div class="main-map-column">
                            <div class="map-legend-header">
                                <span class="map-legend-title">🗺️ Palkhi Route Safety & Resource Map</span>
                                <div class="map-legend-items">
                                    <span class="legend-chip"><span class="chip-dot red"></span> Patient 📍</span>
                                    <span class="legend-chip"><span class="chip-dot blue"></span> Volunteer 🔵</span>
                                    <span class="legend-chip"><span class="chip-dot green"></span> Responder 🚑</span>
                                </div>
                            </div>
                            <div id="main-safety-map" class="full-leaflet-map"></div>
                        </div>

                        <div class="map-info-sidebar" id="map-info-sidebar">
                            <div class="sidebar-default-msg" id="sidebar-empty-state">
                                <span class="empty-icon">📍</span>
                                <h4 data-i18n="map_pin_prompt">Select Any Map Pin</h4>
                                <p data-i18n="map_pin_prompt_sub">Click any service marker or emergency incident to view distance, route, and details.</p>
                            </div>

                            <div class="sidebar-card-content hidden" id="sidebar-detail-card">
                                <div class="sidebar-card-top">
                                    <span class="sidebar-category-tag" id="sb-category-badge">💧 DRINKING WATER</span>
                                    <span class="sidebar-dist-badge" id="sb-dist-badge">250 m away</span>
                                </div>
                                <h3 class="sidebar-facility-name" id="sb-name">Saswad Palkhi Maidan Clean Drinking Water Point</h3>
                                <div class="sidebar-zone-row" id="sb-zone">📍 Zone 04 — Saswad Palkhi Maidan</div>
                                <div class="sidebar-address-row" id="sb-address">Saswad-Hadapsar Road, Gate 2</div>
                                <div class="sidebar-note-row" id="sb-note">ℹ️ 24/7 continuous supply with RO filtration</div>
                                <button type="button" class="sidebar-action-btn" id="sb-action-btn" data-i18n="btn_focus_pin">
                                    🎯 FOCUS ON MAP
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- ================= VIEW 4: EVERYDAY WARI SAFETY SERVICES ================= -->
            <section id="services-view" class="content-view hidden" role="region" aria-label="Safety Services Directory">
                <div class="services-container">
                    
                    <div class="services-header-card">
                        <div class="svc-header-left">
                            <span class="svc-header-icon">🛡️</span>
                            <div>
                                <h2 class="svc-header-title" data-i18n="services_page_title">Wari Safety Directory</h2>
                                <p class="svc-header-sub" data-i18n="services_page_sub">Find verified essential facilities across all 12 pilgrimage route sectors.</p>
                            </div>
                        </div>

                        <!-- Zone Filter Dropdown -->
                        <div class="zone-picker-wrap">
                            <label for="services-zone-dropdown" class="zone-picker-label" data-i18n="select_zone">Select Sector / झोन निवडा:</label>
                            <select id="services-zone-dropdown" class="zone-select-control">
                                <option value="ALL">All Route Zones / संपूर्ण मार्ग (13)</option>
                                <option value="Zone 04" selected>Zone 04 — Saswad Palkhi Maidan</option>
                                <option value="Zone 03">Zone 03 — Hadapsar / Dive Ghat Base</option>
                                <option value="Zone 05">Zone 05 — Jejuri Mandir Tappa</option>
                                <option value="Zone 02">Zone 02 — Pune City / Wakdewadi</option>
                                <option value="Zone 12">Zone 12 — Pandharpur Mandir Parisar</option>
                            </select>
                        </div>
                    </div>

                    <!-- "NEAREST TO ME" Safety Feature (Section 12) -->
                    <div class="nearest-services-summary-strip">
                        <h3 class="nss-title">📍 NEAREST SERVICES</h3>
                        <div class="nss-chips-grid">
                            <div class="nss-chip"><span class="nss-glyph">💧</span> Drinking Water: <strong>55m</strong></div>
                            <div class="nss-chip"><span class="nss-glyph">🚻</span> Toilet: <strong>90m</strong></div>
                            <div class="nss-chip"><span class="nss-glyph">🏥</span> Medical Camp: <strong>180m</strong></div>
                            <div class="nss-chip"><span class="nss-glyph">🛏</span> Rest Area: <strong>240m</strong></div>
                            <div class="nss-chip"><span class="nss-glyph">🍛</span> Food / Prasad: <strong>310m</strong></div>
                        </div>
                    </div>

                    <!-- Category Tile Selector -->
                    <div class="category-tiles-carousel">
                        <button type="button" class="cat-tile-btn active" data-category="WATER">
                            <span class="cat-emoji">💧</span>
                            <span class="cat-name" data-i18n="svc_water">Drinking Water</span>
                            <span class="cat-sub">पिण्याचे पाणी</span>
                        </button>
                        <button type="button" class="cat-tile-btn" data-category="TOILET">
                            <span class="cat-emoji">🚻</span>
                            <span class="cat-name" data-i18n="svc_toilets">Toilets</span>
                            <span class="cat-sub">स्वच्छतागृह</span>
                        </button>
                        <button type="button" class="cat-tile-btn" data-category="FOOD">
                            <span class="cat-emoji">🍛</span>
                            <span class="cat-name" data-i18n="svc_food">Food / Prasad</span>
                            <span class="cat-sub">अन्नछत्र सेवा</span>
                        </button>
                        <button type="button" class="cat-tile-btn" data-category="REST_AREA">
                            <span class="cat-emoji">🛏️</span>
                            <span class="cat-name" data-i18n="svc_rest">Rest Areas</span>
                            <span class="cat-sub">विश्रांती मंडप</span>
                        </button>
                        <button type="button" class="cat-tile-btn" data-category="MEDICAL_CAMP">
                            <span class="cat-emoji">🏥</span>
                            <span class="cat-name" data-i18n="svc_medical">Medical Camps</span>
                            <span class="cat-sub">आरोग्य शिबिर</span>
                        </button>
                        <button type="button" class="cat-tile-btn" data-category="HOSPITAL">
                            <span class="cat-emoji">🚑</span>
                            <span class="cat-name" data-i18n="svc_hospitals">Hospitals</span>
                            <span class="cat-sub">रुग्णालय</span>
                        </button>
                    </div>

                    <!-- Facility Results Cards Grid -->
                    <div class="services-results-section">
                        <div class="results-header-row">
                            <h3 class="results-title" id="services-grid-title">Nearby Drinking Water Facilities</h3>
                            <span class="results-counter" id="services-count-badge">2 facilities</span>
                        </div>
                        <div class="services-cards-grid" id="services-cards-list">
                            <p class="empty-feed-text">Loading verified facilities...</p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- ================= VIEW 5: VOLUNTEER DASHBOARD ================= -->
            <section id="volunteer-view" class="content-view hidden" role="region" aria-label="Volunteer Network Dashboard">
                <div class="responder-container">
                    
                    <div class="responder-header-card volunteer-accent">
                        <div class="resp-header-left">
                            <div class="role-avatar-circle vol-bg">🙋</div>
                            <div>
                                <span class="role-type-kicker">WARISEVA VOLUNTEER NETWORK</span>
                                <h2 class="role-name-title">Ramesh Kulkarni (V-001)</h2>
                                <p class="role-assigned-sector">Assigned Sector: Zone 04 — Saswad Palkhi Maidan</p>
                            </div>
                        </div>
                        <div class="resp-header-right">
                            <span class="status-chip available" id="volunteer-status-chip">STATUS: AVAILABLE</span>
                            <button type="button" class="refresh-feed-btn" id="refresh-volunteer-btn">🔄 Refresh Alerts</button>
                        </div>
                    </div>

                    <!-- Synchronized Active Emergency Dispatch Card (Section 5) -->
                    <div id="volunteer-active-response-box" class="active-task-card">
                        <div class="task-card-header">
                            <span class="task-status-pill enroute" id="vol-response-badge">ACTIVE EMERGENCY DISPATCH</span>
                            <span class="task-id-text" id="vol-response-em-id">EM-28471</span>
                        </div>

                        <div class="task-patient-info">
                            <div class="info-group">
                                <span class="info-label">Patient Name:</span>
                                <strong id="vol-patient-name">Tukaram Shinde</strong>
                            </div>
                            <div class="info-group">
                                <span class="info-label">Location:</span>
                                <strong id="vol-patient-zone">Zone 04 — Saswad Palkhi Maidan</strong>
                            </div>
                            <div class="info-group">
                                <span class="info-label">Distance:</span>
                                <strong class="highlight-cyan" id="vol-distance-val">320m</strong>
                            </div>
                            <div class="info-group">
                                <span class="info-label">Priority:</span>
                                <strong class="text-danger">URGENT</strong>
                            </div>
                        </div>

                        <!-- Live GPS Location Sharing Component -->
                        <div class="location-sharing-panel">
                            <div class="sharing-controls-row">
                                <button type="button" class="btn-feed-accept" id="vol-accept-em-btn">
                                    [ ACCEPT EMERGENCY ]
                                </button>
                                <button type="button" class="reach-btn" id="reached-patient-btn">
                                    🤝 I'M WITH PATIENT
                                </button>
                            </div>

                            <div id="reached-confirmed-banner" class="success-alert-banner hidden">
                                ✅ STATUS: 🟢 WITH PATIENT (0m). Patient initial physical safety verified.
                            </div>
                        </div>
                    </div>

                    <!-- Volunteer Feed -->
                    <div class="feed-container-card">
                        <h3 class="feed-section-head">🚨 Active Emergency Dispatch Alerts</h3>
                        <div id="volunteer-emergency-feed" class="emergency-feed-list">
                            <p class="empty-feed-text">Loading volunteer feed...</p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- ================= VIEW 6: MEDICAL RESPONDER & CROWD ROUTING ================= -->
            <section id="responder-view" class="content-view hidden" role="region" aria-label="Medical Responder Dashboard">
                <div class="responder-container">
                    
                    <div class="responder-header-card responder-accent">
                        <div class="resp-header-left">
                            <div class="role-avatar-circle resp-bg">🚑</div>
                            <div>
                                <span class="role-type-kicker">WARISEVA MEDICAL RESPONDER</span>
                                <h2 class="role-name-title">Dr. Arvind Shinde (MR-001)</h2>
                                <p class="role-assigned-sector">Mobile Ambulance Unit 1 • Saswad Sector</p>
                            </div>
                        </div>
                        <div class="resp-header-right">
                            <span class="status-chip available" id="responder-status-chip">STATUS: AVAILABLE</span>
                            <button type="button" class="refresh-feed-btn" id="refresh-responder-btn">🔄 Refresh Alerts</button>
                        </div>
                    </div>

                    <!-- Synchronized Active Medical Response Box (Section 6) -->
                    <div id="responder-active-box" class="active-task-card">
                        <div class="task-card-header">
                            <span class="task-status-pill enroute" id="resp-status-badge">🚑 INCOMING MEDICAL DISPATCH</span>
                            <span class="task-id-text" id="resp-active-em-id">EM-28471</span>
                        </div>

                        <div class="task-patient-info">
                            <div class="info-group">
                                <span class="info-label">Patient:</span>
                                <strong>Tukaram Shinde</strong>
                            </div>
                            <div class="info-group">
                                <span class="info-label">Zone:</span>
                                <strong>Zone 04 — Saswad Palkhi Maidan</strong>
                            </div>
                            <div class="info-group">
                                <span class="info-label">Assigned Unit:</span>
                                <strong>Dr. Arvind Shinde (MR-001) Mobile Ambulance Unit 1</strong>
                            </div>
                            <div class="info-group">
                                <span class="info-label">Status:</span>
                                <strong class="highlight-orange" id="resp-state-text">🟡 DISPATCHED</strong>
                            </div>
                        </div>

                        <!-- Tactical Interactive Map -->
                        <div class="tactical-map-deck">
                            <div class="tactical-map-header">
                                <span>📍 Live Crowd-Aware Navigation Map</span>
                                <div class="tactical-legend-strip">
                                    <span><strong style="color:#00E676;">― 🟢 Safe Bypass (3 min)</strong></span>
                                    <span><strong style="color:#FF5252;">--- 🔴 Congested Direct (10 min)</strong></span>
                                </div>
                            </div>
                            <div id="responder-map" class="tactical-leaflet-box"></div>
                        </div>

                        <!-- Hospital Escalation Action Deck -->
                        <div class="hospital-deck" id="hospital-escalation-section">
                            <button type="button" id="escalate-hospital-btn" class="escalate-trigger-btn">
                                🏥 ESCALATE TO HOSPITAL / रुग्णालय संदर्भ
                            </button>

                            <div id="hospital-selection-card" class="hospital-picker-modal hidden">
                                <h4 class="hospital-modal-title">🏥 Select Nearby Hospital (Ranked by Trauma Readiness)</h4>
                                <div id="nearby-hospitals-list" class="hospital-list-flow">
                                    <p class="empty-feed-text">Loading suitable hospitals...</p>
                                </div>
                            </div>

                            <div id="hospital-selected-banner" class="hospital-selected-card hidden">
                                <div class="hosp-confirm-kicker">🏥 DESTINATION HOSPITAL SELECTED</div>
                                <h4 class="hosp-confirm-name" id="selected-hospital-name">Saswad Rural Hospital</h4>
                                <div class="hosp-confirm-address" id="selected-hospital-details">Saswad-Hadapsar Road • 2.8 km • ETA 8 min</div>
                                <div class="hosp-confirm-notice">Transport coordinated by emergency responder team.</div>
                            </div>
                        </div>

                        <!-- Responder Transit State Controls -->
                        <div class="responder-state-controls">
                            <div class="resp-transit-dual-btns">
                                <button type="button" id="resp-start-response-btn" class="transit-btn enroute">
                                    🔵 START RESPONSE (EN ROUTE)
                                </button>
                                <button type="button" id="resp-mark-arrived-btn" class="transit-btn arrived">
                                    🟢 MARK ARRIVED ON SCENE
                                </button>
                            </div>
                            <div id="resp-arrived-banner" class="success-alert-banner hidden">
                                🩺 Medical Responder at patient location. Administering triage.
                            </div>
                        </div>
                    </div>

                    <!-- Responder Alert Feed -->
                    <div class="feed-container-card">
                        <h3 class="feed-section-head">Incoming Medical Dispatch Alerts</h3>
                        <div id="responder-emergency-feed" class="emergency-feed-list">
                            <p class="empty-feed-text">Loading responder alerts...</p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- ================= VIEW 7: 3-COLUMN COMMAND CENTER ================= -->
            <section id="command-view" class="content-view hidden" role="region" aria-label="Tactical Command Center">
                <div class="command-dashboard-layout">
                    
                    <!-- Command Center Top Bar -->
                    <div class="command-top-strip">
                        <div class="cmd-strip-left">
                            <span class="cmd-badge">🛰️ TACTICAL COMMAND CENTER</span>
                            <span class="cmd-sub">Palkhi Route Emergency Operations Hub</span>
                        </div>
                        <div class="cmd-tabs-group">
                            <button type="button" class="cmd-tab-btn active" id="cmd-tab-operations">📊 Operations</button>
                            <button type="button" class="cmd-tab-btn" id="cmd-tab-heatmap">🔥 Heatmap</button>
                            <button type="button" class="cmd-tab-btn" id="cmd-tab-readiness">🏕️ Readiness</button>
                        </div>
                        <div class="cmd-strip-right">
                            <span class="cmd-counter-chip" id="command-total-count">TOTAL: 1 INCIDENTS</span>
                            <button type="button" class="refresh-feed-btn" id="refresh-command-btn">🔄 Refresh</button>
                        </div>
                    </div>

                    <!-- TAB 1: 3-Column Tactical Operations Layout -->
                    <div class="command-3col-grid" id="cmd-operations-subview">
                        
                        <!-- COLUMN 1 (LEFT): Active Emergencies List -->
                        <div class="cmd-col-left">
                            <div class="col-head">
                                <h4>Active Incidents</h4>
                                <span class="col-count" id="cmd-incident-count">1</span>
                            </div>
                            <div class="cmd-incident-scroll" id="command-emergency-list">
                                <p class="empty-feed-text">Fetching live incident registry...</p>
                            </div>
                        </div>

                        <!-- COLUMN 2 (CENTER): Large Live Tactical Map -->
                        <div class="cmd-col-center">
                            <div class="col-head">
                                <h4>Tactical Route & Incident Map</h4>
                                <div class="cmd-map-legend">
                                    <span><span class="chip-dot red"></span> Patient</span>
                                    <span><span class="chip-dot blue"></span> Volunteer</span>
                                    <span><span class="chip-dot green"></span> Responder</span>
                                </div>
                            </div>
                            <div id="command-map" class="command-leaflet-map"></div>
                        </div>

                        <!-- COLUMN 3 (RIGHT): Selected Incident Inspector -->
                        <div class="cmd-col-right" id="command-inspector-panel">
                            <div class="col-head">
                                <h4>Incident Telemetry</h4>
                                <span class="selected-id-tag" id="cmd-ins-id">EM-28471</span>
                            </div>

                            <div class="inspector-card-body" id="cmd-inspector-content">
                                <div class="ins-status-badge-row">
                                    <span class="ins-priority-badge">🔴 URGENT</span>
                                    <span class="ins-status-badge" id="cmd-ins-status">WITH_PATIENT</span>
                                </div>

                                <div class="ins-data-block">
                                    <span class="ins-label">Patient:</span>
                                    <strong id="cmd-ins-patient">Tukaram Shinde (WS-28471)</strong>
                                    <div class="ins-sub" id="cmd-ins-zone">Zone 04 — Saswad Palkhi Maidan</div>
                                    <div class="ins-coords" id="cmd-ins-coords">18.3444, 74.0305 (±5m)</div>
                                </div>

                                <div class="ins-data-block">
                                    <span class="ins-label">Volunteer:</span>
                                    <strong id="cmd-ins-volunteer">Ramesh Kulkarni (V-001)</strong>
                                    <div class="ins-sub" id="cmd-ins-vol-status">Status: 👥 WITH PATIENT</div>
                                </div>

                                <div class="ins-data-block">
                                    <span class="ins-label">Medical Responder:</span>
                                    <strong id="cmd-ins-responder">Dr. Arvind Shinde (MR-001)</strong>
                                    <div class="ins-sub" id="cmd-ins-resp-status">Status: 🩺 On Scene</div>
                                </div>

                                <div class="ins-data-block">
                                    <span class="ins-label">Hospital:</span>
                                    <strong id="cmd-ins-hospital">Saswad Rural Hospital</strong>
                                </div>

                                <!-- Tactical Camera Focus Controls -->
                                <div class="ins-cam-controls-row">
                                    <button type="button" class="ins-cam-btn" id="cmd-cam-patient">🎯 Patient</button>
                                    <button type="button" class="ins-cam-btn" id="cmd-cam-vol">🔵 Volunteer</button>
                                    <button type="button" class="ins-cam-btn" id="cmd-cam-resp">🚑 Responder</button>
                                </div>

                                <div class="ins-resolve-box">
                                    <button type="button" class="cmd-escalate-btn" id="cmd-escalate-quick-btn">
                                        🏥 ESCALATE TO HOSPITAL
                                    </button>
                                    <button type="button" class="cmd-resolve-btn" id="cmd-resolve-current-btn">
                                        🏁 MARK INCIDENT RESOLVED
                                    </button>
                                </div>
                            </div>
                        </div>

                    </div>

                    <!-- TAB 2: Emergency Heatmap -->
                    <div class="command-heatmap-subview hidden" id="cmd-heatmap-subview">
                        <div class="heatmap-header-card">
                            <div>
                                <h3>🔥 Palkhi Route Emergency Concentration Heatmap</h3>
                                <p>Visualizing active emergency incidents and crowd congestion risk across all 12 pilgrimage sectors.</p>
                            </div>
                            <span class="proto-tag">🟣 Prototype Risk Index</span>
                        </div>
                        <div class="heatmap-zones-grid" id="cmd-heatmap-grid">
                            <p class="empty-feed-text">Loading heatmap telemetry...</p>
                        </div>
                    </div>

                    <!-- TAB 3: Resource Readiness Panel -->
                    <div class="command-readiness-subview hidden" id="cmd-readiness-subview">
                        <div class="readiness-header-card">
                            <div>
                                <h3>🏕️ Sector Medical Resource Readiness</h3>
                                <p>Real-time staffing, volunteer availability, and medical responder allocation by pilgrimage camp.</p>
                            </div>
                            <span class="proto-tag">🟢 Operational Readiness</span>
                        </div>
                        <div class="readiness-camps-grid" id="cmd-readiness-grid">
                            <p class="empty-feed-text">Loading resource status...</p>
                        </div>
                    </div>

                </div>
            </section>
        </main>

        <!-- ================= 4. MOBILE BOTTOM NAVIGATION ================= -->
        <nav class="mobile-bottom-nav" role="navigation" aria-label="Mobile Navigation">
            <button type="button" class="mob-nav-btn active" data-view="home-view" id="mob-nav-home">
                <span class="mob-icon">🏠</span>
                <span class="mob-label" data-i18n="nav_home">Home</span>
            </button>
            <button type="button" class="mob-nav-btn" data-view="safety-map-view" id="mob-nav-map">
                <span class="mob-icon">🗺️</span>
                <span class="mob-label" data-i18n="nav_map">Map</span>
            </button>
            <button type="button" class="mob-nav-btn mob-sos-btn" data-view="emergency-view" id="mob-nav-sos">
                <div class="mob-sos-circle">
                    <span class="mob-sos-icon">🚨</span>
                </div>
                <span class="mob-label" data-i18n="nav_emergency">SOS</span>
            </button>
            <button type="button" class="mob-nav-btn" data-view="services-view" id="mob-nav-services">
                <span class="mob-icon">🛡️</span>
                <span class="mob-label" data-i18n="nav_services">Safety</span>
            </button>
            <button type="button" class="mob-nav-btn" data-view="command-view" id="mob-nav-command">
                <span class="mob-icon">🛰️</span>
                <span class="mob-label" data-i18n="nav_command">Command</span>
            </button>
        </nav>

        <!-- ================= 5. SOS CONFIRMATION MODAL ================= -->
        <div id="sos-modal" class="modal-overlay hidden" role="dialog" aria-modal="true">
            <div class="modal-card">
                <div class="modal-icon-header">🚨</div>
                <h3 class="modal-title" data-i18n="modal_sos_title">Trigger Emergency SOS?</h3>
                <p class="modal-msg" data-i18n="modal_sos_msg">This will capture your exact coordinates and immediately alert the nearest Palkhi route volunteer and medical responder unit.</p>
                <div class="modal-safety-id-display">
                    <span class="modal-label" data-i18n="modal_using_id">Using Safety ID:</span>
                    <strong id="modal-active-wari-id">WS-28471</strong>
                </div>
                <div class="modal-actions">
                    <button type="button" id="cancel-sos-btn" class="modal-btn cancel-btn" data-i18n="btn_cancel">CANCEL</button>
                    <button type="button" id="confirm-sos-btn" class="modal-btn confirm-btn pulse-red" data-i18n="btn_confirm_sos">DISPATCH SOS</button>
                </div>
            </div>
        </div>

        <!-- ================= 6. COMPANION GROUP MODAL ================= -->
        <div id="group-modal" class="modal-overlay hidden" role="dialog" aria-modal="true">
            <div class="modal-card">
                <div class="modal-icon-header">👥</div>
                <h3 class="modal-title">My Wari Companion Group</h3>
                <p class="modal-msg">Link trusted family or Dindi members. If an emergency occurs, your group is immediately associated with the dispatch alert.</p>
                
                <div class="group-members-list" id="group-members-list">
                    <p class="empty-feed-text">Loading group members...</p>
                </div>

                <form id="add-group-member-form" class="group-add-form">
                    <input type="text" id="new-member-name" class="field-input" placeholder="Companion Name (e.g. Aarti)" required>
                    <input type="tel" id="new-member-phone" class="field-input" placeholder="10-digit Phone" required pattern="[0-9]{10}">
                    <button type="submit" class="form-submit-btn secondary">➕ Add Companion</button>
                </form>

                <div class="modal-actions">
                    <button type="button" id="close-group-modal-btn" class="modal-btn cancel-btn">CLOSE</button>
                </div>
            </div>
        </div>

        <!-- ================= 7. RESPONSE ANALYTICS MODAL ================= -->
        <div id="analytics-modal" class="modal-overlay hidden" role="dialog" aria-modal="true">
            <div class="modal-card analytics-card">
                <div class="modal-icon-header">📊</div>
                <h3 class="modal-title">WariSeva Response Analytics</h3>
                <p class="modal-msg">Emergency incident performance breakdown & coordination report.</p>
                
                <div class="analytics-metrics-deck" id="analytics-metrics-deck">
                    <div class="analytics-stat-row">
                        <span>Total Response Time:</span>
                        <strong class="highlight-green" id="an-total-time">4m 18s</strong>
                    </div>
                    <div class="analytics-stat-row">
                        <span>Volunteer Assignment:</span>
                        <strong id="an-vol-assign">24 sec</strong>
                    </div>
                    <div class="analytics-stat-row">
                        <span>Volunteer Travel:</span>
                        <strong id="an-vol-travel">2m 08s</strong>
                    </div>
                    <div class="analytics-stat-row">
                        <span>Route Strategy:</span>
                        <strong class="highlight-green" id="an-route-savings">Safe Bypass (+7m saved)</strong>
                    </div>
                    <div class="analytics-stat-row">
                        <span>Patient Reached:</span>
                        <strong class="text-success">✓ Verified On Scene</strong>
                    </div>
                </div>

                <!-- WariSeva Response Score Card -->
                <div class="score-display-card">
                    <span class="score-kicker">WARISEVA RESPONSE SCORE</span>
                    <div class="score-number-row">
                        <span class="score-big" id="an-score-val">92</span>
                        <span class="score-denom">/ 100</span>
                    </div>
                    <span class="score-rating-badge" id="an-rating-badge">EXEMPLARY RAPID RESPONSE</span>
                    <p class="score-disclaimer"><em>* Prototype Response Metric based on dispatch time, GPS precision, and bypass routing efficiency.</em></p>
                </div>

                <div class="modal-actions">
                    <button type="button" id="close-analytics-modal-btn" class="modal-btn confirm-btn">DONE</button>
                </div>
            </div>
        </div>

        <!-- ================= 8. WHERE AM I MODAL ================= -->
        <div id="where-modal" class="modal-overlay hidden" role="dialog" aria-modal="true">
            <div class="modal-card">
                <div class="modal-icon-header">📍</div>
                <h3 class="modal-title">Your Current Location</h3>
                <div class="where-data-box">
                    <div class="where-row"><span class="w-lbl">Wari Sector:</span> <strong id="where-zone-val">Zone 04 — Saswad Palkhi Maidan</strong></div>
                    <div class="where-row"><span class="w-lbl">Landmark:</span> <strong id="where-landmark-val">Saswad Central Palkhi Maidan Ground</strong></div>
                    <div class="where-row"><span class="w-lbl">GPS Coordinates:</span> <strong id="where-coords-val">18.3444, 74.0305 (±5 m)</strong></div>
                    <div class="where-row"><span class="w-lbl">Nearest Medical:</span> <strong class="highlight-green" id="where-medical-val">Saswad Medical Tent (180 m)</strong></div>
                </div>
                <div class="modal-actions">
                    <button type="button" id="close-where-modal-btn" class="modal-btn confirm-btn">GOT IT</button>
                </div>
            </div>
        </div>

        <!-- ================= 9. LOCATING SPINNER OVERLAY ================= -->
        <div id="locating-state" class="locating-overlay hidden">
            <div class="spinner"></div>
            <p class="locating-text" data-i18n="acquiring_gps">Acquiring GPS Position...</p>
            <p class="locating-subtext" data-i18n="mapping_checkpoint">Mapping to nearest Palkhi route checkpoint</p>
        </div>

        <!-- ================= 10. TOAST NOTIFICATION CONTAINER ================= -->
        <div id="toast-container" class="toast-stack" aria-live="polite"></div>

        <!-- ================= 11. ACCESSIBLE FOOTER ================= -->
        <footer class="app-footer">
            <div class="footer-pillars-strip">
                <span>🚨 Emergency Response</span>
                <span>📍 Exact Location</span>
                <span>👥 Volunteer Network</span>
                <span>🚑 Medical Response</span>
                <span>🗺️ Crowd-Aware Route</span>
                <span>🏥 Hospital Escalation</span>
                <span>🛡️ Wari Safety Services</span>
            </div>
            <p class="footer-copy">WariSeva AI • Sant Dnyaneshwar & Sant Tukaram Maharaj Palkhi Safety Coordination</p>
            <p class="footer-disclaimer">24h Hackathon Finalist Prototype — Health & Emergency Response Track</p>
        </footer>
    </div>

    <!-- Leaflet OpenStreetMap JS -->
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="/static/script.js"></script>
</body>
</html>
"""

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Updated templates/index.html with synchronized 9-step timeline and response cards!")
