with open('backend/app.py', 'r', encoding='utf-8') as f:
    code = f.read()

target = """    # Delete previous instance of EM-28471 if any
    cursor.execute("DELETE FROM emergencies WHERE emergency_id = ?", (em_id,))
    cursor.execute("DELETE FROM notifications WHERE emergency_id = ?", (em_id,))
    cursor.execute("DELETE FROM location_updates WHERE emergency_id = ?", (em_id,))"""

replacement = """    # Delete previous instance of EM-28471 if any
    cursor.execute("DELETE FROM emergencies WHERE emergency_id = ?", (em_id,))
    cursor.execute("DELETE FROM notifications WHERE emergency_id = ?", (em_id,))
    cursor.execute("DELETE FROM location_updates WHERE emergency_id = ?", (em_id,))
    
    # Ensure V-004 is marked RESPONDING (engaged) and V-001 is AVAILABLE for prototype demo
    cursor.execute("UPDATE users SET status = 'RESPONDING' WHERE wari_id = 'V-004'")
    cursor.execute("UPDATE users SET status = 'AVAILABLE' WHERE wari_id = 'V-001'")"""

assert target in code, "Could not find target in backend/app.py"
code = code.replace(target, replacement)

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated demo_create_emergency in backend/app.py!")
