with open('backend/app.py', 'r', encoding='utf-8') as f:
    code = f.read()

target = """    return jsonify({
        'success': True,
        'emergency_id': emergency_id,
        'wari_id': wari_id,
        'reported_by': reported_by,
        'emergency_type': emergency_type,"""

replacement = """    return jsonify({
        'success': True,
        'emergency_id': emergency_id,
        'wari_id': wari_id,
        'name': reported_by,
        'reported_by': reported_by,
        'emergency_type': emergency_type,"""

assert target in code, "Could not find target in backend/app.py"
code = code.replace(target, replacement)

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated create_emergency in backend/app.py with 'name' alias!")
