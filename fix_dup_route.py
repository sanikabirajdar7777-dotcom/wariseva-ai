with open('backend/app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update first get_responder_dashboard_data to include 'count'
target1 = """@app.route('/api/responder/dashboard-data', methods=['GET'])
def get_responder_dashboard_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM emergencies 
        ORDER BY created_at DESC 
        LIMIT 10
    ''')
    rows = cursor.fetchall()

    emergencies = []
    for r in rows:
        item = dict(r)
        dist_km = calculate_haversine_distance(18.3470, 74.0330, r['latitude'], r['longitude'])
        dist_m = int(round(dist_km * 1000))
        item['distance_m'] = dist_m
        item['distance_km'] = round(dist_km, 2)
        emergencies.append(item)

    conn.close()
    return jsonify({'success': True, 'emergencies': emergencies}), 200"""

replacement1 = """@app.route('/api/responder/dashboard-data', methods=['GET'])
def get_responder_dashboard_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM emergencies 
        ORDER BY created_at DESC 
        LIMIT 10
    ''')
    rows = cursor.fetchall()

    emergencies = []
    for r in rows:
        item = dict(r)
        dist_km = calculate_haversine_distance(18.3470, 74.0330, r['latitude'], r['longitude'])
        dist_m = int(round(dist_km * 1000))
        item['distance_m'] = dist_m
        item['distance_km'] = round(dist_km, 2)
        emergencies.append(item)

    conn.close()
    return jsonify({'success': True, 'count': len(emergencies), 'emergencies': emergencies}), 200"""

assert target1 in code, "Could not find target1 in backend/app.py"
code = code.replace(target1, replacement1)

# 2. Remove duplicate second get_responder_dashboard_data
target2 = """@app.route('/api/responder/dashboard-data', methods=['GET'])
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

assert target2 in code, "Could not find target2 in backend/app.py"
code = code.replace(target2, "")

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Fixed duplicate get_responder_dashboard_data in backend/app.py!")
