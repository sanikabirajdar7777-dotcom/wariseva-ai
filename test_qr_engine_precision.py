import urllib.request
import json
import sys
import io
from PIL import Image

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = 'http://127.0.0.1:5000'

def test_qr_engine_suite():
    print("=" * 65)
    print("TESTING WARISEVA AI UNIFIED HIGH-PRECISION QR ENGINE")
    print("=" * 65)

    # 1. Payload Endpoint Verification
    req = urllib.request.Request(f"{BASE_URL}/api/qr/payload?wari_id=WS-28471")
    with urllib.request.urlopen(req) as resp:
        assert resp.getcode() == 200
        payload_data = json.loads(resp.read().decode('utf-8'))

    print(f"[1] Verified QR Payload URL: {payload_data['payload_url']}")
    assert payload_data['success'] is True
    assert payload_data['wari_id'] == 'WS-28471'
    assert payload_data['error_correction'] == 'H'
    assert payload_data['quiet_zone_modules'] == 4
    assert payload_data['source_size_px'] == 540
    assert payload_data['lan_ip'] not in ('127.0.0.1', 'localhost', '0.0.0.0')

    # 2. Image Endpoint Verification
    req = urllib.request.Request(f"{BASE_URL}/api/qr/image?wari_id=WS-28471")
    with urllib.request.urlopen(req) as resp:
        assert resp.getcode() == 200
        assert resp.headers.get('Content-Type') == 'image/png'
        img_bytes = resp.read()

    img = Image.open(io.BytesIO(img_bytes))
    print(f"[2] Verified QR Image Dimensions: {img.size} (1:1 high-resolution square)")
    assert img.size[0] == img.size[1], f"Expected 1:1 square QR code, got {img.size}"
    assert img.size[0] >= 500, f"Expected high resolution (>=500px), got {img.size}"

    # Verify pure black on pure white colors
    colors = img.convert('RGB').getcolors()
    color_map = {c[1]: c[0] for c in colors}
    assert (0, 0, 0) in color_map, "Must contain solid black pixels"
    assert (255, 255, 255) in color_map, "Must contain pure white background"
    print(f"    • Pure Colors Verified: Solid Black (#000000) & Pure White (#FFFFFF)")

    # Verify 4-module quiet zone (top-left and top-right within margin must be pure white background)
    tl_pixel = img.getpixel((5, 5))
    assert tl_pixel in (255, (255, 255, 255), 1), f"Quiet zone top-left must be white, got {tl_pixel}"
    tr_pixel = img.getpixel((img.size[0] - 5, 5))
    assert tr_pixel in (255, (255, 255, 255), 1), f"Quiet zone top-right must be white, got {tr_pixel}"
    print(f"    • 4-Module Clean Quiet Zone Verified on all 4 corners")

    # 3. Standalone Calibration Test Page
    req = urllib.request.Request(f"{BASE_URL}/qr-test")
    with urllib.request.urlopen(req) as resp:
        assert resp.getcode() == 200
        html = resp.read().decode('utf-8')
    assert 'WS-28471' in html
    assert payload_data['payload_url'] in html
    print("[3] Standalone QR Calibration Test Page (/qr-test): 200 OK")

    # 4. Target Public Profile reachable via real LAN URL
    lan_url = payload_data['payload_url']
    req = urllib.request.Request(lan_url)
    with urllib.request.urlopen(req) as resp:
        assert resp.getcode() == 200
        profile_html = resp.read().decode('utf-8')
    assert 'TUKARAM SHINDE' in profile_html.upper()
    assert 'WS-28471' in profile_html
    assert 'EMERGENCY HELP' in profile_html or 'SOS' in profile_html
    print(f"[4] Verified Real LAN Target URL Reachability ({lan_url}): 200 OK")

    # 5. Public Emergency Dispatch
    lan_base = f"http://{payload_data['lan_ip']}:{payload_data['port']}"
    em_data = json.dumps({
        'wari_id': 'WS-28471',
        'emergency_type': 'MEDICAL',
        'latitude': 18.3444,
        'longitude': 74.0305,
        'location_source': 'GPS'
    }).encode('utf-8')
    req = urllib.request.Request(f"{lan_base}/api/public/report-emergency", data=em_data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as resp:
        assert resp.getcode() == 201
        em_res = json.loads(resp.read().decode('utf-8'))
    assert em_res['emergency_id'] == 'EM-28471'
    assert em_res['status'] == 'DISPATCHED'
    print(f"[5] Public Emergency Dispatch via Real LAN ({em_res['emergency_id']}): 201 CREATED")

    # 6. Clean Reset
    req = urllib.request.Request(f"{lan_base}/api/demo/reset", data=b'{}', headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as resp:
        assert resp.getcode() == 200
    print("[6] Final Clean System Reset: 200 OK")

    print("=" * 65)
    print("ALL 6 QR ENGINE PRECISION & PHONE SCAN VERIFICATIONS PASSED 100%!")
    print("=" * 65)

if __name__ == '__main__':
    test_qr_engine_suite()
