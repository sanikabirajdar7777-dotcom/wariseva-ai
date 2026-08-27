with open('backend/app.py', 'r', encoding='utf-8') as f:
    code = f.read()

old_loc_update = """@app.route('/api/volunteer/location', methods=['POST'])
def volunteer_location_update():
    data = request.get_json(silent=True) if request.is_json else request.form.to_dict() or {}
    volunteer_id = str(data.get('volunteer_id', '')).strip()
    emergency_id = str(data.get('emergency_id', '')).strip()
    raw_lat = data.get('latitude')
    raw_lon = data.get('longitude')
    raw_acc = data.get('accuracy')

    if not volunteer_id or not emergency_id:
        return jsonify({'success': False, 'error': 'Volunteer ID and Emergency ID are required.'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE wari_id = ? AND role = 'VOLUNTEER'", (volunteer_id,))
    vol = cursor.fetchone()
    if not vol:
        conn.close()
        return jsonify({'success': False, 'error': f'Volunteer "{volunteer_id}" not found.'}), 404

    cursor.execute("SELECT * FROM emergencies WHERE emergency_id = ?", (emergency_id,))
    em = cursor.fetchone()
    if not em:
        conn.close()
        return jsonify({'success': False, 'error': f'Emergency "{emergency_id}" not found.'}), 404

    if em['assigned_volunteer'] != volunteer_id:
        conn.close()
        return jsonify({'success': False, 'error': f'Volunteer "{volunteer_id}" is not assigned.'}), 403

    try:
        lat = float(raw_lat)
        lon = float(raw_lon)
    except (ValueError, TypeError):
        conn.close()
        return jsonify({'success': False, 'error': 'Coordinates must be valid numbers.'}), 400

    if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
        conn.close()
        return jsonify({'success': False, 'error': 'Coordinates outside valid ranges.'}), 400

    acc = round(float(raw_acc), 1) if raw_acc is not None else None

    cursor.execute('''
        INSERT INTO location_updates (user_id, emergency_id, latitude, longitude, accuracy)
        VALUES (?, ?, ?, ?, ?)
    ''', (volunteer_id, emergency_id, lat, lon, acc))

    cursor.execute('''
        UPDATE users 
        SET latitude = ?, longitude = ?, location_enabled = 1 
        WHERE wari_id = ?
    ''', (lat, lon, volunteer_id))

    current_status = em['status']
    if current_status in ('CREATED', 'ACCEPTED'):
        cursor.execute('''
            UPDATE emergencies 
            SET status = 'EN_ROUTE', updated_at = CURRENT_TIMESTAMP 
            WHERE emergency_id = ?
        ''', (emergency_id,))
        current_status = 'EN_ROUTE'

    conn.commit()

    dist_km = calculate_haversine_distance(em['latitude'], em['longitude'], lat, lon)
    dist_m = int(round(dist_km * 1000))
    conn.close()

    return jsonify({
        'success': True,
        'volunteer_id': volunteer_id,
        'emergency_id': emergency_id,
        'latitude': lat,
        'longitude': lon,
        'accuracy': acc,
        'distance_to_patient_m': dist_m,
        'distance_to_patient_km': round(dist_km, 2),
        'status': current_status,
        'message': 'Volunteer location updated successfully.'
    }), 200"""

new_loc_update = """@app.route('/api/volunteer/location', methods=['POST'])
def volunteer_location_update():
    data = request.get_json(silent=True) if request.is_json else request.form.to_dict() or {}
    volunteer_id = str(data.get('volunteer_id', '')).strip()
    emergency_id = str(data.get('emergency_id', '')).strip()
    raw_lat = data.get('latitude')
    raw_lon = data.get('longitude')
    raw_acc = data.get('accuracy')

    if not volunteer_id:
        return jsonify({'success': False, 'error': 'Volunteer ID is required.'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE wari_id = ? AND role = 'VOLUNTEER'", (volunteer_id,))
    vol = cursor.fetchone()
    if not vol:
        conn.close()
        return jsonify({'success': False, 'error': f'Volunteer "{volunteer_id}" not found.'}), 404

    try:
        lat = float(raw_lat)
        lon = float(raw_lon)
    except (ValueError, TypeError):
        conn.close()
        return jsonify({'success': False, 'error': 'Coordinates must be valid numbers.'}), 400

    if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
        conn.close()
        return jsonify({'success': False, 'error': 'Coordinates outside valid ranges.'}), 400

    acc = round(float(raw_acc), 1) if raw_acc is not None else None

    cursor.execute('''
        UPDATE users 
        SET latitude = ?, longitude = ?, location_enabled = 1 
        WHERE wari_id = ?
    ''', (lat, lon, volunteer_id))

    dist_m = None
    dist_km = None
    current_status = vol['status']

    if emergency_id:
        cursor.execute("SELECT * FROM emergencies WHERE emergency_id = ?", (emergency_id,))
        em = cursor.fetchone()
        if em:
            cursor.execute('''
                INSERT INTO location_updates (user_id, emergency_id, latitude, longitude, accuracy)
                VALUES (?, ?, ?, ?, ?)
            ''', (volunteer_id, emergency_id, lat, lon, acc))

            if em['status'] in ('CREATED', 'ACCEPTED'):
                cursor.execute('''
                    UPDATE emergencies 
                    SET status = 'EN_ROUTE', updated_at = CURRENT_TIMESTAMP 
                    WHERE emergency_id = ?
                ''', (emergency_id,))
                current_status = 'EN_ROUTE'
            else:
                current_status = em['status']

            dist_km = calculate_haversine_distance(em['latitude'], em['longitude'], lat, lon)
            dist_m = int(round(dist_km * 1000))

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'volunteer_id': volunteer_id,
        'emergency_id': emergency_id or None,
        'latitude': lat,
        'longitude': lon,
        'accuracy': acc,
        'distance_to_patient_m': dist_m,
        'distance_to_patient_km': round(dist_km, 2) if dist_km is not None else None,
        'status': current_status,
        'message': 'Volunteer location updated successfully.'
    }), 200"""

assert old_loc_update in code, "Could not find old_loc_update in backend/app.py"
code = code.replace(old_loc_update, new_loc_update)

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated /api/volunteer/location to support both standalone and emergency tracking location updates!")
