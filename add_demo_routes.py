demo_endpoints = """
# =========================================================================
# DEMO MODE 1-CLICK TRIGGERS & CLEAN RESET
# =========================================================================

@app.route('/api/demo/create-emergency', methods=['POST'])
def demo_create_emergency():
    \"\"\"1-Click Demo Emergency Trigger (EM-28471 Synchronized).\"\"\"
    em_id = 'EM-28471'
    wari_id = 'WS-28471'
    name = 'Tukaram Shinde'
    lat = 18.3444
    lon = 74.0305
    acc = 5.0
    zone = 'Zone 04 — Saswad Palkhi Maidan'

    conn = get_db_connection()
    cursor = conn.cursor()

    # Ensure user exists
    cursor.execute("SELECT 1 FROM users WHERE wari_id = ?", (wari_id,))
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO users (wari_id, name, phone, role, latitude, longitude, location_enabled, status)
            VALUES (?, ?, '9822128471', 'WARKARI', ?, ?, 1, 'ACTIVE')
        ''', (wari_id, name, lat, lon))

    # Delete previous instance of EM-28471 if any
    cursor.execute("DELETE FROM emergencies WHERE emergency_id = ?", (em_id,))
    cursor.execute("DELETE FROM notifications WHERE emergency_id = ?", (em_id,))
    cursor.execute("DELETE FROM location_updates WHERE emergency_id = ?", (em_id,))

    # Insert synchronized emergency
    cursor.execute('''
        INSERT INTO emergencies (
            emergency_id, wari_id, reported_by, emergency_type, priority,
            latitude, longitude, location_accuracy, wari_zone, landmark,
            assigned_volunteer, assigned_camp, assigned_responder, assigned_hospital,
            severity, notes, status
        ) VALUES (?, ?, ?, 'MEDICAL', 'CRITICAL', ?, ?, ?, ?, 'Saswad Central Palkhi Maidan Ground',
                  'V-001', 'CAMP-001', 'MR-001', 'HOSP-001', 'CRITICAL', 'Demo Live Simulation', 'CREATED')
    ''', (em_id, wari_id, name, lat, lon, acc, zone))

    # Insert notifications for volunteer and camp
    cursor.execute('''
        INSERT INTO notifications (emergency_id, recipient_id, recipient_type, notification_type, status)
        VALUES (?, 'V-001', 'VOLUNTEER', 'EMERGENCY_ALERT', 'PENDING')
    ''', (em_id,))
    cursor.execute('''
        INSERT INTO notifications (emergency_id, recipient_id, recipient_type, notification_type, status)
        VALUES (?, 'CAMP-001', 'CAMP', 'EMERGENCY_ALERT', 'PENDING')
    ''', (em_id,))

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'emergency_id': em_id,
        'wari_id': wari_id,
        'name': name,
        'reported_by': name,
        'wari_zone': zone,
        'status': 'CREATED',
        'severity': 'CRITICAL',
        'message': f'Synchronized demo emergency {em_id} created in {zone}.'
    }), 201

@app.route('/api/demo/reset', methods=['POST'])
def demo_reset():
    \"\"\"Clean reset of demo database state for prototype demonstration.\"\"\"
    conn = get_db_connection()
    cursor = conn.cursor()

    # Clear emergencies and notifications
    cursor.execute("DELETE FROM emergencies")
    cursor.execute("DELETE FROM notifications")
    cursor.execute("DELETE FROM location_updates")

    # Reset volunteers
    cursor.execute("UPDATE users SET status = 'AVAILABLE' WHERE role = 'VOLUNTEER'")
    cursor.execute("UPDATE users SET status = 'RESPONDING' WHERE wari_id = 'V-004'") # Priya is engaged on another incident
    cursor.execute("UPDATE users SET status = 'AVAILABLE' WHERE role = 'MEDICAL_RESPONDER'")
    cursor.execute("UPDATE medical_camps SET status = 'AVAILABLE'")

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'message': 'Demo system state cleanly reset to initial prototype state.'
    }), 200
"""

with open('backend/app.py', 'r', encoding='utf-8') as f:
    app_code = f.read()

marker = "if __name__ == '__main__':"
parts = app_code.split(marker)
new_code = parts[0] + demo_endpoints + "\n" + marker + parts[1]

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(new_code)

print("Added demo endpoints to backend/app.py!")
