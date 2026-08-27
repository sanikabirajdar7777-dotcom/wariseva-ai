import json
import urllib.request
import urllib.parse

BASE_URL = "http://127.0.0.1:5000"

def get(endpoint):
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        return resp.getcode(), json.loads(resp.read().decode('utf-8'))

def post(endpoint, data=None):
    url = f"{BASE_URL}{endpoint}"
    payload = json.dumps(data).encode('utf-8') if data else b'{}'
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        return resp.getcode(), json.loads(resp.read().decode('utf-8'))

def test_intelligent_response_suite():
    print("==============================================================")
    print("TESTING WARISEVA AI INTELLIGENT RESPONSE & RESPONDER NETWORK")
    print("==============================================================")

    # 1. Reset Demo State
    code, res = post('/api/demo/reset')
    assert code == 200, "Reset failed"
    print("\n[1] Demo System Reset: PASS")

    # 2. Test Resource Counts
    code, res = get('/api/command-center/resources-count')
    assert code == 200 and res['success'] is True
    assert res['available_volunteers'] >= 5
    assert res['available_medical_responders'] >= 4
    assert res['nearby_hospitals'] == 3
    print(f"[2] Resource Counters: PASS (Vols: {res['available_volunteers']}, Resps: {res['available_medical_responders']}, Camps: {res['active_medical_camps']})")

    # 3. Create Emergency
    code, res = post('/api/demo/create-emergency')
    assert code == 201
    em_id = res['emergency_id']
    print(f"[3] Created Demo Emergency: PASS ({em_id})")

    # 4. Test AI Recommendation Engine
    code, ai_res = get(f'/api/emergency/{em_id}/ai-recommendation')
    assert code == 200 and ai_res['success'] is True
    rec_vol = ai_res['recommended_volunteer']
    assert rec_vol is not None
    assert rec_vol['wari_id'] == 'V-001'
    assert rec_vol['name'] == 'Ramesh Kulkarni'
    assert rec_vol['total_score'] >= 90
    assert 'First Aid Certified' in rec_vol['certification']
    assert rec_vol['verification_status'] == 'VERIFIED'
    assert rec_vol['status'] == 'AVAILABLE'
    assert 'distance_score' in rec_vol['breakdown']
    assert 'skill_match_score' in rec_vol['breakdown']
    assert 'zone_relevance_score' in rec_vol['breakdown']
    print(f"[4] AI Recommendation Engine: PASS")
    print(f"    • Recommended: {rec_vol['name']} ({rec_vol['wari_id']}) — Score: {rec_vol['total_score']}/100")
    print(f"    • Reasoning: {rec_vol['reason']}")
    print(f"    • Score Breakdown: {rec_vol['breakdown']}")

    # Check Backup Responders
    backups = ai_res['backup_volunteers']
    assert len(backups) >= 1
    print(f"    • Backup Candidate: {backups[0]['name']} ({backups[0]['wari_id']}) — Score: {backups[0]['total_score']}/100")

    # Check Excluded Volunteers
    excluded = ai_res['excluded_volunteers']
    assert any(e['wari_id'] == 'V-004' for e in excluded)
    print(f"    • Excluded Busy Volunteers: {[e['name'] for e in excluded]} (Busy on active dispatch)")

    # Check Recommended Hospital
    rec_hosp = ai_res['recommended_hospital']
    assert rec_hosp is not None
    assert 'Hospital' in rec_hosp['name'] or 'Trauma' in rec_hosp['name']
    assert 'TRAUMA' in str(rec_hosp.get('capabilities', [])) or 'Critical Care' in rec_hosp['name']
    print(f"    • Recommended Hospital: {rec_hosp['name']} ({rec_hosp['distance_km']} km • ETA {rec_hosp['eta_min']} min)")

    # 5. Test Volunteer Availability Toggle
    code, toggle_res = post('/api/volunteer/toggle-availability', {'volunteer_id': 'V-001'})
    assert code == 200 and toggle_res['status'] == 'OFFLINE'
    print("\n[5] Volunteer Status Toggle (V-001 -> OFFLINE): PASS")

    # Re-run AI Recommendation with V-001 offline
    code, ai_res_offline = get(f'/api/emergency/{em_id}/ai-recommendation')
    rec_offline = ai_res_offline['recommended_volunteer']
    assert rec_offline['wari_id'] != 'V-001', "AI should not select offline volunteer"
    print(f"    • Dynamic AI Adaptation: Top candidate updated to {rec_offline['name']} ({rec_offline['wari_id']} • Score {rec_offline['total_score']}/100)")

    # Restore V-001 to AVAILABLE
    code, toggle_res2 = post('/api/volunteer/toggle-availability', {'volunteer_id': 'V-001'})
    assert code == 200 and toggle_res2['status'] == 'AVAILABLE'
    print("    • Restored V-001 to AVAILABLE: PASS")

    # 6. Test Prototype Volunteer Onboarding / Registration
    new_vol_data = {
        'name': 'Nilesh Deshpande',
        'phone': '9820077777',
        'zone': 'Zone 04 — Saswad Palkhi Maidan',
        'skills': 'First Aid, CPR, Crowd Marshall',
        'certification': 'First Aid Certified',
        'organization': 'Warkari Seva Mandal'
    }
    code, reg_res = post('/api/volunteer/register', new_vol_data)
    assert code == 201 and reg_res['success'] is True
    print(f"\n[6] Prototype Volunteer Onboarding: PASS ({reg_res['volunteer_id']} • {reg_res['name']} • {reg_res['verification_status']})")

    # 7. Test Incident Creation for Assisted Pilgrim (Without App)
    pilgrim_data = {
        'patient_name': 'Muktabai Kale (Assisted Pilgrim)',
        'wari_id': '',
        'emergency_type': 'HEAT',
        'severity': 'CRITICAL',
        'zone': 'Zone 04 — Saswad Palkhi Maidan',
        'notes': 'Elderly pilgrim experiencing heatstroke near Gate 3'
    }
    code, pilg_res = post('/api/incident/create-for-pilgrim', pilgrim_data)
    assert code == 201 and pilg_res['success'] is True
    assert pilg_res['is_unregistered_pilgrim'] is True
    print(f"\n[7] Assisted Pilgrim Incident Creation: PASS")
    print(f"    • Incident ID: {pilg_res['emergency_id']}")
    print(f"    • Pilgrim: {pilg_res['patient_name']} ({pilg_res['wari_id']})")
    print(f"    • AI Match: {pilg_res['ai_recommendation']['name']} (Score: {pilg_res['ai_recommendation']['total_score']}/100)")

    # 8. Clean Reset
    code, res = post('/api/demo/reset')
    assert code == 200
    print("\n[8] Final Clean Reset: PASS")

    print("\n==============================================================")
    print("ALL INTELLIGENT RESPONSE ENGINE & RESPONDER TESTS PASSED 100%!")
    print("==============================================================")

if __name__ == '__main__':
    test_intelligent_response_suite()
