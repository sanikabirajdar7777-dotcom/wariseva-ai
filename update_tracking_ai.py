with open('backend/app.py', 'r', encoding='utf-8') as f:
    code = f.read()

target = """    nearest_zone = find_nearest_wari_zone(patient_lat, patient_lon)
    crowd_density = nearest_zone.get('crowd_density', 'HIGH')

    recommendation_reason = "Selected based on active proximity, low estimated response time (3 min), and low crowd congestion along bypass path."

    return jsonify({
        'success': True,
        'emergency_id': emergency_id,
        'status': em['status'],
        'has_reached': (em['status'] in ('WITH_PATIENT', 'ARRIVED', 'HOSPITAL_SELECTED', 'RESOLVED')),
        'crowd_density': crowd_density,"""

replacement = """    nearest_zone = find_nearest_wari_zone(patient_lat, patient_lon)
    crowd_density = nearest_zone.get('crowd_density', 'HIGH')

    ai_match_data = ai_response_engine(dict(em))
    rec_vol = ai_match_data.get('recommended_volunteer')
    recommendation_reason = rec_vol.get('reason') if rec_vol else "Selected based on active proximity, low estimated response time (3 min), and low crowd congestion along bypass path."

    return jsonify({
        'success': True,
        'emergency_id': emergency_id,
        'status': em['status'],
        'has_reached': (em['status'] in ('WITH_PATIENT', 'ARRIVED', 'HOSPITAL_SELECTED', 'RESOLVED')),
        'crowd_density': crowd_density,
        'ai_recommendation': ai_match_data,"""

assert target in code, "Could not find target in backend/app.py"
code = code.replace(target, replacement)

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated get_emergency_tracking with ai_recommendation engine integration!")
