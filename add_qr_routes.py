qr_routes_code = """
# =========================================================================
# WARISEVA FUNCTIONAL QR IDENTITY, SCANNER & PIN AUTHORIZATION
# =========================================================================

@app.route('/api/volunteer/login', methods=['POST'])
def volunteer_login():
    \"\"\"Authenticate volunteer against demo registry for secure identity access.\"\"\"
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    v_id = str(data.get('volunteer_id', '')).strip().upper()
    password = str(data.get('password', '')).strip()

    if not v_id or not password:
        return jsonify({'success': False, 'error': 'Volunteer ID and password are required.'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(\"SELECT * FROM users WHERE wari_id = ? AND role = 'VOLUNTEER'\", (v_id,))
    vol = cursor.fetchone()
    conn.close()

    # Demo credentials verification (V-001 / wari123 or valid registered volunteer)
    if not vol:
        return jsonify({'success': False, 'error': f'Volunteer {v_id} not found in registry.'}), 404

    if password != 'wari123' and password != 'demo123':
        return jsonify({'success': False, 'error': 'Invalid volunteer password.'}), 401

    return jsonify({
        'success': True,
        'token': f'demo-token-{v_id.lower()}',
        'volunteer': {
            'id': vol['wari_id'],
            'name': vol['name'],
            'phone': vol['phone'],
            'zone': vol['zone'] or 'Zone 04 — Saswad Palkhi Maidan',
            'skills': vol['skills'] or 'First Aid, CPR',
            'certification': vol['certification'] or 'First Aid Certified',
            'verification_status': vol['verification_status'] or 'VERIFIED',
            'status': vol['status'] or 'AVAILABLE'
        },
        'message': f'Volunteer {vol[\"name\"]} authenticated successfully.'
    }), 200

@app.route('/api/qr/lookup', methods=['POST'])
def qr_lookup():
    \"\"\"
    Step 1: Look up scanned WariSeva QR token/ID.
    Returns unclassified public identity info only (NO sensitive medical/contact data).
    \"\"\"
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    qr_data = str(data.get('qr_data', '')).strip().upper()

    if not qr_data:
        return jsonify({'success': False, 'error': 'No QR code payload received.'}), 400

    # Extract WariSeva ID if embedded in URL or raw string
    if 'WS-' in qr_data:
        match = re.search(r'WS-[A-Z0-9]+', qr_data)
        wari_id = match.group(0) if match else qr_data
    else:
        wari_id = qr_data

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(\"SELECT * FROM pilgrims WHERE wari_id = ?\", (wari_id,))
    pilgrim = cursor.fetchone()
    conn.close()

    if not pilgrim:
        return jsonify({
            'success': False,
            'found': False,
            'error': f'WariSeva ID \"{wari_id}\" not found. This QR is not registered in the WariSeva network.'
        }), 404

    return jsonify({
        'success': True,
        'found': True,
        'wari_id': pilgrim['wari_id'],
        'name': pilgrim['name'],
        'dindi': pilgrim['dindi'],
        'is_protected': True,
        'message': 'Pilgrim identity located. Emergency medical and contact information is protected by PIN.'
    }), 200

@app.route('/api/qr/verify', methods=['POST'])
def qr_verify_pin():
    \"\"\"
    Step 2: Verify Emergency PIN and unlock protected medical profile.
    Audits the access event in access_logs table for accountability.
    \"\"\"
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    wari_id = str(data.get('wari_id', '')).strip().upper()
    pin = str(data.get('pin', '')).strip()
    volunteer_id = str(data.get('volunteer_id', 'V-001')).strip().upper()
    volunteer_name = str(data.get('volunteer_name', 'Ramesh Kulkarni')).strip()

    if not wari_id or not pin:
        return jsonify({'success': False, 'error': 'WariSeva ID and PIN are required.'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(\"SELECT * FROM pilgrims WHERE wari_id = ?\", (wari_id,))
    pilgrim = cursor.fetchone()

    if not pilgrim:
        conn.close()
        return jsonify({'success': False, 'error': f'Pilgrim {wari_id} not found.'}), 404

    # Validate PIN securely (hashed check or fallback demo PIN '2741')
    pin_valid = False
    if pilgrim['pin_hash']:
        try:
            pin_valid = check_password_hash(pilgrim['pin_hash'], pin)
        except Exception:
            pin_valid = (pin == '2741')
    else:
        pin_valid = (pin == '2741')

    if not pin_valid:
        # Audit failed access attempt
        cursor.execute('''
            INSERT INTO access_logs (volunteer_id, volunteer_name, pilgrim_id, reason, status)
            VALUES (?, ?, ?, 'Emergency Assistance', 'DENIED_INVALID_PIN')
        ''', (volunteer_id, volunteer_name, wari_id))
        conn.commit()
        conn.close()
        return jsonify({
            'success': False,
            'authorized': False,
            'error': 'Incorrect emergency access PIN. Access Denied.'
        }), 401

    # Audit successful access
    cursor.execute('''
        INSERT INTO access_logs (volunteer_id, volunteer_name, pilgrim_id, reason, status)
        VALUES (?, ?, ?, 'Emergency Assistance', 'AUTHORIZED')
    ''', (volunteer_id, volunteer_name, wari_id))
    log_id = cursor.lastrowid
    conn.commit()
    conn.close()

    now_str = datetime.now().strftime('%d %b %Y, %I:%M:%S %p')

    return jsonify({
        'success': True,
        'authorized': True,
        'pilgrim': {
            'wari_id': pilgrim['wari_id'],
            'name': pilgrim['name'],
            'dindi': pilgrim['dindi'],
            'blood_group': pilgrim['blood_group'],
            'emergency_contact': pilgrim['emergency_contact'],
            'medical_alert': pilgrim['medical_alert'],
            'status': pilgrim['status']
        },
        'access_audit': {
            'log_id': log_id,
            'accessed_by': f'{volunteer_name} ({volunteer_id})',
            'volunteer_status': 'VERIFIED VOLUNTEER',
            'reason': 'Emergency Assistance',
            'access_time': now_str
        },
        'message': 'Identity verified. Authorized emergency medical profile unlocked.'
    }), 200

@app.route('/api/qr/report-emergency', methods=['POST'])
def qr_report_emergency():
    \"\"\"
    Step 3: Trigger emergency incident directly from scanned & verified QR profile.
    Connects into existing emergency shared state & AI Response Engine.
    \"\"\"
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    wari_id = str(data.get('wari_id', 'WS-28471')).strip().upper()
    volunteer_id = str(data.get('volunteer_id', 'V-001')).strip().upper()
    em_type = str(data.get('emergency_type', 'MEDICAL')).upper()
    severity = str(data.get('severity', 'CRITICAL')).upper()
    lat = float(data.get('latitude', 18.3444))
    lon = float(data.get('longitude', 74.0305))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Look up pilgrim name
    cursor.execute(\"SELECT name FROM pilgrims WHERE wari_id = ?\", (wari_id,))
    row = cursor.fetchone()
    patient_name = row['name'] if row else 'Tukaram Shinde'

    em_id = 'EM-28471' if wari_id == 'WS-28471' else generate_unique_emergency_id()

    # Clean previous demo instance if needed
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
                  'Saswad Central Palkhi Maidan Ground', ?, 'CAMP-001', 'MR-001', 'HOSP-001',
                  ?, 'Reported via QR Wristband Scanner', 'CREATED')
    ''', (em_id, wari_id, patient_name, em_type, severity, lat, lon, volunteer_id, severity))

    cursor.execute('''
        INSERT INTO notifications (emergency_id, recipient_id, recipient_type, notification_type, status)
        VALUES (?, ?, 'VOLUNTEER', 'EMERGENCY_ALERT', 'PENDING')
    ''', (em_id, volunteer_id))

    conn.commit()
    conn.close()

    # Automatically run AI response recommendation
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
        'reported_by_volunteer': volunteer_id,
        'ai_recommendation': ai_match.get('recommended_volunteer'),
        'recommended_hospital': ai_match.get('recommended_hospital'),
        'message': f'Emergency {em_id} created for {patient_name}. AI dispatch initiated.'
    }), 201

@app.route('/api/pilgrim/<wari_id>', methods=['GET'])
def get_pilgrim_card(wari_id):
    \"\"\"Public pilgrim wristband digital ID endpoint.\"\"\"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(\"SELECT wari_id, name, dindi, status, created_at FROM pilgrims WHERE wari_id = ?\", (wari_id.upper(),))
    pilgrim = cursor.fetchone()
    conn.close()

    if not pilgrim:
        return jsonify({'success': False, 'error': 'Pilgrim ID not found.'}), 404

    return jsonify({
        'success': True,
        'pilgrim': dict(pilgrim),
        'qr_value': pilgrim['wari_id'],
        'wristband_type': 'WATERPROOF_SILICONE_QR_NFC',
        'demo_mode': True
    }), 200

@app.route('/api/qr/access-logs', methods=['GET'])
def get_qr_access_logs():
    \"\"\"Return recent emergency access audit logs.\"\"\"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(\"SELECT * FROM access_logs ORDER BY access_time DESC LIMIT 20\")
    logs = [dict(r) for r in cursor.fetchall()]
    conn.close()

    return jsonify({
        'success': True,
        'count': len(logs),
        'logs': logs
    }), 200
"""

with open('backend/app.py', 'r', encoding='utf-8') as f:
    app_code = f.read()

marker = "if __name__ == '__main__':"
parts = app_code.split(marker)
new_code = parts[0] + qr_routes_code + "\n" + marker + parts[1]

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(new_code)

print("Added QR Scanner, Volunteer Auth, PIN Verification & Audit routes to backend/app.py!")
