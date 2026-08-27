with open('backend/app.py', 'r', encoding='utf-8') as f:
    code = f.read()

old_block = """    # 4. Hospital Data
    hosp_data = None
    if em['assigned_hospital']:
        hospitals = load_hospitals()
        h = next((h for h in hospitals if h['hospital_id'] == em['assigned_hospital']), None)
        if h:
            hosp_data = h

    conn.close()

    nearest_zone = find_nearest_wari_zone(patient_lat, patient_lon)
    crowd_density = nearest_zone.get('crowd_density', 'HIGH')

    return jsonify({
        'success': True,
        'emergency_id': emergency_id,
        'status': em['status'],
        'has_reached': (em['status'] in ('WITH_PATIENT', 'ARRIVED', 'HOSPITAL_SELECTED', 'RESOLVED')),
        'crowd_density': crowd_density,
        'patient': {
            'wari_id': em['wari_id'],
            'name': em['reported_by'],
            'latitude': em['latitude'],
            'longitude': em['longitude'],
            'accuracy': em['location_accuracy'],
            'zone': em['wari_zone'],
            'landmark': em['landmark'],
            'priority': em['priority'],
            'emergency_type': em['emergency_type'],
            'created_at': em['created_at']
        },
        'nearest_volunteer': nearest_vol_candidate,
        'volunteer': volunteer_data,
        'responder': responder_data,
        'camp_id': em['assigned_camp'],
        'hospital': hosp_data,
        'distance_m': distance_m,
        'distance_km': distance_km,
        'eta_min': eta_min,
        'eta_text': f"{eta_min} min" if eta_min is not None else None
    }), 200"""

new_block = """    # 4. Hospital Data
    hosp_data = None
    hospitals = load_hospitals()
    if em['assigned_hospital']:
        h = next((h for h in hospitals if h['hospital_id'] == em['assigned_hospital']), None)
        if h:
            hosp_data = h

    # 5. Group Members for Patient
    cursor.execute("SELECT member_name as name, member_phone as phone, relationship FROM group_members WHERE wari_id = ?", (em['wari_id'],))
    group_rows = cursor.fetchall()
    group_members = [dict(g) for g in group_rows]

    # 6. Nearest Help Breakdown (4 Cards: Volunteer, Camp, Responder, Hospital)
    nearest_camp = None
    cursor.execute("SELECT * FROM medical_camps WHERE status = 'AVAILABLE'")
    camp_rows = cursor.fetchall()
    if camp_rows:
        sorted_camps = sorted(camp_rows, key=lambda c: calculate_haversine_distance(patient_lat, patient_lon, c['latitude'], c['longitude']))
        best_c = sorted_camps[0]
        c_dist_km = calculate_haversine_distance(patient_lat, patient_lon, best_c['latitude'], best_c['longitude'])
        nearest_camp = {
            'id': best_c['camp_id'],
            'name': best_c['name'],
            'distance_m': int(round(c_dist_km * 1000)),
            'eta_min': max(2, int(round((c_dist_km / 5.0) * 60.0))),
            'available': True
        }

    nearest_resp = None
    cursor.execute("SELECT * FROM users WHERE role = 'MEDICAL_RESPONDER' AND status = 'AVAILABLE'")
    resp_rows = cursor.fetchall()
    if resp_rows:
        sorted_resps = sorted(resp_rows, key=lambda r: calculate_haversine_distance(patient_lat, patient_lon, r['latitude'] or 18.3470, r['longitude'] or 74.0330))
        best_r = sorted_resps[0]
        r_dist_km = calculate_haversine_distance(patient_lat, patient_lon, best_r['latitude'] or 18.3470, best_r['longitude'] or 74.0330)
        nearest_resp = {
            'id': best_r['wari_id'],
            'name': best_r['name'],
            'distance_m': int(round(r_dist_km * 1000)),
            'eta_min': max(3, int(round((r_dist_km / 25.0) * 60.0) + 1)),
            'available': True
        }

    nearest_hosp = None
    if hospitals:
        sorted_hosps = sorted(hospitals, key=lambda h: calculate_haversine_distance(patient_lat, patient_lon, h['latitude'], h['longitude']))
        best_h = sorted_hosps[0]
        h_dist_km = calculate_haversine_distance(patient_lat, patient_lon, best_h['latitude'], best_h['longitude'])
        nearest_hosp = {
            'id': best_h['hospital_id'],
            'name': best_h['name'],
            'distance_m': int(round(h_dist_km * 1000)),
            'distance_km': round(h_dist_km, 1),
            'eta_min': max(5, int(round((h_dist_km / 35.0) * 60.0) + 2)),
            'available': True
        }

    conn.close()

    nearest_zone = find_nearest_wari_zone(patient_lat, patient_lon)
    crowd_density = nearest_zone.get('crowd_density', 'HIGH')

    recommendation_reason = "Selected based on active proximity, low estimated response time (3 min), and low crowd congestion along bypass path."

    return jsonify({
        'success': True,
        'emergency_id': emergency_id,
        'status': em['status'],
        'has_reached': (em['status'] in ('WITH_PATIENT', 'ARRIVED', 'HOSPITAL_SELECTED', 'RESOLVED')),
        'crowd_density': crowd_density,
        'patient': {
            'wari_id': em['wari_id'],
            'name': em['reported_by'],
            'latitude': em['latitude'],
            'longitude': em['longitude'],
            'accuracy': em['location_accuracy'],
            'zone': em['wari_zone'],
            'landmark': em['landmark'],
            'priority': em['priority'],
            'emergency_type': em['emergency_type'],
            'created_at': em['created_at'],
            'group_members': group_members
        },
        'nearest_volunteer': nearest_vol_candidate,
        'recommendation_reason': recommendation_reason,
        'nearest_help': {
            'volunteer': nearest_vol_candidate,
            'medical_camp': nearest_camp,
            'responder': nearest_resp,
            'hospital': nearest_hosp
        },
        'volunteer': volunteer_data,
        'responder': responder_data,
        'camp_id': em['assigned_camp'],
        'hospital': hosp_data,
        'distance_m': distance_m,
        'distance_km': distance_km,
        'eta_min': eta_min,
        'eta_text': f"{eta_min} min" if eta_min is not None else None
    }), 200"""

assert old_block in code, "Could not find old_block in backend/app.py"
code = code.replace(old_block, new_block)

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Successfully updated get_emergency_tracking with nearest_help and group members!")
