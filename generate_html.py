html_content = """<!DOCTYPE html>
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
                <span class="demo-desc" data-i18n="demo_desc">Prototype Data (Saswad Zone 04 • 18.3444, 74.0305)</span>
                <span class="conn-status-pill online" id="conn-status-pill">🟢 CONNECTED</span>
            </div>
            <div class="demo-bar-actions">
                <button type="button" id="voice-toggle-btn" class="demo-pill-btn voice-btn" title="Toggle Spoken Voice Assistance">
                    🔊 Voice: ON
                </button>
                <button type="button" id="toggle-demo-mode-btn" class="demo-pill-btn" data-i18n="toggle_demo">DEMO ACTIVE</button>
                <button type="button" id="run-simulation-demo-btn" class="demo-action-btn pulse-orange" title="Auto-advance complete emergency response lifecycle">
                    ▶️ RUN FULL DEMO SIMULATION
                </button>
                <button type="button" id="create-demo-em-btn" class="demo-action-btn primary">
                    ⚡ SEED DEMO (EM-28471)
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
                        <span class="elder-btn-desc" data-i18n="elder_med_desc">जवळचे आरोग्य शिबिर (८०० मीटर)</span>
                    </div>
                </button>

                <!-- 4. WATER -->
                <button type="button" class="elder-btn elder-water-btn" id="elder-water-btn">
                    <span class="elder-btn-icon">💧</span>
                    <div class="elder-btn-text-col">
                        <span class="elder-btn-title" data-i18n="elder_water_title">💧 पिण्याचे पाणी (WATER)</span>
                        <span class="elder-btn-desc" data-i18n="elder_water_desc">सासवड पालखी मैदान जल केंद्र (२५० मीटर)</span>
                    </div>
                </button>

                <!-- 5. TOILET -->
                <button type="button" class="elder-btn elder-toilet-btn" id="elder-toilet-btn">
                    <span class="elder-btn-icon">🚻</span>
                    <div class="elder-btn-text-col">
                        <span class="elder-btn-title" data-i18n="elder_toilet_title">🚻 स्वच्छतागृह (TOILETS)</span>
                        <span class="elder-btn-desc" data-i18n="elder_toilet_desc">स्वच्छ मोबाईल टॉयलेट (३०० मीटर)</span>
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
                                <p class="alert-em-sub" id="home-em-status-summary">Dispatched to Volunteer V-001 • Medical Responder en route</p>
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
                    
                    <!-- Reassuring Patient Response Card (Section 7) -->
                    <div class="patient-emergency-alert-card" id="patient-emergency-alert-card">
                        <div class="em-alert-badge">
                            <span class="em-pulsing-badge">🚨</span>
                            <span class="em-badge-title" data-i18n="em_kicker">HELP IS ON THE WAY • मदत येत आहे</span>
                        </div>
                        <div class="em-alert-stats-row">
                            <div class="em-stat-box">
                                <span class="em-stat-label" data-i18n="palkhi_zone">Your Location</span>
                                <strong class="em-stat-val" id="em-alert-zone">Zone 04 — Saswad Palkhi Maidan</strong>
                            </div>
                            <div class="em-stat-box">
                                <span class="em-stat-label">Nearest Volunteer</span>
                                <strong class="em-stat-val highlight-cyan" id="em-alert-vol-info">👥 Searching for volunteer...</strong>
                            </div>
                            <div class="em-stat-box">
                                <span class="em-stat-label">Response Status</span>
                                <strong class="em-stat-val highlight-green" id="em-alert-status-pill">🟢 DISPATCH ACTIVE</strong>
                            </div>
                        </div>
                        <div class="em-safety-notice">
                            ℹ️ <strong>"You can stay where you are unless it is unsafe."</strong> <span class="sub-text">(Safety assistance guidance • सुरक्षित ठिकाणी थांबा)</span>
                        </div>
                    </div>

                    <!-- Emergency Incident Header Details & Live Stopwatch (Section 8) -->
                    <div class="emergency-state-hero" id="emergency-state-hero">
                        <div class="em-hero-top">
                            <div class="em-hero-badge-group">
                                <span class="em-pulsing-badge">🛡️</span>
                                <div>
                                    <span class="em-kicker" data-i18n="em_kicker">EMERGENCY COORDINATION ACTIVE</span>
                                    <h2 class="em-hero-title" id="em-live-title" data-i18n="em_help_requested">HELP REQUESTED</h2>
                                </div>
                            </div>
                            <div class="em-hero-id-col">
                                <div class="stopwatch-display-box" id="em-stopwatch-box">
                                    <span class="stopwatch-label">⏱️ RESPONSE TIME</span>
                                    <span class="stopwatch-time" id="em-stopwatch-timer">00:00</span>
                                </div>
                                <div class="em-id-row">
                                    <span class="em-id-label">INCIDENT ID:</span>
                                    <span class="em-id-value" id="em-id-display">EM-28471</span>
                                </div>
                            </div>
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
                    </div>

                    <!-- Decision Support & Recommended Responder Card (Section 6 & 7) -->
                    <div class="decision-support-card" id="decision-support-card">
                        <div class="ds-card-head">
                            <div class="ds-head-left">
                                <span class="ds-star-badge">⭐ RECOMMENDED RESPONDER</span>
                                <h3 class="ds-vol-title" id="ds-vol-title">Volunteer V-104 (Ramesh Kulkarni)</h3>
                            </div>
                            <span class="ds-status-badge" id="ds-vol-status">🟢 AVAILABLE</span>
                        </div>
                        <div class="ds-metrics-bar">
                            <div class="ds-metric"><span class="ds-m-lbl">Distance:</span> <strong class="highlight-cyan" id="ds-dist-val">520 m away</strong></div>
                            <div class="ds-metric"><span class="ds-m-lbl">Est. Response:</span> <strong class="highlight-orange" id="ds-eta-val">3 min</strong></div>
                            <div class="ds-metric"><span class="ds-m-lbl">Crowd Delay:</span> <strong class="highlight-green">Low (+1 min via Bypass)</strong></div>
                        </div>
                        <div class="ds-reason-box">
                            <span class="ds-reason-icon">🧠</span>
                            <span class="ds-reason-text" id="ds-reason-text"><strong>Decision Support Reason:</strong> Selected based on active proximity, low estimated response time (3 min), and low crowd congestion along bypass corridor.</span>
                        </div>
                        <div class="ds-disclaimer-text">
                            ⚠️ <em>"Shortest distance is not always the fastest route through a dense Wari." Prototype Decision Support — does not replace clinical triage.</em>
                        </div>
                    </div>

                    <!-- Nearest Help Summary 4-Card Grid (Section 16) -->
                    <div class="nearest-help-section">
                        <h4 class="nearest-help-title">🏥 Nearest Emergency Help / मदत केंद्रे</h4>
                        <div class="nearest-help-grid">
                            <div class="help-mini-card" id="help-card-vol">
                                <div class="help-mini-head">👥 Volunteer</div>
                                <strong class="help-mini-name" id="nh-vol-name">Ramesh Kulkarni</strong>
                                <div class="help-mini-meta"><span id="nh-vol-dist">520 m</span> • <span class="highlight-orange" id="nh-vol-eta">3 min</span></div>
                                <span class="help-mini-status text-success">🟢 Active</span>
                            </div>
                            <div class="help-mini-card" id="help-card-camp">
                                <div class="help-mini-head">🏥 Medical Camp</div>
                                <strong class="help-mini-name" id="nh-camp-name">Saswad Medical Tent</strong>
                                <div class="help-mini-meta"><span id="nh-camp-dist">800 m</span> • <span class="highlight-orange" id="nh-camp-eta">5 min</span></div>
                                <span class="help-mini-status text-success">🟢 Open 24h</span>
                            </div>
                            <div class="help-mini-card" id="help-card-resp">
                                <div class="help-mini-head">🚑 Responder</div>
                                <strong class="help-mini-name" id="nh-resp-name">Mobile Ambulance 1</strong>
                                <div class="help-mini-meta"><span id="nh-resp-dist">1.4 km</span> • <span class="highlight-orange" id="nh-resp-eta">7 min</span></div>
                                <span class="help-mini-status text-warning">🟠 Standby</span>
                            </div>
                            <div class="help-mini-card" id="help-card-hosp">
                                <div class="help-mini-head">🏥 Hospital</div>
                                <strong class="help-mini-name" id="nh-hosp-name">Saswad Sub-District Hospital</strong>
                                <div class="help-mini-meta"><span id="nh-hosp-dist">3.2 km</span> • <span class="highlight-orange" id="nh-hosp-eta">12 min</span></div>
                                <span class="help-mini-status text-cyan">🏥 Trauma ICU</span>
                            </div>
                        </div>
                    </div>

                    <!-- Interactive Live Emergency Map Section (Sections 4 & 5) -->
                    <div class="em-interactive-map-card">
                        <div class="em-map-card-head">
                            <div class="head-left">
                                <span class="em-map-title">📍 Live Multi-Party Response Map</span>
                                <span class="em-map-sub">Real-time GPS coordinates of Patient, Volunteer, and Medical Responder</span>
                            </div>
                            <!-- Camera Controls (Section 5) -->
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

                    <!-- Dynamic Nearest Volunteer Proximity Card (Sections 1, 2, 3, 11) -->
                    <div class="volunteer-tracking-card" id="nearest-vol-dynamic-card">
                        <div class="vol-tracking-head">
                            <div class="vol-head-left">
                                <span class="vol-radar-dot"></span>
                                <div>
                                    <h3 class="vol-tracking-title" id="vol-card-title">👥 NEAREST VOLUNTEER</h3>
                                    <span class="vol-tracking-sub" id="vol-card-sub">Calculated via nearest available volunteer algorithm</span>
                                </div>
                            </div>
                            <span class="vol-status-chip" id="vol-card-status-chip">SEARCHING...</span>
                        </div>

                        <div class="vol-tracking-body">
                            <div class="vol-info-col">
                                <div class="vol-name-row">
                                    <span class="vol-avatar-circle">👤</span>
                                    <div>
                                        <strong class="vol-assigned-name" id="vol-assigned-name">Searching for nearby volunteer...</strong>
                                        <span class="vol-assigned-id" id="vol-assigned-id">Standby • शोधत आहे</span>
                                    </div>
                                </div>
                            </div>

                            <div class="vol-metrics-row">
                                <div class="vol-metric-box">
                                    <span class="metric-lbl">Distance to Patient</span>
                                    <strong class="metric-val highlight-cyan" id="vol-metric-dist">-- m</strong>
                                </div>
                                <div class="vol-metric-box">
                                    <span class="metric-lbl">Walking ETA</span>
                                    <strong class="metric-val highlight-orange" id="vol-metric-eta">-- min</strong>
                                </div>
                                <div class="vol-metric-box">
                                    <span class="metric-lbl">GPS Stream</span>
                                    <strong class="metric-val highlight-green" id="vol-metric-ping">Connecting...</strong>
                                </div>
                            </div>
                        </div>

                        <div class="vol-tracking-foot">
                            <span class="foot-update-text" id="vol-last-update-time">Location updated: Just now</span>
                            <button type="button" class="vol-focus-btn" id="vol-focus-map-btn">
                                🎯 VIEW VOLUNTEER ON MAP
                            </button>
                        </div>
                    </div>

                    <!-- Dynamic Visual Response Timeline (Section 6) -->
                    <div class="timeline-card">
                        <h3 class="timeline-header" data-i18n="response_timeline">📊 Emergency Response Timeline</h3>
                        
                        <div class="timeline-stepper">
                            <!-- Step 1: SOS Sent -->
                            <div class="timeline-step step-done" id="step-sos-sent">
                                <div class="step-marker">✓</div>
                                <div class="step-body">
                                    <div class="step-title" data-i18n="step_sos_sent">🚨 SOS Sent & Registered</div>
                                    <div class="step-desc" data-i18n="step_sos_sent_desc">Emergency created in central SQLite registry.</div>
                                </div>
                            </div>

                            <!-- Step 2: Location Shared -->
                            <div class="timeline-step step-done" id="step-loc-shared">
                                <div class="step-marker">✓</div>
                                <div class="step-body">
                                    <div class="step-title" data-i18n="step_loc_shared">📍 Location & Wari Zone Identified</div>
                                    <div class="step-desc" data-i18n="step_loc_shared_desc">Matched to Zone 04 — Saswad Palkhi Maidan.</div>
                                </div>
                            </div>

                            <!-- Step 3: Volunteer Assigned -->
                            <div class="timeline-step" id="step-vol-assigned">
                                <div class="step-marker">3</div>
                                <div class="step-body">
                                    <div class="step-title" data-i18n="step_vol_found">👥 Nearest Volunteer Found</div>
                                    <div class="step-desc" id="step-vol-desc">Identified nearest available volunteer on route.</div>
                                </div>
                            </div>

                            <!-- Step 4: Volunteer En Route -->
                            <div class="timeline-step" id="step-vol-enroute">
                                <div class="step-marker">4</div>
                                <div class="step-body">
                                    <div class="step-title" data-i18n="step_vol_enroute">🚶 Volunteer En Route (Live GPS)</div>
                                    <div class="step-desc" id="step-vol-enroute-desc">Moving toward patient.</div>
                                </div>
                            </div>

                            <!-- Step 5: Volunteer With Patient -->
                            <div class="timeline-step" id="step-vol-with-patient">
                                <div class="step-marker">5</div>
                                <div class="step-body">
                                    <div class="step-title" data-i18n="step_vol_with_pat">👥 Volunteer Reached Patient</div>
                                    <div class="step-desc" id="step-vol-with-pat-desc">Initial physical safety assessment.</div>
                                </div>
                            </div>

                            <!-- Step 6: Medical Responder Dispatched -->
                            <div class="timeline-step" id="step-responder-dispatched">
                                <div class="step-marker">6</div>
                                <div class="step-body">
                                    <div class="step-title" data-i18n="step_resp_dispatched">🚑 Medical Responder Dispatched (Crowd-Aware)</div>
                                    <div class="step-desc" id="step-resp-desc">Navigating via recommended safe bypass.</div>
                                </div>
                            </div>

                            <!-- Step 7: Hospital Escalation -->
                            <div class="timeline-step" id="step-hospital-escalation">
                                <div class="step-marker">7</div>
                                <div class="step-body">
                                    <div class="step-title" data-i18n="step_hosp_escalation">🏥 Hospital Escalation (If Required)</div>
                                    <div class="step-desc" id="step-hosp-desc">Secondary tertiary care coordination.</div>
                                </div>
                            </div>

                            <!-- Step 8: Resolved -->
                            <div class="timeline-step" id="step-emergency-resolved">
                                <div class="step-marker">8</div>
                                <div class="step-body">
                                    <div class="step-title" data-i18n="step_resolved">✅ Emergency Resolved</div>
                                    <div class="step-desc" id="step-resolved-desc">Patient safe and incident closed.</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Live Telemetry Resource Columns -->
                    <div class="telemetry-grid">
                        <!-- Volunteer Card -->
                        <div class="resource-card" id="em-vol-card">
                            <div class="res-card-top">
                                <span class="res-icon">🙋</span>
                                <div>
                                    <h4 class="res-title" data-i18n="res_vol_title">Assigned Volunteer</h4>
                                    <span class="res-status-badge" id="em-vol-status-badge">SEARCHING...</span>
                                </div>
                            </div>
                            <div class="res-detail-body">
                                <div class="res-row">
                                    <span class="res-label">Volunteer Name:</span>
                                    <strong id="em-vol-name">Ramesh Kulkarni (V-001)</strong>
                                </div>
                                <div class="res-row">
                                    <span class="res-label">Distance to Patient:</span>
                                    <strong class="highlight-cyan" id="em-vol-dist">Calculating...</strong>
                                </div>
                                <div class="res-row">
                                    <span class="res-label">Last GPS Ping:</span>
                                    <span id="em-vol-ping">Connecting...</span>
                                </div>
                            </div>
                        </div>

                        <!-- Medical Responder Card -->
                        <div class="resource-card" id="em-resp-card">
                            <div class="res-card-top">
                                <span class="res-icon">🚑</span>
                                <div>
                                    <h4 class="res-title" data-i18n="res_resp_title">Medical Responder</h4>
                                    <span class="res-status-badge" id="em-resp-status-badge">PENDING DISPATCH</span>
                                </div>
                            </div>
                            <div class="res-detail-body">
                                <div class="res-row">
                                    <span class="res-label">Responder Unit:</span>
                                    <strong id="em-resp-name">Dr. Arvind Shinde (MR-001)</strong>
                                </div>
                                <div class="res-row">
                                    <span class="res-label">Route Strategy:</span>
                                    <strong class="highlight-green" id="em-resp-route">Safe Bypass Corridor</strong>
                                </div>
                                <div class="res-row">
                                    <span class="res-label">Estimated Arrival:</span>
                                    <strong class="highlight-orange" id="em-resp-eta">3 min (⚡ Saves 7 min)</strong>
                                </div>
                            </div>
                        </div>

                        <!-- Hospital Escalation Status Card -->
                        <div class="resource-card" id="em-hosp-card">
                            <div class="res-card-top">
                                <span class="res-icon">🏥</span>
                                <div>
                                    <h4 class="res-title" data-i18n="res_hosp_title">Destination Hospital</h4>
                                    <span class="res-status-badge" id="em-hosp-status-badge">NOT REQUIRED / PENDING</span>
                                </div>
                            </div>
                            <div class="res-detail-body">
                                <div class="res-row">
                                    <span class="res-label">Hospital Name:</span>
                                    <strong id="em-hosp-name">Saswad Sub-District Hospital</strong>
                                </div>
                                <div class="res-row">
                                    <span class="res-label">Capabilities:</span>
                                    <span>Trauma Care • Emergency ICU</span>
                                </div>
                                <div class="res-row">
                                    <span class="res-label">Coordination:</span>
                                    <span class="sub-notice">Transport coordinated by responder unit.</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Companion Group Alert Bar (Section 26) -->
                    <div class="companion-alert-strip" id="em-companion-strip">
                        <span class="comp-icon">👨‍👩‍👧</span>
                        <div class="comp-text">
                            <strong>Companion Group Linked:</strong> <span id="em-companion-list">Sunita Shinde (Spouse • 9822114455), Ganesh Shinde (Son • 9822114466)</span>
                        </div>
                    </div>

                    <!-- Emergency Actions Footer & Sharing (Section 21) -->
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
                    
                    <!-- Map Filter Bar (ALL, MEDICAL, WATER, TOILETS, REST, FOOD, HOSPITALS, EMERGENCIES) -->
                    <div class="map-filter-toolbar">
                        <span class="filter-label" data-i18n="filter_label">Filters:</span>
                        <div class="filter-pills-row" id="map-filter-group">
                            <button type="button" class="filter-pill active" data-filter="ALL">ALL (13)</button>
                            <button type="button" class="filter-pill" data-filter="WATER">💧 Water</button>
                            <button type="button" class="filter-pill" data-filter="TOILET">🚻 Toilets</button>
                            <button type="button" class="filter-pill" data-filter="MEDICAL_CAMP">🏥 Medical Camps</button>
                            <button type="button" class="filter-pill" data-filter="REST_AREA">🛏️ Rest Areas</button>
                            <button type="button" class="filter-pill" data-filter="FOOD">🍱 Food / Prasad</button>
                            <button type="button" class="filter-pill" data-filter="HOSPITAL">🚑 Hospitals</button>
                            <button type="button" class="filter-pill" data-filter="EMERGENCIES">🚨 Incidents</button>
                        </div>
                    </div>

                    <!-- Map + Interactive Sidebar Container -->
                    <div class="map-and-sidebar-layout">
                        <div class="main-map-column">
                            <div class="map-legend-header">
                                <span class="map-legend-title">🗺️ Palkhi Route Safety & Resource Map</span>
                                <div class="map-legend-items">
                                    <span class="legend-chip"><span class="chip-dot red"></span> Patient 📍</span>
                                    <span class="legend-chip"><span class="chip-dot blue"></span> Volunteer 🔵</span>
                                    <span class="legend-chip"><span class="chip-dot green"></span> Responder 🚑</span>
                                    <span class="legend-chip"><span class="chip-dot red-ring"></span> Choke Zone ⚠️</span>
                                </div>
                            </div>
                            <div id="main-safety-map" class="full-leaflet-map"></div>
                        </div>

                        <!-- Sidebar Info Card Panel (Shows clicked pin detail) -->
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
                                <div class="sidebar-status-row">
                                    <span class="status-indicator-dot green"></span>
                                    <span>Status: <strong class="text-success">Available / कार्यरत</strong></span>
                                </div>
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

                    <!-- Category Tile Selector (Large, Elderly-Friendly) -->
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
                            <span class="cat-emoji">🍱</span>
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

                    <!-- Active Accepted Response Card -->
                    <div id="volunteer-active-response-box" class="active-task-card hidden">
                        <div class="task-card-header">
                            <span class="task-status-pill enroute" id="vol-response-badge">🟢 EN ROUTE</span>
                            <span class="task-id-text" id="vol-response-em-id">EM-28471</span>
                        </div>

                        <div class="task-patient-info">
                            <div class="info-group">
                                <span class="info-label">Patient Incident Zone:</span>
                                <strong id="vol-patient-zone">Zone 04 — Saswad Palkhi Maidan</strong>
                            </div>
                            <div class="info-group">
                                <span class="info-label">Nearest Landmark:</span>
                                <strong id="vol-patient-landmark">Saswad Central Palkhi Maidan Ground</strong>
                            </div>
                        </div>

                        <!-- Live GPS Location Sharing Component -->
                        <div class="location-sharing-panel">
                            <div class="sharing-status-line">
                                <span class="pulse-green-dot"></span>
                                <span id="location-sharing-status-text">📡 <strong>Opt-in GPS sharing active</strong> for active emergency.</span>
                            </div>

                            <div class="live-telemetry-row" id="sharing-telemetry">
                                <div class="telemetry-box">
                                    <span class="t-label">Distance to Patient:</span>
                                    <strong class="t-val highlight-cyan" id="vol-distance-val">69 m away</strong>
                                </div>
                                <div class="telemetry-box">
                                    <span class="t-label">Last Streamed Ping:</span>
                                    <strong class="t-val" id="vol-last-ping-val">Just now (±4m)</strong>
                                </div>
                            </div>

                            <div class="sharing-controls-row">
                                <button type="button" class="share-gps-btn" id="start-location-sharing-btn">
                                    📡 START SHARING LOCATION
                                </button>
                                <button type="button" class="reach-btn" id="reached-patient-btn">
                                    👥 I'M WITH PATIENT
                                </button>
                            </div>

                            <div id="reached-confirmed-banner" class="success-alert-banner hidden">
                                ✅ You have reached the patient's side. Initial safety triage in progress.
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

                    <!-- Active Medical Response Box -->
                    <div id="responder-active-box" class="active-task-card hidden">
                        <div class="task-card-header">
                            <span class="task-status-pill enroute" id="resp-status-badge">🚑 RESPONDER ASSIGNED</span>
                            <span class="task-id-text" id="resp-active-em-id">EM-28471</span>
                        </div>

                        <!-- Crowd Condition & AI Intelligence Insight Card (Section 13) -->
                        <div class="crowd-condition-banner">
                            <div class="crowd-banner-top">
                                <div class="crowd-title-col">
                                    <span class="crowd-title">🤖 AI / Crowd Intelligence Panel</span>
                                    <span class="crowd-sub-notice">🟣 Simulated / Prototype Crowd Sensor Model</span>
                                </div>
                                <span class="crowd-badge-critical" id="resp-crowd-density-badge">CRITICAL (94%)</span>
                            </div>
                            <div class="crowd-grid-details">
                                <div class="crowd-col">
                                    <span class="crowd-label">⚠️ Bottleneck Choke Point:</span>
                                    <strong class="text-danger" id="resp-choke-desc">Saswad Central Mandir Ringan & Bazar Chowk</strong>
                                </div>
                                <div class="crowd-col">
                                    <span class="crowd-label">✅ Clear Service Corridor:</span>
                                    <strong class="text-success" id="resp-bypass-desc">Saswad South Bypass Service Corridor (Ambulance Lane)</strong>
                                </div>
                            </div>
                            <div class="crowd-ai-reasoning">
                                💡 <strong>Routing Intelligence:</strong> "Shortest distance is not always fastest route through dense Wari. Outer ambulance corridor (Route B) recommended to bypass pedestrian surge."
                            </div>
                        </div>

                        <!-- Route Comparison Matrix (Section 12) -->
                        <div class="route-comparison-deck">
                            <div class="route-card-choice congested" id="choice-direct-route">
                                <div class="route-kicker">Route A (Direct Procession Line)</div>
                                <div class="route-metrics"><span id="direct-dist-text">391 m</span> • <span class="text-danger" id="direct-eta-text">10 min</span></div>
                                <div class="route-note">🔴 High Crowd (Delay: +8 min)</div>
                            </div>
                            <div class="route-card-choice recommended" id="choice-safe-route">
                                <div class="route-star-badge">⭐ RECOMMENDED ROUTE</div>
                                <div class="route-kicker">Route B (Safe Bypass Corridor)</div>
                                <div class="route-metrics"><span id="safe-dist-text">808 m</span> • <span class="text-success" id="safe-eta-text">3 min</span></div>
                                <div class="route-savings" id="safe-savings-text">🟢 Low Crowd (⚡ Saves 7 min)</div>
                            </div>
                        </div>

                        <!-- Tactical Interactive Map -->
                        <div class="tactical-map-deck">
                            <div class="tactical-map-header">
                                <span>📍 Live Crowd-Aware Navigation Map</span>
                                <div class="tactical-legend-strip">
                                    <span><strong style="color:#00E676;">― 🟢 Safe Bypass</strong></span>
                                    <span><strong style="color:#FF5252;">--- 🔴 Congested Direct</strong></span>
                                </div>
                            </div>
                            <div id="responder-map" class="tactical-leaflet-box"></div>
                        </div>

                        <!-- Hospital Escalation Action Deck (Section 25) -->
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
                                <h4 class="hosp-confirm-name" id="selected-hospital-name">Saswad Rural Sub-District Hospital</h4>
                                <div class="hosp-confirm-address" id="selected-hospital-details">Saswad-Hadapsar Road • Ph: 02115-222333</div>
                                <div class="hosp-confirm-notice">Transport coordinated by emergency responder team.</div>
                            </div>
                        </div>

                        <!-- Responder Transit State Controls -->
                        <div class="responder-state-controls">
                            <button type="button" id="resp-share-gps-btn" class="share-gps-btn">
                                📡 SHARE RESPONDER GPS
                            </button>
                            <div class="resp-transit-dual-btns">
                                <button type="button" id="resp-start-response-btn" class="transit-btn enroute">
                                    🚨 START RESPONSE (EN ROUTE)
                                </button>
                                <button type="button" id="resp-mark-arrived-btn" class="transit-btn arrived">
                                    🏁 MARK ARRIVED ON SCENE
                                </button>
                            </div>
                            <div id="resp-arrived-banner" class="success-alert-banner hidden">
                                🩺 Medical Responder on scene. Administering emergency medical care.
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
                    
                    <!-- Command Center Top Bar & Sub-Nav Tabs -->
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
                            <span class="cmd-counter-chip" id="command-total-count">TOTAL: 0 INCIDENTS</span>
                            <button type="button" class="refresh-feed-btn" id="refresh-command-btn">🔄 Refresh Operations</button>
                        </div>
                    </div>

                    <!-- Real-Time Crowd Conditions Monitor -->
                    <div class="command-crowd-monitor">
                        <div class="monitor-cell"><span class="m-dot red"></span> Saswad (94% Critical)</div>
                        <div class="monitor-cell"><span class="m-dot red"></span> Wakhari (92% Critical)</div>
                        <div class="monitor-cell"><span class="m-dot yellow"></span> Dive Ghat (82% High)</div>
                        <div class="monitor-cell"><span class="m-dot green"></span> Taradgaon (32% Clear)</div>
                        <div class="monitor-cell"><span class="m-dot green"></span> Pandharpur (45% Normal)</div>
                    </div>

                    <!-- TAB 1: 3-Column Tactical Operations Layout -->
                    <div class="command-3col-grid" id="cmd-operations-subview">
                        
                        <!-- COLUMN 1 (LEFT): Active Emergencies List -->
                        <div class="cmd-col-left">
                            <div class="col-head">
                                <h4>Active Incidents</h4>
                                <span class="col-count" id="cmd-incident-count">0</span>
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
                                    <span class="ins-label">Assigned Volunteer:</span>
                                    <strong id="cmd-ins-volunteer">Ramesh Kulkarni (V-001)</strong>
                                    <div class="ins-sub" id="cmd-ins-vol-status">Status: 👥 With Patient (0 m)</div>
                                </div>

                                <div class="ins-data-block">
                                    <span class="ins-label">Medical Responder:</span>
                                    <strong id="cmd-ins-responder">Dr. Arvind Shinde (MR-001)</strong>
                                    <div class="ins-sub" id="cmd-ins-resp-status">Status: 🩺 On Scene</div>
                                </div>

                                <div class="ins-data-block">
                                    <span class="ins-label">Crowd & Route Decision:</span>
                                    <div class="ins-crowd-row">
                                        <span>Density: <strong class="text-danger">CRITICAL (94%)</strong></span>
                                        <span>Route: <strong class="text-success">⭐ Safe Bypass</strong></span>
                                    </div>
                                </div>

                                <div class="ins-data-block">
                                    <span class="ins-label">Destination Hospital:</span>
                                    <strong id="cmd-ins-hospital">Saswad Rural Sub-District Hospital</strong>
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

                    <!-- TAB 2: Emergency Heatmap (Section 14) -->
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

                    <!-- TAB 3: Resource Readiness Panel (Section 15) -->
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
            <!-- Prominent Floating SOS Tab -->
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

        <!-- ================= 6. COMPANION GROUP MODAL (Section 26) ================= -->
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

        <!-- ================= 7. RESPONSE ANALYTICS MODAL (Section 17 & 32) ================= -->
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
                    <div class="where-row"><span class="w-lbl">Nearest Medical:</span> <strong class="highlight-green" id="where-medical-val">Saswad Medical Tent (800 m)</strong></div>
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
    f.write(html_content)

print(f"Successfully generated winning-prototype templates/index.html ({len(html_content)} characters)!")
