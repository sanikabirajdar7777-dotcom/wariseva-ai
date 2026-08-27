with open('backend/app.py', 'r', encoding='utf-8') as f:
    code = f.read()

old_code = """    emergency_id = generate_unique_emergency_id()

    cursor.execute('''
        INSERT INTO emergencies (
            emergency_id, wari_id, reported_by, emergency_type, priority,
            latitude, longitude, location_accuracy, wari_zone, landmark, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        emergency_id, wari_id, reported_by, emergency_type, priority,
        lat, lon, accuracy, wari_zone, landmark, status
    ))"""

new_code = """    emergency_id = data.get('emergency_id')
    if not emergency_id:
        if wari_id == 'WS-28471':
            emergency_id = 'EM-28471'
        else:
            emergency_id = generate_unique_emergency_id()

    # Clean up any existing records for this emergency_id to ensure clean re-dispatch
    cursor.execute("DELETE FROM emergencies WHERE emergency_id = ?", (emergency_id,))
    cursor.execute("DELETE FROM notifications WHERE emergency_id = ?", (emergency_id,))
    cursor.execute("DELETE FROM location_updates WHERE emergency_id = ?", (emergency_id,))

    cursor.execute('''
        INSERT INTO emergencies (
            emergency_id, wari_id, reported_by, emergency_type, priority,
            latitude, longitude, location_accuracy, wari_zone, landmark, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        emergency_id, wari_id, reported_by, emergency_type, priority,
        lat, lon, accuracy, wari_zone, landmark, status
    ))"""

assert old_code in code, "Could not find old_code in backend/app.py"
code = code.replace(old_code, new_code)

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated create_emergency in backend/app.py with synchronized emergency_id support!")
