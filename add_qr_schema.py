import re

with open('backend/app.py', 'r', encoding='utf-8') as f:
    app_code = f.read()

# 1. Add werkzeug security import if needed
if 'from werkzeug.security import generate_password_hash, check_password_hash' not in app_code:
    app_code = "from werkzeug.security import generate_password_hash, check_password_hash\n" + app_code

# 2. Add pilgrims and access_logs tables to init_db
old_tables_marker = """    # 6. Companion / Group Members table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS group_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wari_id TEXT NOT NULL,
            member_name TEXT NOT NULL,
            member_phone TEXT NOT NULL,
            relationship TEXT DEFAULT 'Family',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')"""

new_tables = """    # 6. Companion / Group Members table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS group_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wari_id TEXT NOT NULL,
            member_name TEXT NOT NULL,
            member_phone TEXT NOT NULL,
            relationship TEXT DEFAULT 'Family',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 7. Pilgrims Table (WariSeva QR Identity & Protected Medical Profiles)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pilgrims (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wari_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            dindi TEXT DEFAULT '27',
            blood_group TEXT DEFAULT 'B+',
            emergency_contact TEXT DEFAULT '+91 98221 28542',
            medical_alert TEXT DEFAULT '⚠️ Asthma (Requires Inhaler Support)',
            pin_hash TEXT NOT NULL,
            status TEXT DEFAULT 'REGISTERED',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 8. Access Logs Table (Audited Emergency Identity Access)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS access_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            volunteer_id TEXT NOT NULL,
            volunteer_name TEXT NOT NULL,
            pilgrim_id TEXT NOT NULL,
            reason TEXT DEFAULT 'Emergency Assistance',
            status TEXT DEFAULT 'AUTHORIZED',
            access_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')"""

assert old_tables_marker in app_code, "Could not find group_members table marker in app.py"
app_code = app_code.replace(old_tables_marker, new_tables)

# 3. Seed demo pilgrim in seed_demo_data
seed_marker = """    for resp in demo_responders:
        cursor.execute("SELECT 1 FROM users WHERE wari_id = ?", (resp[0],))
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO users (wari_id, name, phone, role, latitude, longitude, location_enabled, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', resp)"""

seed_pilgrim_code = """    for resp in demo_responders:
        cursor.execute("SELECT 1 FROM users WHERE wari_id = ?", (resp[0],))
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO users (wari_id, name, phone, role, latitude, longitude, location_enabled, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', resp)

    # Seed Demo Pilgrim Tukaram Shinde with hashed PIN '2741'
    demo_pin_hash = generate_password_hash('2741')
    cursor.execute("SELECT 1 FROM pilgrims WHERE wari_id = 'WS-28471'")
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO pilgrims (wari_id, name, dindi, blood_group, emergency_contact, medical_alert, pin_hash, status)
            VALUES ('WS-28471', 'Tukaram Shinde', '27', 'B+', '+91 98221 28542', '⚠️ Asthma (Requires Inhaler Support)', ?, 'REGISTERED')
        ''', (demo_pin_hash,))
    else:
        cursor.execute('''
            UPDATE pilgrims SET name = 'Tukaram Shinde', dindi = '27', blood_group = 'B+', emergency_contact = '+91 98221 28542',
                               medical_alert = '⚠️ Asthma (Requires Inhaler Support)', pin_hash = ?, status = 'REGISTERED'
            WHERE wari_id = 'WS-28471'
        ''', (demo_pin_hash,))"""

assert seed_marker in app_code, "Could not find seed_marker in app.py"
app_code = app_code.replace(seed_marker, seed_pilgrim_code)

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(app_code)

print("Updated backend/app.py with pilgrims and access_logs tables & seeded demo pilgrim!")
