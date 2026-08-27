with open('backend/app.py', 'r', encoding='utf-8') as f:
    code = f.read()

target = """    conn.close()
    return jsonify({'success': True, 'emergencies': emergencies}), 200

@app.route('/api/camp/dashboard-data', methods=['GET'])
def get_camp_dashboard_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT e.*, n.status as notif_status, n.recipient_id as notif_camp
        FROM emergencies e
        LEFT JOIN notifications n ON e.emergency_id = n.emergency_id AND n.recipient_type = 'CAMP'
        ORDER BY e.created_at DESC
        LIMIT 10
    ''')
    rows = cursor.fetchall()

    emergencies = []
    for r in rows:
        dist_km = calculate_haversine_distance(18.3460, 74.0320, r['latitude'], r['longitude'])
        dist_m = int(round(dist_km * 1000))
        item = dict(r)
        item['distance_m'] = dist_m
        item['distance_km'] = round(dist_km, 2)
        emergencies.append(item)

    conn.close()
    return jsonify({'success': True, 'emergencies': emergencies}), 200"""

replacement = """    conn.close()
    return jsonify({'success': True, 'count': len(emergencies), 'emergencies': emergencies}), 200

@app.route('/api/camp/dashboard-data', methods=['GET'])
def get_camp_dashboard_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT e.*, n.status as notif_status, n.recipient_id as notif_camp
        FROM emergencies e
        LEFT JOIN notifications n ON e.emergency_id = n.emergency_id AND n.recipient_type = 'CAMP'
        ORDER BY e.created_at DESC
        LIMIT 10
    ''')
    rows = cursor.fetchall()

    emergencies = []
    for r in rows:
        dist_km = calculate_haversine_distance(18.3460, 74.0320, r['latitude'], r['longitude'])
        dist_m = int(round(dist_km * 1000))
        item = dict(r)
        item['distance_m'] = dist_m
        item['distance_km'] = round(dist_km, 2)
        emergencies.append(item)

    conn.close()
    return jsonify({'success': True, 'count': len(emergencies), 'emergencies': emergencies}), 200

@app.route('/api/responder/dashboard-data', methods=['GET'])
def get_responder_dashboard_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT e.*, n.status as notif_status, n.recipient_id as notif_responder
        FROM emergencies e
        LEFT JOIN notifications n ON e.emergency_id = n.emergency_id AND n.recipient_type = 'RESPONDER'
        WHERE e.status NOT IN ('RESOLVED', 'DECLINED')
        ORDER BY e.created_at DESC
        LIMIT 10
    ''')
    rows = cursor.fetchall()

    emergencies = []
    for r in rows:
        dist_km = calculate_haversine_distance(18.3390, 74.0260, r['latitude'], r['longitude'])
        dist_m = int(round(dist_km * 1000))
        item = dict(r)
        item['distance_m'] = dist_m
        item['distance_km'] = round(dist_km, 2)
        emergencies.append(item)

    conn.close()
    return jsonify({'success': True, 'count': len(emergencies), 'emergencies': emergencies}), 200"""

assert target in code, "Could not find target in backend/app.py"
code = code.replace(target, replacement)

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated backend/app.py with get_responder_dashboard_data and count property!")
