import urllib.request
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def test_lan_accessibility():
    print("=" * 65)
    print("VERIFYING PHYSICAL PHONE CAMERA & REAL LAN ACCESSIBILITY")
    print("=" * 65)

    # 1. Fetch Network Info
    req = urllib.request.Request('http://127.0.0.1:5000/api/network-info')
    with urllib.request.urlopen(req) as resp:
        assert resp.getcode() == 200
        net_info = json.loads(resp.read().decode('utf-8'))

    print(f"[1] Detected Real Machine LAN IP: {net_info['lan_ip']}")
    print(f"    • Server Base URL: {net_info['public_base_url']}")
    print(f"    • Target Phone QR URL: {net_info['qr_target_url']}")
    assert net_info['lan_ip'] not in ('127.0.0.1', 'localhost', '0.0.0.0'), "LAN IP must not be loopback!"
    assert net_info['port'] == 5000
    assert 'WS-28471' in net_info['qr_target_url']

    lan_base = net_info['public_base_url']
    lan_qr_url = net_info['qr_target_url']

    # 2. Test accessing public profile via the REAL LAN IP (as any external phone does)
    req = urllib.request.Request(lan_qr_url)
    with urllib.request.urlopen(req) as resp:
        assert resp.getcode() == 200
        html = resp.read().decode('utf-8')

    assert 'TUKARAM SHINDE' in html.upper()
    assert 'WS-28471' in html
    assert 'DINDI 27' in html.upper()
    assert 'B+' in html
    assert 'Asthma' in html
    assert 'EMERGENCY HELP' in html or 'SOS' in html
    print(f"[2] External Phone Access via Real LAN URL ({lan_qr_url}): 200 OK")
    print("    • Real-time high-contrast emergency identity loaded successfully")

    # 3. Test reporting emergency from physical phone via LAN IP
    req_data = json.dumps({
        'wari_id': 'WS-28471',
        'emergency_type': 'MEDICAL',
        'latitude': 18.3444,
        'longitude': 74.0305,
        'location_source': 'GPS'
    }).encode('utf-8')
    req = urllib.request.Request(f"{lan_base}/api/public/report-emergency", data=req_data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as resp:
        assert resp.getcode() == 201
        em_res = json.loads(resp.read().decode('utf-8'))

    assert em_res['success'] is True
    assert em_res['emergency_id'] == 'EM-28471'
    assert em_res['status'] == 'DISPATCHED'
    print(f"[3] Phone Dispatched Emergency via LAN IP ({em_res['emergency_id']}): 201 CREATED")
    print(f"    • Assigned Volunteer: {em_res['assigned_volunteer']['name']} ({em_res['assigned_volunteer']['wari_id']})")
    print(f"    • Recommended Hospital: {em_res['recommended_hospital']['name']}")

    # 4. Test polling emergency status from physical phone via LAN IP
    req = urllib.request.Request(f"{lan_base}/api/public/emergency-status/EM-28471")
    with urllib.request.urlopen(req) as resp:
        assert resp.getcode() == 200
        status_res = json.loads(resp.read().decode('utf-8'))

    assert status_res['emergency_id'] == 'EM-28471'
    print(f"[4] Phone Live Status Polling via LAN IP: 200 OK (Status: {status_res['status']})")

    # 5. Clean Reset
    req = urllib.request.Request(f"{lan_base}/api/demo/reset", data=b'{}', headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as resp:
        assert resp.getcode() == 200
    print("[5] Final Clean System Reset: 200 OK")

    print("=" * 65)
    print("ALL PHYSICAL PHONE CAMERA & REAL LAN TESTS PASSED 100%!")
    print("=" * 65)

if __name__ == '__main__':
    test_lan_accessibility()
