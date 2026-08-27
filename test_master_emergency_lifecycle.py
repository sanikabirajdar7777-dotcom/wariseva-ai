import sys
import os
import io
import json

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
from app import app, get_db_connection

def test_full_sos_lifecycle():
    client = app.test_client()
    print("======================================================================")
    print("TESTING FULL SOS → VOLUNTEER → HOSPITAL → RESOLUTION WORKFLOW")
    print("======================================================================")

    # 1. Reset Demo State
    print("\n[Step 1] Resetting Demo System State...")
    res = client.post('/api/demo/reset', json={})
    assert res.status_code == 200, f"Demo reset failed: {res.status_code}"
    print("  ✓ Demo state reset successfully.")

    # 2. Verify Home Page Loads
    print("\n[Step 2] Loading Home Page...")
    res = client.get('/')
    assert res.status_code == 200
    assert b"WariSeva" in res.data
    print("  ✓ Home dashboard loaded successfully.")

    # 3. Trigger & Register Emergency SOS
    print("\n[Step 3] Dispatching Emergency SOS...")
    sos_payload = {
        "wari_id": "WS-28471",
        "name": "Tukaram Shinde",
        "phone": "9822128471",
        "emergency_type": "MEDICAL",
        "severity": "CRITICAL",
        "condition": "Severe Chest Pain & Heat Dehydration",
        "latitude": 18.3444,
        "longitude": 74.0305,
        "zone": "Zone 04 — Saswad Palkhi Maidan",
        "landmark": "Saswad Central Palkhi Maidan Ground"
    }
    res = client.post('/emergency/create', json=sos_payload)
    if res.status_code != 200 and res.status_code != 201:
        res = client.post('/api/emergency/create', json=sos_payload)
    assert res.status_code in (200, 201), f"Emergency create failed: {res.data}"
    em_data = json.loads(res.data)
    em_id = em_data.get("emergency_id") or em_data.get("id") or "EM-28471"
    print(f"  ✓ Emergency Registered: {em_id}")

    # 4. Volunteer Notification & Case Acceptance
    print(f"\n[Step 4] Volunteer V-001 Receiving & Accepting Case {em_id}...")
    accept_payload = {
        "emergency_id": em_id,
        "volunteer_id": "V-001",
        "status": "ACCEPTED"
    }
    res = client.post(f'/api/emergency/{em_id}/volunteer-accept', json=accept_payload)
    assert res.status_code == 200, f"Volunteer accept failed: {res.data}"
    print(f"  ✓ Volunteer Accepted Dispatch: {res.status_code}")

    # 5. Volunteer En Route Status
    print(f"\n[Step 5] Volunteer En Route...")
    enroute_payload = {
        "emergency_id": em_id,
        "volunteer_id": "V-001",
        "status": "EN_ROUTE"
    }
    res = client.post(f'/api/emergency/{em_id}/volunteer-enroute', json=enroute_payload)
    assert res.status_code == 200, f"Volunteer enroute failed: {res.data}"
    print(f"  ✓ Volunteer En Route: {res.status_code}")

    # 6. Volunteer Arrived at Location
    print(f"\n[Step 6] Volunteer Arrived at Patient Location...")
    arrived_payload = {
        "emergency_id": em_id,
        "volunteer_id": "V-001",
        "status": "ARRIVED"
    }
    res = client.post(f'/api/emergency/{em_id}/volunteer-arrived', json=arrived_payload)
    assert res.status_code == 200, f"Volunteer arrived failed: {res.data}"
    print(f"  ✓ Volunteer Arrived: {res.status_code}")

    # 7. Hospital Receives Patient & Accepts
    print(f"\n[Step 7] Hospital H-001 Accepting Patient...")
    hosp_payload = {
        "emergency_id": em_id,
        "hospital_id": "H-001",
        "status": "ACCEPTED"
    }
    res = client.post(f'/api/emergency/{em_id}/hospital-accept', json=hosp_payload)
    assert res.status_code == 200, f"Hospital accept failed: {res.data}"
    print(f"  ✓ Hospital Accepted Patient: {res.status_code}")

    # 8. Patient Transfer / Treatment Started
    print(f"\n[Step 8] Patient Transfer / Treatment Started...")
    treatment_payload = {
        "emergency_id": em_id,
        "hospital_id": "H-001",
        "status": "TREATMENT_STARTED"
    }
    res = client.post(f'/api/emergency/{em_id}/transfer', json=treatment_payload)
    assert res.status_code == 200, f"Transfer failed: {res.data}"
    print(f"  ✓ Patient Transferred to Medical Facility: {res.status_code}")

    # 9. Case Resolution
    print(f"\n[Step 9] Resolving Case...")
    resolve_payload = {
        "emergency_id": em_id,
        "status": "RESOLVED",
        "resolution_notes": "Patient treated for dehydration, vitals stabilized."
    }
    res = client.post(f'/api/emergency/{em_id}/resolve', json=resolve_payload)
    assert res.status_code == 200, f"Resolve failed: {res.data}"
    print(f"  ✓ Incident Successfully Resolved: {res.status_code}")

    # 10. Command Center Live Telemetry Check
    print(f"\n[Step 10] Checking Command Center Resources & Feed...")
    res = client.get('/api/command-center/emergencies')
    assert res.status_code == 200
    res2 = client.get('/api/command-center/resources')
    assert res2.status_code == 200
    print("  ✓ Command Center queries verified.")

    # 11. QR Wristband Workflow Check
    print(f"\n[Step 11] Checking QR Identity & Wristband Workflow...")
    res = client.get('/public/pilgrim/WS-28471')
    assert res.status_code == 200
    assert b"Tukaram Shinde" in res.data
    res = client.get('/api/pilgrim/WS-28471')
    assert res.status_code == 200
    print("  ✓ QR Wristband public profile & telemetry verified.")

    print("\n======================================================================")
    print("SUCCESS: ALL 11 STEPS OF THE EMERGENCY LIFECYCLE PASSED 100%!")
    print("======================================================================")

if __name__ == '__main__':
    test_full_sos_lifecycle()
