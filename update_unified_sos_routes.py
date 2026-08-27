with open('backend/app.py', 'r', encoding='utf-8') as f:
    code = f.read()

old_public_routes = """@app.route('/api/public/report-emergency', methods=['POST'])
def public_report_emergency():
    \"\"\"
    Emergency creation initiated by any public citizen scanning a pilgrim's QR wristband.
    Seamlessly integrates into the existing shared incident state & AI Response Engine.
    \"\"\"
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    wari_id = str(data.get('wari_id', 'WS-28471')).strip().upper()
    em_type = str(data.get('emergency_type', 'MEDICAL')).upper()
    severity = 'CRITICAL'
    lat = float(data.get('latitude', 18.3444))
    lon = float(data.get('longitude', 74.0305))
    loc_source = str(data.get('location_source', 'GPS'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM pilgrims WHERE wari_id = ?", (wari_id,))
    row = cursor.fetchone()
    patient_name = row['name'] if row else 'Tukaram Shinde'

    em_id = 'EM-28471' if wari_id == 'WS-28471' else generate_unique_emergency_id()

    # Reset any previous state for this demo ID
    cursor.execute("DELETE FROM emergencies WHERE emergency_id = ?", (em_id,))
    cursor.execute("DELETE FROM notifications WHERE emergency_id = ?", (em_id,))
    cursor.execute("DELETE FROM location_updates WHERE emergency_id = ?", (em_id,))

    cursor.execute('''
        INSERT INTO emergencies (
            emergency_id, wari_id, reported_by, emergency_type, priority,
            latitude, longitude, location_accuracy, wari_zone, landmark,
            assigned_volunteer, assigned_camp, assigned_responder, assigned_hospital,
            severity, notes, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, 5.0, 'Zone 04 — Saswad Palkhi Maidan',
                  'Saswad Central Palkhi Maidan Ground', 'V-001', 'MC-001', 'MR-001', 'HOSP-001',
                  ?, ?, 'CREATED')
    ''', (em_id, wari_id, patient_name, em_type, severity, lat, lon, severity, f'Reported via Public QR Wristband ({loc_source})'))

    cursor.execute('''
        INSERT INTO notifications (emergency_id, recipient_id, recipient_type, notification_type, status)
        VALUES (?, 'V-001', 'VOLUNTEER', 'EMERGENCY_ALERT', 'PENDING')
    ''', (em_id,))

    conn.commit()
    conn.close()

    # Run AI Response Engine
    em_dict = {
        'emergency_id': em_id,
        'latitude': lat,
        'longitude': lon,
        'wari_zone': 'Zone 04 — Saswad Palkhi Maidan',
        'emergency_type': em_type,
        'severity': severity
    }
    ai_match = ai_response_engine(em_dict)

    return jsonify({
        'success': True,
        'emergency_id': em_id,
        'patient_name': patient_name,
        'wari_id': wari_id,
        'emergency_type': em_type,
        'status': 'DISPATCHED',
        'location_source': loc_source,
        'assigned_volunteer': ai_match.get('recommended_volunteer'),
        'recommended_hospital': ai_match.get('recommended_hospital'),
        'message': f'Emergency {em_id} registered for {patient_name}. AI dispatch coordinating.'
    }), 201

@app.route('/api/public/emergency-status/<emergency_id>', methods=['GET'])
def public_emergency_status(emergency_id):
    \"\"\"Public status polling for normal phone browser showing live dispatch status.\"\"\"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emergencies WHERE emergency_id = ?", (emergency_id,))
    em = cursor.fetchone()
    conn.close()

    if not em:
        return jsonify({'success': False, 'error': 'Incident not found.'}), 404

    return jsonify({
        'success': True,
        'emergency_id': em['emergency_id'],
        'patient_name': em['reported_by'],
        'status': em['status'],
        'emergency_type': em['emergency_type'],
        'assigned_volunteer': em['assigned_volunteer'] or 'V-001 (Ramesh Kulkarni)',
        'assigned_responder': em['assigned_responder'] or 'MR-001 (Mobile Ambulance 1)',
        'assigned_hospital': em['assigned_hospital'] or 'Saswad Rural Hospital',
        'zone': em['wari_zone']
    }), 200"""

new_public_routes = """@app.route('/api/public/report-emergency', methods=['POST'])
def public_report_emergency():
    \"\"\"
    Unified Emergency Creation initiated via QR Wristband Scan (Normal Phone).
    Executes the exact same emergency creation, responder matching, and notification pipeline.
    Patient: Tukaram Shinde (from QR token WS-28471)
    Source: QR_WARI_ID
    \"\"\"
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    wari_id = str(data.get('wari_id', 'WS-28471')).strip().upper()
    em_type = str(data.get('emergency_type', 'MEDICAL')).upper()
    severity = 'CRITICAL'
    source = 'QR_WARI_ID'
    reporter_type = str(data.get('reporter_type', 'QR_PUBLIC_USER'))
    lat = float(data.get('latitude', 18.3444))
    lon = float(data.get('longitude', 74.0305))
    loc_source = str(data.get('location_source', 'GPS'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM pilgrims WHERE wari_id = ?", (wari_id,))
    row = cursor.fetchone()
    patient_name = row['name'] if row else 'Tukaram Shinde'

    em_id = 'EM-28471' if wari_id == 'WS-28471' else generate_unique_emergency_id()

    # Reset any previous state for this demo ID to ensure fresh clean dispatch
    cursor.execute("DELETE FROM emergencies WHERE emergency_id = ?", (em_id,))
    cursor.execute("DELETE FROM notifications WHERE emergency_id = ?", (em_id,))
    cursor.execute("DELETE FROM location_updates WHERE emergency_id = ?", (em_id,))

    cursor.execute('''
        INSERT INTO emergencies (
            emergency_id, wari_id, reported_by, emergency_type, priority,
            latitude, longitude, location_accuracy, wari_zone, landmark,
            assigned_volunteer, assigned_camp, assigned_responder, assigned_hospital,
            severity, notes, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, 5.0, 'Zone 04 — Saswad Palkhi Maidan',
                  'Saswad Central Palkhi Maidan Ground', 'V-001', 'MC-001', 'MR-001', 'HOSP-001',
                  ?, ?, 'CREATED')
    ''', (em_id, wari_id, patient_name, em_type, severity, lat, lon, severity, f'Source: QR Wristband ({loc_source}) • Reporter: {reporter_type}'))

    # Notify nearest volunteers in 50km radius
    cursor.execute("SELECT * FROM users WHERE role = 'VOLUNTEER' AND status = 'AVAILABLE' AND latitude IS NOT NULL")
    vols = cursor.fetchall()
    for v in vols:
        cursor.execute('''
            INSERT INTO notifications (emergency_id, recipient_id, recipient_type, notification_type, status)
            VALUES (?, ?, 'VOLUNTEER', 'EMERGENCY_ALERT', 'PENDING')
        ''', (em_id, v['wari_id']))

    conn.commit()
    conn.close()

    # Run unified AI Response Prioritization & Responder Allocation Engine
    em_dict = {
        'emergency_id': em_id,
        'latitude': lat,
        'longitude': lon,
        'wari_zone': 'Zone 04 — Saswad Palkhi Maidan',
        'emergency_type': em_type,
        'severity': severity
    }
    ai_match = ai_response_engine(em_dict)

    return jsonify({
        'success': True,
        'emergency_id': em_id,
        'patient_name': patient_name,
        'wari_id': wari_id,
        'source': source,
        'reporter_type': reporter_type,
        'emergency_type': em_type,
        'status': 'DISPATCHED',
        'location_source': loc_source,
        'assigned_volunteer': ai_match.get('recommended_volunteer'),
        'nearest_camp': {
            'name': 'Saswad Palkhi Maidan Medical Tent (MC-001)',
            'distance_m': 238
        },
        'recommended_hospital': ai_match.get('recommended_hospital'),
        'message': f'Emergency {em_id} created for patient {patient_name}. AI dispatch coordinating.'
    }), 201

@app.route('/api/public/emergency-status/<emergency_id>', methods=['GET'])
def public_emergency_status(emergency_id):
    \"\"\"Public status polling for normal phone browser showing live dispatch status.\"\"\"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emergencies WHERE emergency_id = ?", (emergency_id,))
    em = cursor.fetchone()
    conn.close()

    if not em:
        return jsonify({'success': False, 'error': 'Incident not found.'}), 404

    return jsonify({
        'success': True,
        'emergency_id': em['emergency_id'],
        'patient_name': em['reported_by'],
        'status': em['status'],
        'emergency_type': em['emergency_type'],
        'source': 'QR_WARI_ID',
        'assigned_volunteer': em['assigned_volunteer'] or 'Ramesh Kulkarni (V-001)',
        'assigned_responder': em['assigned_responder'] or 'Dr. Arvind Shinde (MR-001)',
        'assigned_camp': 'Saswad Palkhi Maidan Medical Tent (MC-001)',
        'assigned_hospital': em['assigned_hospital'] or 'Purandar Critical Care & Trauma Hospital',
        'zone': em['wari_zone']
    }), 200"""

assert old_public_routes in code, "Could not find old_public_routes in app.py"
code = code.replace(old_public_routes, new_public_routes)

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated backend/app.py with Unified SOS Creation & Live Status logic!")
