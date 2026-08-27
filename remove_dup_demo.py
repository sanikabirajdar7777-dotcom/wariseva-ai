with open('backend/app.py', 'r', encoding='utf-8') as f:
    code = f.read()

target = """# =========================================================================
# STEP 9: DEMO MODE APIS & FULL WORKFLOW RESET
# =========================================================================

@app.route('/api/demo/create-emergency', methods=['POST'])
def create_demo_emergency():
    \"\"\"Create a clean pre-seeded demonstration emergency for hackathon judging.\"\"\"
    conn = get_db_connection()
    cursor = conn.cursor()

    demo_wari_id = "WS-28471"
    cursor.execute("SELECT 1 FROM users WHERE wari_id = ?", (demo_wari_id,))
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO users (wari_id, name, phone, role, latitude, longitude, location_enabled, status)
            VALUES (?, 'Tukaram Shinde', '9822128471', 'WARKARI', 18.3444, 74.0305, 1, 'ACTIVE')
        ''', (demo_wari_id,))

    demo_em_id = "EM-28471"
    cursor.execute("DELETE FROM emergencies WHERE emergency_id = ?", (demo_em_id,))
    cursor.execute("DELETE FROM notifications WHERE emergency_id = ?", (demo_em_id,))
    cursor.execute("DELETE FROM location_updates WHERE emergency_id = ?", (demo_em_id,))

    cursor.execute('''
        INSERT INTO emergencies (
            emergency_id, wari_id, reported_by, emergency_type, priority,
            latitude, longitude, location_accuracy, wari_zone, landmark,
            assigned_volunteer, assigned_camp, assigned_responder, status
        ) VALUES (
            ?, ?, 'Tukaram Shinde', 'MEDICAL', 'URGENT',
            18.3444, 74.0305, 5.0, 'Zone 04 — Saswad Palkhi Maidan', 'Saswad Central Palkhi Maidan Ground',
            NULL, 'MC-001', NULL, 'CREATED'
        )
    ''', (demo_em_id, demo_wari_id))

    # Notify V-001 & MC-001
    cursor.execute('''
        INSERT INTO notifications (emergency_id, recipient_id, recipient_type, notification_type, status)
        VALUES (?, 'V-001', 'VOLUNTEER', 'EMERGENCY_ALERT', 'PENDING')
    ''', (demo_em_id,))
    cursor.execute('''
        INSERT INTO notifications (emergency_id, recipient_id, recipient_type, notification_type, status)
        VALUES (?, 'MC-001', 'CAMP', 'EMERGENCY_ALERT', 'PENDING')
    ''', (demo_em_id,))

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'emergency_id': demo_em_id,
        'wari_id': demo_wari_id,
        'name': 'Tukaram Shinde',
        'wari_zone': 'Zone 04 — Saswad Palkhi Maidan',
        'landmark': 'Saswad Central Palkhi Maidan Ground',
        'latitude': 18.3444,
        'longitude': 74.0305,
        'status': 'CREATED',
        'message': 'Demo emergency EM-28471 successfully created in Saswad Zone 04.'
    }), 201

@app.route('/api/demo/reset', methods=['POST'])
def reset_demo_data():
    \"\"\"Reset all test emergency states back to clean initial demo state.\"\"\"
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM emergencies")
    cursor.execute("DELETE FROM notifications")
    cursor.execute("DELETE FROM location_updates")
    cursor.execute("UPDATE users SET status = 'AVAILABLE' WHERE role IN ('VOLUNTEER', 'MEDICAL_RESPONDER')")
    cursor.execute("UPDATE medical_camps SET status = 'AVAILABLE'")

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'message': 'Demo database successfully reset to clean initial state.'
    }), 200"""

assert target in code, "Could not find target in backend/app.py"
code = code.replace(target, "")

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Removed duplicate demo routes block from backend/app.py!")
