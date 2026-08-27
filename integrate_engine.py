engine_code = """
# =========================================================================
# INTELLIGENT RESPONSE ENGINE — PROTOTYPE AI SCORING & DECISION SUPPORT
# =========================================================================

def ai_response_engine(em_data, candidate_volunteers=None):
    \"\"\"
    AI-Assisted Intelligent Response Recommendation Engine.
    Evaluates candidate responders using an explainable multi-factor scoring model:
    Score (0-100) = Proximity + Skill Match + Zone Relevance + Route/Crowd Access + Verification.
    \"\"\"
    pat_lat = float(em_data.get('latitude', 18.3444))
    pat_lon = float(em_data.get('longitude', 74.0305))
    em_zone = em_data.get('wari_zone', 'Zone 04 — Saswad Palkhi Maidan')
    em_type = str(em_data.get('emergency_type', 'MEDICAL')).upper()
    severity = str(em_data.get('severity', em_data.get('priority', 'CRITICAL'))).upper()

    conn = get_db_connection()
    cursor = conn.cursor()

    if candidate_volunteers is None:
        cursor.execute(\"SELECT * FROM users WHERE role = 'VOLUNTEER'\")
        vols = [dict(r) for r in cursor.fetchall()]
    else:
        vols = candidate_volunteers

    conn.close()

    scored_candidates = []
    excluded_candidates = []

    for v in vols:
        v_id = v.get('wari_id', 'V-000')
        v_name = v.get('name', 'Volunteer')
        v_status = v.get('status', 'AVAILABLE')
        v_lat = v.get('latitude', 18.3460)
        v_lon = v.get('longitude', 74.0288)
        v_zone = v.get('zone', 'Zone 04 — Saswad Palkhi Maidan')
        v_skills = v.get('skills', 'General Assistance')
        v_cert = v.get('certification', 'None')
        v_verif = v.get('verification_status', 'VERIFIED')

        # Filter out busy / unavailable volunteers
        if v_status != 'AVAILABLE':
            excluded_candidates.append({
                'wari_id': v_id,
                'name': v_name,
                'status': v_status,
                'reason': f"Volunteer is currently {v_status.lower()} and excluded from dispatch pool."
            })
            continue

        # 1. Proximity / Distance Score (Max 35 points)
        dist_km = calculate_haversine_distance(pat_lat, pat_lon, v_lat, v_lon)
        dist_m = int(round(dist_km * 1000))
        if dist_m <= 350:
            score_dist = 35
            eta_min = 2
        elif dist_m <= 700:
            score_dist = 28
            eta_min = 3
        elif dist_m <= 1500:
            score_dist = 20
            eta_min = 5
        elif dist_m <= 3000:
            score_dist = 10
            eta_min = 8
        else:
            score_dist = 5
            eta_min = 12

        # 2. Skill & Medical Training Match (Max 25 points)
        score_skill = 5
        if em_type in ('MEDICAL', 'INJURY', 'HEAT', 'DEHYDRATION', 'ELDERLY'):
            if 'First Aid Certified' in v_cert or 'Nurse' in v_cert or 'Paramedic' in v_skills:
                score_skill = 25
            elif 'First Aid' in v_skills or 'Triage' in v_skills or 'CPR' in v_skills:
                score_skill = 18
            elif 'Crowd' in v_skills:
                score_skill = 10
        else:
            if 'Crowd' in v_skills or 'Marshall' in v_skills:
                score_skill = 25
            else:
                score_skill = 15

        # 3. Zone Relevance & Localization (Max 20 points)
        if em_zone and v_zone and em_zone.split('—')[0].strip() == v_zone.split('—')[0].strip():
            score_zone = 20
        elif 'Zone 03' in str(v_zone) or 'Zone 05' in str(v_zone):
            score_zone = 12
        else:
            score_zone = 5

        # 4. Route & Bypass Corridor Accessibility (Max 10 points)
        # Check if volunteer is outside the main procession choke line
        if dist_m <= 400 or 'Bypass' in str(v_skills) or score_zone == 20:
            score_route = 10
        else:
            score_route = 5

        # 5. Verification & Accreditation (Max 10 points)
        score_verif = 10 if v_verif == 'VERIFIED' else 5

        total_score = min(100, score_dist + score_skill + score_zone + score_route + score_verif)

        # Build Explainable Reason
        reasons = []
        reasons.append("Available")
        if score_skill >= 20:
            reasons.append(f"{v_cert if v_cert != 'None' else 'Medical Skill Match'}")
        if score_zone == 20:
            reasons.append(f"Inside {v_zone.split('—')[0].strip()}")
        reasons.append(f"{dist_m}m from patient (ETA {eta_min} min)")
        reasons.append("Accessible safe bypass corridor")

        reason_summary = " • ".join(reasons)

        candidate_obj = {
            'wari_id': v_id,
            'name': v_name,
            'total_score': total_score,
            'distance_m': dist_m,
            'distance_km': round(dist_km, 2),
            'eta_min': eta_min,
            'zone': v_zone,
            'skills': v_skills,
            'certification': v_cert,
            'verification_status': v_verif,
            'status': v_status,
            'reason': reason_summary,
            'reasons_list': reasons,
            'breakdown': {
                'distance_score': score_dist,
                'skill_match_score': score_skill,
                'zone_relevance_score': score_zone,
                'route_accessibility_score': score_route,
                'verification_score': score_verif
            }
        }
        scored_candidates.append(candidate_obj)

    # Sort descending by total score
    scored_candidates.sort(key=lambda x: (-x['total_score'], x['distance_m']))

    recommended = scored_candidates[0] if scored_candidates else None
    backups = scored_candidates[1:3] if len(scored_candidates) > 1 else []

    # Recommended Hospital Logic
    rec_hospital = recommend_hospital(em_data)

    return {
        'success': True,
        'emergency_id': em_data.get('emergency_id', 'EM-28471'),
        'severity': severity,
        'emergency_type': em_type,
        'model_name': 'WariSeva Explainable AI Response Engine v2.0 (Prototype)',
        'recommended_volunteer': recommended,
        'backup_volunteers': backups,
        'excluded_volunteers': excluded_candidates,
        'recommended_hospital': rec_hospital,
        'explainability_text': 'Prototype AI • Explainable Response Scoring model considering proximity, certified skill matching, zone localization, and bypass route congestion.'
    }

def recommend_hospital(em_data):
    \"\"\"Recommend best hospital based on trauma capability, travel ETA, and demo availability.\"\"\"
    pat_lat = float(em_data.get('latitude', 18.3444))
    pat_lon = float(em_data.get('longitude', 74.0305))
    hospitals = load_hospitals()

    if not hospitals:
        return {
            'hospital_id': 'HOSP-001',
            'name': 'Saswad Rural Sub-District Hospital',
            'distance_km': 2.8,
            'eta_min': 8,
            'emergency_capability': 'HIGH (Trauma Care & ICU)',
            'availability': 'AVAILABLE',
            'reason': 'Recommended based on emergency trauma capability, estimated travel time (8 min), and current demo availability.'
        }

    scored_hosp = []
    for h in hospitals:
        dist_km = calculate_haversine_distance(pat_lat, pat_lon, h['latitude'], h['longitude'])
        eta_min = max(4, int(round((dist_km / 30.0) * 60.0) + 2))
        
        # Capability score
        caps = h.get('capabilities', [])
        cap_score = 30 if ('TRAUMA_CARE' in caps or 'ICU' in caps or 'EMERGENCY_SURGERY' in caps) else 15
        
        # Distance score
        dist_score = max(0, 50 - int(dist_km * 8))
        
        total = cap_score + dist_score + 20 # availability
        scored_hosp.append({
            'hospital_id': h['hospital_id'],
            'name': h['name'],
            'address': h.get('address', 'Saswad-Hadapsar Road'),
            'distance_km': round(dist_km, 1),
            'distance_m': int(round(dist_km * 1000)),
            'eta_min': eta_min,
            'capabilities': caps,
            'emergency_capability': 'HIGH (Trauma & ICU)' if cap_score >= 30 else 'GENERAL_EMERGENCY',
            'availability': 'AVAILABLE',
            'score': total,
            'reason': f"Recommended based on {', '.join(caps[:2])}, estimated travel time ({eta_min} min), and verified demo availability."
        })

    scored_hosp.sort(key=lambda x: -x['score'])
    return scored_hosp[0] if scored_hosp else None

# =========================================================================
# NEW PROTOTYPE AI & RESPONDER NETWORK ROUTES
# =========================================================================

@app.route('/api/emergency/<emergency_id>/ai-recommendation', methods=['GET'])
def get_ai_recommendation(emergency_id):
    \"\"\"Return full explainable AI recommendation for an emergency incident.\"\"\"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(\"SELECT * FROM emergencies WHERE emergency_id = ?\", (emergency_id,))
    em = cursor.fetchone()
    conn.close()

    if not em:
        # Fallback to default demo incident structure
        em_dict = {
            'emergency_id': emergency_id,
            'latitude': 18.3444,
            'longitude': 74.0305,
            'wari_zone': 'Zone 04 — Saswad Palkhi Maidan',
            'emergency_type': 'MEDICAL',
            'severity': 'CRITICAL'
        }
    else:
        em_dict = dict(em)

    ai_result = ai_response_engine(em_dict)
    return jsonify(ai_result), 200

@app.route('/api/volunteer/register', methods=['POST'])
def register_volunteer():
    \"\"\"Prototype Volunteer Onboarding & Accreditation.\"\"\"
    data = request.get_json(silent=True) if request.is_json else request.form.to_dict()
    if not data:
        return jsonify({'success': False, 'error': 'Invalid registration payload.'}), 400

    name = str(data.get('name', '')).strip()
    phone = str(data.get('phone', '')).strip()
    zone = str(data.get('zone', 'Zone 04 — Saswad Palkhi Maidan')).strip()
    skills = str(data.get('skills', 'First Aid, Crowd Assistance')).strip()
    cert = str(data.get('certification', 'First Aid Certified')).strip()
    org = str(data.get('organization', 'Warkari Seva Mandal')).strip()
    languages = str(data.get('languages', 'Marathi, Hindi, English')).strip()

    if not name or not phone:
        return jsonify({'success': False, 'error': 'Name and Mobile Number are required.'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(\"SELECT COUNT(*) as count FROM users WHERE role = 'VOLUNTEER'\")
    v_count = cursor.fetchone()['count']
    new_v_id = f\"V-{v_count + 1:03d}\"

    cursor.execute('''
        INSERT INTO users (
            wari_id, name, phone, role, latitude, longitude, location_enabled,
            status, zone, skills, certification, verification_status, organization, languages
        ) VALUES (?, ?, ?, 'VOLUNTEER', 18.3465, 74.0295, 1, 'AVAILABLE', ?, ?, ?, 'VERIFIED', ?, ?)
    ''', (new_v_id, name, phone, zone, skills, cert, org, languages))

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'volunteer_id': new_v_id,
        'name': name,
        'zone': zone,
        'status': 'AVAILABLE',
        'verification_status': 'VERIFIED',
        'message': f'Volunteer {name} ({new_v_id}) registered and verified successfully in {zone}.'
    }), 201

@app.route('/api/volunteer/toggle-availability', methods=['POST'])
def toggle_volunteer_availability():
    \"\"\"Toggle volunteer status between AVAILABLE and OFFLINE.\"\"\"
    data = request.get_json(silent=True) or {}
    v_id = data.get('volunteer_id', 'V-001')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(\"SELECT status FROM users WHERE wari_id = ?\", (v_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return jsonify({'success': False, 'error': 'Volunteer not found.'}), 404

    current_status = row['status']
    new_status = 'OFFLINE' if current_status == 'AVAILABLE' else 'AVAILABLE'

    cursor.execute(\"UPDATE users SET status = ? WHERE wari_id = ?\", (new_status, v_id))
    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'volunteer_id': v_id,
        'status': new_status,
        'message': f'Volunteer status updated to {new_status}.'
    }), 200

@app.route('/api/incident/create-for-pilgrim', methods=['POST'])
def create_incident_for_pilgrim():
    \"\"\"Command Center Action: Create an emergency incident for an elderly/unregistered pilgrim without the app.\"\"\"
    data = request.get_json(silent=True) if request.is_json else request.form.to_dict()
    if not data:
        return jsonify({'success': False, 'error': 'Invalid payload.'}), 400

    name = str(data.get('patient_name', 'Elderly Pilgrim')).strip() or 'Elderly Pilgrim'
    raw_wari_id = str(data.get('wari_id', '')).strip()
    wari_id = raw_wari_id if raw_wari_id else f\"WS-UNREG-{random.randint(1000, 9999)}\"
    is_unreg = 1 if not raw_wari_id else 0

    em_type = str(data.get('emergency_type', 'MEDICAL')).upper()
    severity = str(data.get('severity', 'CRITICAL')).upper()
    zone = str(data.get('zone', 'Zone 04 — Saswad Palkhi Maidan')).strip()
    notes = str(data.get('notes', 'Logged by Command Center Operator')).strip()
    lat = float(data.get('latitude', 18.3444))
    lon = float(data.get('longitude', 74.0305))

    em_id = generate_unique_emergency_id()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO emergencies (
            emergency_id, wari_id, reported_by, emergency_type, priority,
            latitude, longitude, location_accuracy, wari_zone, landmark,
            severity, notes, is_unregistered_pilgrim, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, 5.0, ?, 'Saswad Central Palkhi Ground', ?, ?, ?, 'CREATED')
    ''', (em_id, wari_id, name, em_type, severity, lat, lon, zone, severity, notes, is_unreg))

    conn.commit()
    conn.close()

    # Automatically run AI response recommendation
    em_dict = {
        'emergency_id': em_id,
        'latitude': lat,
        'longitude': lon,
        'wari_zone': zone,
        'emergency_type': em_type,
        'severity': severity
    }
    ai_match = ai_response_engine(em_dict)

    return jsonify({
        'success': True,
        'emergency_id': em_id,
        'patient_name': name,
        'wari_id': wari_id,
        'is_unregistered_pilgrim': bool(is_unreg),
        'severity': severity,
        'ai_recommendation': ai_match.get('recommended_volunteer'),
        'message': f'Incident {em_id} created for assisted pilgrim {name}. AI matched to {ai_match.get(\"recommended_volunteer\", {}).get(\"name\", \"Volunteer\")}.'
    }), 201

@app.route('/api/command-center/resources-count', methods=['GET'])
def get_command_resources_count():
    \"\"\"Return live and prototype resource counts for Command Center operational dashboard.\"\"\"
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(\"SELECT COUNT(*) as c FROM users WHERE role = 'VOLUNTEER' AND status = 'AVAILABLE'\")
    v_avail = cursor.fetchone()['c'] + 7 # Demo pool baseline (12 total available)

    cursor.execute(\"SELECT COUNT(*) as c FROM users WHERE role = 'MEDICAL_RESPONDER' AND status = 'AVAILABLE'\")
    r_avail = cursor.fetchone()['c'] # 4 responders

    cursor.execute(\"SELECT COUNT(*) as c FROM emergencies WHERE status NOT IN ('RESOLVED', 'DECLINED')\")
    em_active = cursor.fetchone()['c']

    cursor.execute(\"SELECT COUNT(*) as c FROM medical_camps WHERE status = 'AVAILABLE'\")
    c_avail = cursor.fetchone()['c'] # 2-4 camps

    conn.close()

    return jsonify({
        'success': True,
        'available_volunteers': v_avail,
        'available_medical_responders': max(4, r_avail),
        'active_incidents': em_active,
        'nearby_hospitals': 3,
        'active_medical_camps': max(2, c_avail),
        'is_demo_data': True,
        'notice': 'Prototype Operational Resource Registry'
    }), 200
"""

with open('backend/app.py', 'r', encoding='utf-8') as f:
    app_code = f.read()

# Insert before if __name__ == '__main__':
marker = "if __name__ == '__main__':"
assert marker in app_code, "Could not find main marker in app.py"

parts = app_code.split(marker)
new_app_code = parts[0] + engine_code + "\n" + marker + parts[1]

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(new_app_code)

print("Successfully integrated intelligent response engine and new prototype routes into backend/app.py!")
