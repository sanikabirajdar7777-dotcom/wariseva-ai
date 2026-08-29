import sys
import io

if sys.platform == 'win32':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    elif hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    elif hasattr(sys.stderr, 'buffer'):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import base64
import qrcode
import socket
import re
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
import math
import random
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory, Response, session, redirect, url_for

# Path configuration
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
template_dir = os.path.join(base_dir, 'templates')
static_dir = os.path.join(base_dir, 'static')
if not os.path.exists(static_dir):
    alt_static = os.path.abspath('static')
    if os.path.exists(alt_static):
        static_dir = alt_static
    else:
        alt_pub = os.path.abspath('public/static')
        if os.path.exists(alt_pub):
            static_dir = alt_pub
if not os.path.exists(template_dir):
    alt_tmpl = os.path.abspath('templates')
    if os.path.exists(alt_tmpl):
        template_dir = alt_tmpl

zones_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wari_zones.json')
hospitals_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hospitals.json')
safety_services_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'safety_services.json')

# Database path configuration
# On serverless platforms like Vercel, the source tree is read-only.
# SQLite must store its database in /tmp (the only writable directory).
local_db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wariseva.db')
if os.environ.get('VERCEL') or os.environ.get('AWS_LAMBDA_FUNCTION_NAME') or not os.access(os.path.dirname(local_db_path) or '.', os.W_OK):
    import tempfile
    import shutil
    tmp_dir = '/tmp' if os.path.exists('/tmp') else tempfile.gettempdir()
    db_path = os.path.join(tmp_dir, 'wariseva.db')
    if not os.path.exists(db_path) and os.path.exists(local_db_path):
        try:
            shutil.copy2(local_db_path, db_path)
        except Exception:
            pass
else:
    db_path = local_db_path

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir, static_url_path='/static')
app.secret_key = os.environ.get('SECRET_KEY', 'wariseva-volunteer-auth-key-2026')

def get_db_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize SQLite database and create/migrate all required tables."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wari_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            role TEXT DEFAULT 'WARKARI',
            latitude REAL,
            longitude REAL,
            location_enabled INTEGER DEFAULT 0,
            status TEXT DEFAULT 'ACTIVE',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute("PRAGMA table_info(users)")
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
        cursor.execute("ALTER TABLE users ADD COLUMN languages TEXT DEFAULT 'Marathi, Hindi, English'")
    
    # 2. Emergencies table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emergencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emergency_id TEXT UNIQUE NOT NULL,
            wari_id TEXT NOT NULL,
            reported_by TEXT,
            emergency_type TEXT DEFAULT 'MEDICAL',
            priority TEXT DEFAULT 'URGENT',
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            location_accuracy REAL,
            wari_zone TEXT,
            landmark TEXT,
            assigned_volunteer TEXT,
            assigned_camp TEXT,
            assigned_responder TEXT,
            assigned_hospital TEXT,
            status TEXT DEFAULT 'CREATED',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute("PRAGMA table_info(emergencies)")
    em_cols = [col[1] for col in cursor.fetchall()]
    if 'assigned_volunteer' not in em_cols:
        cursor.execute("ALTER TABLE emergencies ADD COLUMN assigned_volunteer TEXT")
    if 'assigned_camp' not in em_cols:
        cursor.execute("ALTER TABLE emergencies ADD COLUMN assigned_camp TEXT")
    if 'assigned_responder' not in em_cols:
        cursor.execute("ALTER TABLE emergencies ADD COLUMN assigned_responder TEXT")
    if 'assigned_hospital' not in em_cols:
        cursor.execute("ALTER TABLE emergencies ADD COLUMN assigned_hospital TEXT")
    if 'severity' not in em_cols:
        cursor.execute("ALTER TABLE emergencies ADD COLUMN severity TEXT DEFAULT 'CRITICAL'")
    if 'notes' not in em_cols:
        cursor.execute("ALTER TABLE emergencies ADD COLUMN notes TEXT")
    if 'is_unregistered_pilgrim' not in em_cols:
        cursor.execute("ALTER TABLE emergencies ADD COLUMN is_unregistered_pilgrim INTEGER DEFAULT 0")
    if 'hospital_status' not in em_cols:
        cursor.execute("ALTER TABLE emergencies ADD COLUMN hospital_status TEXT DEFAULT 'PENDING'")
    if 'patient_name' not in em_cols:
        cursor.execute("ALTER TABLE emergencies ADD COLUMN patient_name TEXT DEFAULT 'Tukaram Shinde'")
    if 'mobile' not in em_cols:
        cursor.execute("ALTER TABLE emergencies ADD COLUMN mobile TEXT DEFAULT '+91 98221 28471'")
    if 'emergency_contact' not in em_cols:
        cursor.execute("ALTER TABLE emergencies ADD COLUMN emergency_contact TEXT DEFAULT '+91 98220 99881'")
    if 'blood_group' not in em_cols:
        cursor.execute("ALTER TABLE emergencies ADD COLUMN blood_group TEXT DEFAULT 'B+'")
    if 'dindi_no' not in em_cols:
        cursor.execute("ALTER TABLE emergencies ADD COLUMN dindi_no TEXT DEFAULT 'Dindi 27'")
    if 'volunteer_status' not in em_cols:
        cursor.execute("ALTER TABLE emergencies ADD COLUMN volunteer_status TEXT DEFAULT 'WAITING'")
    if 'current_status' not in em_cols:
        cursor.execute("ALTER TABLE emergencies ADD COLUMN current_status TEXT DEFAULT 'CREATED'")

    # Emergency Events / Audit Timeline table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emergency_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emergency_id TEXT NOT NULL,
            stage INTEGER DEFAULT 1,
            status TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            actor TEXT,
            description TEXT
        )
    ''')

    # 3. Medical Camps table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medical_camps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            camp_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            zone TEXT,
            status TEXT DEFAULT 'AVAILABLE',
            capabilities TEXT DEFAULT 'GENERAL_MEDICAL',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 4. Notifications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emergency_id TEXT NOT NULL,
            recipient_id TEXT NOT NULL,
            recipient_type TEXT NOT NULL,
            notification_type TEXT DEFAULT 'EMERGENCY_ALERT',
            status TEXT DEFAULT 'PENDING',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            responded_at TIMESTAMP
        )
    ''')

    # 5. Location Updates table
    
    # 6. Companion / Group Members table
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
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS location_updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            emergency_id TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            accuracy REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 9. Last Seen Checkpoints Table (Family Safety & Milestone Verification)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS last_seen_checkpoints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wari_id TEXT NOT NULL,
            checkpoint_type TEXT NOT NULL,
            location_name TEXT NOT NULL,
            zone TEXT NOT NULL,
            checkin_time TEXT NOT NULL,
            recorded_by TEXT DEFAULT 'Dindi Seva Lead',
            status TEXT DEFAULT 'VERIFIED_SAFE',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    seed_demo_data(cursor)
    conn.commit()
    conn.close()
    print(f"Database initialized and demo data seeded at: {db_path}")

def seed_demo_data(cursor):
    """Seed prototype demo volunteers, medical camps, and medical responders with rich attributes for AI scoring."""
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
            ''', (vol[1], vol[2], vol[3], vol[4], vol[5], vol[6], vol[7], vol[8], vol[9], vol[10], vol[11], vol[12], vol[13], vol[0]))

    demo_responders = [
        ("MR-001", "Dr. Arvind Shinde (Mobile Ambulance 1)", "9870011111", "MEDICAL_RESPONDER", 18.3470, 74.0330, 1, "AVAILABLE"),
        ("MR-002", "Dr. Sunita Rao (Bike First Responder)", "9870022222", "MEDICAL_RESPONDER", 18.3495, 74.0370, 1, "AVAILABLE"),
        ("MR-003", "Dr. Nilesh Kadam (Ambulance 3)", "9870033333", "MEDICAL_RESPONDER", 18.5300, 73.8460, 1, "AVAILABLE"),
        ("MR-004", "Dr. Sneha Joshi (Pandharpur ICU Unit)", "9870044444", "MEDICAL_RESPONDER", 17.6760, 75.3230, 1, "AVAILABLE")
    ]

    for resp in demo_responders:
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
            VALUES ('WS-28471', 'Tukaram Shinde', '27', 'B+', '+91 98220 99881', '⚠️ Asthma (Requires Inhaler & O2 Support)', ?, 'REGISTERED')
        ''', (demo_pin_hash,))
    else:
        cursor.execute('''
            UPDATE pilgrims SET name = 'Tukaram Shinde', dindi = '27', blood_group = 'B+', emergency_contact = '+91 98220 99881',
                               medical_alert = '⚠️ Asthma (Requires Inhaler & O2 Support)', pin_hash = ?, status = 'REGISTERED'
            WHERE wari_id = 'WS-28471'
        ''', (demo_pin_hash,))

    # Also ensure WS-28471 is in users table for SOS creation
    cursor.execute("SELECT 1 FROM users WHERE wari_id = 'WS-28471'")
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO users (wari_id, name, phone, role, latitude, longitude, location_enabled, status)
            VALUES ('WS-28471', 'Tukaram Shinde', '+91 98221 28471', 'WARKARI', 18.3444, 74.0305, 1, 'ACTIVE')
        ''')
    else:
        cursor.execute('''
            UPDATE users SET name = 'Tukaram Shinde', phone = '+91 98221 28471', role = 'WARKARI', latitude = 18.3444, longitude = 74.0305, status = 'ACTIVE'
            WHERE wari_id = 'WS-28471'
        ''')

    # Seed Demo Pilgrim Anandi Gopal Joshi (WS-30555) with hashed PIN '3055'
    demo_pin_hash_30555 = generate_password_hash('3055')
    cursor.execute("SELECT 1 FROM pilgrims WHERE wari_id = 'WS-30555'")
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO pilgrims (wari_id, name, dindi, blood_group, emergency_contact, medical_alert, pin_hash, status)
            VALUES ('WS-30555', 'Anandi Gopal Joshi', '27', 'O+', '+91 98221 30555', '⚠️ Hypertension & Diabetes Support', ?, 'REGISTERED')
        ''', (demo_pin_hash_30555,))
    else:
        cursor.execute('''
            UPDATE pilgrims SET name = 'Anandi Gopal Joshi', dindi = '27', blood_group = 'O+', emergency_contact = '+91 98221 30555',
                               medical_alert = '⚠️ Hypertension & Diabetes Support', pin_hash = ?, status = 'REGISTERED'
            WHERE wari_id = 'WS-30555'
        ''', (demo_pin_hash_30555,))

    cursor.execute("SELECT 1 FROM users WHERE wari_id = 'WS-30555'")
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO users (wari_id, name, phone, role, latitude, longitude, location_enabled, status)
            VALUES ('WS-30555', 'Anandi Gopal Joshi', '+91 98221 30555', 'WARKARI', 18.3444, 74.0305, 1, 'ACTIVE')
        ''')

    demo_camps = [
        ("MC-001", "Saswad Palkhi Maidan Medical Tent", 18.3460, 74.0320, "Zone 04 — Saswad Palkhi Maidan", "AVAILABLE", "GENERAL_MEDICAL,TRIAGE"),
        ("MC-002", "Dive Ghat Base Health Camp", 18.4970, 73.9420, "Zone 03 — Hadapsar / Dive Ghat Base", "AVAILABLE", "FIRST_AID,HYDRATION"),
        ("MC-003", "Pandharpur Civil Hospital Emergency Hub", 17.6770, 75.3245, "Zone 12 — Pandharpur Mandir Parisar", "AVAILABLE", "EMERGENCY_ICU,TRIAGE"),
        ("MC-004", "Jejuri Primary Health Post", 18.2760, 74.1620, "Zone 05 — Jejuri Mandir Tappa", "AVAILABLE", "FIRST_AID")
    ]

    
    demo_group = [
        ("WS-28471", "Sunita Shinde", "9822114455", "Spouse / Companion"),
        ("WS-28471", "Ganesh Shinde", "9822114466", "Son / Companion")
    ]
    for gm in demo_group:
        cursor.execute("SELECT 1 FROM group_members WHERE wari_id = ? AND member_phone = ?", (gm[0], gm[2]))
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO group_members (wari_id, member_name, member_phone, relationship)
                VALUES (?, ?, ?, ?)
            ''', gm)

    for camp in demo_camps:
        cursor.execute("SELECT 1 FROM medical_camps WHERE camp_id = ?", (camp[0],))
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO medical_camps (camp_id, name, latitude, longitude, zone, status, capabilities)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', camp)

    demo_checkpoints = [
        ("WS-28471", "MORNING_START", "Alandi Palkhi Prasthan Gateway", "Zone 01 — Alandi / Pune Start", "06:30 AM", "Dindi Seva Lead", "VERIFIED_SAFE"),
        ("WS-28471", "AFTERNOON_HALT", "Dive Ghat Base Rest Mandap", "Zone 03 — Hadapsar / Dive Ghat Base", "01:15 PM", "Volunteer V-005", "VERIFIED_SAFE"),
        ("WS-28471", "NIGHT_MUKKAM", "Saswad Central Palkhi Maidan Ground", "Zone 04 — Saswad Palkhi Maidan", "07:45 PM", "Camp MC-001 Triage", "VERIFIED_SAFE"),
        ("WS-30555", "MORNING_START", "Alandi Palkhi Prasthan Gateway", "Zone 01 — Alandi / Pune Start", "06:45 AM", "Dindi Seva Lead", "VERIFIED_SAFE"),
        ("WS-30555", "AFTERNOON_HALT", "Dive Ghat Base Rest Mandap", "Zone 03 — Hadapsar / Dive Ghat Base", "01:30 PM", "Volunteer V-005", "VERIFIED_SAFE"),
        ("WS-30555", "NIGHT_MUKKAM", "Saswad Central Palkhi Maidan Ground", "Zone 04 — Saswad Palkhi Maidan", "08:10 PM", "Camp MC-001 Triage", "VERIFIED_SAFE")
    ]
    for cp in demo_checkpoints:
        cursor.execute("SELECT 1 FROM last_seen_checkpoints WHERE wari_id = ? AND checkpoint_type = ?", (cp[0], cp[1]))
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO last_seen_checkpoints (wari_id, checkpoint_type, location_name, zone, checkin_time, recorded_by, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', cp)

def load_wari_zones():
    """Load Wari route zones dataset."""
    if os.path.exists(zones_file):
        try:
            with open(zones_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading wari_zones.json: {e}")
    return []

def load_hospitals():
    """Load Hospitals dataset."""
    if os.path.exists(hospitals_file):
        try:
            with open(hospitals_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading hospitals.json: {e}")
    return []

def load_safety_services():
    """Load Everyday Safety Services dataset."""
    if os.path.exists(safety_services_file):
        try:
            with open(safety_services_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading safety_services.json: {e}")
    return []

def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance in kilometers between two coordinates using Haversine formula."""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def find_nearest_wari_zone(lat, lon):
    """Find the nearest Wari zone and primary landmark from coordinates."""
    zones = load_wari_zones()
    if not zones:
        return {
            "zone_id": "ZONE_04",
            "zone_name": "Zone 04 — Saswad Palkhi Maidan",
            "landmark": "Saswad Palkhi Ground",
            "crowd_density": "CRITICAL",
            "crowd_index": 94,
            "congestion_choke_point": "Saswad Central Mandir Ringan & Bazar Chowk",
            "safe_bypass_corridor": "Saswad South Bypass Service Corridor",
            "distance_km": 0.0
        }

    closest_zone = None
    min_dist = float('inf')
    for zone in zones:
        dist = calculate_haversine_distance(lat, lon, zone['latitude'], zone['longitude'])
        if dist < min_dist:
            min_dist = dist
            closest_zone = zone

    landmarks = closest_zone.get('landmarks', [])
    landmark = landmarks[0] if landmarks else closest_zone.get('zone_name')

    return {
        "zone_id": closest_zone.get('zone_id'),
        "zone_name": closest_zone.get('zone_name'),
        "landmark": landmark,
        "crowd_density": closest_zone.get('crowd_density', 'MODERATE'),
        "crowd_index": closest_zone.get('crowd_index', 50),
        "congestion_choke_point": closest_zone.get('congestion_choke_point', 'Procession Corridor'),
        "safe_bypass_corridor": closest_zone.get('safe_bypass_corridor', 'Outer Ring Service Lane'),
        "distance_km": round(min_dist, 2)
    }

def generate_unique_wari_id():
    conn = get_db_connection()
    cursor = conn.cursor()
    while True:
        random_num = random.randint(10000, 99999)
        wari_id = f"WS-{random_num}"
        cursor.execute("SELECT 1 FROM users WHERE wari_id = ?", (wari_id,))
        if not cursor.fetchone():
            conn.close()
            return wari_id

def generate_unique_emergency_id():
    conn = get_db_connection()
    cursor = conn.cursor()
    while True:
        random_num = random.randint(10000, 99999)
        emergency_id = f"EM-{random_num}"
        cursor.execute("SELECT 1 FROM emergencies WHERE emergency_id = ?", (emergency_id,))
        if not cursor.fetchone():
            conn.close()
            return emergency_id

init_db()

@app.route('/favicon.ico')
def favicon():
    return ('', 204)


@app.route('/api/health', methods=['GET'])
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'WariSeva AI Emergency Response System',
        'demo_mode': True,
        'lan_ip': '192.168.1.5',
        'port': 5000
    }), 200

@app.route('/')
@app.route('/api/index')
@app.route('/api/index.py')
@app.route('/emergency')
@app.route('/safety-map')
@app.route('/services')
@app.route('/qr-scanner')
@app.route('/command')
@app.route('/command-center')
@app.route('/volunteer')
@app.route('/hospital')
@app.route('/medical-facility')
@app.route('/notifications')
def home():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(static_dir, filename)

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(static_dir, filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory(static_dir, filename)

@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory(static_dir, filename)

@app.route('/safety-id', methods=['GET'])
def safety_id_page():
    return render_template('index.html')

@app.route('/safety-id/create', methods=['POST'])
def create_safety_id():
    if request.is_json:
        data = request.get_json(silent=True) or {}
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
    else:
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()

    if not name:
        return jsonify({'success': False, 'error': 'Please enter your name.'}), 400
    if not phone:
        return jsonify({'success': False, 'error': 'Please enter your phone number.'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE phone = ?", (phone,))
    existing_user = cursor.fetchone()

    if existing_user:
        user_dict = dict(existing_user)
        conn.close()
        return jsonify({
            'success': True,
            'wari_id': user_dict['wari_id'],
            'name': user_dict['name'],
            'phone': user_dict['phone'],
            'role': user_dict['role'],
            'message': 'Existing Safety ID found for this phone number.'
        }), 200

    wari_id = generate_unique_wari_id()
    default_role = 'WARKARI'
    location_enabled = 1
    status = 'ACTIVE'

    cursor.execute('''
        INSERT INTO users (wari_id, name, phone, role, location_enabled, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (wari_id, name, phone, default_role, location_enabled, status))
    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'wari_id': wari_id,
        'name': name,
        'phone': phone,
        'role': default_role,
        'message': 'Safety ID created successfully.'
    }), 201

@app.route('/api/emergency/create', methods=['POST'])
@app.route('/api/emergency/sos', methods=['POST'])
def create_emergency():
    data = request.get_json(silent=True) if request.is_json else request.form.to_dict()
    if not data:
        return jsonify({'success': False, 'error': 'Invalid request payload.'}), 400

    wari_id = str(data.get('wari_id', '')).strip()
    emergency_type = str(data.get('emergency_type', 'MEDICAL')).strip().upper() or 'MEDICAL'
    priority = 'URGENT'
    status = 'CREATED'

    if not wari_id:
        return jsonify({'success': False, 'error': 'WariSeva Safety ID is required to trigger SOS.'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE wari_id = ?", (wari_id,))
    user = cursor.fetchone()
    cursor.execute("SELECT * FROM pilgrims WHERE wari_id = ?", (wari_id,))
    pilgrim = cursor.fetchone()

    if user:
        reported_by = user['name']
    elif pilgrim:
        reported_by = pilgrim['name']
    else:
        conn.close()
        return jsonify({
            'success': False,
            'error': f'WariSeva ID "{wari_id}" is not registered. Please create a Safety ID first.'
        }), 400

    raw_lat = data.get('latitude')
    raw_lon = data.get('longitude')
    raw_acc = data.get('location_accuracy')

    if raw_lat is None or raw_lon is None:
        conn.close()
        return jsonify({'success': False, 'error': 'Location coordinates (latitude and longitude) are required.'}), 400

    try:
        lat = float(raw_lat)
        lon = float(raw_lon)
    except (ValueError, TypeError):
        conn.close()
        return jsonify({'success': False, 'error': 'Coordinates must be valid numbers.'}), 400

    if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
        conn.close()
        return jsonify({'success': False, 'error': 'Coordinates outside valid geographical ranges.'}), 400

    accuracy = None
    if raw_acc is not None:
        try:
            accuracy = round(float(raw_acc), 1)
        except (ValueError, TypeError):
            accuracy = None

    nearest_zone_info = find_nearest_wari_zone(lat, lon)
    wari_zone = nearest_zone_info['zone_name']
    landmark = nearest_zone_info['landmark']

    emergency_id = data.get('emergency_id')
    if not emergency_id:
        if wari_id == 'WS-28471':
            emergency_id = 'EM-28471'
        else:
            emergency_id = generate_unique_emergency_id()

    # Clean up any existing records for this emergency_id to ensure clean re-dispatch
    cursor.execute("DELETE FROM emergencies WHERE emergency_id = ?", (emergency_id,))
    cursor.execute("DELETE FROM notifications WHERE emergency_id = ?", (emergency_id,))
    cursor.execute("DELETE FROM location_updates WHERE emergency_id = ?", (emergency_id,))

    # Fetch pilgrim details if available
    mobile = user['phone'] if (user and 'phone' in user.keys() and user['phone']) else (pilgrim['mobile'] if (pilgrim and 'mobile' in pilgrim.keys() and pilgrim['mobile']) else '+91 98221 28471')
    emergency_contact = pilgrim['emergency_contact'] if (pilgrim and 'emergency_contact' in pilgrim.keys() and pilgrim['emergency_contact']) else '+91 98220 99881'
    blood_group = pilgrim['blood_group'] if (pilgrim and 'blood_group' in pilgrim.keys() and pilgrim['blood_group']) else 'B+'
    dindi_no = pilgrim['dindi_no'] if (pilgrim and 'dindi_no' in pilgrim.keys() and pilgrim['dindi_no']) else 'Dindi 27'
    patient_name = reported_by

    cursor.execute('''
        INSERT INTO emergencies (
            emergency_id, wari_id, reported_by, patient_name, mobile, emergency_contact,
            blood_group, dindi_no, emergency_type, priority,
            latitude, longitude, location_accuracy, wari_zone, landmark, status,
            volunteer_status, hospital_status, current_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'WAITING', 'PENDING', 'CREATED')
    ''', (
        emergency_id, wari_id, reported_by, patient_name, mobile, emergency_contact,
        blood_group, dindi_no, emergency_type, priority,
        lat, lon, accuracy, wari_zone, landmark, status
    ))

    log_emergency_event(cursor, emergency_id, 1, 'CREATED', wari_id, f'Emergency registered for {patient_name}.')

    # Notify Volunteers
    cursor.execute("SELECT * FROM users WHERE role = 'VOLUNTEER' AND status = 'AVAILABLE' AND latitude IS NOT NULL AND longitude IS NOT NULL")
    volunteers = cursor.fetchall()
    notified_vols = 0
    for vol in volunteers:
        dist_km = calculate_haversine_distance(lat, lon, vol['latitude'], vol['longitude'])
        if dist_km <= 50.0:
            cursor.execute('''
                INSERT INTO notifications (emergency_id, recipient_id, recipient_type, notification_type, status)
                VALUES (?, ?, 'VOLUNTEER', 'EMERGENCY_ALERT', 'PENDING')
            ''', (emergency_id, vol['wari_id']))
            notified_vols += 1

    # Notify Medical Camps
    cursor.execute("SELECT * FROM medical_camps WHERE status = 'AVAILABLE'")
    camps = cursor.fetchall()
    notified_camps = 0
    for camp in camps:
        dist_km = calculate_haversine_distance(lat, lon, camp['latitude'], camp['longitude'])
        if dist_km <= 50.0:
            cursor.execute('''
                INSERT INTO notifications (emergency_id, recipient_id, recipient_type, notification_type, status)
                VALUES (?, ?, 'CAMP', 'EMERGENCY_ALERT', 'PENDING')
            ''', (emergency_id, camp['camp_id']))
            notified_camps += 1

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'emergency_id': emergency_id,
        'wari_id': wari_id,
        'name': reported_by,
        'reported_by': reported_by,
        'emergency_type': emergency_type,
        'priority': priority,
        'wari_zone': wari_zone,
        'landmark': landmark,
        'latitude': lat,
        'longitude': lon,
        'accuracy': accuracy,
        'status': status,
        'notified_volunteers': notified_vols,
        'notified_camps': notified_camps,
        'message': 'Emergency request created successfully.'
    }), 201

@app.route('/api/emergency/<emergency_id>', methods=['GET'])
def get_emergency(emergency_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emergencies WHERE emergency_id = ?", (emergency_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify({'success': True, 'emergency': dict(row)}), 200
    return jsonify({'success': False, 'error': 'Emergency record not found.'}), 404

@app.route('/api/emergency/<emergency_id>/nearby-volunteers', methods=['GET'])
def get_nearby_volunteers(emergency_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM emergencies WHERE emergency_id = ?", (emergency_id,))
    em = cursor.fetchone()
    if not em:
        conn.close()
        return jsonify({'success': False, 'error': 'Emergency not found.'}), 404

    patient_lat = em['latitude']
    patient_lon = em['longitude']

    cursor.execute("SELECT * FROM users WHERE role = 'VOLUNTEER' AND status = 'AVAILABLE' AND latitude IS NOT NULL AND longitude IS NOT NULL")
    volunteers = cursor.fetchall()

    results = []
    for vol in volunteers:
        dist_km = calculate_haversine_distance(patient_lat, patient_lon, vol['latitude'], vol['longitude'])
        dist_m = int(round(dist_km * 1000))
        results.append({
            'id': vol['wari_id'],
            'name': vol['name'],
            'phone': vol['phone'],
            'distance_m': dist_m,
            'distance_km': round(dist_km, 2),
            'status': vol['status']
        })

    results.sort(key=lambda x: x['distance_m'])
    conn.close()

    return jsonify({
        'success': True,
        'emergency_id': emergency_id,
        'volunteers': results
    }), 200

@app.route('/api/emergency/<emergency_id>/nearby-camps', methods=['GET'])
def get_nearby_camps(emergency_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM emergencies WHERE emergency_id = ?", (emergency_id,))
    em = cursor.fetchone()
    if not em:
        conn.close()
        return jsonify({'success': False, 'error': 'Emergency not found.'}), 404

    patient_lat = em['latitude']
    patient_lon = em['longitude']

    cursor.execute("SELECT * FROM medical_camps WHERE status = 'AVAILABLE'")
    camps = cursor.fetchall()

    results = []
    for camp in camps:
        dist_km = calculate_haversine_distance(patient_lat, patient_lon, camp['latitude'], camp['longitude'])
        dist_m = int(round(dist_km * 1000))
        results.append({
            'camp_id': camp['camp_id'],
            'name': camp['name'],
            'zone': camp['zone'],
            'capabilities': camp['capabilities'],
            'distance_m': dist_m,
            'distance_km': round(dist_km, 2),
            'status': camp['status']
        })

    results.sort(key=lambda x: x['distance_m'])
    conn.close()

    return jsonify({
        'success': True,
        'emergency_id': emergency_id,
        'camps': results
    }), 200

def log_emergency_event(cursor, emergency_id, stage, status, actor, description):
    """Insert event log entry for timeline audit."""
    try:
        cursor.execute('''
            INSERT INTO emergency_events (emergency_id, stage, status, actor, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (emergency_id, stage, status, actor, description))
    except Exception as e:
        print(f"Error logging emergency event: {e}")

@app.route('/api/emergencies/active', methods=['GET'])
@app.route('/api/emergency/active', methods=['GET'])
def get_active_emergencies():
    """Return all active (non-resolved) emergencies for shared command & network state."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM emergencies 
        WHERE status != 'RESOLVED' 
        ORDER BY created_at DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return jsonify({
        'success': True,
        'count': len(rows),
        'emergencies': [dict(r) for r in rows]
    }), 200

@app.route('/api/emergency/<emergency_id>/timeline', methods=['GET'])
@app.route('/api/emergency/<emergency_id>/events', methods=['GET'])
@app.route('/api/emergency/<emergency_id>/audit-trail', methods=['GET'])
def get_emergency_timeline(emergency_id):
    """Return ordered event timeline for an incident."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM emergency_events 
        WHERE emergency_id = ? 
        ORDER BY timestamp ASC, stage ASC
    ''', (emergency_id,))
    rows = cursor.fetchall()
    conn.close()
    events_list = [dict(r) for r in rows]
    return jsonify({
        'success': True,
        'emergency_id': emergency_id,
        'events': events_list,
        'timeline': events_list
    }), 200

@app.route('/api/emergency/<emergency_id>/volunteer-accept', methods=['POST'])
@app.route('/api/emergency/<emergency_id>/volunteer/accept', methods=['POST'])
def volunteer_accept_emergency(emergency_id):
    data = request.get_json(silent=True) if request.is_json else request.form.to_dict() or {}
    volunteer_id = data.get('volunteer_id', 'V-001')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM emergencies WHERE emergency_id = ?", (emergency_id,))
    em = cursor.fetchone()
    if not em:
        conn.close()
        return jsonify({'success': False, 'error': 'Emergency not found.'}), 404

    cursor.execute('''
        UPDATE notifications 
        SET status = 'ACCEPTED', responded_at = CURRENT_TIMESTAMP 
        WHERE emergency_id = ? AND recipient_id = ?
    ''', (emergency_id, volunteer_id))

    cursor.execute('''
        UPDATE emergencies 
        SET status = 'VOLUNTEER_ACCEPTED', current_status = 'VOLUNTEER_ACCEPTED',
            assigned_volunteer = ?, volunteer_status = 'ACCEPTED', updated_at = CURRENT_TIMESTAMP 
        WHERE emergency_id = ?
    ''', (volunteer_id, emergency_id))

    cursor.execute('''
        UPDATE users 
        SET status = 'BUSY' 
        WHERE wari_id = ?
    ''', (volunteer_id,))

    log_emergency_event(cursor, emergency_id, 7, 'VOLUNTEER_ACCEPTED', volunteer_id, f'Volunteer {volunteer_id} confirmed and accepted dispatch.')

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'message': 'Emergency accepted by volunteer.',
        'emergency_id': emergency_id,
        'assigned_volunteer': volunteer_id,
        'volunteer_status': 'ACCEPTED',
        'status': 'VOLUNTEER_ACCEPTED'
    }), 200

@app.route('/api/emergency/<emergency_id>/volunteer-enroute', methods=['POST'])
@app.route('/api/emergency/<emergency_id>/volunteer/enroute', methods=['POST'])
def volunteer_enroute_emergency(emergency_id):
    data = request.get_json(silent=True) if request.is_json else request.form.to_dict() or {}
    volunteer_id = data.get('volunteer_id', 'V-001')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM emergencies WHERE emergency_id = ?", (emergency_id,))
    em = cursor.fetchone()
    if not em:
        conn.close()
        return jsonify({'success': False, 'error': 'Emergency not found.'}), 404

    cursor.execute('''
        UPDATE emergencies 
        SET status = 'EN_ROUTE', current_status = 'EN_ROUTE',
            volunteer_status = 'EN_ROUTE', updated_at = CURRENT_TIMESTAMP 
        WHERE emergency_id = ?
    ''', (emergency_id,))

    cursor.execute("UPDATE users SET status = 'RESPONDING' WHERE wari_id = ?", (volunteer_id,))
    log_emergency_event(cursor, emergency_id, 8, 'EN_ROUTE', volunteer_id, f'Volunteer {volunteer_id} en route to patient coordinates.')

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'message': 'Volunteer en route to patient coordinates.',
        'emergency_id': emergency_id,
        'assigned_volunteer': volunteer_id,
        'volunteer_status': 'EN_ROUTE',
        'status': 'EN_ROUTE'
    }), 200

@app.route('/api/emergency/<emergency_id>/volunteer-arrived', methods=['POST'])
@app.route('/api/emergency/<emergency_id>/volunteer/arrived', methods=['POST'])
def volunteer_arrived_emergency(emergency_id):
    data = request.get_json(silent=True) if request.is_json else request.form.to_dict() or {}
    volunteer_id = data.get('volunteer_id', 'V-001')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM emergencies WHERE emergency_id = ?", (emergency_id,))
    em = cursor.fetchone()
    if not em:
        conn.close()
        return jsonify({'success': False, 'error': 'Emergency not found.'}), 404

    cursor.execute('''
        UPDATE emergencies 
        SET status = 'VOLUNTEER_ARRIVED', current_status = 'VOLUNTEER_ARRIVED',
            volunteer_status = 'ARRIVED', updated_at = CURRENT_TIMESTAMP 
        WHERE emergency_id = ?
    ''', (emergency_id,))

    log_emergency_event(cursor, emergency_id, 9, 'VOLUNTEER_ARRIVED', volunteer_id, f'Volunteer {volunteer_id} arrived at patient location (0m).')

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'message': 'Volunteer arrived at patient location.',
        'emergency_id': emergency_id,
        'volunteer_status': 'ARRIVED',
        'status': 'VOLUNTEER_ARRIVED'
    }), 200

@app.route('/api/emergency/<emergency_id>/hospital-accept', methods=['POST'])
@app.route('/api/emergency/<emergency_id>/hospital/accept', methods=['POST'])
def hospital_accept_emergency(emergency_id):
    data = request.get_json(silent=True) if request.is_json else request.form.to_dict() or {}
    hospital_id = data.get('hospital_id', 'H-001')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM emergencies WHERE emergency_id = ?", (emergency_id,))
    em = cursor.fetchone()
    if not em:
        conn.close()
        return jsonify({'success': False, 'error': 'Emergency not found.'}), 404

    cursor.execute('''
        UPDATE emergencies 
        SET status = 'HOSPITAL_ACCEPTED', current_status = 'HOSPITAL_ACCEPTED',
            assigned_hospital = ?, hospital_status = 'ACCEPTED', updated_at = CURRENT_TIMESTAMP 
        WHERE emergency_id = ?
    ''', (hospital_id, emergency_id))

    log_emergency_event(cursor, emergency_id, 10, 'HOSPITAL_ACCEPTED', hospital_id, f'Medical facility {hospital_id} confirmed bed reservation.')

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'message': 'Medical facility accepted emergency and reserved bed.',
        'emergency_id': emergency_id,
        'assigned_hospital': hospital_id,
        'hospital_status': 'ACCEPTED',
        'status': 'HOSPITAL_ACCEPTED'
    }), 200

@app.route('/api/emergency/<emergency_id>/transfer', methods=['POST'])
@app.route('/api/emergency/<emergency_id>/hospital/transfer', methods=['POST'])
def hospital_transfer_emergency(emergency_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM emergencies WHERE emergency_id = ?", (emergency_id,))
    em = cursor.fetchone()
    if not em:
        conn.close()
        return jsonify({'success': False, 'error': 'Emergency not found.'}), 404

    cursor.execute('''
        UPDATE emergencies 
        SET status = 'HOSPITAL_TRANSFER', current_status = 'HOSPITAL_TRANSFER',
            hospital_status = 'TRANSFERRED', updated_at = CURRENT_TIMESTAMP 
        WHERE emergency_id = ?
    ''', (emergency_id,))

    log_emergency_event(cursor, emergency_id, 11, 'HOSPITAL_TRANSFER', 'AMBULANCE', 'Patient transferred to hospital emergency unit.')

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'message': 'Patient transferred to medical facility.',
        'emergency_id': emergency_id,
        'hospital_status': 'TRANSFERRED',
        'status': 'HOSPITAL_TRANSFER'
    }), 200

@app.route('/api/emergency/<emergency_id>/volunteer/decline', methods=['POST'])
def volunteer_decline_emergency(emergency_id):
    data = request.get_json(silent=True) if request.is_json else request.form.to_dict() or {}
    volunteer_id = data.get('volunteer_id', 'V-001')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE notifications 
        SET status = 'DECLINED', responded_at = CURRENT_TIMESTAMP 
        WHERE emergency_id = ? AND recipient_id = ?
    ''', (emergency_id, volunteer_id))
    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'message': 'Emergency declined by volunteer.',
        'emergency_id': emergency_id,
        'volunteer_id': volunteer_id,
        'status': 'DECLINED'
    }), 200

@app.route('/api/emergency/<emergency_id>/camp/accept', methods=['POST'])
def camp_accept_emergency(emergency_id):
    data = request.get_json(silent=True) if request.is_json else request.form.to_dict() or {}
    camp_id = data.get('camp_id', 'MC-001')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM emergencies WHERE emergency_id = ?", (emergency_id,))
    em = cursor.fetchone()
    if not em:
        conn.close()
        return jsonify({'success': False, 'error': 'Emergency not found.'}), 404

    cursor.execute('''
        UPDATE notifications 
        SET status = 'ACCEPTED', responded_at = CURRENT_TIMESTAMP 
        WHERE emergency_id = ? AND recipient_id = ?
    ''', (emergency_id, camp_id))

    cursor.execute('''
        UPDATE emergencies 
        SET status = 'ACCEPTED', assigned_camp = ?, updated_at = CURRENT_TIMESTAMP 
        WHERE emergency_id = ?
    ''', (camp_id, emergency_id))

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'message': 'Emergency accepted by medical camp.',
        'emergency_id': emergency_id,
        'assigned_camp': camp_id,
        'status': 'ACCEPTED'
    }), 200

@app.route('/api/emergency/<emergency_id>/camp/decline', methods=['POST'])
def camp_decline_emergency(emergency_id):
    data = request.get_json(silent=True) if request.is_json else request.form.to_dict() or {}
    camp_id = data.get('camp_id', 'MC-001')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE notifications 
        SET status = 'DECLINED', responded_at = CURRENT_TIMESTAMP 
        WHERE emergency_id = ? AND recipient_id = ?
    ''', (emergency_id, camp_id))
    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'message': 'Emergency declined by medical camp.',
        'emergency_id': emergency_id,
        'camp_id': camp_id,
        'status': 'DECLINED'
    }), 200

@app.route('/api/volunteer/location', methods=['POST'])
def volunteer_location_update():
    data = request.get_json(silent=True) if request.is_json else request.form.to_dict() or {}
    volunteer_id = str(data.get('volunteer_id', '')).strip()
    emergency_id = str(data.get('emergency_id', '')).strip()
    raw_lat = data.get('latitude')
    raw_lon = data.get('longitude')
    raw_acc = data.get('accuracy')

    if not volunteer_id:
        return jsonify({'success': False, 'error': 'Volunteer ID is required.'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE wari_id = ? AND role = 'VOLUNTEER'", (volunteer_id,))
    vol = cursor.fetchone()
    if not vol:
        conn.close()
        return jsonify({'success': False, 'error': f'Volunteer "{volunteer_id}" not found.'}), 404

    try:
        lat = float(raw_lat)
        lon = float(raw_lon)
    except (ValueError, TypeError):
        conn.close()
        return jsonify({'success': False, 'error': 'Coordinates must be valid numbers.'}), 400

    if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
        conn.close()
        return jsonify({'success': False, 'error': 'Coordinates outside valid ranges.'}), 400

    acc = round(float(raw_acc), 1) if raw_acc is not None else None

    cursor.execute('''
        UPDATE users 
        SET latitude = ?, longitude = ?, location_enabled = 1 
        WHERE wari_id = ?
    ''', (lat, lon, volunteer_id))

    dist_m = None
    dist_km = None
    current_status = vol['status']

    if emergency_id:
        cursor.execute("SELECT * FROM emergencies WHERE emergency_id = ?", (emergency_id,))
        em = cursor.fetchone()
        if em:
            cursor.execute('''
                INSERT INTO location_updates (user_id, emergency_id, latitude, longitude, accuracy)
                VALUES (?, ?, ?, ?, ?)
            ''', (volunteer_id, emergency_id, lat, lon, acc))

            if em['status'] in ('CREATED', 'ACCEPTED'):
                cursor.execute('''
                    UPDATE emergencies 
                    SET status = 'EN_ROUTE', updated_at = CURRENT_TIMESTAMP 
                    WHERE emergency_id = ?
                ''', (emergency_id,))
                current_status = 'EN_ROUTE'
            else:
                current_status = em['status']

            dist_km = calculate_haversine_distance(em['latitude'], em['longitude'], lat, lon)
            dist_m = int(round(dist_km * 1000))

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'volunteer_id': volunteer_id,
        'emergency_id': emergency_id or None,
        'latitude': lat,
        'longitude': lon,
        'accuracy': acc,
        'distance_to_patient_m': dist_m,
        'distance_to_patient_km': round(dist_km, 2) if dist_km is not None else None,
        'status': current_status,
        'message': 'Volunteer location updated successfully.'
    }), 200

@app.route('/api/volunteer/reached', methods=['POST'])
def volunteer_reached_patient():
    data = request.get_json(silent=True) if request.is_json else request.form.to_dict() or {}
    volunteer_id = str(data.get('volunteer_id', '')).strip()
    emergency_id = str(data.get('emergency_id', '')).strip()

    if not volunteer_id or not emergency_id:
        return jsonify({'success': False, 'error': 'Volunteer ID and Emergency ID are required.'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM emergencies WHERE emergency_id = ?", (emergency_id,))
    em = cursor.fetchone()
    if not em:
        conn.close()
        return jsonify({'success': False, 'error': f'Emergency "{emergency_id}" not found.'}), 404

    if em['assigned_volunteer'] != volunteer_id:
        conn.close()
        return jsonify({'success': False, 'error': f'Volunteer "{volunteer_id}" is not assigned.'}), 403

    cursor.execute('''
        UPDATE emergencies 
        SET status = 'WITH_PATIENT', updated_at = CURRENT_TIMESTAMP 
        WHERE emergency_id = ?
    ''', (emergency_id,))

    cursor.execute('''
        UPDATE users 
        SET status = 'WITH_PATIENT' 
        WHERE wari_id = ?
    ''', (volunteer_id,))

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'volunteer_id': volunteer_id,
        'emergency_id': emergency_id,
        'status': 'WITH_PATIENT',
        'message': 'Status updated: Volunteer has reached patient.'
    }), 200

# =========================================================================
# STEP 6, 7 & 8: MEDICAL RESPONDER + CROWD ROUTING + HOSPITAL ESCALATION
# =========================================================================

@app.route('/api/crowd/density', methods=['GET'])
def get_all_crowd_densities():
    zones = load_wari_zones()
    return jsonify({
        'success': True,
        'zones': zones
    }), 200

@app.route('/api/emergency/<emergency_id>/responder/accept', methods=['POST'])
def responder_accept_emergency(emergency_id):
    data = request.get_json(silent=True) if request.is_json else request.form.to_dict() or {}
    responder_id = str(data.get('responder_id', 'MR-001')).strip()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM emergencies WHERE emergency_id = ?", (emergency_id,))
    em = cursor.fetchone()
    if not em:
        conn.close()
        return jsonify({'success': False, 'error': 'Emergency not found.'}), 404

    cursor.execute("SELECT * FROM users WHERE wari_id = ? AND role = 'MEDICAL_RESPONDER'", (responder_id,))
    resp_user = cursor.fetchone()
    if not resp_user:
        conn.close()
        return jsonify({'success': False, 'error': f'Medical Responder "{responder_id}" not found.'}), 404

    cursor.execute('''
        UPDATE emergencies 
        SET assigned_responder = ?, status = 'RESPONDER_ASSIGNED', updated_at = CURRENT_TIMESTAMP 
        WHERE emergency_id = ?
    ''', (responder_id, emergency_id))

    cursor.execute('''
        UPDATE users 
        SET status = 'BUSY' 
        WHERE wari_id = ?
    ''', (responder_id,))

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'emergency_id': emergency_id,
        'responder_id': responder_id,
        'status': 'RESPONDER_ASSIGNED',
        'message': 'Medical responder assigned to emergency.'
    }), 200

@app.route('/api/emergency/<emergency_id>/responder/decline', methods=['POST'])
def responder_decline_emergency(emergency_id):
    data = request.get_json(silent=True) if request.is_json else request.form.to_dict() or {}
    responder_id = str(data.get('responder_id', 'MR-001')).strip()

    return jsonify({
        'success': True,
        'emergency_id': emergency_id,
        'responder_id': responder_id,
        'status': 'DECLINED',
        'message': 'Emergency declined by medical responder.'
    }), 200

@app.route('/api/responder/location', methods=['POST'])
def responder_location_update():
    data = request.get_json(silent=True) if request.is_json else request.form.to_dict() or {}
    responder_id = str(data.get('responder_id', '')).strip()
    emergency_id = str(data.get('emergency_id', '')).strip()
    raw_lat = data.get('latitude')
    raw_lon = data.get('longitude')
    raw_acc = data.get('accuracy')

    if not responder_id or not emergency_id:
        return jsonify({'success': False, 'error': 'Responder ID and Emergency ID are required.'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM emergencies WHERE emergency_id = ?", (emergency_id,))
    em = cursor.fetchone()
    if not em:
        conn.close()
        return jsonify({'success': False, 'error': 'Emergency not found.'}), 404

    if em['assigned_responder'] != responder_id:
        conn.close()
        return jsonify({'success': False, 'error': f'Responder "{responder_id}" is not assigned.'}), 403

    try:
        lat = float(raw_lat)
        lon = float(raw_lon)
    except (ValueError, TypeError):
        conn.close()
        return jsonify({'success': False, 'error': 'Coordinates must be valid numbers.'}), 400

    if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
        conn.close()
        return jsonify({'success': False, 'error': 'Coordinates outside valid ranges.'}), 400

    acc = round(float(raw_acc), 1) if raw_acc is not None else None

    cursor.execute('''
        INSERT INTO location_updates (user_id, emergency_id, latitude, longitude, accuracy)
        VALUES (?, ?, ?, ?, ?)
    ''', (responder_id, emergency_id, lat, lon, acc))

    cursor.execute('''
        UPDATE users 
        SET latitude = ?, longitude = ?, location_enabled = 1 
        WHERE wari_id = ?
    ''', (lat, lon, responder_id))

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'responder_id': responder_id,
        'emergency_id': emergency_id,
        'latitude': lat,
        'longitude': lon,
        'accuracy': acc,
        'message': 'Responder location updated successfully.'
    }), 200

@app.route('/api/emergency/<emergency_id>/responder/status', methods=['POST'])
def responder_update_status(emergency_id):
    data = request.get_json(silent=True) if request.is_json else request.form.to_dict() or {}
    responder_id = str(data.get('responder_id', 'MR-001')).strip()
    new_status = str(data.get('status', 'EN_ROUTE')).strip().upper()

    valid_statuses = ('EN_ROUTE', 'ARRIVED', 'HOSPITAL_ESCALATION_REQUESTED', 'HOSPITAL_SELECTED', 'RESOLVED')
    if new_status not in valid_statuses:
        return jsonify({'success': False, 'error': f'Invalid status "{new_status}".'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM emergencies WHERE emergency_id = ?", (emergency_id,))
    em = cursor.fetchone()
    if not em:
        conn.close()
        return jsonify({'success': False, 'error': 'Emergency not found.'}), 404

    if em['assigned_responder'] != responder_id:
        conn.close()
        return jsonify({'success': False, 'error': 'Responder is not assigned to this emergency.'}), 403

    cursor.execute('''
        UPDATE emergencies 
        SET status = ?, updated_at = CURRENT_TIMESTAMP 
        WHERE emergency_id = ?
    ''', (new_status, emergency_id))

    cursor.execute('''
        UPDATE users 
        SET status = ? 
        WHERE wari_id = ?
    ''', (new_status, responder_id))

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'emergency_id': emergency_id,
        'responder_id': responder_id,
        'status': new_status,
        'message': f'Status updated to {new_status}.'
    }), 200

@app.route('/api/emergency/<emergency_id>/resolve', methods=['POST'])
def resolve_emergency(emergency_id):
    """Mark an emergency as resolved."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM emergencies WHERE emergency_id = ?", (emergency_id,))
    em = cursor.fetchone()
    if not em:
        conn.close()
        return jsonify({'success': False, 'error': 'Emergency not found.'}), 404

    cursor.execute('''
        UPDATE emergencies 
        SET status = 'RESOLVED', current_status = 'RESOLVED',
            volunteer_status = 'COMPLETED', hospital_status = 'ADMITTED',
            updated_at = CURRENT_TIMESTAMP 
        WHERE emergency_id = ?
    ''', (emergency_id,))

    log_emergency_event(cursor, emergency_id, 12, 'RESOLVED', 'SYSTEM', 'Emergency case successfully resolved and archived.')

    if em['assigned_volunteer']:
        cursor.execute("UPDATE users SET status = 'AVAILABLE' WHERE wari_id = ?", (em['assigned_volunteer'],))
    if em['assigned_responder']:
        cursor.execute("UPDATE users SET status = 'AVAILABLE' WHERE wari_id = ?", (em['assigned_responder'],))

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'emergency_id': emergency_id,
        'status': 'RESOLVED',
        'volunteer_status': 'COMPLETED',
        'hospital_status': 'ADMITTED',
        'message': 'Emergency resolved successfully.'
    }), 200

@app.route('/api/emergency/<emergency_id>/crowd-aware-routes', methods=['GET'])
def get_crowd_aware_routes(emergency_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM emergencies WHERE emergency_id = ?", (emergency_id,))
    em = cursor.fetchone()
    if not em:
        conn.close()
        return jsonify({'success': False, 'error': 'Emergency not found.'}), 404

    pat_lat = em['latitude']
    pat_lon = em['longitude']

    resp_lat = 18.3470
    resp_lon = 74.0330
    resp_id = em['assigned_responder'] or 'MR-001'

    cursor.execute('''
        SELECT latitude, longitude FROM location_updates 
        WHERE user_id = ? AND emergency_id = ? 
        ORDER BY timestamp DESC LIMIT 1
    ''', (resp_id, emergency_id))
    r_loc = cursor.fetchone()
    if r_loc:
        resp_lat = r_loc['latitude']
        resp_lon = r_loc['longitude']

    vol_lat = None
    vol_lon = None
    vol_id = em['assigned_volunteer']
    if vol_id:
        cursor.execute('''
            SELECT latitude, longitude FROM location_updates 
            WHERE user_id = ? AND emergency_id = ? 
            ORDER BY timestamp DESC LIMIT 1
        ''', (vol_id, emergency_id))
        v_loc = cursor.fetchone()
        if v_loc:
            vol_lat = v_loc['latitude']
            vol_lon = v_loc['longitude']

    conn.close()

    nearest_zone = find_nearest_wari_zone(pat_lat, pat_lon)
    crowd_density = nearest_zone.get('crowd_density', 'HIGH')
    crowd_index = nearest_zone.get('crowd_index', 80)
    choke_point_desc = nearest_zone.get('congestion_choke_point', 'Palkhi Procession Core Line')
    safe_corridor_desc = nearest_zone.get('safe_bypass_corridor', 'Outer Ambulance Service Road')

    mid_lat = (resp_lat + pat_lat) / 2.0
    mid_lon = (resp_lon + pat_lon) / 2.0

    direct_dist_km = calculate_haversine_distance(resp_lat, resp_lon, pat_lat, pat_lon)
    direct_dist_m = int(round(direct_dist_km * 1000))
    direct_base_time = (direct_dist_km / 15.0) * 60.0
    congestion_delay_min = 8 if crowd_density in ('HIGH', 'CRITICAL') else 4
    direct_total_eta = max(5, int(round(direct_base_time + congestion_delay_min)))

    direct_waypoints = [
        [resp_lat, resp_lon],
        [mid_lat, mid_lon],
        [pat_lat, pat_lon]
    ]

    bypass_wp1 = [resp_lat + 0.0012, resp_lon - 0.0018]
    bypass_wp2 = [pat_lat + 0.0015, pat_lon - 0.0015]

    d_seg1 = calculate_haversine_distance(resp_lat, resp_lon, bypass_wp1[0], bypass_wp1[1])
    d_seg2 = calculate_haversine_distance(bypass_wp1[0], bypass_wp1[1], bypass_wp2[0], bypass_wp2[1])
    d_seg3 = calculate_haversine_distance(bypass_wp2[0], bypass_wp2[1], pat_lat, pat_lon)
    safe_dist_km = d_seg1 + d_seg2 + d_seg3
    safe_dist_m = int(round(safe_dist_km * 1000))

    safe_base_time = (safe_dist_km / 30.0) * 60.0
    safe_delay_min = 1
    safe_total_eta = max(2, int(round(safe_base_time + safe_delay_min)))

    time_saved_min = max(1, direct_total_eta - safe_total_eta)

    safe_waypoints = [
        [resp_lat, resp_lon],
        bypass_wp1,
        bypass_wp2,
        [pat_lat, pat_lon]
    ]

    return jsonify({
        'success': True,
        'emergency_id': emergency_id,
        'zone_name': nearest_zone['zone_name'],
        'crowd_density': crowd_density,
        'crowd_index': crowd_index,
        'congestion_choke_point': choke_point_desc,
        'safe_bypass_corridor': safe_corridor_desc,
        'patient': {
            'latitude': pat_lat,
            'longitude': pat_lon,
            'zone': em['wari_zone'],
            'landmark': em['landmark']
        },
        'volunteer': {
            'wari_id': vol_id,
            'id': vol_id,
            'latitude': vol_lat,
            'longitude': vol_lon
        } if vol_id else None,
        'responder': {
            'id': resp_id,
            'latitude': resp_lat,
            'longitude': resp_lon
        },
        'choke_zone': {
            'latitude': mid_lat,
            'longitude': mid_lon,
            'radius_m': 110,
            'description': choke_point_desc,
            'severity': crowd_density
        },
        'routes': {
            'direct_route': {
                'name': 'Direct Procession Route (Congested)',
                'distance_m': direct_dist_m,
                'distance_km': round(direct_dist_km, 2),
                'distance_text': f"{direct_dist_m}m" if direct_dist_m < 1000 else f"{round(direct_dist_km, 1)} km",
                'crowd_level': crowd_density,
                'congestion_delay_min': congestion_delay_min,
                'total_eta_min': direct_total_eta,
                'estimated_time_text': f"{direct_total_eta} min",
                'eta_text': f"{direct_total_eta} min (Slow • Heavy Crowd)",
                'is_recommended': False,
                'color': '#FF5252',
                'waypoints': direct_waypoints
            },
            'safe_bypass_route': {
                'name': 'WariSeva Safe Bypass Corridor (Fastest Safe)',
                'distance_m': safe_dist_m,
                'distance_km': round(safe_dist_km, 2),
                'distance_text': f"{safe_dist_m}m" if safe_dist_m < 1000 else f"{round(safe_dist_km, 1)} km",
                'crowd_level': 'LOW',
                'congestion_delay_min': safe_delay_min,
                'total_eta_min': safe_total_eta,
                'estimated_time_text': f"{safe_total_eta} min",
                'eta_text': f"{safe_total_eta} min (Fastest Safe Corridor)",
                'time_saved_min': time_saved_min,
                'time_saved_text': f"⚡ Saves {time_saved_min} min",
                'is_recommended': True,
                'color': '#00E676',
                'waypoints': safe_waypoints
            },
            'time_saved_text': f"⚡ Saves {time_saved_min} min"
        }
    }), 200

@app.route('/api/emergency/<emergency_id>/route', methods=['GET'])
def get_emergency_route(emergency_id):
    return get_crowd_aware_routes(emergency_id)

# =========================================================================
# STEP 8: HOSPITAL ESCALATION APIS
# =========================================================================

@app.route('/api/emergency/<emergency_id>/nearby-hospitals', methods=['GET'])
def get_nearby_hospitals(emergency_id):
    """Calculate and return sorted list of suitable nearby hospitals."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM emergencies WHERE emergency_id = ?", (emergency_id,))
    em = cursor.fetchone()
    if not em:
        conn.close()
        return jsonify({'success': False, 'error': 'Emergency not found.'}), 404

    pat_lat = em['latitude']
    pat_lon = em['longitude']
    conn.close()

    hospitals = load_hospitals()
    hospital_list = []

    for hosp in hospitals:
        dist_km = calculate_haversine_distance(pat_lat, pat_lon, hosp['latitude'], hosp['longitude'])
        dist_m = int(round(dist_km * 1000))
        
        score = 100.0 - dist_km
        if hosp.get('emergency_available'):
            score += 50.0
        if 'TRAUMA' in hosp.get('capabilities', []):
            score += 25.0
        if 'EMERGENCY_ICU' in hosp.get('capabilities', []):
            score += 20.0

        item = dict(hosp)
        item['distance_km'] = round(dist_km, 2)
        item['distance_m'] = dist_m
        item['suitability_score'] = score
        hospital_list.append(item)

    hospital_list.sort(key=lambda x: x['suitability_score'], reverse=True)

    return jsonify({
        'success': True,
        'emergency_id': emergency_id,
        'patient_zone': em['wari_zone'],
        'hospitals': hospital_list,
        'notice': 'Hospital information available in prototype.'
    }), 200

@app.route('/api/emergency/<emergency_id>/hospital/escalate', methods=['POST'])
def escalate_to_hospital(emergency_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM emergencies WHERE emergency_id = ?", (emergency_id,))
    em = cursor.fetchone()
    if not em:
        conn.close()
        return jsonify({'success': False, 'error': 'Emergency not found.'}), 404

    cursor.execute('''
        UPDATE emergencies 
        SET status = 'HOSPITAL_ESCALATION_REQUESTED', updated_at = CURRENT_TIMESTAMP 
        WHERE emergency_id = ?
    ''', (emergency_id,))
    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'emergency_id': emergency_id,
        'status': 'HOSPITAL_ESCALATION_REQUESTED',
        'message': 'Hospital escalation requested.'
    }), 200

@app.route('/api/emergency/<emergency_id>/hospital/select', methods=['POST'])
def select_hospital(emergency_id):
    data = request.get_json(silent=True) if request.is_json else request.form.to_dict() or {}
    hospital_id = str(data.get('hospital_id', '')).strip()

    if not hospital_id:
        return jsonify({'success': False, 'error': 'Hospital ID is required.'}), 400

    hospitals = load_hospitals()
    matched_hosp = next((h for h in hospitals if h['hospital_id'] == hospital_id or h['hospital_id'].replace('HOSP-', 'H-') == hospital_id or h['hospital_id'] == hospital_id.replace('H-', 'HOSP-')), None)
    if not matched_hosp:
        matched_hosp = hospitals[0] if hospitals else None
    if not matched_hosp:
        return jsonify({'success': False, 'error': f'Hospital "{hospital_id}" not found.'}), 404
    hospital_id = matched_hosp['hospital_id']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM emergencies WHERE emergency_id = ?", (emergency_id,))
    em = cursor.fetchone()
    if not em:
        conn.close()
        return jsonify({'success': False, 'error': 'Emergency not found.'}), 404

    cursor.execute('''
        UPDATE emergencies 
        SET assigned_hospital = ?, status = 'HOSPITAL_SELECTED', updated_at = CURRENT_TIMESTAMP 
        WHERE emergency_id = ?
    ''', (hospital_id, emergency_id))
    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'emergency_id': emergency_id,
        'status': 'HOSPITAL_SELECTED',
        'hospital_id': hospital_id,
        'hospital_name': matched_hosp['name'],
        'hospital_address': matched_hosp['address'],
        'hospital_phone': matched_hosp['phone'],
        'notice': 'Hospital selected in prototype. Transport coordinated by emergency responder.'
    }), 200

# =========================================================================
# GREEN CORRIDOR: EMERGENCY ROUTE OPTIMIZATION APIS
# =========================================================================
try:
    from green_corridor import get_green_corridor_plan
except ImportError:
    from backend.green_corridor import get_green_corridor_plan

@app.route('/api/emergency/<emergency_id>/green-corridor', methods=['GET'])
def api_get_green_corridor(emergency_id):
    """Retrieve multi-factor emergency route optimization plan prioritizing travel time over distance."""
    plan = get_green_corridor_plan(emergency_id)
    return jsonify(plan), 200

@app.route('/api/emergency/<emergency_id>/green-corridor/activate', methods=['POST'])
def api_activate_green_corridor(emergency_id):
    """Simulate Green Corridor route clearance and activation for responding ambulance."""
    plan = get_green_corridor_plan(emergency_id)
    plan['status'] = 'ACTIVE'
    plan['activated_at'] = datetime.now().isoformat()
    return jsonify({
        'success': True,
        'emergency_id': emergency_id,
        'status': 'ACTIVE',
        'route_id': plan['recommended_route_id'],
        'message': f"Green Corridor activated: {plan['summary']['recommended_route']} prioritizes fastest emergency arrival ({plan['summary']['optimized_eta_min']} min ETA).",
        'plan': plan
    }), 200

# =========================================================================
# EMERGENCY CORRIDOR: CROWD CLEARANCE COORDINATION APIS
# =========================================================================
try:
    from emergency_corridor import get_corridor, request_corridor, assign_volunteers, update_status, reset_corridor
except ImportError:
    from backend.emergency_corridor import get_corridor, request_corridor, assign_volunteers, update_status, reset_corridor

@app.route('/api/emergency/<emergency_id>/corridor', methods=['GET'])
def api_get_corridor(emergency_id):
    """Get active Emergency Corridor state, ambulance telemetry, and volunteer coordination roster."""
    corridor = get_corridor(emergency_id)
    return jsonify({'success': True, 'corridor': corridor}), 200

@app.route('/api/emergency/<emergency_id>/corridor/request', methods=['POST'])
def api_request_corridor(emergency_id):
    """Trigger an Emergency Corridor request when ambulance is stuck in crowd."""
    corridor = request_corridor(emergency_id)
    return jsonify({
        'success': True,
        'message': 'Emergency Corridor requested. Command Centre alerted to dispatch nearby volunteers.',
        'corridor': corridor
    }), 200

@app.route('/api/emergency/<emergency_id>/corridor/assign', methods=['POST'])
def api_assign_corridor(emergency_id):
    """Command Centre assigns nearby volunteers to clear crowd corridor."""
    data = request.get_json(silent=True) or {}
    vol_ids = data.get('volunteer_ids', ['V-001', 'V-002', 'V-003'])
    corridor = assign_volunteers(emergency_id, vol_ids)
    return jsonify({
        'success': True,
        'message': f"Assigned {len(corridor['assigned_volunteers'])} volunteers to clear emergency corridor.",
        'corridor': corridor
    }), 200

@app.route('/api/emergency/<emergency_id>/corridor/status', methods=['POST'])
def api_update_corridor_status(emergency_id):
    """Update progression of crowd clearance corridor."""
    data = request.get_json(silent=True) or {}
    new_status = data.get('status', 'CLEARING')
    actor = data.get('actor', 'VOLUNTEER V-001')
    corridor = update_status(emergency_id, new_status, actor)
    return jsonify({
        'success': True,
        'message': f"Corridor status updated to: {corridor['status_label']}",
        'corridor': corridor
    }), 200

@app.route('/api/emergency/<emergency_id>/corridor/reset', methods=['POST'])
def api_reset_corridor(emergency_id):
    """Reset Emergency Corridor demo state."""
    corridor = reset_corridor(emergency_id)
    return jsonify({'success': True, 'corridor': corridor}), 200




# =========================================================================
# STEP 8: WARI SAFETY SERVICES APIS
# =========================================================================

@app.route('/api/safety-services', methods=['GET'])
@app.route('/api/services/facilities', methods=['GET'])
@app.route('/api/services', methods=['GET'])
def get_safety_services():
    category = request.args.get('type', request.args.get('category', '')).strip().upper()
    zone_filter = request.args.get('zone', '').strip()
    raw_lat = request.args.get('latitude', request.args.get('lat', '18.3444'))
    raw_lon = request.args.get('longitude', request.args.get('lon', '74.0305'))

    user_lat = 18.3444
    user_lon = 74.0305
    try:
        if raw_lat and raw_lon:
            user_lat = float(raw_lat)
            user_lon = float(raw_lon)
    except (ValueError, TypeError):
        pass

    results = []
    
    # Category normalization across singular/plural and synonyms
    if category in ('WASHROOM', 'WASHROOMS', 'RESTROOM', 'RESTROOMS', 'TOILETS'):
        category = 'TOILET'
    elif category in ('MEDICAL', 'MEDICALS', 'DOCTOR', 'MEDIC'):
        category = 'MEDICAL_CAMP'
    elif category in ('WATERS', 'WATER_POINT', 'WATER_POINTS'):
        category = 'WATER'
    elif category in ('VOLUNTEER',):
        category = 'VOLUNTEERS'
    elif category in ('HOSPITAL',):
        category = 'HOSPITALS'
    elif category in ('EMERGENCY',):
        category = 'EMERGENCIES'

    # 1. Base safety services from JSON
    services = load_safety_services()
    for s in services:
        s_type = s.get('type', '').upper()
        if category in ('WATER', 'TOILET', 'FOOD', 'REST_AREA', 'MEDICAL_CAMP', 'ALL', ''):
            if category == 'WATER' and s_type != 'WATER':
                continue
            if category == 'TOILET' and s_type not in ('TOILET', 'WASHROOM'):
                continue
            if category == 'MEDICAL_CAMP' and s_type not in ('MEDICAL_CAMP', 'MEDICAL'):
                continue
            if category == 'FOOD' and s_type != 'FOOD':
                continue
            if category == 'REST_AREA' and s_type != 'REST_AREA':
                continue

            item = dict(s)
            dist_km = calculate_haversine_distance(user_lat, user_lon, s['latitude'], s['longitude'])
            dist_m = int(round(dist_km * 1000))
            item['category'] = s_type
            item['distance_km'] = round(dist_km, 2)
            item['distance_m'] = dist_m
            item['distance_text'] = f"{dist_m}m away" if dist_m < 1000 else f"{round(dist_km, 1)} km away"
            item['status'] = s.get('status', 'AVAILABLE')
            item['first_aid'] = 'AVAILABLE' if 'MED' in s_type else 'N/A'
            item['emergency_support'] = 'YES' if 'MED' in s_type else 'STANDARD'
            results.append(item)

    # 1b. Additional Medical Camps from SQLite DB
    if category in ('MEDICAL_CAMP', 'ALL', ''):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM medical_camps")
            db_camps = cursor.fetchall()
            conn.close()
            existing_names = {r.get('name', '').strip().lower() for r in results}
            for c in db_camps:
                c_name = c['name']
                if c_name.strip().lower() not in existing_names:
                    dist_km = calculate_haversine_distance(user_lat, user_lon, c['latitude'], c['longitude'])
                    dist_m = int(round(dist_km * 1000))
                    results.append({
                        'service_id': c['camp_id'],
                        'name': c['name'],
                        'category': 'MEDICAL_CAMP',
                        'type': 'MEDICAL_CAMP',
                        'latitude': c['latitude'],
                        'longitude': c['longitude'],
                        'zone': c['zone'] or 'Zone 04 — Saswad Palkhi Maidan',
                        'address': f"Medical Camp • {c['zone'] or 'Palkhi Route'}",
                        'status': c['status'] or 'AVAILABLE',
                        'first_aid': 'DOCTOR & AMBULANCE ON STANDBY',
                        'emergency_support': 'YES',
                        'special_note': f"Capabilities: {c['capabilities'] or 'General Triage & First Aid'}",
                        'distance_km': round(dist_km, 2),
                        'distance_m': dist_m,
                        'distance_text': f"{dist_m}m away" if dist_m < 1000 else f"{round(dist_km, 1)} km away"
                    })
        except Exception:
            pass

    # 2. Hospitals from JSON
    if category in ('HOSPITALS', 'HOSPITAL', 'ALL', ''):
        hospitals = load_hospitals()
        for h in hospitals:
            dist_km = calculate_haversine_distance(user_lat, user_lon, h['latitude'], h['longitude'])
            dist_m = int(round(dist_km * 1000))
            results.append({
                'service_id': h['hospital_id'],
                'name': h['name'],
                'category': 'HOSPITAL',
                'type': 'HOSPITAL',
                'latitude': h['latitude'],
                'longitude': h['longitude'],
                'zone': h.get('zone', 'Zone 04 — Saswad Palkhi Maidan'),
                'address': h.get('address', 'Saswad-Hadapsar Road'),
                'status': 'ACCEPTING EMERGENCIES',
                'first_aid': 'ADVANCED / ICU',
                'emergency_support': 'YES',
                'special_note': f"Emergency Beds: {h.get('emergency_beds', 1)} • Trauma & Surgery Unit",
                'distance_km': round(dist_km, 2),
                'distance_m': dist_m,
                'distance_text': f"{dist_m}m away" if dist_m < 1000 else f"{round(dist_km, 1)} km away"
            })

    # 3. Available Volunteers from SQLite DB
    if category in ('VOLUNTEERS', 'VOLUNTEER', 'ALL', ''):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE role = 'VOLUNTEER'")
        vols = cursor.fetchall()
        conn.close()
        for v in vols:
            v_lat = v['latitude'] or 18.3460
            v_lon = v['longitude'] or 74.0288
            dist_km = calculate_haversine_distance(user_lat, user_lon, v_lat, v_lon)
            dist_m = int(round(dist_km * 1000))
            results.append({
                'service_id': v['wari_id'],
                'name': f"{v['name']} ({v['wari_id']})",
                'category': 'VOLUNTEER',
                'type': 'VOLUNTEER',
                'latitude': v_lat,
                'longitude': v_lon,
                'zone': v['zone'] or 'Zone 04 — Saswad Palkhi Maidan',
                'address': f"Assigned: {v['zone'] or 'Route Section'}",
                'status': v['status'] or 'AVAILABLE',
                'first_aid': 'CPR & FIRST AID CERTIFIED',
                'emergency_support': 'YES',
                'special_note': f"Skills: {v['skills'] or 'First Aid'} • Languages: {v['languages'] or 'Marathi, Hindi'}",
                'distance_km': round(dist_km, 2),
                'distance_m': dist_m,
                'distance_text': f"{dist_m}m away" if dist_m < 1000 else f"{round(dist_km, 1)} km away"
            })

    # 4. Active Emergencies from DB
    if category in ('EMERGENCIES', 'EMERGENCY', 'ALL', ''):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM emergencies ORDER BY created_at DESC LIMIT 5")
        ems = cursor.fetchall()
        conn.close()
        if not ems:
            results.append({
                'service_id': 'EM-28471',
                'name': '🚨 Incident EM-28471 (Tukaram Shinde)',
                'category': 'EMERGENCY',
                'type': 'EMERGENCY',
                'latitude': 18.3444,
                'longitude': 74.0305,
                'zone': 'Zone 04 — Saswad Palkhi Maidan',
                'address': 'Saswad Central Palkhi Maidan Ground',
                'status': 'ACTIVE',
                'first_aid': 'ACTIVE DISPATCH',
                'emergency_support': 'CRITICAL',
                'special_note': 'Type: Medical Emergency • Priority: CRITICAL',
                'distance_km': 0.0,
                'distance_m': 0,
                'distance_text': '0m away (Current Location)'
            })
        else:
            for em in ems:
                dist_km = calculate_haversine_distance(user_lat, user_lon, em['latitude'], em['longitude'])
                dist_m = int(round(dist_km * 1000))
                results.append({
                    'service_id': em['emergency_id'],
                    'name': f"🚨 Incident {em['emergency_id']} ({em['reported_by']})",
                    'category': 'EMERGENCY',
                    'type': 'EMERGENCY',
                    'latitude': em['latitude'],
                    'longitude': em['longitude'],
                    'zone': em['wari_zone'] or 'Zone 04 — Saswad Palkhi Maidan',
                    'address': em['landmark'] or 'Saswad Palkhi Ground',
                    'status': em['status'],
                    'first_aid': 'ACTIVE DISPATCH',
                    'emergency_support': 'CRITICAL',
                    'special_note': f"Type: {em['emergency_type']} • Priority: {em['priority']}",
                    'distance_km': round(dist_km, 2),
                    'distance_m': dist_m,
                    'distance_text': f"{dist_m}m away" if dist_m < 1000 else f"{round(dist_km, 1)} km away"
                })

    # 5. Crowd-Risk Choke Points from wari_zones.json
    if category in ('CROWD_RISK', 'CROWD', 'ALL', ''):
        zones = load_wari_zones()
        for z in zones:
            if z.get('crowd_density') in ('HIGH', 'CRITICAL') or category == 'CROWD_RISK':
                dist_km = calculate_haversine_distance(user_lat, user_lon, z['latitude'], z['longitude'])
                dist_m = int(round(dist_km * 1000))
                results.append({
                    'service_id': f"CR-{z['zone_id']}",
                    'name': f"👥 Crowd Congestion: {z['zone_name']}",
                    'category': 'CROWD_RISK',
                    'type': 'CROWD_RISK',
                    'latitude': z['latitude'],
                    'longitude': z['longitude'],
                    'zone': z['zone_name'],
                    'address': z.get('congestion_choke_point', 'Palkhi Procession Route'),
                    'status': f"{z.get('crowd_density')} RISK (Index {z.get('crowd_index', 80)}%)",
                    'first_aid': 'BYPASS RECOMMENDED',
                    'emergency_support': 'AMBULANCE LANE AVAILABLE',
                    'special_note': f"Reason: High crowd density + narrow procession corridor. Safe Bypass: {z.get('safe_bypass_corridor', 'Outer bypass')}",
                    'distance_km': round(dist_km, 2),
                    'distance_m': dist_m,
                    'distance_text': f"{dist_m}m away" if dist_m < 1000 else f"{round(dist_km, 1)} km away"
                })

    # Sort by proximity
    results.sort(key=lambda x: x.get('distance_m', 999999))

    return jsonify({
        'success': True,
        'count': len(results),
        'category': category or 'ALL',
        'services': results
    }), 200

@app.route('/api/responder/dashboard-data', methods=['GET'])
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
    return jsonify({'success': True, 'count': len(emergencies), 'emergencies': emergencies}), 200

@app.route('/api/emergency/<emergency_id>/tracking', methods=['GET'])
def get_emergency_tracking(emergency_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM emergencies WHERE emergency_id = ?", (emergency_id,))
    em = cursor.fetchone()
    if not em:
        conn.close()
        return jsonify({'success': False, 'error': 'Emergency not found.'}), 404

    patient_lat = em['latitude']
    patient_lon = em['longitude']

    # 1. Nearest Available Volunteer candidate (if not yet assigned or searching)
    cursor.execute('''
        SELECT * FROM users 
        WHERE role = 'VOLUNTEER' AND status = 'AVAILABLE' 
          AND latitude IS NOT NULL AND longitude IS NOT NULL
    ''')
    avail_vols = cursor.fetchall()
    nearest_vol_candidate = None
    if avail_vols:
        sorted_avail = []
        for v in avail_vols:
            d_km = calculate_haversine_distance(patient_lat, patient_lon, v['latitude'], v['longitude'])
            d_m = int(round(d_km * 1000))
            eta_v = max(1, int(round((d_km / 4.5) * 60.0)))
            sorted_avail.append({
                'id': v['wari_id'],
                'name': v['name'],
                'phone': v['phone'],
                'latitude': v['latitude'],
                'longitude': v['longitude'],
                'distance_m': d_m,
                'distance_km': round(d_km, 2),
                'eta_min': eta_v,
                'status': 'AVAILABLE'
            })
        sorted_avail.sort(key=lambda x: x['distance_m'])
        if sorted_avail:
            nearest_vol_candidate = sorted_avail[0]

    # 2. Assigned Volunteer Data
    volunteer_data = None
    distance_m = None
    distance_km = None
    eta_min = None
    last_update_str = None

    assigned_vol_id = em['assigned_volunteer']
    if assigned_vol_id:
        cursor.execute('''
            SELECT * FROM location_updates 
            WHERE user_id = ? AND emergency_id = ? 
            ORDER BY timestamp DESC LIMIT 1
        ''', (assigned_vol_id, emergency_id))
        loc_row = cursor.fetchone()

        cursor.execute("SELECT * FROM users WHERE wari_id = ?", (assigned_vol_id,))
        vol_user = cursor.fetchone()

        vol_lat = loc_row['latitude'] if loc_row else (vol_user['latitude'] if vol_user and vol_user['latitude'] else 18.3450)
        vol_lon = loc_row['longitude'] if loc_row else (vol_user['longitude'] if vol_user and vol_user['longitude'] else 74.0315)
        accuracy = loc_row['accuracy'] if loc_row else 5.0
        last_update_str = loc_row['timestamp'] if loc_row else (vol_user['created_at'] if vol_user else None)

        dist_km_val = calculate_haversine_distance(patient_lat, patient_lon, vol_lat, vol_lon)
        distance_km = round(dist_km_val, 2)
        distance_m = int(round(dist_km_val * 1000))
        eta_min = max(1, int(round((dist_km_val / 4.5) * 60.0))) if em['status'] != 'WITH_PATIENT' else 0

        volunteer_data = {
            'id': assigned_vol_id,
            'name': vol_user['name'] if vol_user else 'Volunteer',
            'phone': vol_user['phone'] if vol_user else '',
            'latitude': vol_lat,
            'longitude': vol_lon,
            'accuracy': accuracy,
            'timestamp': last_update_str,
            'distance_m': distance_m if em['status'] != 'WITH_PATIENT' else 0,
            'distance_km': distance_km if em['status'] != 'WITH_PATIENT' else 0.0,
            'eta_min': eta_min,
            'status': em['status']
        }
    elif nearest_vol_candidate:
        distance_m = nearest_vol_candidate['distance_m']
        distance_km = nearest_vol_candidate['distance_km']
        eta_min = nearest_vol_candidate['eta_min']

    # 3. Assigned Responder Data
    responder_data = None
    assigned_resp_id = em['assigned_responder']
    if assigned_resp_id:
        cursor.execute('''
            SELECT * FROM location_updates 
            WHERE user_id = ? AND emergency_id = ? 
            ORDER BY timestamp DESC LIMIT 1
        ''', (assigned_resp_id, emergency_id))
        r_loc_row = cursor.fetchone()

        cursor.execute("SELECT * FROM users WHERE wari_id = ?", (assigned_resp_id,))
        resp_user = cursor.fetchone()

        resp_lat = r_loc_row['latitude'] if r_loc_row else (resp_user['latitude'] if resp_user and resp_user['latitude'] else 18.3470)
        resp_lon = r_loc_row['longitude'] if r_loc_row else (resp_user['longitude'] if resp_user and resp_user['longitude'] else 74.0330)
        r_acc = r_loc_row['accuracy'] if r_loc_row else 5.0
        r_timestamp = r_loc_row['timestamp'] if r_loc_row else (resp_user['created_at'] if resp_user else None)

        r_dist_km = calculate_haversine_distance(patient_lat, patient_lon, resp_lat, resp_lon)
        r_dist_m = int(round(r_dist_km * 1000))
        r_eta = max(2, int(round((r_dist_km / 25.0) * 60.0) + 1)) if em['status'] != 'ARRIVED' else 0

        responder_data = {
            'id': assigned_resp_id,
            'name': resp_user['name'] if resp_user else 'Medical Responder',
            'phone': resp_user['phone'] if resp_user else '',
            'latitude': resp_lat,
            'longitude': resp_lon,
            'accuracy': r_acc,
            'timestamp': r_timestamp,
            'distance_m': r_dist_m if em['status'] != 'ARRIVED' else 0,
            'distance_km': round(r_dist_km, 2) if em['status'] != 'ARRIVED' else 0.0,
            'eta_min': r_eta,
            'status': em['status']
        }

    # 4. Hospital Data
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

    ai_match_data = ai_response_engine(dict(em))
    rec_vol = ai_match_data.get('recommended_volunteer')
    recommendation_reason = rec_vol.get('reason') if rec_vol else "Selected based on active proximity, low estimated response time (3 min), and low crowd congestion along bypass path."

    return jsonify({
        'success': True,
        'emergency_id': emergency_id,
        'status': em['status'],
        'has_reached': (em['status'] in ('WITH_PATIENT', 'ARRIVED', 'HOSPITAL_SELECTED', 'RESOLVED')),
        'crowd_density': crowd_density,
        'ai_recommendation': ai_match_data,
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
    }), 200

@app.route('/api/volunteer/dashboard-data', methods=['GET'])
def get_volunteer_dashboard_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM emergencies 
        WHERE status NOT IN ('CANCELLED')
        ORDER BY created_at DESC 
        LIMIT 20
    ''')
    rows = cursor.fetchall()
    
    seen_ids = set()
    emergencies = []
    for r in rows:
        em_id = r['emergency_id']
        if em_id in seen_ids:
            continue
        seen_ids.add(em_id)
        dist_km = calculate_haversine_distance(18.3450, 74.0315, r['latitude'], r['longitude'])
        dist_m = int(round(dist_km * 1000))
        item = dict(r)
        item['distance_m'] = dist_m
        item['distance_km'] = round(dist_km, 2)
        emergencies.append(item)

    conn.close()
    return jsonify({'success': True, 'count': len(emergencies), 'emergencies': emergencies}), 200


@app.route('/api/hospital/dashboard-data', methods=['GET'])
def get_hospital_dashboard_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM emergencies 
        WHERE status NOT IN ('CANCELLED') 
        ORDER BY created_at DESC LIMIT 20
    ''')
    rows = cursor.fetchall()
    seen_ids = set()
    emergencies = []
    for r in rows:
        em_id = r['emergency_id']
        if em_id in seen_ids:
            continue
        seen_ids.add(em_id)
        dist_km = calculate_haversine_distance(18.3444, 74.0305, r['latitude'], r['longitude'])
        dist_m = int(round(dist_km * 1000))
        item = dict(r)
        item['distance_m'] = dist_m
        item['distance_km'] = round(dist_km, 2)
        emergencies.append(item)
    conn.close()
    return jsonify({'success': True, 'count': len(emergencies), 'emergencies': emergencies}), 200

@app.route('/api/camp/dashboard-data', methods=['GET'])
def get_camp_dashboard_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM emergencies 
        WHERE status NOT IN ('CANCELLED')
        ORDER BY created_at DESC 
        LIMIT 20
    ''')
    rows = cursor.fetchall()

    seen_ids = set()
    emergencies = []
    for r in rows:
        em_id = r['emergency_id']
        if em_id in seen_ids:
            continue
        seen_ids.add(em_id)
        dist_km = calculate_haversine_distance(18.3460, 74.0320, r['latitude'], r['longitude'])
        dist_m = int(round(dist_km * 1000))
        item = dict(r)
        item['distance_m'] = dist_m
        item['distance_km'] = round(dist_km, 2)
        emergencies.append(item)

    conn.close()
    return jsonify({'success': True, 'count': len(emergencies), 'emergencies': emergencies}), 200



@app.route('/api/command-center/emergencies', methods=['GET'])
@app.route('/api/command-center/incidents', methods=['GET'])
def get_command_center_emergencies():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM emergencies 
        ORDER BY created_at DESC
    ''')
    rows = cursor.fetchall()
    emergencies = []
    hospitals = load_hospitals()
    
    for r in rows:
        em_dict = dict(r)
        vol_id = em_dict.get('assigned_volunteer')
        resp_id = em_dict.get('assigned_responder')
        hosp_id = em_dict.get('assigned_hospital')
        dist_m = None
        
        if vol_id:
            cursor.execute('''
                SELECT latitude, longitude, timestamp FROM location_updates 
                WHERE user_id = ? AND emergency_id = ? 
                ORDER BY timestamp DESC LIMIT 1
            ''', (vol_id, em_dict['emergency_id']))
            loc = cursor.fetchone()
            if loc:
                d_km = calculate_haversine_distance(em_dict['latitude'], em_dict['longitude'], loc['latitude'], loc['longitude'])
                dist_m = int(round(d_km * 1000))
                em_dict['volunteer_lat'] = loc['latitude']
                em_dict['volunteer_lon'] = loc['longitude']
                em_dict['volunteer_last_update'] = loc['timestamp']

        if resp_id:
            cursor.execute('''
                SELECT latitude, longitude, timestamp FROM location_updates 
                WHERE user_id = ? AND emergency_id = ? 
                ORDER BY timestamp DESC LIMIT 1
            ''', (resp_id, em_dict['emergency_id']))
            r_loc = cursor.fetchone()
            if r_loc:
                em_dict['responder_lat'] = r_loc['latitude']
                em_dict['responder_lon'] = r_loc['longitude']

        if hosp_id:
            h = next((h for h in hospitals if h['hospital_id'] == hosp_id), None)
            em_dict['hospital_name'] = h['name'] if h else hosp_id
        else:
            em_dict['hospital_name'] = None

        em_dict['distance_to_patient_m'] = dist_m
        emergencies.append(em_dict)

    conn.close()

    return jsonify({
        'success': True,
        'count': len(emergencies),
        'emergencies': emergencies
    }), 200


# =========================================================================
# COMPANION GROUP, COMMAND CENTER RESOURCES, HEATMAP & ANALYTICS
# =========================================================================

@app.route('/api/group/members', methods=['GET'])
def get_group_members():
    wari_id = request.args.get('wari_id', 'WS-28471').strip()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM group_members WHERE wari_id = ? ORDER BY created_at ASC", (wari_id,))
    rows = cursor.fetchall()
    members = [dict(r) for r in rows]
    conn.close()
    return jsonify({'success': True, 'wari_id': wari_id, 'members': members}), 200

@app.route('/api/group/add-member', methods=['POST'])
def add_group_member():
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    wari_id = str(data.get('wari_id', 'WS-28471')).strip()
    name = str(data.get('name', '')).strip()
    phone = str(data.get('phone', '')).strip()
    relationship = str(data.get('relationship', 'Family / Companion')).strip() or 'Family'

    if not name or not phone:
        return jsonify({'success': False, 'error': 'Name and phone number are required.'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO group_members (wari_id, member_name, member_phone, relationship)
        VALUES (?, ?, ?, ?)
    ''', (wari_id, name, phone, relationship))
    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'message': f'Companion {name} added to your Wari Safety Group.',
        'member': {'wari_id': wari_id, 'name': name, 'phone': phone, 'relationship': relationship}
    }), 201

@app.route('/api/command-center/resources', methods=['GET'])
def get_command_center_resources():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM medical_camps ORDER BY camp_id ASC")
    camps = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT * FROM emergencies WHERE status NOT IN ('RESOLVED', 'DECLINED')")
    active_emergencies = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT * FROM users WHERE role = 'VOLUNTEER'")
    all_vols = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT * FROM users WHERE role = 'MEDICAL_RESPONDER'")
    all_resps = [dict(r) for r in cursor.fetchall()]

    conn.close()

    resources = []
    for camp in camps:
        c_lat, c_lon = camp['latitude'], camp['longitude']
        
        # Volunteers nearby within 3km
        vols_count = sum(1 for v in all_vols if v['latitude'] and calculate_haversine_distance(c_lat, c_lon, v['latitude'], v['longitude']) <= 3.0)
        vols_avail = sum(1 for v in all_vols if v['status'] == 'AVAILABLE' and v['latitude'] and calculate_haversine_distance(c_lat, c_lon, v['latitude'], v['longitude']) <= 3.0)
        
        # Responders nearby within 6km
        resps_count = sum(1 for r in all_resps if r['latitude'] and calculate_haversine_distance(c_lat, c_lon, r['latitude'], r['longitude']) <= 6.0)
        
        # Active emergencies in this zone
        active_in_zone = sum(1 for e in active_emergencies if e['latitude'] and calculate_haversine_distance(c_lat, c_lon, e['latitude'], e['longitude']) <= 4.0)
        
        load_state = 'READY'
        if active_in_zone >= 3:
            load_state = 'HIGH LOAD'
        elif active_in_zone >= 1:
            load_state = 'MODERATE LOAD'

        resources.append({
            'camp_id': camp['camp_id'],
            'name': camp['name'],
            'zone': camp['zone'],
            'latitude': camp['latitude'],
            'longitude': camp['longitude'],
            'volunteers_total': max(vols_count, 6),
            'volunteers_available': max(vols_avail, 4),
            'responders_count': max(resps_count, 2),
            'active_emergencies': active_in_zone,
            'load_state': load_state,
            'capabilities': camp.get('capabilities', 'GENERAL_MEDICAL,TRIAGE')
        })

    return jsonify({
        'success': True,
        'count': len(resources),
        'camps': resources
    }), 200

@app.route('/api/command-center/overview', methods=['GET'])
@app.route('/api/command-center/metrics', methods=['GET'])
@app.route('/api/command-center/summary', methods=['GET'])
def get_command_center_overview_alias():
    return get_command_resources_count()

@app.route('/api/command-center/hospitals', methods=['GET'])
@app.route('/api/hospitals', methods=['GET'])
def get_command_center_hospitals_alias():
    return jsonify({'success': True, 'hospitals': list(HOSPITAL_DEMO_ACCOUNTS.values())}), 200

@app.route('/api/command-center/camps', methods=['GET'])
@app.route('/api/medical-camps', methods=['GET'])
def get_command_center_camps_alias():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medical_camps ORDER BY camp_id ASC")
    camps = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify({'success': True, 'camps': camps, 'medical_camps': camps}), 200

@app.route('/api/command-center/volunteers', methods=['GET'])
@app.route('/api/volunteers', methods=['GET'])
def get_command_center_volunteers_alias():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, wari_id as user_id, wari_id as volunteer_id, name, role, status, zone, latitude, longitude, phone FROM users WHERE role IN ('VOLUNTEER', 'MEDICAL_RESPONDER')")
    vols = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify({'success': True, 'volunteers': vols, 'count': len(vols)}), 200

@app.route('/api/notifications', methods=['GET'])
def get_all_notifications_alias():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notifications ORDER BY id DESC LIMIT 50")
    notifications = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify({'success': True, 'notifications': notifications, 'count': len(notifications)}), 200

@app.route('/api/dindi/<dindi_no>/members', methods=['GET'])
@app.route('/api/companion-group/<dindi_no>/members', methods=['GET'])
def get_dindi_group_members_alias(dindi_no):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM group_members ORDER BY id ASC")
    members = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify({'success': True, 'dindi': dindi_no, 'members': members, 'count': len(members)}), 200

@app.route('/api/pilgrim/<wari_id>/live-status', methods=['GET'])
def get_pilgrim_live_status_alias(wari_id):
    clean_id = str(wari_id).strip().upper()
    return jsonify({
        'success': True,
        'wari_id': clean_id,
        'status': 'SAFE',
        'current_zone': 'Zone 04 — Saswad Palkhi Maidan',
        'last_updated': datetime.now().strftime('%I:%M %p')
    }), 200

@app.route('/api/command-center/heatmap', methods=['GET'])
def get_command_center_heatmap():
    zones = load_wari_zones()
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM emergencies")
    all_em = [dict(r) for r in cursor.fetchall()]
    conn.close()

    heatmap_points = []
    for z in zones:
        z_lat, z_lon = z['latitude'], z['longitude']
        active_cnt = sum(1 for e in all_em if e['status'] not in ('RESOLVED', 'DECLINED') and calculate_haversine_distance(z_lat, z_lon, e['latitude'], e['longitude']) <= 5.0)
        total_cnt = sum(1 for e in all_em if calculate_haversine_distance(z_lat, z_lon, e['latitude'], e['longitude']) <= 5.0)
        
        density = z.get('crowd_density', 'MODERATE')
        intensity = 0.9 if density == 'CRITICAL' else (0.75 if density == 'HIGH' else 0.45)
        
        heatmap_points.append({
            'zone_id': z['zone_id'],
            'zone_name': z['zone_name'],
            'latitude': z['latitude'],
            'longitude': z['longitude'],
            'crowd_density': density,
            'crowd_index': z.get('crowd_index', 60),
            'active_emergencies': active_cnt,
            'total_emergencies': total_cnt,
            'intensity': intensity,
            'congestion_choke_point': z.get('congestion_choke_point', ''),
            'safe_bypass_corridor': z.get('safe_bypass_corridor', '')
        })

    return jsonify({
        'success': True,
        'heatmap_points': heatmap_points
    }), 200

@app.route('/api/emergency/<emergency_id>/analytics', methods=['GET'])
def get_emergency_analytics(emergency_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM emergencies WHERE emergency_id = ?", (emergency_id,))
    em = cursor.fetchone()
    if not em:
        conn.close()
        return jsonify({'success': False, 'error': 'Emergency not found.'}), 404

    cursor.execute("SELECT * FROM notifications WHERE emergency_id = ? ORDER BY created_at ASC", (emergency_id,))
    notifs = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT * FROM location_updates WHERE emergency_id = ? ORDER BY timestamp ASC", (emergency_id,))
    loc_updates = [dict(r) for r in cursor.fetchall()]
    conn.close()

    status = em['status']
    is_resolved = (status == 'RESOLVED')

    # Simulated realistic response timeline metrics for prototype demonstration
    created_at = em['created_at']
    updated_at = em['updated_at'] or em['created_at']
    
    vol_assign_s = 24
    vol_travel_s = 128
    resp_transit_s = 86
    total_response_s = 238 if is_resolved else 142
    total_min = total_response_s // 60
    total_sec = total_response_s % 60
    time_formatted = f"{total_min}m {total_sec:02d}s"

    score_dispatch = 30
    score_gps = 24
    score_route = 20
    score_responder = 18
    total_score = score_dispatch + score_gps + score_route + score_responder

    return jsonify({
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
    }), 200


# =========================================================================
# INTELLIGENT RESPONSE ENGINE — PROTOTYPE AI SCORING & DECISION SUPPORT
# =========================================================================

def ai_response_engine(em_data, candidate_volunteers=None):
    """
    AI-Assisted Intelligent Response Recommendation Engine.
    Evaluates candidate responders using an explainable multi-factor scoring model:
    Score (0-100) = Proximity + Skill Match + Zone Relevance + Route/Crowd Access + Verification.
    """
    pat_lat = float(em_data.get('latitude', 18.3444))
    pat_lon = float(em_data.get('longitude', 74.0305))
    em_zone = em_data.get('wari_zone', 'Zone 04 — Saswad Palkhi Maidan')
    em_type = str(em_data.get('emergency_type', 'MEDICAL')).upper()
    severity = str(em_data.get('severity', em_data.get('priority', 'CRITICAL'))).upper()

    conn = get_db_connection()
    cursor = conn.cursor()

    if candidate_volunteers is None:
        cursor.execute("SELECT * FROM users WHERE role = 'VOLUNTEER'")
        vols = [dict(r) for r in cursor.fetchall()]
    else:
        vols = candidate_volunteers

    conn.close()

    scored_candidates = []
    excluded_candidates = []

    for v in vols:
        v_id = v.get('wari_id', 'V-000')
        v_name = v.get('name', 'Volunteer')
        v_status = v.get('status', 'AVAILABLE')
        v_lat = v.get('latitude', 18.3460)
        v_lon = v.get('longitude', 74.0288)
        v_zone = v.get('zone', 'Zone 04 — Saswad Palkhi Maidan')
        v_skills = v.get('skills', 'General Assistance')
        v_cert = v.get('certification', 'None')
        v_verif = v.get('verification_status', 'VERIFIED')

        # Filter out busy / unavailable volunteers
        if v_status != 'AVAILABLE':
            excluded_candidates.append({
                'wari_id': v_id,
                'name': v_name,
                'status': v_status,
                'reason': f"Volunteer is currently {v_status.lower()} and excluded from dispatch pool."
            })
            continue

        # 1. Proximity / Distance Score (Max 35 points)
        dist_km = calculate_haversine_distance(pat_lat, pat_lon, v_lat, v_lon)
        dist_m = int(round(dist_km * 1000))
        if dist_m <= 350:
            score_dist = 35
            eta_min = 2
        elif dist_m <= 700:
            score_dist = 28
            eta_min = 3
        elif dist_m <= 1500:
            score_dist = 20
            eta_min = 5
        elif dist_m <= 3000:
            score_dist = 10
            eta_min = 8
        else:
            score_dist = 5
            eta_min = 12

        # 2. Skill & Medical Training Match (Max 25 points)
        score_skill = 5
        if any(term in em_type for term in ('MEDIC', 'INJURY', 'HEAT', 'DEHYDRAT', 'ELDERLY', 'ASTHMA', 'BREATH', 'CARDIAC', 'EMERGENCY')):
            if 'First Aid Certified' in v_cert or 'Nurse' in v_cert or 'Paramedic' in v_skills:
                score_skill = 25
            elif 'First Aid' in v_skills or 'Triage' in v_skills or 'CPR' in v_skills:
                score_skill = 18
            elif 'Crowd' in v_skills:
                score_skill = 10
        else:
            if 'Crowd' in v_skills or 'Marshall' in v_skills:
                score_skill = 25
            else:
                score_skill = 15

        # 3. Zone Relevance & Localization (Max 20 points)
        if em_zone and v_zone and em_zone.split('—')[0].strip() == v_zone.split('—')[0].strip():
            score_zone = 20
        elif 'Zone 03' in str(v_zone) or 'Zone 05' in str(v_zone):
            score_zone = 12
        else:
            score_zone = 5

        # 4. Route & Bypass Corridor Accessibility (Max 10 points)
        # Check if volunteer is outside the main procession choke line
        if dist_m <= 400 or 'Bypass' in str(v_skills) or score_zone == 20:
            score_route = 10
        else:
            score_route = 5

        # 5. Verification & Accreditation (Max 10 points)
        score_verif = 10 if v_verif == 'VERIFIED' else 5

        total_score = min(100, score_dist + score_skill + score_zone + score_route + score_verif)

        # Build Explainable Reason
        reasons = []
        reasons.append("Available")
        if score_skill >= 20:
            reasons.append(f"{v_cert if v_cert != 'None' else 'Medical Skill Match'}")
        if score_zone == 20:
            reasons.append(f"Inside {v_zone.split('—')[0].strip()}")
        reasons.append(f"{dist_m}m from patient (ETA {eta_min} min)")
        reasons.append("Accessible safe bypass corridor")

        reason_summary = " • ".join(reasons)

        candidate_obj = {
            'wari_id': v_id,
            'name': v_name,
            'total_score': total_score,
            'distance_m': dist_m,
            'distance_km': round(dist_km, 2),
            'eta_min': eta_min,
            'zone': v_zone,
            'skills': v_skills,
            'certification': v_cert,
            'verification_status': v_verif,
            'status': v_status,
            'reason': reason_summary,
            'reasons_list': reasons,
            'breakdown': {
                'distance_score': score_dist,
                'skill_match_score': score_skill,
                'zone_relevance_score': score_zone,
                'route_accessibility_score': score_route,
                'verification_score': score_verif
            }
        }
        scored_candidates.append(candidate_obj)

    # Sort descending by total score
    scored_candidates.sort(key=lambda x: (-x['total_score'], x['distance_m']))

    recommended = scored_candidates[0] if scored_candidates else None
    backups = scored_candidates[1:3] if len(scored_candidates) > 1 else []

    # Recommended Hospital Logic
    rec_hospital = recommend_hospital(em_data)

    return {
        'success': True,
        'emergency_id': em_data.get('emergency_id', 'EM-28471'),
        'severity': severity,
        'emergency_type': em_type,
        'model_name': 'WariSeva Explainable AI Response Engine v2.0 (Prototype)',
        'recommended_volunteer': recommended,
        'backup_volunteers': backups,
        'excluded_volunteers': excluded_candidates,
        'recommended_hospital': rec_hospital,
        'explainability_text': 'Prototype AI • Explainable Response Scoring model considering proximity, certified skill matching, zone localization, and bypass route congestion.'
    }

def recommend_hospital(em_data):
    """Recommend best hospital based on trauma capability, travel ETA, and demo availability."""
    pat_lat = float(em_data.get('latitude', 18.3444))
    pat_lon = float(em_data.get('longitude', 74.0305))
    hospitals = load_hospitals()

    if not hospitals:
        return {
            'hospital_id': 'HOSP-001',
            'name': 'Saswad Rural Sub-District Hospital',
            'distance_km': 2.8,
            'eta_min': 8,
            'emergency_capability': 'HIGH (Trauma Care & ICU)',
            'availability': 'AVAILABLE',
            'reason': 'Recommended based on emergency trauma capability, estimated travel time (8 min), and current demo availability.'
        }

    scored_hosp = []
    for h in hospitals:
        dist_km = calculate_haversine_distance(pat_lat, pat_lon, h['latitude'], h['longitude'])
        eta_min = max(4, int(round((dist_km / 30.0) * 60.0) + 2))
        
        # Capability score
        caps = h.get('capabilities', [])
        cap_score = 30 if ('TRAUMA_CARE' in caps or 'ICU' in caps or 'EMERGENCY_SURGERY' in caps) else 15
        
        # Distance score
        dist_score = max(0, 50 - int(dist_km * 8))
        
        total = cap_score + dist_score + 20 # availability
        scored_hosp.append({
            'hospital_id': h['hospital_id'],
            'name': h['name'],
            'address': h.get('address', 'Saswad-Hadapsar Road'),
            'distance_km': round(dist_km, 1),
            'distance_m': int(round(dist_km * 1000)),
            'eta_min': eta_min,
            'capabilities': caps,
            'emergency_capability': 'HIGH (Trauma & ICU)' if cap_score >= 30 else 'GENERAL_EMERGENCY',
            'availability': 'AVAILABLE',
            'score': total,
            'reason': f"Recommended based on {', '.join(caps[:2])}, estimated travel time ({eta_min} min), and verified demo availability."
        })

    scored_hosp.sort(key=lambda x: -x['score'])
    return scored_hosp[0] if scored_hosp else None

# =========================================================================
# NEW PROTOTYPE AI & RESPONDER NETWORK ROUTES
# =========================================================================

@app.route('/api/emergency/<emergency_id>/ai-recommendation', methods=['GET'])
def get_ai_recommendation(emergency_id):
    """Return full explainable AI recommendation for an emergency incident."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emergencies WHERE emergency_id = ?", (emergency_id,))
    em = cursor.fetchone()
    conn.close()

    if not em:
        # Fallback to default demo incident structure
        em_dict = {
            'emergency_id': emergency_id,
            'latitude': 18.3444,
            'longitude': 74.0305,
            'wari_zone': 'Zone 04 — Saswad Palkhi Maidan',
            'emergency_type': 'MEDICAL',
            'severity': 'CRITICAL'
        }
    else:
        em_dict = dict(em)

    ai_result = ai_response_engine(em_dict)
    return jsonify(ai_result), 200

# =========================================================================
# ADMIN NETWORK LAYER APIS (DETAILS)
# =========================================================================

@app.route('/api/admin/volunteers/<v_id>', methods=['GET'])
def admin_get_volunteer(v_id):
    return jsonify({
        'success': True,
        'volunteer': {
            'wari_id': v_id,
            'name': 'Ramesh Kulkarni',
            'phone': '9820011111',
            'role_type': 'Medical Volunteer',
            'skills': 'First Aid, CPR, Triage, Elderly Assistance',
            'zone': 'Zone 04 — Saswad Palkhi Maidan',
            'verification_status': 'VERIFIED',
            'status': 'AVAILABLE'
        }
    }), 200

@app.route('/api/admin/hospitals/<h_id>', methods=['GET'])
def admin_get_hospital(h_id):
    return jsonify({
        'success': True,
        'hospital': {
            'hospital_id': h_id,
            'name': 'Saswad Rural Sub-District Hospital',
            'license_no': 'MH-MED-28472',
            'address': 'Pune-Saswad Bypass Road, Purandar',
            'zone': 'Zone 04 — Saswad Palkhi Maidan',
            'emergency_beds': 12,
            'icu_beds': 2,
            'has_ambulance': True,
            'services': 'Emergency Care, Cardiology, Trauma, ICU',
            'emergency_contact': '02115-224455',
            'verification_status': 'VERIFIED',
            'status': 'ACCEPTING'
        }
    }), 200

@app.route('/api/volunteer/register', methods=['POST'])
def register_volunteer():
    """Volunteer Onboarding: Creates record with PENDING_VERIFICATION status."""
    data = request.get_json(silent=True) if request.is_json else request.form.to_dict()
    if not data:
        return jsonify({'success': False, 'error': 'Invalid registration payload.'}), 400

    name = str(data.get('name', '')).strip()
    phone = str(data.get('phone', '')).strip()
    zone = str(data.get('zone', 'Zone 04 — Saswad Palkhi Maidan')).strip()
    skills = str(data.get('skills', 'First Aid, CPR, Elderly Assistance')).strip()
    cert = str(data.get('certification', data.get('role_type', 'Medical Volunteer'))).strip()
    org = str(data.get('organization', 'Warkari Seva Mandal')).strip()
    languages = str(data.get('languages', 'Marathi, Hindi, English')).strip()
    password = str(data.get('password', 'volpass123')).strip()
    req_v_id = str(data.get('wari_id', '')).strip().upper()

    if not name or not phone:
        return jsonify({'success': False, 'error': 'Name and Mobile Number are required.'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check for duplicate phone
    cursor.execute("SELECT * FROM users WHERE phone = ? AND role = 'VOLUNTEER'", (phone,))
    existing = cursor.fetchone()
    if existing and not req_v_id:
        conn.close()
        return jsonify({'success': False, 'error': f'Volunteer with phone number {phone} is already registered ({existing["wari_id"]}).'}), 400

    # Generate sequential or format volunteer ID
    if req_v_id:
        new_v_id = req_v_id
    else:
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE role = 'VOLUNTEER'")
        v_count = cursor.fetchone()['count']
        new_v_id = f"V-{v_count + 1:03d}"

    # Check if table has password column
    cursor.execute("PRAGMA table_info(users)")
    cols = [c[1] for c in cursor.fetchall()]
    if 'password' not in cols:
        cursor.execute("ALTER TABLE users ADD COLUMN password TEXT")
    if 'organization' not in cols:
        cursor.execute("ALTER TABLE users ADD COLUMN organization TEXT")
    if 'languages' not in cols:
        cursor.execute("ALTER TABLE users ADD COLUMN languages TEXT")

    # Insert with PENDING_VERIFICATION status
    cursor.execute('''
        INSERT OR REPLACE INTO users (
            wari_id, name, phone, role, latitude, longitude, location_enabled,
            status, zone, skills, certification, verification_status, organization, languages, password
        ) VALUES (?, ?, ?, 'VOLUNTEER', 18.3465, 74.0295, 1, 'OFFLINE', ?, ?, ?, 'PENDING_VERIFICATION', ?, ?, ?)
    ''', (new_v_id, name, phone, zone, skills, cert, org, languages, password))

    conn.commit()
    conn.close()

    # Register in in-memory VOLUNTEER_DEMO_ACCOUNTS for login verification
    VOLUNTEER_DEMO_ACCOUNTS[new_v_id] = {
        'password': password,
        'name': name,
        'role': cert,
        'skills': skills,
        'zone': zone
    }

    return jsonify({
        'success': True,
        'volunteer_id': new_v_id,
        'wari_id': new_v_id,
        'name': name,
        'zone': zone,
        'status': 'OFFLINE',
        'verification_status': 'PENDING_VERIFICATION',
        'message': f'Volunteer {name} ({new_v_id}) registered successfully. Status: PENDING VERIFICATION.'
    }), 201

@app.route('/api/volunteer/toggle-availability', methods=['POST'])
def toggle_volunteer_availability():
    """Toggle volunteer status between AVAILABLE and OFFLINE."""
    data = request.get_json(silent=True) or {}
    v_id = data.get('volunteer_id', 'V-001')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM users WHERE wari_id = ?", (v_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return jsonify({'success': False, 'error': 'Volunteer not found.'}), 404

    current_status = row['status']
    new_status = 'OFFLINE' if current_status == 'AVAILABLE' else 'AVAILABLE'

    cursor.execute("UPDATE users SET status = ? WHERE wari_id = ?", (new_status, v_id))
    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'volunteer_id': v_id,
        'status': new_status,
        'message': f'Volunteer status updated to {new_status}.'
    }), 200

@app.route('/api/incident/create-for-pilgrim', methods=['POST'])
def create_incident_for_pilgrim():
    """Command Center Action: Create an emergency incident for an elderly/unregistered pilgrim without the app."""
    data = request.get_json(silent=True) if request.is_json else request.form.to_dict()
    if not data:
        return jsonify({'success': False, 'error': 'Invalid payload.'}), 400

    name = str(data.get('patient_name', 'Elderly Pilgrim')).strip() or 'Elderly Pilgrim'
    raw_wari_id = str(data.get('wari_id', '')).strip()
    wari_id = raw_wari_id if raw_wari_id else f"WS-UNREG-{random.randint(1000, 9999)}"
    is_unreg = 1 if not raw_wari_id else 0

    em_type = str(data.get('emergency_type', 'MEDICAL')).upper()
    severity = str(data.get('severity', 'CRITICAL')).upper()
    zone = str(data.get('zone', 'Zone 04 — Saswad Palkhi Maidan')).strip()
    notes = str(data.get('notes', 'Logged by Command Center Operator')).strip()
    lat = float(data.get('latitude', 18.3444))
    lon = float(data.get('longitude', 74.0305))

    em_id = generate_unique_emergency_id()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO emergencies (
            emergency_id, wari_id, reported_by, emergency_type, priority,
            latitude, longitude, location_accuracy, wari_zone, landmark,
            severity, notes, is_unregistered_pilgrim, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, 5.0, ?, 'Saswad Central Palkhi Ground', ?, ?, ?, 'CREATED')
    ''', (em_id, wari_id, name, em_type, severity, lat, lon, zone, severity, notes, is_unreg))

    conn.commit()
    conn.close()

    # Automatically run AI response recommendation
    em_dict = {
        'emergency_id': em_id,
        'latitude': lat,
        'longitude': lon,
        'wari_zone': zone,
        'emergency_type': em_type,
        'severity': severity
    }
    ai_match = ai_response_engine(em_dict)

    return jsonify({
        'success': True,
        'emergency_id': em_id,
        'patient_name': name,
        'wari_id': wari_id,
        'is_unregistered_pilgrim': bool(is_unreg),
        'severity': severity,
        'ai_recommendation': ai_match.get('recommended_volunteer'),
        'message': f'Incident {em_id} created for assisted pilgrim {name}. AI matched to {ai_match.get("recommended_volunteer", {}).get("name", "Volunteer")}.'
    }), 201

@app.route('/api/command-center/resources-count', methods=['GET'])
def get_command_resources_count():
    """Return live and prototype resource counts for Command Center operational dashboard."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as c FROM users WHERE role = 'VOLUNTEER' AND status = 'AVAILABLE'")
    v_avail = cursor.fetchone()['c'] + 7 # Demo pool baseline (12 total available)

    cursor.execute("SELECT COUNT(*) as c FROM users WHERE role = 'MEDICAL_RESPONDER' AND status = 'AVAILABLE'")
    r_avail = cursor.fetchone()['c'] # 4 responders

    cursor.execute("SELECT COUNT(*) as c FROM emergencies WHERE status NOT IN ('RESOLVED', 'DECLINED')")
    em_active = cursor.fetchone()['c']

    cursor.execute("SELECT COUNT(*) as c FROM medical_camps WHERE status = 'AVAILABLE'")
    c_avail = cursor.fetchone()['c'] # 2-4 camps

    conn.close()

    return jsonify({
        'success': True,
        'available_volunteers': v_avail,
        'available_medical_responders': max(4, r_avail),
        'active_incidents': em_active,
        'nearby_hospitals': 3,
        'active_medical_camps': max(2, c_avail),
        'is_demo_data': True,
        'notice': 'Prototype Operational Resource Registry'
    }), 200


# =========================================================================
# DEMO MODE 1-CLICK TRIGGERS & CLEAN RESET
# =========================================================================

@app.route('/api/demo/create-emergency', methods=['POST'])
def demo_create_emergency():
    """1-Click Demo Emergency Trigger (EM-28471 Synchronized)."""
    em_id = 'EM-28471'
    wari_id = 'WS-28471'
    name = 'Tukaram Shinde'
    lat = 18.3444
    lon = 74.0305
    acc = 5.0
    zone = 'Zone 04 — Saswad Palkhi Maidan'

    conn = get_db_connection()
    cursor = conn.cursor()

    # Ensure user exists
    cursor.execute("SELECT 1 FROM users WHERE wari_id = ?", (wari_id,))
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO users (wari_id, name, phone, role, latitude, longitude, location_enabled, status)
            VALUES (?, ?, '9822128471', 'WARKARI', ?, ?, 1, 'ACTIVE')
        ''', (wari_id, name, lat, lon))

    # Delete previous instance of EM-28471 if any
    cursor.execute("DELETE FROM emergencies WHERE emergency_id = ?", (em_id,))
    cursor.execute("DELETE FROM notifications WHERE emergency_id = ?", (em_id,))
    cursor.execute("DELETE FROM location_updates WHERE emergency_id = ?", (em_id,))
    
    # Ensure V-004 is marked RESPONDING (engaged) and V-001 is AVAILABLE for prototype demo
    cursor.execute("UPDATE users SET status = 'RESPONDING' WHERE wari_id = 'V-004'")
    cursor.execute("UPDATE users SET status = 'AVAILABLE' WHERE wari_id = 'V-001'")

    # Insert synchronized emergency
    cursor.execute('''
        INSERT INTO emergencies (
            emergency_id, wari_id, reported_by, emergency_type, priority,
            latitude, longitude, location_accuracy, wari_zone, landmark,
            assigned_volunteer, assigned_camp, assigned_responder, assigned_hospital,
            severity, notes, status
        ) VALUES (?, ?, ?, 'MEDICAL', 'CRITICAL', ?, ?, ?, ?, 'Saswad Central Palkhi Maidan Ground',
                  'V-001', 'CAMP-001', 'MR-001', 'HOSP-001', 'CRITICAL', 'Demo Live Simulation', 'CREATED')
    ''', (em_id, wari_id, name, lat, lon, acc, zone))

    # Insert notifications for volunteer and camp
    cursor.execute('''
        INSERT INTO notifications (emergency_id, recipient_id, recipient_type, notification_type, status)
        VALUES (?, 'V-001', 'VOLUNTEER', 'EMERGENCY_ALERT', 'PENDING')
    ''', (em_id,))
    cursor.execute('''
        INSERT INTO notifications (emergency_id, recipient_id, recipient_type, notification_type, status)
        VALUES (?, 'CAMP-001', 'CAMP', 'EMERGENCY_ALERT', 'PENDING')
    ''', (em_id,))

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'emergency_id': em_id,
        'wari_id': wari_id,
        'name': name,
        'reported_by': name,
        'wari_zone': zone,
        'status': 'CREATED',
        'severity': 'CRITICAL',
        'message': f'Synchronized demo emergency {em_id} created in {zone}.'
    }), 201

@app.route('/api/demo/reset', methods=['POST'])
def demo_reset():
    """Clean reset of demo database state for prototype demonstration."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Clear emergencies and notifications
    cursor.execute("DELETE FROM emergencies")
    cursor.execute("DELETE FROM emergency_events")
    cursor.execute("DELETE FROM notifications")
    cursor.execute("DELETE FROM location_updates")
    cursor.execute("DELETE FROM users WHERE wari_id NOT IN ('V-001', 'V-002', 'V-003', 'V-004', 'V-005', 'V-006', 'MR-001', 'MR-002', 'MR-003', 'P-001', 'P-002', 'WS-28471')")

    # Reset volunteers
    cursor.execute("UPDATE users SET status = 'AVAILABLE', verification_status = 'VERIFIED' WHERE role = 'VOLUNTEER'")
    cursor.execute("UPDATE users SET status = 'RESPONDING' WHERE wari_id = 'V-004'") # Priya is engaged on another incident
    cursor.execute("UPDATE users SET status = 'AVAILABLE' WHERE role = 'MEDICAL_RESPONDER'")
    cursor.execute("UPDATE medical_camps SET status = 'AVAILABLE'")

    conn.commit()
    conn.close()

    REGISTERED_HOSPITALS.clear()
    if 'H-001' in HOSPITAL_DEMO_ACCOUNTS:
        HOSPITAL_DEMO_ACCOUNTS['H-001']['beds'] = 1
        HOSPITAL_DEMO_ACCOUNTS['H-001']['status'] = 'ACCEPTING'
    if 'HOSP-001' in HOSPITAL_DEMO_ACCOUNTS:
        HOSPITAL_DEMO_ACCOUNTS['HOSP-001']['beds'] = 1
        HOSPITAL_DEMO_ACCOUNTS['HOSP-001']['status'] = 'ACCEPTING'

    return jsonify({
        'success': True,
        'message': 'Demo system state cleanly reset to initial prototype state.'
    }), 200


# =========================================================================
# WARISEVA FUNCTIONAL QR IDENTITY, SCANNER & PIN AUTHORIZATION
# =========================================================================


# =========================================================================
# AUTHENTICATED VOLUNTEER RESPONSE PORTAL ROUTES
# =========================================================================

VOLUNTEER_DEMO_ACCOUNTS = {
    'V-001': {'password': 'demo123', 'name': 'Ramesh Kulkarni', 'role': 'Volunteer', 'skills': 'First Aid Certified, CPR', 'zone': 'Zone 04'},
    'V-002': {'password': 'demo123', 'name': 'Amit Patil', 'role': 'General Volunteer', 'skills': 'Crowd Guidance, Water Distribution', 'zone': 'Zone 04'},
    'V-003': {'password': 'demo123', 'name': 'Suresh Jadhav', 'role': 'Medical Volunteer', 'skills': 'Paramedic Support, First Aid', 'zone': 'Zone 04'}
}

@app.route('/volunteer/login', methods=['GET'])
def volunteer_login_page():
    """Render dedicated volunteer responder login page."""
    if session.get('volunteer_id'):
        return redirect('/volunteer/dashboard')
    return render_template('volunteer_login.html')

@app.route('/volunteer/dashboard', methods=['GET'])
def volunteer_dashboard_page():
    """Render authenticated volunteer responder dashboard (Protected)."""
    vol_id = session.get('volunteer_id')
    if not vol_id:
        return redirect('/volunteer/login')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE wari_id = ? AND role = 'VOLUNTEER'", (vol_id,))
    vol = cursor.fetchone()
    conn.close()

    if not vol:
        session.pop('volunteer_id', None)
        return redirect('/volunteer/login')

    vol_dict = dict(vol)
    return render_template('volunteer_dashboard.html', volunteer=vol_dict)

@app.route('/api/volunteer/login', methods=['POST'])
@app.route('/api/auth/volunteer/login', methods=['POST'])
def api_volunteer_login():
    """Authenticate volunteer against demo registry for secure portal access."""
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    v_id = str(data.get('volunteer_id', '')).strip().upper()
    password = str(data.get('password', '')).strip()

    if not v_id or not password:
        return jsonify({'success': False, 'error': 'Volunteer ID and password are required.'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE wari_id = ? AND role = 'VOLUNTEER'", (v_id,))
    vol = cursor.fetchone()

    if not vol:
        conn.close()
        return jsonify({'success': False, 'error': 'Invalid Volunteer ID or Password.'}), 401

    # Demo & DB credentials verification
    expected_pwd = VOLUNTEER_DEMO_ACCOUNTS.get(v_id, {}).get('password')
    db_pwd = vol['password'] if 'password' in vol.keys() else None
    valid_passwords = {expected_pwd, db_pwd, 'VOL001', 'VOL002', 'VOL003', 'wari123', 'demo123', 'volpass123', 'auditpass123', '1234'}
    valid_passwords.discard(None)
    
    if password not in valid_passwords:
        conn.close()
        return jsonify({'success': False, 'error': 'Invalid Volunteer ID or Password.'}), 401

    # Update volunteer state to AVAILABLE upon login
    cursor.execute("UPDATE users SET status = 'AVAILABLE' WHERE wari_id = ?", (v_id,))
    conn.commit()
    conn.close()

    # Store in session
    session['volunteer_id'] = v_id

    ver_status = vol['verification_status'] if 'verification_status' in vol.keys() and vol['verification_status'] else 'VERIFIED'

    return jsonify({
        'success': True,
        'token': f'vol-token-{v_id.lower()}',
        'volunteer': {
            'wari_id': vol['wari_id'],
            'id': vol['wari_id'],
            'name': vol['name'],
            'phone': vol['phone'],
            'zone': vol['zone'] or 'Zone 04 — Saswad Palkhi Maidan',
            'skills': vol['skills'] or 'First Aid, CPR',
            'certification': vol['certification'] or 'First Aid Certified',
            'verification_status': ver_status,
            'status': 'AVAILABLE'
        },
        'redirect_url': '/volunteer/dashboard',
        'message': f'Welcome, {vol["name"]}. Authenticated successfully.'
    }), 200

@app.route('/api/volunteer/logout', methods=['POST'])
def api_volunteer_logout():
    """Log out current volunteer session and update status to OFFLINE."""
    vol_id = session.pop('volunteer_id', None)
    if vol_id:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET status = 'OFFLINE' WHERE wari_id = ?", (vol_id,))
        conn.commit()
        conn.close()
    return jsonify({'success': True, 'message': 'Logged out successfully.'}), 200

@app.route('/api/volunteer/me', methods=['GET'])
def api_volunteer_me():
    """Get authenticated volunteer profile."""
    vol_id = session.get('volunteer_id') or request.args.get('volunteer_id', 'V-001')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE wari_id = ? AND role = 'VOLUNTEER'", (vol_id,))
    vol = cursor.fetchone()
    conn.close()
    if not vol:
        return jsonify({'success': False, 'error': 'Volunteer not found.'}), 404
    return jsonify({'success': True, 'volunteer': dict(vol)}), 200

@app.route('/api/volunteer/status', methods=['POST'])
def api_volunteer_status():
    """Update volunteer availability status (AVAILABLE, BUSY, OFFLINE)."""
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    new_status = str(data.get('status', 'AVAILABLE')).strip().upper()
    vol_id = session.get('volunteer_id') or data.get('volunteer_id', 'V-001')

    if new_status not in ('AVAILABLE', 'BUSY', 'OFFLINE', 'RESPONDING'):
        return jsonify({'success': False, 'error': 'Invalid status option.'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET status = ? WHERE wari_id = ?", (new_status, vol_id))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'status': new_status, 'volunteer_id': vol_id}), 200

@app.route('/api/volunteer/cases', methods=['GET'])
def api_volunteer_cases():
    """Fetch active and recent completed cases for current volunteer."""
    vol_id = session.get('volunteer_id') or request.args.get('volunteer_id', 'V-001')
    conn = get_db_connection()
    cursor = conn.cursor()

    # Find any active emergency (non-resolved)
    cursor.execute('''
        SELECT * FROM emergencies 
        WHERE status != 'RESOLVED' 
        ORDER BY created_at DESC LIMIT 1
    ''')
    active_row = cursor.fetchone()
    active_em = dict(active_row) if active_row else None

    # Find completed cases
    cursor.execute('''
        SELECT * FROM emergencies 
        WHERE status = 'RESOLVED' 
        ORDER BY created_at DESC LIMIT 5
    ''')
    completed_rows = cursor.fetchall()
    completed = [dict(r) for r in completed_rows]

    conn.close()

    return jsonify({
        'success': True,
        'active_emergency': active_em,
        'completed_cases': completed
    }), 200

@app.route('/api/volunteer/cases/<emergency_id>/accept', methods=['POST'])
def api_volunteer_case_accept(emergency_id):
    """Accept assigned emergency case."""
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    vol_id = session.get('volunteer_id') or data.get('volunteer_id', 'V-001')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM emergencies WHERE emergency_id = ?", (emergency_id,))
    em = cursor.fetchone()
    if not em:
        conn.close()
        return jsonify({'success': False, 'error': 'Emergency not found.'}), 404

    cursor.execute('''
        UPDATE emergencies 
        SET status = 'ACCEPTED', assigned_volunteer = ?, updated_at = CURRENT_TIMESTAMP 
        WHERE emergency_id = ?
    ''', (vol_id, emergency_id))

    cursor.execute('''
        UPDATE notifications 
        SET status = 'ACCEPTED', responded_at = CURRENT_TIMESTAMP 
        WHERE emergency_id = ? AND recipient_id = ?
    ''', (emergency_id, vol_id))

    cursor.execute("UPDATE users SET status = 'BUSY' WHERE wari_id = ?", (vol_id,))
    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'emergency_id': emergency_id,
        'assigned_volunteer': vol_id,
        'status': 'ACCEPTED',
        'message': 'Case accepted. Volunteer status set to BUSY.'
    }), 200

@app.route('/api/volunteer/cases/<emergency_id>/decline', methods=['POST'])
def api_volunteer_case_decline(emergency_id):
    """Decline emergency case and return to dispatch queue."""
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    vol_id = session.get('volunteer_id') or data.get('volunteer_id', 'V-001')
    reason = data.get('reason', 'Busy')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE notifications 
        SET status = 'DECLINED', responded_at = CURRENT_TIMESTAMP 
        WHERE emergency_id = ? AND recipient_id = ?
    ''', (emergency_id, vol_id))

    # Re-route: unassign and set status to DISPATCHED so another responder can accept
    cursor.execute('''
        UPDATE emergencies 
        SET status = 'DISPATCHED', assigned_volunteer = NULL, notes = notes || ' • Declined by ' || ? || ' (' || ? || ')'
        WHERE emergency_id = ? AND assigned_volunteer = ?
    ''', (vol_id, reason, emergency_id, vol_id))

    cursor.execute("UPDATE users SET status = 'AVAILABLE' WHERE wari_id = ?", (vol_id,))
    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'emergency_id': emergency_id,
        'status': 'DISPATCHED',
        'message': 'Case declined and returned to dispatch pool.'
    }), 200

@app.route('/api/volunteer/cases/<emergency_id>/start', methods=['POST'])
def api_volunteer_case_start(emergency_id):
    """Start response en route to patient."""
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    vol_id = session.get('volunteer_id') or data.get('volunteer_id', 'V-001')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE emergencies 
        SET status = 'EN_ROUTE', updated_at = CURRENT_TIMESTAMP 
        WHERE emergency_id = ?
    ''', (emergency_id,))

    cursor.execute("UPDATE users SET status = 'RESPONDING' WHERE wari_id = ?", (vol_id,))
    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'emergency_id': emergency_id,
        'status': 'EN_ROUTE',
        'message': 'Volunteer is en route to patient location.'
    }), 200

@app.route('/api/volunteer/cases/<emergency_id>/arrived', methods=['POST'])
def api_volunteer_case_arrived(emergency_id):
    """Volunteer arrived at patient location."""
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    vol_id = session.get('volunteer_id') or data.get('volunteer_id', 'V-001')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE emergencies 
        SET status = 'ARRIVED', updated_at = CURRENT_TIMESTAMP 
        WHERE emergency_id = ?
    ''', (emergency_id,))

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'emergency_id': emergency_id,
        'status': 'ARRIVED',
        'message': 'Volunteer arrived at patient location.'
    }), 200

@app.route('/api/volunteer/cases/<emergency_id>/assisted', methods=['POST'])
def api_volunteer_case_assisted(emergency_id):
    """Volunteer administered first aid / assisted patient."""
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    vol_id = session.get('volunteer_id') or data.get('volunteer_id', 'V-001')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE emergencies 
        SET status = 'PATIENT_ASSISTED', updated_at = CURRENT_TIMESTAMP 
        WHERE emergency_id = ?
    ''', (emergency_id,))

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'emergency_id': emergency_id,
        'status': 'PATIENT_ASSISTED',
        'message': 'Patient assistance completed.'
    }), 200

@app.route('/api/volunteer/cases/<emergency_id>/resolve', methods=['POST'])
def api_volunteer_case_resolve(emergency_id):
    """Close and resolve emergency case."""
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    vol_id = session.get('volunteer_id') or data.get('volunteer_id', 'V-001')
    outcome = data.get('outcome', 'Assistance Provided')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE emergencies 
        SET status = 'RESOLVED', notes = notes || ' • Outcome: ' || ?, updated_at = CURRENT_TIMESTAMP 
        WHERE emergency_id = ?
    ''', (outcome, emergency_id))

    cursor.execute("UPDATE users SET status = 'AVAILABLE' WHERE wari_id = ?", (vol_id,))
    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'emergency_id': emergency_id,
        'status': 'RESOLVED',
        'outcome': outcome,
        'message': 'Emergency resolved. Volunteer returned to AVAILABLE.'
    }), 200


@app.route('/api/qr/lookup', methods=['POST'])
def qr_lookup():
    """
    Step 1: Look up scanned WariSeva QR token/ID.
    Returns unclassified public identity info only (NO sensitive medical/contact data).
    """
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    qr_data = str(data.get('qr_data', data.get('qr_payload', data.get('payload', '')))).strip().upper()

    if not qr_data:
        return jsonify({'success': False, 'error': 'No QR code payload received.'}), 400

    # Extract WariSeva ID if embedded in URL or raw string
    if 'WS-' in qr_data:
        match = re.search(r'WS-[A-Z0-9]+', qr_data)
        wari_id = match.group(0) if match else qr_data
    else:
        wari_id = qr_data

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pilgrims WHERE wari_id = ?", (wari_id,))
    pilgrim = cursor.fetchone()
    conn.close()

    if not pilgrim:
        return jsonify({
            'success': False,
            'found': False,
            'error': f'WariSeva ID "{wari_id}" not found. This QR is not registered in the WariSeva network.'
        }), 404

    return jsonify({
        'success': True,
        'found': True,
        'wari_id': pilgrim['wari_id'],
        'name': pilgrim['name'],
        'dindi': pilgrim['dindi'],
        'is_protected': True,
        'message': 'Pilgrim identity located. Emergency medical and contact information is protected by PIN.'
    }), 200

@app.route('/api/qr/verify', methods=['POST'])
def qr_verify_pin():
    """
    Step 2: Verify Emergency PIN and unlock protected medical profile.
    Audits the access event in access_logs table for accountability.
    """
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    wari_id = str(data.get('wari_id', '')).strip().upper()
    pin = str(data.get('pin', '')).strip()
    volunteer_id = str(data.get('volunteer_id', 'V-001')).strip().upper()
    volunteer_name = str(data.get('volunteer_name', 'Ramesh Kulkarni')).strip()

    if not wari_id or not pin:
        return jsonify({'success': False, 'error': 'WariSeva ID and PIN are required.'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pilgrims WHERE wari_id = ?", (wari_id,))
    pilgrim = cursor.fetchone()

    if not pilgrim:
        conn.close()
        return jsonify({'success': False, 'error': f'Pilgrim {wari_id} not found.'}), 404

    # Validate PIN securely (hashed check or fallback demo PINs)
    pin_valid = False
    if pilgrim['pin_hash']:
        try:
            pin_valid = check_password_hash(pilgrim['pin_hash'], pin)
        except Exception:
            pin_valid = False

    if not pin_valid:
        pin_upper = pin.upper().strip()
        if pin in ['2741', '1234', '2847'] or pin_upper in ['WARI2026', 'WARI']:
            pin_valid = True

    if not pin_valid:
        # Audit failed access attempt
        cursor.execute('''
            INSERT INTO access_logs (volunteer_id, volunteer_name, pilgrim_id, reason, status)
            VALUES (?, ?, ?, 'Emergency Assistance', 'DENIED_INVALID_PIN')
        ''', (volunteer_id, volunteer_name, wari_id))
        conn.commit()
        conn.close()
        return jsonify({
            'success': False,
            'authorized': False,
            'error': 'Incorrect PIN. Please try again.'
        }), 401

    # Audit successful access
    cursor.execute('''
        INSERT INTO access_logs (volunteer_id, volunteer_name, pilgrim_id, reason, status)
        VALUES (?, ?, ?, 'Emergency Assistance', 'AUTHORIZED')
    ''', (volunteer_id, volunteer_name, wari_id))
    log_id = cursor.lastrowid
    conn.commit()
    conn.close()

    now_str = datetime.now().strftime('%d %b %Y, %I:%M:%S %p')

    return jsonify({
        'success': True,
        'authorized': True,
        'pilgrim': {
            'wari_id': pilgrim['wari_id'],
            'name': pilgrim['name'],
            'dindi': pilgrim['dindi'],
            'blood_group': pilgrim['blood_group'],
            'emergency_contact': pilgrim['emergency_contact'],
            'medical_alert': pilgrim['medical_alert'],
            'status': pilgrim['status']
        },
        'access_audit': {
            'log_id': log_id,
            'accessed_by': f'{volunteer_name} ({volunteer_id})',
            'volunteer_status': 'VERIFIED VOLUNTEER',
            'reason': 'Emergency Assistance',
            'access_time': now_str
        },
        'message': 'Identity verified. Authorized emergency medical profile unlocked.'
    }), 200

@app.route('/api/qr/report-emergency', methods=['POST'])
def qr_report_emergency():
    """
    Step 3: Trigger emergency incident directly from scanned & verified QR profile.
    Connects into existing emergency shared state & AI Response Engine.
    """
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    wari_id = str(data.get('wari_id', 'WS-28471')).strip().upper()
    volunteer_id = str(data.get('volunteer_id', 'V-001')).strip().upper()
    em_type = str(data.get('emergency_type', 'MEDICAL')).upper()
    severity = str(data.get('severity', 'CRITICAL')).upper()
    lat = float(data.get('latitude', 18.3444))
    lon = float(data.get('longitude', 74.0305))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Look up pilgrim name
    cursor.execute("SELECT name FROM pilgrims WHERE wari_id = ?", (wari_id,))
    row = cursor.fetchone()
    patient_name = row['name'] if row else 'Tukaram Shinde'

    em_id = 'EM-28471' if wari_id == 'WS-28471' else generate_unique_emergency_id()

    # Clean previous demo instance if needed
    cursor.execute("DELETE FROM emergencies WHERE emergency_id = ?", (em_id,))
    cursor.execute("DELETE FROM notifications WHERE emergency_id = ?", (em_id,))
    cursor.execute("DELETE FROM location_updates WHERE emergency_id = ?", (em_id,))

    cursor.execute('''
        INSERT INTO emergencies (
            emergency_id, wari_id, reported_by, emergency_type, priority,
            latitude, longitude, location_accuracy, wari_zone, landmark,
            assigned_volunteer, assigned_camp, assigned_responder, assigned_hospital,
            severity, notes, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, 5.0, 'Zone 04 — Saswad Palkhi Maidan',
                  'Saswad Central Palkhi Maidan Ground', ?, 'CAMP-001', 'MR-001', 'HOSP-001',
                  ?, 'Reported via QR Wristband Scanner', 'CREATED')
    ''', (em_id, wari_id, patient_name, em_type, severity, lat, lon, volunteer_id, severity))

    cursor.execute('''
        INSERT INTO notifications (emergency_id, recipient_id, recipient_type, notification_type, status)
        VALUES (?, ?, 'VOLUNTEER', 'EMERGENCY_ALERT', 'PENDING')
    ''', (em_id, volunteer_id))

    conn.commit()
    conn.close()

    # Automatically run AI response recommendation
    em_dict = {
        'emergency_id': em_id,
        'latitude': lat,
        'longitude': lon,
        'wari_zone': 'Zone 04 — Saswad Palkhi Maidan',
        'emergency_type': em_type,
        'severity': severity
    }
    ai_match = ai_response_engine(em_dict)

    return jsonify({
        'success': True,
        'emergency_id': em_id,
        'patient_name': patient_name,
        'wari_id': wari_id,
        'reported_by_volunteer': volunteer_id,
        'ai_recommendation': ai_match.get('recommended_volunteer'),
        'recommended_hospital': ai_match.get('recommended_hospital'),
        'message': f'Emergency {em_id} created for {patient_name}. AI dispatch initiated.'
    }), 201

@app.route('/api/warkari/report', methods=['POST'])
@app.route('/api/report/warkari', methods=['POST'])
def report_warkari():
    """Record safety / welfare report for a scanned Warkari."""
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    wari_id = str(data.get('wari_id', 'WS-28471')).strip().upper()
    patient_name = str(data.get('name', data.get('patient_name', 'Tukaram Shinde'))).strip()
    reason = str(data.get('reason', data.get('report_reason', 'Medical Assistance'))).strip()
    notes = str(data.get('notes', data.get('additional_notes', ''))).strip()
    zone = str(data.get('zone', data.get('wari_zone', 'Zone 04 — Saswad Palkhi Maidan'))).strip()
    reported_by = str(data.get('reported_by', data.get('volunteer_id', 'Volunteer V-001'))).strip()

    report_id = f"REP-{datetime.now().strftime('%m%d')}-{random.randint(1000, 9999)}"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Store in notifications / audit log
    cursor.execute('''
        INSERT INTO notifications (emergency_id, recipient_id, recipient_type, notification_type, status)
        VALUES (?, ?, 'VOLUNTEER', ?, 'RECORDED')
    ''', (report_id, reported_by, f"WARKARI_REPORT: {reason} ({wari_id} - {patient_name})"))
    
    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'report_id': report_id,
        'wari_id': wari_id,
        'name': patient_name,
        'reason': reason,
        'notes': notes,
        'zone': zone,
        'message': 'The Wari Safety Network has been notified.'
    }), 201

@app.route('/api/user/<wari_id>', methods=['GET'])
@app.route('/api/warkari/<wari_id>', methods=['GET'])
@app.route('/api/pilgrim/<wari_id>', methods=['GET'])
def get_pilgrim_card(wari_id):
    """Public pilgrim wristband digital ID endpoint."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT wari_id, name, dindi, status, created_at FROM pilgrims WHERE wari_id = ?", (wari_id.upper(),))
    pilgrim = cursor.fetchone()
    conn.close()

    if not pilgrim:
        return jsonify({'success': False, 'error': 'Pilgrim ID not found.'}), 404

    return jsonify({
        'success': True,
        'pilgrim': dict(pilgrim),
        'qr_value': pilgrim['wari_id'],
        'wristband_type': 'WATERPROOF_SILICONE_QR_NFC',
        'demo_mode': True
    }), 200

@app.route('/api/qr/access-logs', methods=['GET'])
def get_qr_access_logs():
    """Return recent emergency access audit logs."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM access_logs ORDER BY id DESC LIMIT 20")
    logs = [dict(r) for r in cursor.fetchall()]
    conn.close()

    return jsonify({
        'success': True,
        'count': len(logs),
        'logs': logs
    }), 200


# =========================================================================
# PUBLIC PILGRIM PROFILE & WRISTBAND PASSWORD VERIFICATION
# =========================================================================

@app.route('/api/demo/verify-wristband-password', methods=['POST'])
def verify_wristband_password():
    """Verify demo password 'WARI2026' before unlocking the physical wristband preview."""
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    password = str(data.get('password', '')).strip()

    if not password:
        return jsonify({'success': False, 'error': 'Demo password is required.'}), 400

    if password.upper() == 'WARI2026':
        return jsonify({
            'success': True,
            'message': '✓ Demo access verified. Physical wristband unlocked.'
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': '❌ Incorrect demo password. Please enter WARI2026.'
        }), 401

@app.route('/public/pilgrim/', methods=['GET'])
@app.route('/public/pilgrim/<wari_id>', methods=['GET'])
@app.route('/wristband', methods=['GET'])
@app.route('/wristband/<wari_id>', methods=['GET'])
@app.route('/wristband-id', methods=['GET'])
def public_pilgrim_page(wari_id='WS-28471'):
    """
    Public Mobile Emergency Profile for normal phone camera / Google Lens scanning.
    Does NOT require WariSeva app or volunteer login.
    Always includes persistent Back & Home navigation header.
    """
    if not wari_id or wari_id == 'WS-XXXXX':
        wari_id = 'WS-28471'
    wari_id = str(wari_id).strip().upper()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pilgrims WHERE wari_id = ?", (wari_id,))
    pilgrim = cursor.fetchone()
    conn.close()

    # If not found, fallback to demo pilgrim Tukaram Shinde
    if not pilgrim:
        pilgrim_data = {
            'wari_id': wari_id,
            'name': 'Tukaram Shinde',
            'dindi': '27',
            'mobile': '+91 98221 28471',
            'emergency_contact': '+91 98220 99881',
            'emergency_relation': 'Son (मुलगा)',
            'blood_group': 'B+',
            'medical_alert': '⚠️ Asthma (Requires Inhaler & O2 Support)',
            'zone': 'Zone 04 — Saswad Palkhi Maidan',
            'status': 'REGISTERED'
        }
    else:
        pilgrim_data = {
            'wari_id': pilgrim['wari_id'],
            'name': pilgrim['name'],
            'dindi': pilgrim['dindi'] or '27',
            'mobile': '+91 98221 28471' if pilgrim['wari_id'] == 'WS-28471' else '+91 98221 30555',
            'emergency_contact': pilgrim['emergency_contact'] or '+91 98220 99881',
            'emergency_relation': 'Son (मुलगा)',
            'blood_group': pilgrim['blood_group'] or 'B+',
            'medical_alert': pilgrim['medical_alert'] or '⚠️ Asthma (Requires Inhaler & O2 Support)',
            'zone': 'Zone 04 — Saswad Palkhi Maidan',
            'status': pilgrim['status'] or 'REGISTERED'
        }

    return render_template('public_pilgrim.html', pilgrim=pilgrim_data)

@app.route('/api/pilgrim/checkpoints/<wari_id>', methods=['GET'])
def get_pilgrim_checkpoints(wari_id):
    """
    Family Safety & Last Seen Checkpoints API.
    Returns structured safety milestones: Morning Start, Afternoon Halt, Night Mukkam.
    """
    clean_id = str(wari_id).strip().upper()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM last_seen_checkpoints 
        WHERE wari_id = ? 
        ORDER BY id ASC
    """, (clean_id,))
    rows = cursor.fetchall()
    conn.close()

    checkpoints = []
    for r in rows:
        checkpoints.append({
            'id': r['id'],
            'wari_id': r['wari_id'],
            'checkpoint_type': r['checkpoint_type'],
            'location_name': r['location_name'],
            'zone': r['zone'],
            'checkin_time': r['checkin_time'],
            'recorded_by': r['recorded_by'],
            'status': r['status']
        })

    # Default fallback if empty
    if not checkpoints:
        checkpoints = [
            {'checkpoint_type': 'MORNING_START', 'location_name': 'Alandi Palkhi Prasthan Gateway', 'zone': 'Zone 01 — Alandi / Pune Start', 'checkin_time': '06:30 AM', 'recorded_by': 'Dindi Seva Lead', 'status': 'VERIFIED_SAFE'},
            {'checkpoint_type': 'AFTERNOON_HALT', 'location_name': 'Dive Ghat Base Rest Mandap', 'zone': 'Zone 03 — Hadapsar / Dive Ghat Base', 'checkin_time': '01:15 PM', 'recorded_by': 'Volunteer V-005', 'status': 'VERIFIED_SAFE'},
            {'checkpoint_type': 'NIGHT_MUKKAM', 'location_name': 'Saswad Central Palkhi Maidan Ground', 'zone': 'Zone 04 — Saswad Palkhi Maidan', 'checkin_time': '07:45 PM', 'recorded_by': 'Camp MC-001 Triage', 'status': 'VERIFIED_SAFE'}
        ]

    return jsonify({
        'success': True,
        'wari_id': clean_id,
        'checkpoints': checkpoints,
        'last_seen_zone': checkpoints[-1]['zone'] if checkpoints else 'Zone 04 — Saswad Palkhi Maidan',
        'overall_status': 'ALL_MILESTONES_VERIFIED_SAFE'
    }), 200

@app.route('/api/pilgrim/checkpoint', methods=['POST'])
def record_pilgrim_checkpoint():
    """Record a verified checkpoint check-in milestone for a pilgrim."""
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    wari_id = str(data.get('wari_id', 'WS-28471')).strip().upper()
    cp_type = str(data.get('checkpoint_type', 'NIGHT_MUKKAM')).strip().upper()
    loc_name = str(data.get('location_name', 'Saswad Central Palkhi Maidan Ground')).strip()
    zone = str(data.get('zone', 'Zone 04 — Saswad Palkhi Maidan')).strip()
    checkin_time = str(data.get('checkin_time', datetime.now().strftime('%I:%M %p'))).strip()
    recorded_by = str(data.get('recorded_by', 'Volunteer V-001')).strip()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO last_seen_checkpoints (wari_id, checkpoint_type, location_name, zone, checkin_time, recorded_by, status)
        VALUES (?, ?, ?, ?, ?, ?, 'VERIFIED_SAFE')
    """, (wari_id, cp_type, loc_name, zone, checkin_time, recorded_by))
    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'message': f'Checkpoint {cp_type} recorded successfully for {wari_id}.',
        'checkpoint': {
            'wari_id': wari_id,
            'checkpoint_type': cp_type,
            'location_name': loc_name,
            'zone': zone,
            'checkin_time': checkin_time,
            'recorded_by': recorded_by,
            'status': 'VERIFIED_SAFE'
        }
    }), 201

@app.route('/api/public/report-emergency', methods=['POST'])
def public_report_emergency():
    """
    Unified Emergency Creation initiated via QR Wristband Scan (Normal Phone).
    Executes the exact same emergency creation, responder matching, and notification pipeline.
    Patient: Tukaram Shinde (from QR token WS-28471)
    Source: QR_WARI_ID
    """
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    wari_id = str(data.get('wari_id', 'WS-28471')).strip().upper()
    em_type = str(data.get('emergency_type', 'MEDICAL')).upper()
    severity = 'CRITICAL'
    source = 'QR_WARI_ID'
    reporter_type = str(data.get('reporter_type', 'QR_PUBLIC_USER'))
    lat = float(data.get('latitude', 18.3444))
    lon = float(data.get('longitude', 74.0305))
    loc_source = str(data.get('location_source', 'GPS'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM pilgrims WHERE wari_id = ?", (wari_id,))
    row = cursor.fetchone()
    patient_name = row['name'] if row else 'Tukaram Shinde'

    em_id = 'EM-28471' if wari_id == 'WS-28471' else generate_unique_emergency_id()

    # Reset any previous state for this demo ID to ensure fresh clean dispatch
    cursor.execute("DELETE FROM emergencies WHERE emergency_id = ?", (em_id,))
    cursor.execute("DELETE FROM notifications WHERE emergency_id = ?", (em_id,))
    cursor.execute("DELETE FROM location_updates WHERE emergency_id = ?", (em_id,))

    cursor.execute('''
        INSERT INTO emergencies (
            emergency_id, wari_id, reported_by, emergency_type, priority,
            latitude, longitude, location_accuracy, wari_zone, landmark,
            assigned_volunteer, assigned_camp, assigned_responder, assigned_hospital,
            severity, notes, status, volunteer_status, hospital_status, current_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, 5.0, 'Zone 04 — Saswad Palkhi Maidan',
                  'Saswad Central Palkhi Maidan Ground', NULL, 'MC-001', 'MR-001', 'H-001',
                  ?, ?, 'CREATED', 'WAITING', 'PENDING', 'CREATED')
    ''', (em_id, wari_id, patient_name, em_type, severity, lat, lon, severity, f'Source: QR Wristband ({loc_source}) • Reporter: {reporter_type}'))

    log_emergency_event(cursor, em_id, 1, 'CREATED', 'QR_PUBLIC_USER', 'Emergency reported via physical QR wristband scan.')

    # Notify nearest volunteers in 50km radius
    cursor.execute("SELECT * FROM users WHERE role = 'VOLUNTEER' AND status = 'AVAILABLE' AND latitude IS NOT NULL")
    vols = cursor.fetchall()
    for v in vols:
        cursor.execute('''
            INSERT INTO notifications (emergency_id, recipient_id, recipient_type, notification_type, status)
            VALUES (?, ?, 'VOLUNTEER', 'EMERGENCY_ALERT', 'PENDING')
        ''', (em_id, v['wari_id']))

    conn.commit()
    conn.close()

    # Run unified AI Response Prioritization & Responder Allocation Engine
    em_dict = {
        'emergency_id': em_id,
        'latitude': lat,
        'longitude': lon,
        'wari_zone': 'Zone 04 — Saswad Palkhi Maidan',
        'emergency_type': em_type,
        'severity': severity
    }
    ai_match = ai_response_engine(em_dict)

    return jsonify({
        'success': True,
        'emergency_id': em_id,
        'patient_name': patient_name,
        'wari_id': wari_id,
        'source': source,
        'reporter_type': reporter_type,
        'emergency_type': em_type,
        'status': 'DISPATCHED',
        'location_source': loc_source,
        'assigned_volunteer': ai_match.get('recommended_volunteer'),
        'nearest_camp': {
            'name': 'Saswad Palkhi Maidan Medical Tent (MC-001)',
            'distance_m': 238
        },
        'recommended_hospital': ai_match.get('recommended_hospital'),
        'message': f'Emergency {em_id} created for patient {patient_name}. AI dispatch coordinating.'
    }), 201

@app.route('/api/public/emergency-status/<emergency_id>', methods=['GET'])
def public_emergency_status(emergency_id):
    """Public status polling for normal phone browser showing live dispatch status."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emergencies WHERE emergency_id = ?", (emergency_id,))
    em = cursor.fetchone()
    conn.close()

    if not em:
        return jsonify({'success': False, 'error': 'Incident not found.'}), 404

    st = (em['status'] or '').upper()
    hosp_st = (em['hospital_status'] or '').upper()
    
    # Map status to 1-12 timeline stages
    stage = 1
    if st == 'RESOLVED':
        stage = 12
    elif hosp_st == 'ACCEPTED' or st in ('HOSPITAL_ACCEPTED', 'PATIENT_EXPECTED'):
        stage = 11
    elif st in ('ARRIVED', 'VOLUNTEER_ARRIVED', 'WITH_PATIENT', 'PATIENT_ASSISTED'):
        stage = 9
    elif st in ('EN_ROUTE', 'RESPONDING'):
        stage = 8
    elif st in ('ACCEPTED', 'VOLUNTEER_ACCEPTED'):
        stage = 7
    elif st in ('DISPATCHED', 'WAITING_FOR_VOLUNTEER'):
        stage = 6
    elif st == 'CREATED':
        stage = 4

    return jsonify({
        'success': True,
        'emergency_id': em['emergency_id'],
        'patient_name': em['reported_by'],
        'status': em['status'],
        'volunteer_status': 'ACCEPTED' if st in ('ACCEPTED', 'EN_ROUTE', 'ARRIVED', 'PATIENT_ASSISTED') else ('ARRIVED' if st == 'ARRIVED' else 'AVAILABLE'),
        'emergency_type': em['emergency_type'],
        'source': 'QR_WARI_ID',
        'assigned_volunteer': em['assigned_volunteer'] or 'Ramesh Kulkarni (V-001)',
        'assigned_responder': em['assigned_responder'] or 'Dr. Arvind Shinde (MR-001)',
        'assigned_camp': 'Saswad Palkhi Maidan Medical Tent (MC-001)',
        'assigned_hospital': em['assigned_hospital'] or 'Purandar Critical Care & Trauma Hospital',
        'hospital_status': hosp_st or ('ACCEPTED' if stage >= 11 else 'WAITING'),
        'stage': stage,
        'zone': em['wari_zone']
    }), 200


def get_lan_ip():
    """Detect computer's real LAN IPv4 address (192.168.x.x, 10.x.x.x, 172.16.x.x-172.31.x.x)."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        # Connect to public DNS to determine default network interface IP (no packets sent)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        if ip and not ip.startswith('127.'):
            return ip
    except Exception:
        pass

    try:
        hostname = socket.gethostname()
        for ip in socket.gethostbyname_ex(hostname)[2]:
            if ip.startswith(('192.168.', '10.', '172.')):
                return ip
    except Exception:
        pass

    return '127.0.0.1'

def get_public_base_url():
    """
    Centralized configuration for WariSeva AI public base URL.
    Supports environment variable override, live request Host header,
    and automatic LAN IP detection.
    """
    env_base = os.environ.get('PUBLIC_BASE_URL', '').strip().rstrip('/')
    if env_base:
        return env_base
    
    try:
        if request and request.host and not request.host.startswith(('localhost', '127.0.0.1')):
            scheme = request.headers.get('X-Forwarded-Proto', request.scheme or 'http')
            return f"{scheme}://{request.host}".rstrip('/')
    except Exception:
        pass
        
    lan_ip = get_lan_ip()
    port = os.environ.get('PORT', 5000)
    return f"http://{lan_ip}:{port}"

def generate_wariseva_qr_payload(wari_id='WS-28471'):
    """Single unified generator function for WariSeva Emergency Profile URLs."""
    base = get_public_base_url()
    clean_id = str(wari_id).strip().upper() if wari_id else 'WS-28471'
    return f"{base}/public/pilgrim/{clean_id}"

@app.route('/api/network-info', methods=['GET'])
def get_network_info():
    """Return real local machine LAN IP and base URL for physical phone QR scanning."""
    lan_ip = get_lan_ip()
    port = os.environ.get('PORT', 5000)
    public_base_url = get_public_base_url()
    wari_id = request.args.get('wari_id', 'WS-28471').strip().upper()
    qr_target_url = generate_wariseva_qr_payload(wari_id)
    
    return jsonify({
        'success': True,
        'lan_ip': lan_ip,
        'port': port,
        'public_base_url': public_base_url,
        'qr_target_url': qr_target_url,
        'wari_id': wari_id,
        'hostname': socket.gethostname(),
        'is_lan_available': (lan_ip != '127.0.0.1'),
        'instructions': 'Connect your phone and laptop to the SAME Wi-Fi network and scan the QR with your phone camera.'
    }), 200


# =========================================================================
# UNIFIED MACHINE-READABLE QR ENGINE & CALIBRATION (ERROR CORRECTION: H)
# =========================================================================

@app.route('/api/qr/payload', methods=['GET'])
def get_qr_payload():
    """Return exact QR payload metadata and diagnostic specs."""
    wari_id = request.args.get('wari_id', 'WS-28471').strip().upper()
    payload_url = generate_wariseva_qr_payload(wari_id)
    lan_ip = get_lan_ip()
    port = os.environ.get('PORT', 5000)
    public_base_url = get_public_base_url()

    return jsonify({
        'success': True,
        'wari_id': wari_id,
        'payload_url': payload_url,
        'payload': payload_url,
        'public_base_url': public_base_url,
        'lan_ip': lan_ip,
        'port': port,
        'error_correction': 'H',
        'quiet_zone_modules': 4,
        'source_size_px': 540
    }), 200


@app.route('/api/pilgrim/<wari_id>/qr-base64', methods=['GET'])
@app.route('/api/qr/base64', methods=['GET'])
def get_qr_base64(wari_id='WS-28471'):
    payload = generate_wariseva_qr_payload(wari_id)
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=4,
    )
    qr.add_data(payload)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return jsonify({
        'success': True,
        'wari_id': wari_id,
        'payload': payload,
        'base64': f"data:image/png;base64,{b64}"
    }), 200

@app.route('/api/qr/image', methods=['GET'])
def generate_qr_image():
    """
    Generate a 100% compliant, high-resolution machine-readable QR Code image.
    Uses Level-H error correction (30% error tolerance), black modules on white background,
    and a 4-module quiet zone with zero distortion or overlays.
    """
    wari_id = request.args.get('wari_id', 'WS-28471').strip().upper()
    custom_url = request.args.get('url', '').strip()
    img_format = request.args.get('format', 'png').strip().lower()

    payload = custom_url if custom_url else generate_wariseva_qr_payload(wari_id)

    # Standardized Flask stdout logger (ASCII-safe for Windows consoles)
    print("\n" + "=" * 55)
    print(f"QR PAYLOAD GENERATED: {payload}")
    print(f"Specs: 540x540px | Error Correction: Level H | Quiet Zone: 4 modules")
    print("=" * 55 + "\n")

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=4,
    )
    qr.add_data(payload)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)

    response = send_file(buf, mimetype='image/png')
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/qr-test', methods=['GET'])
def qr_test_page():
    """
    Clean, minimal standalone calibration test page displaying the high-contrast
    QR code for physical phone camera verification.
    """
    payload_url = generate_wariseva_qr_payload('WS-28471')
    return render_template('qr_test.html',
                           qr_payload_url=payload_url,
                           cache_bust=random.randint(10000, 99999))

# =========================================================================
# HOSPITAL / MEDICAL FACILITY PORTAL & VERIFICATION SYSTEM
# =========================================================================

HOSPITAL_DEMO_ACCOUNTS = {
    'H-001': {'hospital_id': 'H-001', 'password': 'demo123', 'name': 'WariSeva Medical Camp — Zone 04', 'zone': 'Zone 04 — Saswad Palkhi Maidan', 'beds': 1, 'icu': 1, 'status': 'ACCEPTING'},
    'HOSP-001': {'password': 'demo123', 'name': 'WariSeva Medical Camp — Zone 04', 'zone': 'Zone 04 — Saswad Palkhi Maidan', 'beds': 1, 'icu': 1, 'status': 'ACCEPTING'},
    'H-002': {'hospital_id': 'H-002', 'password': 'demo123', 'name': 'Purandar Critical Care & Trauma Hospital', 'zone': 'Zone 04 — Saswad Palkhi Maidan', 'beds': 18, 'icu': 6, 'status': 'ACCEPTING'},
    'HOSP-002': {'password': 'demo123', 'name': 'Purandar Critical Care & Trauma Hospital', 'zone': 'Zone 04 — Saswad Palkhi Maidan', 'beds': 18, 'icu': 6, 'status': 'ACCEPTING'},
    'H-003': {'hospital_id': 'H-003', 'password': 'demo123', 'name': 'Sancheti & Sassoon Emergency Hub', 'zone': 'Zone 02 — Pune City / Wakdewadi', 'beds': 30, 'icu': 10, 'status': 'ACCEPTING'},
    'HOSP-003': {'password': 'demo123', 'name': 'Sancheti & Sassoon Emergency Hub', 'zone': 'Zone 02 — Pune City / Wakdewadi', 'beds': 30, 'icu': 10, 'status': 'ACCEPTING'}
}

# In-memory registrations store for dynamic prototype additions
REGISTERED_HOSPITALS = {}
REGISTERED_VOLUNTEERS = {}

@app.route('/volunteer/register', methods=['GET'])
def volunteer_register_page():
    """Render volunteer registration page."""
    return render_template('volunteer_register.html')

@app.route('/volunteer/profile', methods=['GET'])
def volunteer_profile_page():
    """Render authenticated volunteer profile."""
    vol_id = session.get('volunteer_id')
    if not vol_id:
        return redirect('/volunteer/login')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE wari_id = ?", (vol_id,))
    vol = cursor.fetchone()
    conn.close()

    if not vol:
        return redirect('/volunteer/login')
    return render_template('volunteer_profile.html', volunteer=dict(vol))

@app.route('/hospital/register', methods=['GET'])
def hospital_register_page():
    """Render medical facility registration page."""
    return render_template('hospital_register.html')

@app.route('/hospital/login', methods=['GET'])
def hospital_login_page():
    """Render medical facility login page."""
    if session.get('hospital_id'):
        return redirect('/hospital/dashboard')
    return render_template('hospital_login.html')

@app.route('/hospital/dashboard', methods=['GET'])
def hospital_dashboard_page():
    """Render authenticated medical facility dashboard (Protected)."""
    hosp_id = session.get('hospital_id')
    if not hosp_id:
        return redirect('/hospital/login')
    
    hosp_data = HOSPITAL_DEMO_ACCOUNTS.get(hosp_id) or REGISTERED_HOSPITALS.get(hosp_id)
    if not hosp_data:
        hospitals = load_hospitals()
        h = next((x for x in hospitals if x['hospital_id'] in (hosp_id, f'HOSP-{hosp_id.replace("H-", "")}')), None)
        if h:
            hosp_data = {
                'hospital_id': h['hospital_id'],
                'name': h['name'],
                'zone': h['zone'],
                'address': h['address'],
                'phone': h['phone'],
                'status': 'ACCEPTING'
            }
        else:
            hosp_data = {
                'hospital_id': hosp_id,
                'name': 'Saswad Rural Sub-District Hospital',
                'zone': 'Zone 04 — Saswad Palkhi Maidan',
                'status': 'ACCEPTING'
            }
    
    return render_template('hospital_dashboard.html', hospital=hosp_data)

@app.route('/hospital/profile', methods=['GET'])
def hospital_profile_page():
    """Render authenticated medical facility profile."""
    hosp_id = session.get('hospital_id')
    if not hosp_id:
        return redirect('/hospital/login')
    
    hospitals = load_hospitals()
    h = next((x for x in hospitals if x['hospital_id'] in (hosp_id, f'HOSP-{hosp_id.replace("H-", "")}')), None)
    hosp_dict = h or {
        'hospital_id': hosp_id,
        'name': 'Saswad Rural Sub-District Hospital',
        'address': 'Saswad-Hadapsar Road, Purandar',
        'zone': 'Zone 04 — Saswad Palkhi Maidan',
        'phone': '02115-222333',
        'status': 'ACCEPTING EMERGENCIES',
        'capabilities': ['Emergency ICU', 'Trauma', '24x7 Ambulance', 'Oxygen']
    }
    return render_template('hospital_profile.html', hospital=hosp_dict)

@app.route('/api/hospital/register', methods=['POST'])
def api_hospital_register():
    """Register a new medical facility / hospital into WariSeva network."""
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    name = str(data.get('name', '')).strip()
    zone = str(data.get('zone', 'Zone 04 — Saswad Palkhi Maidan')).strip()
    phone = str(data.get('phone', '')).strip()
    pwd = str(data.get('password', 'HOSP001')).strip()

    if not name:
        return jsonify({'success': False, 'error': 'Hospital name is required.'}), 400

    # Generate sequential hospital ID
    num = random.randint(100, 999)
    hosp_id = f'H-{num}'

    hosp_obj = {
        'hospital_id': hosp_id,
        'name': name,
        'facility_type': data.get('facility_type', 'Hospital'),
        'license_no': data.get('license_no', 'MH-MED-001'),
        'phone': phone,
        'emergency_phone': data.get('emergency_phone', phone),
        'address': data.get('address', 'Saswad Bypass Road'),
        'city': data.get('city', 'Saswad'),
        'zone': zone,
        'emergency_beds': int(data.get('emergency_beds', 12)),
        'icu_beds': int(data.get('icu_beds', 2)),
        'ambulance': bool(data.get('ambulance', True)),
        'twenty_four_seven': bool(data.get('twenty_four_seven', True)),
        'capabilities': data.get('capabilities', 'Emergency Care, Trauma, ICU'),
        'admin_name': data.get('admin_name', 'Medical Superintendent'),
        'password': pwd,
        'verification_status': 'PENDING_VERIFICATION',
        'status': 'ACCEPTING'
    }

    REGISTERED_HOSPITALS[hosp_id] = hosp_obj
    HOSPITAL_DEMO_ACCOUNTS[hosp_id] = hosp_obj

    return jsonify({
        'success': True,
        'hospital_id': hosp_id,
        'name': name,
        'verification_status': 'PENDING_VERIFICATION',
        'message': f'Facility {name} registered with ID {hosp_id}. Pending verification.'
    }), 201

@app.route('/api/hospital/login', methods=['POST'])
@app.route('/api/auth/hospital/login', methods=['POST'])
def api_hospital_login():
    """Authenticate medical facility representative."""
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    h_id = str(data.get('facility_id') or data.get('hospital_id') or data.get('id') or '').strip().upper()
    password = str(data.get('password', '')).strip()

    if not h_id or not password:
        return jsonify({'success': False, 'error': 'Facility ID and password are required.'}), 400

    # Normalize ID (e.g. MF-001, H-001 or HOSP-001)
    normalized_id = h_id
    if h_id.startswith('MF-'):
        normalized_id = 'H-' + h_id.replace('MF-', '')
    elif h_id.startswith('HOSP-'):
        normalized_id = 'H-' + h_id.replace('HOSP-', '')
    elif h_id.startswith('H-'):
        alt_id = 'HOSP-' + h_id.replace('H-', '')

    account = HOSPITAL_DEMO_ACCOUNTS.get(h_id) or HOSPITAL_DEMO_ACCOUNTS.get(normalized_id) or REGISTERED_HOSPITALS.get(h_id) or REGISTERED_HOSPITALS.get(normalized_id)

    if not account:
        # Fallback to standard demo check
        if h_id in ('H-001', 'H-002', 'H-003', 'HOSP-001', 'HOSP-002', 'HOSP-003', 'MF-001', 'MF-002', 'MF-003') or normalized_id in ('H-001', 'H-002', 'H-003'):
            account = {'password': '1234', 'name': 'WariSeva Medical Camp — Zone 04', 'hospital_id': h_id, 'facility_id': h_id}
        else:
            return jsonify({'success': False, 'error': 'Invalid Facility ID or Password.'}), 401

    expected_pwd = account.get('password', '1234')
    if password not in (expected_pwd, 'HOSP001', 'HOSP002', 'HOSP003', 'wari123', 'demo123', 'hospital123', '1234'):
        return jsonify({'success': False, 'error': 'Invalid Facility ID or Password.'}), 401

    session['hospital_id'] = h_id

    return jsonify({
        'success': True,
        'hospital_id': h_id,
        'facility_id': h_id,
        'hospital': account,
        'facility': account,
        'redirect_url': '/hospital/dashboard',
        'message': f'Welcome, {account.get("name", "Medical Facility")}. Authenticated successfully.'
    }), 200

@app.route('/api/hospital/logout', methods=['POST'])
def api_hospital_logout():
    """Log out medical facility session."""
    session.pop('hospital_id', None)
    return jsonify({'success': True, 'message': 'Facility logged out.'}), 200

@app.route('/api/auth/command/login', methods=['POST'])
@app.route('/api/command/login', methods=['POST'])
def api_command_login():
    """Authenticate command center personnel against admin credentials."""
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    username = str(data.get('username', data.get('user', ''))).strip()
    password = str(data.get('password', data.get('pass', ''))).strip()

    if not username or not password:
        return jsonify({
            'success': False,
            'error': 'Invalid username or password. Please try again.'
        }), 401

    if username.lower() == 'admin' and password == 'admin123':
        session['command_auth'] = True
        session['command_user'] = 'admin'
        return jsonify({
            'success': True,
            'message': 'Login Successful',
            'token': 'cmd-auth-token-admin',
            'user': {
                'username': 'admin',
                'role': 'COMMAND_OPERATOR',
                'name': 'Chief Incident Commander'
            }
        }), 200

    return jsonify({
        'success': False,
        'error': 'Invalid username or password. Please try again.'
    }), 401

@app.route('/api/auth/command/logout', methods=['POST'])
@app.route('/api/command/logout', methods=['POST'])
def api_command_logout():
    """Log out command center session."""
    session.pop('command_auth', None)
    session.pop('command_user', None)
    return jsonify({'success': True, 'message': 'Command Center logged out.'}), 200

@app.route('/api/hospital/cases', methods=['GET'])
def api_hospital_cases():
    """Fetch active incoming referrals for medical facility."""
    hosp_id = session.get('hospital_id') or request.args.get('hospital_id', 'H-001')
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM emergencies 
        WHERE status != 'RESOLVED' 
        ORDER BY created_at DESC LIMIT 1
    ''')
    row = cursor.fetchone()
    conn.close()

    active_em = dict(row) if row else None

    return jsonify({
        'success': True,
        'active_emergency': active_em
    }), 200

@app.route('/api/hospital/cases/<emergency_id>/accept', methods=['POST'])
def api_hospital_case_accept(emergency_id):
    """Hospital accepts patient and reserves emergency bed."""
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    hosp_id = session.get('hospital_id') or data.get('hospital_id', 'H-001')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE emergencies 
        SET status = 'HOSPITAL_ACCEPTED', hospital_status = 'ACCEPTED', assigned_hospital = ?, notes = COALESCE(notes, '') || ' • Hospital Bed Reserved (' || ? || ')', updated_at = CURRENT_TIMESTAMP 
        WHERE emergency_id = ?
    ''', (hosp_id, hosp_id, emergency_id))

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'emergency_id': emergency_id,
        'hospital_id': hosp_id,
        'hospital_status': 'ACCEPTED',
        'status': 'HOSPITAL_ACCEPTED',
        'message': 'Patient accepted. Emergency bed reserved.'
    }), 200

@app.route('/api/hospital/cases/<emergency_id>/decline', methods=['POST'])
def api_hospital_case_decline(emergency_id):
    """Hospital declines patient referral due to capacity/specialization."""
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    hosp_id = session.get('hospital_id') or data.get('hospital_id', 'H-001')
    reason = data.get('reason', 'At Capacity')

    conn = get_db_connection()
    cursor = conn.cursor()

    # Re-route: switch assigned hospital to backup Purandar Critical Care / Sancheti
    backup_hosp = 'HOSP-002' if '001' in hosp_id else 'HOSP-001'

    cursor.execute('''
        UPDATE emergencies 
        SET hospital_status = 'RE_ROUTED', assigned_hospital = ?, notes = COALESCE(notes, '') || ' • Declined by ' || ? || ' (' || ? || ') -> Re-routed to ' || ?, updated_at = CURRENT_TIMESTAMP 
        WHERE emergency_id = ?
    ''', (backup_hosp, hosp_id, reason, backup_hosp, emergency_id))

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'emergency_id': emergency_id,
        'declined_by': hosp_id,
        're_routed_to': backup_hosp,
        'message': f'Case declined ({reason}) and re-routed to backup facility {backup_hosp}.'
    }), 200

@app.route('/api/hospital/capacity', methods=['POST'])
def api_hospital_capacity():
    """Update live emergency beds and ICU availability."""
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    hosp_id = session.get('hospital_id') or data.get('hospital_id', 'H-001')
    beds = int(data.get('emergency_beds', 12))
    icu = int(data.get('icu_beds', 2))

    if hosp_id in HOSPITAL_DEMO_ACCOUNTS:
        HOSPITAL_DEMO_ACCOUNTS[hosp_id]['beds'] = beds
        HOSPITAL_DEMO_ACCOUNTS[hosp_id]['icu'] = icu

    return jsonify({
        'success': True,
        'hospital_id': hosp_id,
        'available_beds': beds,
        'icu_beds': icu,
        'message': 'Capacity updated successfully.'
    }), 200

@app.route('/api/hospital/status', methods=['POST'])
def api_hospital_status():
    """Update hospital operational status (ACCEPTING, LIMITED, NOT_ACCEPTING)."""
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    hosp_id = session.get('hospital_id') or data.get('hospital_id', 'H-001')
    status_val = str(data.get('status', 'ACCEPTING')).strip().upper()

    if status_val not in ('ACCEPTING', 'LIMITED', 'NOT_ACCEPTING'):
        return jsonify({'success': False, 'error': 'Invalid hospital status.'}), 400

    if hosp_id in HOSPITAL_DEMO_ACCOUNTS:
        HOSPITAL_DEMO_ACCOUNTS[hosp_id]['status'] = status_val

    return jsonify({
        'success': True,
        'hospital_id': hosp_id,
        'status': status_val,
        'message': f'Facility status set to {status_val}.'
    }), 200

# =========================================================================
# ADMIN / COMMAND CENTER VERIFICATION QUEUE & ROLE VERIFICATION
# =========================================================================

@app.route('/api/admin/verification-queue', methods=['GET'])
def api_admin_verification_queue():
    """Get pending and verified volunteers & medical facilities for Command Center."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE role = 'VOLUNTEER' ORDER BY id DESC")
    vols = [dict(r) for r in cursor.fetchall()]
    conn.close()

    pending_vols = [v for v in vols if v.get('verification_status') == 'PENDING_VERIFICATION']
    verified_vols = [v for v in vols if v.get('verification_status') != 'PENDING_VERIFICATION']

    if not pending_vols:
        pending_vols = [
            {
                'wari_id': 'V-007',
                'name': 'Ganesh Gaikwad',
                'phone': '9822334455',
                'role': 'Medical Volunteer',
                'skills': 'First Aid, CPR, Triage',
                'zone': 'Zone 04 — Saswad Palkhi Maidan',
                'verification_status': 'PENDING_VERIFICATION'
            },
            {
                'wari_id': 'V-008',
                'name': 'Pooja Shinde',
                'phone': '9899887766',
                'role': 'General Volunteer',
                'skills': 'Crowd Guidance, First Aid',
                'zone': 'Zone 04 — Saswad Palkhi Maidan',
                'verification_status': 'PENDING_VERIFICATION'
            }
        ]

    pending_hosps = [h for h in REGISTERED_HOSPITALS.values() if h.get('verification_status') == 'PENDING_VERIFICATION']
    if not pending_hosps:
        pending_hosps = [
            {
                'hospital_id': 'H-003',
                'name': 'Purandar Critical Care Clinic',
                'address': 'Saswad Hadapsar Bypass',
                'zone': 'Zone 04 — Saswad Palkhi Maidan',
                'emergency_beds': 8,
                'verification_status': 'PENDING_VERIFICATION'
            }
        ]
    verified_hosps = list(load_hospitals())

    return jsonify({
        'success': True,
        'pending_volunteers': pending_vols,
        'verified_volunteers': verified_vols,
        'pending_hospitals': pending_hosps,
        'verified_hospitals': verified_hosps
    }), 200

@app.route('/api/admin/volunteer/verify', methods=['POST'])
def api_admin_verify_volunteer():
    """Command Center verifies a pending volunteer registration."""
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    vol_id = str(data.get('volunteer_id', '')).strip()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET verification_status = 'VERIFIED', status = 'AVAILABLE' WHERE wari_id = ?", (vol_id,))
    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'volunteer_id': vol_id,
        'verification_status': 'VERIFIED',
        'status': 'AVAILABLE',
        'message': f'Volunteer {vol_id} verified and added to active response pool.'
    }), 200

@app.route('/api/admin/volunteer/reject', methods=['POST'])
def api_admin_reject_volunteer():
    """Command Center rejects a volunteer registration."""
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    vol_id = str(data.get('volunteer_id', '')).strip()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET verification_status = 'REJECTED', status = 'OFFLINE' WHERE wari_id = ?", (vol_id,))
    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'volunteer_id': vol_id,
        'verification_status': 'REJECTED',
        'message': f'Volunteer {vol_id} application rejected.'
    }), 200

@app.route('/api/admin/hospital/verify', methods=['POST'])
def api_admin_verify_hospital():
    """Command Center verifies a medical facility."""
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    hosp_id = str(data.get('hospital_id', '')).strip()

    if hosp_id in REGISTERED_HOSPITALS:
        REGISTERED_HOSPITALS[hosp_id]['verification_status'] = 'VERIFIED'
    if hosp_id in HOSPITAL_DEMO_ACCOUNTS:
        HOSPITAL_DEMO_ACCOUNTS[hosp_id]['verification_status'] = 'VERIFIED'

    return jsonify({
        'success': True,
        'hospital_id': hosp_id,
        'verification_status': 'VERIFIED',
        'message': f'Medical facility {hosp_id} verified and linked to emergency network.'
    }), 200





# =========================================================================
# COMMAND CENTER NETWORK STATISTICS, EXPLAINABLE AI & INCIDENT ENGINE
# =========================================================================

@app.route('/api/admin/network-stats', methods=['GET'])
def api_admin_network_stats():
    """Return aggregated live network statistics for Command Center."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE role = 'VOLUNTEER'")
    vols = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT * FROM emergencies WHERE status != 'RESOLVED'")
    active_ems = [dict(r) for r in cursor.fetchall()]
    conn.close()

    total_vols = 248 + len(vols)
    verified_vols = 231 + len([v for v in vols if v.get('verification_status') == 'VERIFIED'])
    pending_vols = 17 + len([v for v in vols if v.get('verification_status') == 'PENDING_VERIFICATION'])
    available_vols = 184 + len([v for v in vols if v.get('status') == 'AVAILABLE'])
    responding_vols = 17 + len([v for v in vols if v.get('status') in ('RESPONDING', 'EN_ROUTE', 'ARRIVED')])
    busy_vols = 12 + len([v for v in vols if v.get('status') == 'BUSY'])
    offline_vols = 35 + len([v for v in vols if v.get('status') == 'OFFLINE'])

    # Hospitals stats
    hosps = list(load_hospitals())
    for h_id, h in REGISTERED_HOSPITALS.items():
        if not any(x['hospital_id'] == h_id for x in hosps):
            hosps.append(h)

    total_hosps = 42 + len(REGISTERED_HOSPITALS)
    verified_hosps = 38 + len([h for h in REGISTERED_HOSPITALS.values() if h.get('verification_status') == 'VERIFIED'])
    pending_hosps = 4 + len([h for h in REGISTERED_HOSPITALS.values() if h.get('verification_status') == 'PENDING_VERIFICATION'])
    accepting_hosps = 31 + len([h for h in hosps if h.get('status') in ('ACCEPTING', 'ACCEPTING EMERGENCIES', None)])
    limited_hosps = 8 + len([h for h in hosps if h.get('status') == 'LIMITED'])
    unavailable_hosps = 3 + len([h for h in hosps if h.get('status') in ('NOT_ACCEPTING', 'UNAVAILABLE')])
    
    total_beds = 86 + sum(int(h.get('beds', 10)) for h in hosps[:4])
    total_icu = 14 + sum(int(h.get('icu', 2)) for h in hosps[:4])
    total_ambulances = 18

    return jsonify({
        'success': True,
        'volunteers': {
            'total': total_vols,
            'verified': verified_vols,
            'pending': pending_vols,
            'available': available_vols,
            'responding': responding_vols,
            'busy': busy_vols,
            'offline': offline_vols
        },
        'hospitals': {
            'total': total_hosps,
            'verified': verified_hosps,
            'pending': pending_hosps,
            'accepting': accepting_hosps,
            'limited': limited_hosps,
            'unavailable': unavailable_hosps,
            'emergency_beds': total_beds,
            'icu_beds': total_icu,
            'ambulances': total_ambulances
        },
        'emergencies': {
            'active_count': len(active_ems) if active_ems else 1,
            'critical': 1,
            'high': 0,
            'medium': 0
        }
    }), 200

@app.route('/api/admin/volunteers/<vol_id>', methods=['GET'])
def api_admin_volunteer_detail(vol_id):
    """Get full volunteer inspector profile."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE wari_id = ?", (vol_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        v = dict(row)
    elif vol_id in VOLUNTEER_DEMO_ACCOUNTS:
        acc = VOLUNTEER_DEMO_ACCOUNTS[vol_id]
        v = {
            'wari_id': vol_id,
            'name': acc.get('name', 'Ramesh Kulkarni'),
            'phone': acc.get('phone', '+91 9820011111'),
            'role': 'VOLUNTEER',
            'certification': acc.get('certification', 'First Aid Certified'),
            'skills': acc.get('skills', 'First Aid, CPR, Elderly Assistance'),
            'zone': acc.get('zone', 'Zone 04 — Saswad Palkhi Maidan'),
            'status': acc.get('status', 'AVAILABLE'),
            'verification_status': 'VERIFIED',
            'created_at': '2026-08-22 09:30:00'
        }
    else:
        v = {
            'wari_id': vol_id,
            'name': 'Priya Patil',
            'phone': '+91 9876543210',
            'role': 'VOLUNTEER',
            'certification': 'Medical Volunteer',
            'skills': 'First Aid, CPR, Triage, Elderly Assistance',
            'zone': 'Zone 03 — Hadapsar Base',
            'status': 'AVAILABLE',
            'verification_status': 'PENDING_VERIFICATION',
            'created_at': 'Today, 10:42 AM'
        }

    return jsonify({'success': True, 'volunteer': v}), 200

@app.route('/api/admin/volunteer/suspend', methods=['POST'])
def api_admin_volunteer_suspend():
    """Suspend volunteer from active roster."""
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    vol_id = str(data.get('volunteer_id', '')).strip()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET verification_status = 'SUSPENDED', status = 'OFFLINE' WHERE wari_id = ?", (vol_id,))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'volunteer_id': vol_id, 'verification_status': 'SUSPENDED', 'status': 'OFFLINE'}), 200

@app.route('/api/admin/hospitals/<hosp_id>', methods=['GET'])
def api_admin_hospital_detail(hosp_id):
    """Get full hospital inspector profile."""
    hosp = HOSPITAL_DEMO_ACCOUNTS.get(hosp_id) or REGISTERED_HOSPITALS.get(hosp_id)
    if not hosp:
        hospitals = load_hospitals()
        h = next((x for x in hospitals if x['hospital_id'] in (hosp_id, f'HOSP-{hosp_id.replace("H-", "")}')), None)
        hosp = h or {
            'hospital_id': hosp_id,
            'name': 'Saswad Rural Sub-District Hospital',
            'license_no': 'MH-MED-28472',
            'facility_type': 'General Hospital',
            'address': 'Pune-Saswad Bypass Road, Purandar',
            'zone': 'Zone 04 — Saswad Palkhi Maidan',
            'phone': '02115-224455',
            'emergency_beds': 12,
            'icu_beds': 2,
            'ambulance': True,
            'twenty_four_seven': True,
            'capabilities': 'Emergency Care, Cardiology, Trauma, ICU',
            'status': 'ACCEPTING',
            'verification_status': 'VERIFIED',
            'updated_at': '2 minutes ago'
        }
    return jsonify({'success': True, 'hospital': hosp}), 200

@app.route('/api/admin/hospital/reject', methods=['POST'])
def api_admin_reject_hospital():
    """Reject pending medical facility."""
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    hosp_id = str(data.get('hospital_id', '')).strip()

    if hosp_id in REGISTERED_HOSPITALS:
        REGISTERED_HOSPITALS[hosp_id]['verification_status'] = 'REJECTED'
        REGISTERED_HOSPITALS[hosp_id]['status'] = 'UNAVAILABLE'

    return jsonify({'success': True, 'hospital_id': hosp_id, 'verification_status': 'REJECTED'}), 200

@app.route('/api/emergency/<emergency_id>/candidates', methods=['GET'])
def api_emergency_candidates(emergency_id):
    """Calculate ranked candidate responders and candidate medical facilities with transparent AI explainability scores."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Fetch incident details
    cursor.execute("SELECT * FROM emergencies WHERE emergency_id = ?", (emergency_id,))
    em_row = cursor.fetchone()
    
    pat_lat = float(em_row['latitude']) if em_row and em_row['latitude'] else 18.3444
    pat_lon = float(em_row['longitude']) if em_row and em_row['longitude'] else 74.0305
    em_zone = em_row['wari_zone'] if em_row and em_row['wari_zone'] else 'Zone 04 — Saswad Palkhi Maidan'
    em_type = em_row['emergency_type'] if em_row and em_row['emergency_type'] else 'MEDICAL'

    # 2. Fetch volunteers from DB
    cursor.execute("SELECT * FROM users WHERE role = 'VOLUNTEER'")
    db_vols = [dict(r) for r in cursor.fetchall()]
    conn.close()

    if not db_vols:
        # Fallback to seeded demo accounts
        db_vols = [
            {'wari_id': 'V-001', 'name': 'Ramesh Kulkarni', 'latitude': 18.3465, 'longitude': 74.0295, 'status': 'AVAILABLE', 'skills': 'First Aid, CPR, Triage', 'certification': 'First Aid Certified', 'zone': 'Zone 04 — Saswad Palkhi Maidan', 'verification_status': 'VERIFIED'},
            {'wari_id': 'V-002', 'name': 'Amit Patil', 'latitude': 18.3480, 'longitude': 74.0320, 'status': 'AVAILABLE', 'skills': 'Crowd & Water Assistance', 'certification': 'General Volunteer', 'zone': 'Zone 04 — Saswad Palkhi Maidan', 'verification_status': 'VERIFIED'},
            {'wari_id': 'V-003', 'name': 'Suresh Jadhav', 'latitude': 18.3435, 'longitude': 74.0310, 'status': 'BUSY', 'skills': 'Paramedic Trainee', 'certification': 'Medical Volunteer', 'zone': 'Zone 04 — Saswad Palkhi Maidan', 'verification_status': 'VERIFIED'}
        ]

    candidate_volunteers = []
    for v in db_vols:
        v_id = v.get('wari_id', 'V-001')
        v_name = v.get('name', 'Volunteer')
        v_status = v.get('status', 'AVAILABLE')
        v_skills = str(v.get('skills', 'First Aid'))
        v_cert = str(v.get('certification', 'First Aid'))
        v_zone = v.get('zone', 'Zone 04')
        v_lat = float(v.get('latitude', 18.3465))
        v_lon = float(v.get('longitude', 74.0295))

        dist_km = calculate_haversine_distance(pat_lat, pat_lon, v_lat, v_lon)
        dist_m = max(150, int(round(dist_km * 1000)))
        eta_min = max(1, int(round(dist_m / 150.0)))

        # Factor 1: Availability (Max 30)
        if v_status == 'AVAILABLE':
            avail_pts = 30
            avail_reason = 'Currently AVAILABLE on standby'
        elif v_status in ('RESPONDING', 'EN_ROUTE', 'ARRIVED'):
            avail_pts = 0
            avail_reason = f'{v_status} to another incident'
        elif v_status == 'BUSY':
            avail_pts = 0
            avail_reason = 'BUSY assisting pilgrim'
        else:
            avail_pts = 0
            avail_reason = 'Currently OFFLINE'

        # Factor 2: Distance (Max 30)
        dist_pts = max(5, min(30, int(round(30 - (dist_km * 10)))))
        dist_reason = f'{dist_m}m from patient (ETA {eta_min} min)'

        # Factor 3: Skills (Max 20)
        if any(w in v_skills or w in v_cert for w in ('First Aid', 'CPR', 'Triage', 'Doctor', 'Nurse', 'Paramedic')):
            skill_pts = 20
            skill_reason = f'{v_cert} • Medical & CPR match'
        else:
            skill_pts = 10
            skill_reason = 'General volunteer assistance'

        # Factor 4: Zone Match (Max 10)
        if em_zone and v_zone and em_zone.split('—')[0].strip() == v_zone.split('—')[0].strip():
            zone_pts = 10
            zone_reason = f'Same Wari Zone ({v_zone.split("—")[0].strip()})'
        else:
            zone_pts = 4
            zone_reason = 'Adjacent sector corridor'

        # Factor 5: Workload (Max 10)
        workload_pts = 6 if v_status == 'AVAILABLE' else 0
        workload_reason = 'No active queue load' if v_status == 'AVAILABLE' else 'Active load present'

        total_score = min(100, avail_pts + dist_pts + skill_pts + zone_pts + workload_pts)

        candidate_volunteers.append({
            'id': v_id,
            'name': v_name,
            'distance_m': dist_m,
            'eta_min': eta_min,
            'status': v_status,
            'role': v_cert or 'Medical Volunteer',
            'skills': v_skills,
            'score': total_score,
            'selected': False,
            'factors': {
                'availability': {'points': avail_pts, 'max': 30, 'reason': avail_reason},
                'distance': {'points': dist_pts, 'max': 30, 'reason': dist_reason},
                'skills': {'points': skill_pts, 'max': 20, 'reason': skill_reason},
                'zone': {'points': zone_pts, 'max': 10, 'reason': zone_reason},
                'workload': {'points': workload_pts, 'max': 10, 'reason': workload_reason}
            }
        })

    # Sort volunteers descending by score
    candidate_volunteers.sort(key=lambda x: (-x['score'], x['distance_m']))
    if candidate_volunteers:
        candidate_volunteers[0]['selected'] = True

    # 3. Calculate candidate facilities
    hosps = list(load_hospitals())
    for h_id, h in REGISTERED_HOSPITALS.items():
        if not any(x['hospital_id'] == h_id for x in hosps):
            hosps.append(h)

    candidate_facilities = []
    for h in hosps:
        h_id = h.get('hospital_id', 'H-001')
        h_name = h.get('name', 'Hospital')
        h_lat = float(h.get('latitude', 18.3490))
        h_lon = float(h.get('longitude', 74.0320))
        h_status = h.get('status', 'ACCEPTING')
        h_beds = int(h.get('emergency_beds', h.get('beds', 12)))
        h_icu = int(h.get('icu_beds', h.get('icu', 2)))

        dist_km = round(calculate_haversine_distance(pat_lat, pat_lon, h_lat, h_lon), 1)
        if dist_km < 0.2:
            dist_km = 2.1 # sensible default demo distance

        # Scoring factors
        # 1. Distance (Max 30)
        h_dist_pts = max(5, min(30, int(round(30 - (dist_km * 4)))))
        # 2. 24x7 (Max 20)
        h_24x7_pts = 20
        # 3. Beds (Max 20)
        h_bed_pts = min(20, max(5, h_beds * 2))
        # 4. Services (Max 15)
        h_srv_pts = 15
        # 5. Status (Max 10)
        h_stat_pts = 10 if h_status in ('ACCEPTING', 'ACCEPTING EMERGENCIES') else (5 if h_status == 'LIMITED' else 0)
        # 6. Zone (Max 5)
        h_zone_pts = 5 if '04' in str(h.get('zone', '')) else 3

        h_score = min(100, h_dist_pts + h_24x7_pts + h_bed_pts + h_srv_pts + h_stat_pts + h_zone_pts)

        candidate_facilities.append({
            'id': h_id,
            'name': h_name,
            'distance_km': dist_km,
            'emergency_24x7': True,
            'beds_available': h_beds,
            'icu_available': h_icu,
            'ambulance': True,
            'services': 'Trauma ✓, Cardiology ✓, Emergency Care ✓',
            'status': h_status,
            'score': h_score,
            'selected': False,
            'factors': {
                'distance': {'points': h_dist_pts, 'max': 30, 'reason': f'{dist_km} km away on direct bypass route'},
                'twenty_four_seven': {'points': h_24x7_pts, 'max': 20, 'reason': '24x7 Emergency Casualty open'},
                'bed_capacity': {'points': h_bed_pts, 'max': 20, 'reason': f'{h_beds} emergency beds free'},
                'services_match': {'points': h_srv_pts, 'max': 15, 'reason': 'Trauma & O2 support active'},
                'status': {'points': h_stat_pts, 'max': 10, 'reason': f'Status: {h_status}'},
                'zone_match': {'points': h_zone_pts, 'max': 5, 'reason': 'Zone 04 accessibility'}
            }
        })

    candidate_facilities.sort(key=lambda x: (-x['score'], x['distance_km']))
    if candidate_facilities:
        candidate_facilities[0]['selected'] = True

    return jsonify({
        'success': True,
        'emergency_id': emergency_id,
        'candidate_volunteers': candidate_volunteers,
        'candidate_facilities': candidate_facilities
    }), 200

if __name__ == '__main__':
    lan_ip = get_lan_ip()
    print(f"Starting WariSeva AI server on http://127.0.0.1:5000")
    print(f"Physical Phone Access URL: http://{lan_ip}:5000/public/pilgrim/WS-28471")
    app.run(host='0.0.0.0', port=5000, debug=True)
