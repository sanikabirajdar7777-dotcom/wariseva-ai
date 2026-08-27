public_routes_code = """
# =========================================================================
# PUBLIC PILGRIM PROFILE & WRISTBAND PASSWORD VERIFICATION
# =========================================================================

@app.route('/api/demo/verify-wristband-password', methods=['POST'])
def verify_wristband_password():
    \"\"\"Verify demo password 'WARI2026' before unlocking the physical wristband preview.\"\"\"
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    password = str(data.get('password', '')).strip()

    if not password:
        return jsonify({'success': False, 'error': 'Demo password is required.'}), 400

    if password.upper() == 'WARI2026':
        return jsonify({
            'success': True,
            'message': '✓ Demo access verified. Physical wristband unlocked.'
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': '❌ Incorrect demo password. Please enter WARI2026.'
        }), 401

@app.route('/public/pilgrim/<wari_id>', methods=['GET'])
def public_pilgrim_page(wari_id):
    \"\"\"
    Public Mobile Emergency Profile for normal phone camera / Google Lens scanning.
    Does NOT require WariSeva app or volunteer login.
    \"\"\"
    wari_id = str(wari_id).strip().upper()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(\"SELECT * FROM pilgrims WHERE wari_id = ?\", (wari_id,))
    pilgrim = cursor.fetchone()
    conn.close()

    # If not found, fallback to demo pilgrim Tukaram Shinde
    if not pilgrim:
        pilgrim_data = {
            'wari_id': wari_id,
            'name': 'Tukaram Shinde',
            'dindi': '27',
            'mobile': '+91 98XXXXXX42',
            'emergency_contact': '+91 97XXXXXX31',
            'emergency_relation': 'Son (मुलगा)',
            'blood_group': 'B+',
            'medical_alert': 'Asthma (दमा) — Requires Inhaler Support',
            'zone': 'Zone 04 — Saswad Palkhi Maidan',
            'status': 'REGISTERED'
        }
    else:
        pilgrim_data = {
            'wari_id': pilgrim['wari_id'],
            'name': pilgrim['name'],
            'dindi': pilgrim['dindi'] or '27',
            'mobile': '+91 98XXXXXX42',
            'emergency_contact': '+91 97XXXXXX31',
            'emergency_relation': 'Son (मुलगा)',
            'blood_group': pilgrim['blood_group'] or 'B+',
            'medical_alert': pilgrim['medical_alert'] or 'Asthma (दमा) — Requires Inhaler Support',
            'zone': 'Zone 04 — Saswad Palkhi Maidan',
            'status': pilgrim['status'] or 'REGISTERED'
        }

    return render_template('public_pilgrim.html', pilgrim=pilgrim_data)

@app.route('/api/public/report-emergency', methods=['POST'])
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

    cursor.execute(\"SELECT name FROM pilgrims WHERE wari_id = ?\", (wari_id,))
    row = cursor.fetchone()
    patient_name = row['name'] if row else 'Tukaram Shinde'

    em_id = 'EM-28471' if wari_id == 'WS-28471' else generate_unique_emergency_id()

    # Reset any previous state for this demo ID
    cursor.execute(\"DELETE FROM emergencies WHERE emergency_id = ?\", (em_id,))
    cursor.execute(\"DELETE FROM notifications WHERE emergency_id = ?\", (em_id,))
    cursor.execute(\"DELETE FROM location_updates WHERE emergency_id = ?\", (em_id,))

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
    cursor.execute(\"SELECT * FROM emergencies WHERE emergency_id = ?\", (emergency_id,))
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
    }), 200
"""

with open('backend/app.py', 'r', encoding='utf-8') as f:
    app_code = f.read()

marker = "if __name__ == '__main__':"
parts = app_code.split(marker)
new_app_code = parts[0] + public_routes_code + "\n" + marker + parts[1]

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(new_app_code)

print("Added public pilgrim profile and wristband password routes to backend/app.py!")
