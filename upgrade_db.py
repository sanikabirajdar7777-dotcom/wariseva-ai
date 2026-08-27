with open('backend/app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Schema migration in init_db()
old_schema = """    cursor.execute("PRAGMA table_info(users)")
    user_cols = [col[1] for col in cursor.fetchall()]
    if 'latitude' not in user_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN latitude REAL")
    if 'longitude' not in user_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN longitude REAL")"""

new_schema = """    cursor.execute("PRAGMA table_info(users)")
    user_cols = [col[1] for col in cursor.fetchall()]
    if 'latitude' not in user_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN latitude REAL")
    if 'longitude' not in user_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN longitude REAL")
    if 'zone' not in user_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN zone TEXT")
    if 'skills' not in user_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN skills TEXT")
    if 'certification' not in user_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN certification TEXT")
    if 'verification_status' not in user_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN verification_status TEXT DEFAULT 'VERIFIED'")
    if 'organization' not in user_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN organization TEXT")
    if 'languages' not in user_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN languages TEXT DEFAULT 'Marathi, Hindi, English'")"""

assert old_schema in code, "Could not find old_schema in backend/app.py"
code = code.replace(old_schema, new_schema)

# 2. Update emergencies schema
old_em_schema = """    if 'assigned_hospital' not in em_cols:
        cursor.execute("ALTER TABLE emergencies ADD COLUMN assigned_hospital TEXT")"""

new_em_schema = """    if 'assigned_hospital' not in em_cols:
        cursor.execute("ALTER TABLE emergencies ADD COLUMN assigned_hospital TEXT")
    if 'severity' not in em_cols:
        cursor.execute("ALTER TABLE emergencies ADD COLUMN severity TEXT DEFAULT 'CRITICAL'")
    if 'notes' not in em_cols:
        cursor.execute("ALTER TABLE emergencies ADD COLUMN notes TEXT")
    if 'is_unregistered_pilgrim' not in em_cols:
        cursor.execute("ALTER TABLE emergencies ADD COLUMN is_unregistered_pilgrim INTEGER DEFAULT 0")"""

assert old_em_schema in code, "Could not find old_em_schema in backend/app.py"
code = code.replace(old_em_schema, new_em_schema)

# 3. Update seed_demo_data
old_seed = """def seed_demo_data(cursor):
    \"\"\"Seed prototype demo volunteers, medical camps, and medical responders.\"\"\"
    demo_volunteers = [
        ("V-001", "Ramesh Kulkarni", "9820011111", "VOLUNTEER", 18.3450, 74.0315, 1, "AVAILABLE"),
        ("V-002", "Anjali Deshmukh", "9820022222", "VOLUNTEER", 18.3490, 74.0360, 1, "AVAILABLE"),
        ("V-003", "Sachin More", "9820033333", "VOLUNTEER", 18.3440, 74.0300, 1, "AVAILABLE"),
        ("V-004", "Pooja Gaikwad", "9820044444", "VOLUNTEER", 18.5320, 73.8450, 1, "AVAILABLE"),
        ("V-005", "Mahesh Jadhav", "9820055555", "VOLUNTEER", 17.6780, 75.3250, 1, "AVAILABLE")
    ]

    for vol in demo_volunteers:
        cursor.execute("SELECT 1 FROM users WHERE wari_id = ?", (vol[0],))
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO users (wari_id, name, phone, role, latitude, longitude, location_enabled, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', vol)"""

new_seed = """def seed_demo_data(cursor):
    \"\"\"Seed prototype demo volunteers, medical camps, and medical responders with rich attributes for AI scoring.\"\"\"
    # Prototype volunteers with varied skills, certifications, zones, and proximity for AI matching demonstration
    demo_volunteers = [
        ("V-001", "Ramesh Kulkarni", "9820011111", "VOLUNTEER", 18.3460, 74.0288, 1, "AVAILABLE", "Zone 04 — Saswad Palkhi Maidan", "First Aid, CPR, Crowd Assistance", "First Aid Certified", "VERIFIED", "Warkari Mitra Mandal", "Marathi, Hindi, English"),
        ("V-002", "Suresh Patil", "9820022222", "VOLUNTEER", 18.3452, 74.0312, 1, "AVAILABLE", "Zone 04 — Saswad Palkhi Maidan", "Crowd Guidance, Water Distribution", "None", "VERIFIED", "Dindi Seva Dal", "Marathi, Hindi"),
        ("V-003", "Aniket Deshmukh", "9820033333", "VOLUNTEER", 18.3510, 74.0380, 1, "AVAILABLE", "Zone 05 — Jejuri Mandir Tappa", "First Aid, Basic Triage", "First Aid Certified", "VERIFIED", "Youth Seva Trust", "Marathi, Hindi, English"),
        ("V-004", "Priya Joshi", "9820044444", "VOLUNTEER", 18.3440, 74.0300, 1, "RESPONDING", "Zone 04 — Saswad Palkhi Maidan", "Paramedic Support, First Aid", "Certified Medical Nurse", "VERIFIED", "Aarogya Seva Network", "Marathi, Hindi, English"),
        ("V-005", "Deepak Shinde", "9820055555", "VOLUNTEER", 18.3380, 74.0240, 1, "AVAILABLE", "Zone 03 — Hadapsar / Dive Ghat Base", "General Support, Crowd Marshall", "None", "VERIFIED", "Swayamsevak Sangh", "Marathi"),
        ("V-006", "Kavita Rane", "9820066666", "VOLUNTEER", 18.3475, 74.0325, 1, "AVAILABLE", "Zone 04 — Saswad Palkhi Maidan", "Elderly Assistance, First Aid", "First Aid Certified", "VERIFIED", "St. John Ambulance Volunteer", "Marathi, Hindi, English")
    ]

    for vol in demo_volunteers:
        cursor.execute("SELECT 1 FROM users WHERE wari_id = ?", (vol[0],))
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO users (wari_id, name, phone, role, latitude, longitude, location_enabled, status, zone, skills, certification, verification_status, organization, languages)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', vol)
        else:
            cursor.execute('''
                UPDATE users SET 
                    name = ?, phone = ?, role = ?, latitude = ?, longitude = ?, location_enabled = ?,
                    status = ?, zone = ?, skills = ?, certification = ?, verification_status = ?, organization = ?, languages = ?
                WHERE wari_id = ?
            ''', (vol[1], vol[2], vol[3], vol[4], vol[5], vol[6], vol[7], vol[8], vol[9], vol[10], vol[11], vol[12], vol[13], vol[0]))"""

assert old_seed in code, "Could not find old_seed in backend/app.py"
code = code.replace(old_seed, new_seed)

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated backend/app.py database schema and seed data!")
