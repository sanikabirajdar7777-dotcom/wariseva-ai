import urllib.request
import urllib.parse
import json
import sys

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = 'http://127.0.0.1:5000'

def request_json(path, method='GET', payload=None):
    url = f"{BASE_URL}{path}"
    data = json.dumps(payload).encode('utf-8') if payload is not None else None
    headers = {'Content-Type': 'application/json'} if data else {}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        res = urllib.request.urlopen(req)
        body = res.read().decode('utf-8')
        return res.status, json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        try:
            return e.code, json.loads(body) if body else {}
        except Exception:
            return e.code, {'raw_error': body}

def test_new_endpoints():
    print("Testing newly added endpoints...")

    # 1. Reset
    code, data = request_json('/api/demo/reset', method='POST')
    assert code == 200, "Reset failed"

    # 2. Demo Emergency
    code, data = request_json('/api/demo/create-emergency', method='POST')
    assert code == 201, "Create demo emergency failed"
    em_id = data['emergency_id']

    # 3. Tracking with Nearest Help & Group
    code, data = request_json(f'/api/emergency/{em_id}/tracking')
    assert code == 200, "Tracking failed"
    assert 'nearest_help' in data, "Missing nearest_help"
    assert data['nearest_help']['volunteer'] is not None, "Missing volunteer in nearest_help"
    assert data['nearest_help']['medical_camp'] is not None, "Missing camp in nearest_help"
    assert data['nearest_help']['responder'] is not None, "Missing responder in nearest_help"
    assert data['nearest_help']['hospital'] is not None, "Missing hospital in nearest_help"
    print("[PASS] GET /api/emergency/<id>/tracking verified with 4 nearest_help cards")

    # 4. Group Members
    code, data = request_json('/api/group/members?wari_id=WS-28471')
    assert code == 200 and len(data['members']) >= 2, "Group members fetch failed"
    print(f"[PASS] GET /api/group/members verified ({len(data['members'])} companions)")

    # 5. Add Group Member
    code, data = request_json('/api/group/add-member', method='POST', payload={
        'wari_id': 'WS-28471',
        'name': 'Aarav Patil',
        'phone': '9822114477',
        'relationship': 'Brother / Palkhi Sevak'
    })
    assert code == 201, "Add group member failed"
    print("[PASS] POST /api/group/add-member verified")

    # 6. Command Center Resources
    code, data = request_json('/api/command-center/resources')
    assert code == 200 and len(data['camps']) > 0, "Resources fetch failed"
    print(f"[PASS] GET /api/command-center/resources verified ({len(data['camps'])} medical camps)")

    # 7. Command Center Heatmap
    code, data = request_json('/api/command-center/heatmap')
    assert code == 200 and len(data['heatmap_points']) > 0, "Heatmap fetch failed"
    print(f"[PASS] GET /api/command-center/heatmap verified ({len(data['heatmap_points'])} zones)")

    # 8. Emergency Analytics
    code, data = request_json(f'/api/emergency/{em_id}/analytics')
    assert code == 200 and 'scores' in data, "Analytics fetch failed"
    print(f"[PASS] GET /api/emergency/<id>/analytics verified (Response Score: {data['scores']['total_score']}/100)")

    print("\nALL NEW BACKEND ENDPOINTS PASSED WITH 100% SUCCESS!")

if __name__ == '__main__':
    test_new_endpoints()
