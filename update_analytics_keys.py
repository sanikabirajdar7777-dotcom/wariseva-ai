with open('backend/app.py', 'r', encoding='utf-8') as f:
    code = f.read()

target = """    return jsonify({
        'success': True,
        'emergency_id': emergency_id,
        'status': status,
        'created_at': created_at,
        'resolved_at': updated_at if is_resolved else None,
        'response_time_seconds': total_response_s,
        'response_time_formatted': time_formatted,
        'volunteer_assignment_seconds': vol_assign_s,
        'volunteer_travel_seconds': vol_travel_s,
        'responder_transit_seconds': resp_transit_s,
        'patient_reached': (status in ('WITH_PATIENT', 'RESPONDER_ASSIGNED', 'EN_ROUTE', 'ARRIVED', 'HOSPITAL_SELECTED', 'RESOLVED')),
        'route_efficiency': 'HIGH (Saved 7 min via South Bypass Corridor)',
        'scores': {
            'dispatch_score': score_dispatch,
            'gps_accuracy_score': score_gps,
            'route_efficiency_score': score_route,
            'responder_score': score_responder,
            'total_score': total_score,
            'max_score': 100
        },
        'rating': 'EXEMPLARY RAPID RESPONSE',
        'is_prototype_metric': True
    }), 200"""

replacement = """    return jsonify({
        'success': True,
        'emergency_id': emergency_id,
        'status': status,
        'created_at': created_at,
        'resolved_at': updated_at if is_resolved else None,
        'total_response_time': time_formatted,
        'response_time_seconds': total_response_s,
        'response_time_formatted': time_formatted,
        'volunteer_assignment_seconds': vol_assign_s,
        'volunteer_travel_seconds': vol_travel_s,
        'responder_transit_seconds': resp_transit_s,
        'patient_reached': (status in ('WITH_PATIENT', 'RESPONDER_ASSIGNED', 'EN_ROUTE', 'ARRIVED', 'HOSPITAL_SELECTED', 'RESOLVED')),
        'route_efficiency': 'HIGH (Saved 7 min via South Bypass Corridor)',
        'wariseva_score': total_score,
        'rating_text': 'EXEMPLARY RAPID RESPONSE',
        'scores': {
            'dispatch_score': score_dispatch,
            'gps_accuracy_score': score_gps,
            'route_efficiency_score': score_route,
            'responder_score': score_responder,
            'total_score': total_score,
            'max_score': 100
        },
        'rating': 'EXEMPLARY RAPID RESPONSE',
        'is_prototype_metric': True
    }), 200"""

assert target in code, "Could not find target in backend/app.py"
code = code.replace(target, replacement)

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated get_emergency_analytics return dictionary with aliases!")
