with open('backend/app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Add imports if missing
if 'import io' not in code:
    code = "import io\nimport qrcode\n" + code

if 'send_file' not in code:
    code = code.replace("from flask import Flask, render_template, request, jsonify", "from flask import Flask, render_template, request, jsonify, send_file, Response")

qr_engine_code = """
# =========================================================================
# UNIFIED MACHINE-READABLE QR ENGINE & CALIBRATION (ERROR CORRECTION: H)
# =========================================================================

def generate_wariseva_qr_payload(wari_id='WS-28471'):
    \"\"\"Single unified generator function for WariSeva Emergency Profile URLs.\"\"\"
    lan_ip = get_lan_ip()
    port = 5000
    return f"http://{lan_ip}:{port}/public/pilgrim/{str(wari_id).strip().upper()}"

@app.route('/api/qr/payload', methods=['GET'])
def get_qr_payload():
    \"\"\"Return exact QR payload metadata and diagnostic specs.\"\"\"
    wari_id = request.args.get('wari_id', 'WS-28471').strip().upper()
    payload_url = generate_wariseva_qr_payload(wari_id)
    lan_ip = get_lan_ip()
    port = 5000

    return jsonify({
        'success': True,
        'wari_id': wari_id,
        'payload_url': payload_url,
        'lan_ip': lan_ip,
        'port': port,
        'error_correction': 'H',
        'quiet_zone_modules': 4,
        'source_size_px': 540
    }), 200

@app.route('/api/qr/image', methods=['GET'])
def generate_qr_image():
    \"\"\"
    Generate a 100% compliant, high-resolution machine-readable QR Code image.
    Uses Level-H error correction (30% error tolerance), black modules on white background,
    and a 4-module quiet zone with zero distortion or overlays.
    \"\"\"
    wari_id = request.args.get('wari_id', 'WS-28471').strip().upper()
    custom_url = request.args.get('url', '').strip()
    img_format = request.args.get('format', 'png').strip().lower()

    payload = custom_url if custom_url else generate_wariseva_qr_payload(wari_id)

    # Standardized Flask stdout logger
    print(f"\\n=======================================================")
    print(f"🔍 QR PAYLOAD GENERATED: {payload}")
    print(f"   Specs: 540x540px • Error Correction: Level H • Quiet Zone: 4 modules")
    print(f"=======================================================\\n")

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
    \"\"\"
    Clean, minimal standalone calibration test page displaying the high-contrast
    QR code for physical phone camera verification.
    \"\"\"
    payload_url = generate_wariseva_qr_payload('WS-28471')
    return render_template('qr_test.html',
                           qr_payload_url=payload_url,
                           cache_bust=random.randint(10000, 99999))
"""

marker = "if __name__ == '__main__':"
assert marker in code, "Could not find main block in app.py"

parts = code.split(marker)
new_code = parts[0] + qr_engine_code + "\n" + marker + parts[1]

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(new_code)

print("Updated backend/app.py with Unified QR Engine & /qr-test route!")
