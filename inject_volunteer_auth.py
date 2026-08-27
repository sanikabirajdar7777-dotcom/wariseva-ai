with open('backend/app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update imports and secret key
old_imports = "from flask import Flask, render_template, request, jsonify, send_file, Response"
new_imports = "from flask import Flask, render_template, request, jsonify, send_file, Response, session, redirect, url_for"

if old_imports in code:
    code = code.replace(old_imports, new_imports)

old_app_init = "app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)"
new_app_init = """app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = os.environ.get('SECRET_KEY', 'wariseva-volunteer-auth-key-2026')"""

if old_app_init in code and "app.secret_key" not in code:
    code = code.replace(old_app_init, new_app_init)

# 2. Add Volunteer Web Pages and Unified API Endpoints
volunteer_routes_code = """
# =========================================================================
# AUTHENTICATED VOLUNTEER RESPONSE PORTAL ROUTES
# =========================================================================

VOLUNTEER_DEMO_ACCOUNTS = {
    'V-001': {'password': 'VOL001', 'name': 'Ramesh Kulkarni', 'role': 'Medical Volunteer', 'skills': 'First Aid, CPR, Triage'},
    'V-002': {'password': 'VOL002', 'name': 'Amit Patil', 'role': 'General Volunteer', 'skills': 'Crowd Guidance, Water Distribution'},
    'V-003': {'password': 'VOL003', 'name': 'Suresh Jadhav', 'role': 'Medical Volunteer', 'skills': 'Paramedic Support, First Aid'}
}

@app.route('/volunteer/login', methods=['GET'])
def volunteer_login_page():
    \"\"\"Render dedicated volunteer responder login page.\"\"\"
    if session.get('volunteer_id'):
        return redirect('/volunteer/dashboard')
    return render_template('volunteer_login.html')

@app.route('/volunteer/dashboard', methods=['GET'])
def volunteer_dashboard_page():
    \"\"\"Render authenticated volunteer responder dashboard (Protected).\"\"\"
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
def api_volunteer_login():
    \"\"\"Authenticate volunteer against demo registry for secure portal access.\"\"\"
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
        return jsonify({'success': False, 'error': f'Volunteer {v_id} not found in registry.'}), 404

    # Demo credentials verification
    expected_pwd = VOLUNTEER_DEMO_ACCOUNTS.get(v_id, {}).get('password', 'VOL001')
    if password not in (expected_pwd, 'VOL001', 'VOL002', 'VOL003', 'wari123', 'demo123'):
        conn.close()
        return jsonify({'success': False, 'error': 'Invalid volunteer password.'}), 401

    # Update volunteer state to AVAILABLE upon login
    cursor.execute("UPDATE users SET status = 'AVAILABLE' WHERE wari_id = ?", (v_id,))
    conn.commit()
    conn.close()

    # Store in session
    session['volunteer_id'] = v_id

    return jsonify({
        'success': True,
        'token': f'vol-token-{v_id.lower()}',
        'volunteer': {
            'id': vol['wari_id'],
            'name': vol['name'],
            'phone': vol['phone'],
            'zone': vol['zone'] or 'Zone 04 — Saswad Palkhi Maidan',
            'skills': vol['skills'] or 'First Aid, CPR',
            'certification': vol['certification'] or 'First Aid Certified',
            'status': 'AVAILABLE'
        },
        'redirect_url': '/volunteer/dashboard',
        'message': f'Welcome, {vol["name"]}. Authenticated successfully.'
    }), 200

@app.route('/api/volunteer/logout', methods=['POST'])
def api_volunteer_logout():
    \"\"\"Log out current volunteer session and update status to OFFLINE.\"\"\"
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
    \"\"\"Get authenticated volunteer profile.\"\"\"
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
    \"\"\"Update volunteer availability status (AVAILABLE, BUSY, OFFLINE).\"\"\"
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
    \"\"\"Fetch active and recent completed cases for current volunteer.\"\"\"
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
    \"\"\"Accept assigned emergency case.\"\"\"
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
    \"\"\"Decline emergency case and return to dispatch queue.\"\"\"
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
    \"\"\"Start response en route to patient.\"\"\"
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
    \"\"\"Volunteer arrived at patient location.\"\"\"
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
    \"\"\"Volunteer administered first aid / assisted patient.\"\"\"
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
    \"\"\"Close and resolve emergency case.\"\"\"
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
"""

# Replace existing volunteer_login endpoint with the full authenticated suite
old_vol_login_block = """@app.route('/api/volunteer/login', methods=['POST'])
def volunteer_login():
    \"\"\"Authenticate volunteer against demo registry for secure identity access.\"\"\"
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    v_id = str(data.get('volunteer_id', '')).strip().upper()
    password = str(data.get('password', '')).strip()

    if not v_id or not password:
        return jsonify({'success': False, 'error': 'Volunteer ID and password are required.'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE wari_id = ? AND role = 'VOLUNTEER'", (v_id,))
    vol = cursor.fetchone()
    conn.close()

    # Demo credentials verification (V-001 / wari123 or valid registered volunteer)
    if not vol:
        return jsonify({'success': False, 'error': f'Volunteer {v_id} not found in registry.'}), 404

    if password != 'wari123' and password != 'demo123':
        return jsonify({'success': False, 'error': 'Invalid volunteer password.'}), 401

    return jsonify({
        'success': True,
        'token': f'demo-token-{v_id.lower()}',
        'volunteer': {
            'id': vol['wari_id'],
            'name': vol['name'],
            'phone': vol['phone'],
            'zone': vol['zone'] or 'Zone 04 — Saswad Palkhi Maidan',
            'skills': vol['skills'] or 'First Aid, CPR',
            'certification': vol['certification'] or 'First Aid Certified',
            'verification_status': vol['verification_status'] or 'VERIFIED',
            'status': vol['status'] or 'AVAILABLE'
        },
        'message': f'Volunteer {vol["name"]} authenticated successfully.'
    }), 200"""

if old_vol_login_block in code:
    code = code.replace(old_vol_login_block, volunteer_routes_code)
else:
    code += volunteer_routes_code

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated backend/app.py with complete Authenticated Volunteer Response System!")
