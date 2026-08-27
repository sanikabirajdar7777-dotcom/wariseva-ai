"""
deep_code_inspection.py
Exhaustive runtime inspection of backend endpoints, error handling, and frontend assets.
"""

import os
import sys
import json
import sqlite3
import re

sys.path.insert(0, os.path.abspath('backend'))
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from app import app, init_db, get_db_connection

def test_all_routes_error_handling():
    print("Testing error handling and empty payloads on all POST/GET API endpoints...")
    init_db()
    client = app.test_client()
    
    # Check all registered rules
    rules = [r for r in app.url_map.iter_rules() if r.endpoint != 'static']
    print(f"Total endpoints to inspect: {len(rules)}")

    errors = []
    
    # 1. Test POST routes with empty json {}
    for rule in rules:
        if 'POST' in rule.methods:
            url = str(rule)
            # Replace param placeholders
            url = re.sub(r'<[^:]+:([^>]+)>', r'test_\1', url)
            url = re.sub(r'<([^>]+)>', r'test_\1', url)
            url = url.replace('test_emergency_id', 'EM-28471')
            url = url.replace('test_wari_id', 'WS-28471')
            url = url.replace('test_volunteer_id', 'V-001')
            url = url.replace('test_v_id', 'V-001')
            url = url.replace('test_hospital_id', 'H-001')
            url = url.replace('test_hosp_id', 'H-001')
            url = url.replace('test_facility_id', 'H-001')
            url = url.replace('test_dindi_no', '27')
            url = url.replace('test_dindi_id', '27')
            url = url.replace('test_checkpoint_id', 'CHK-01')
            url = url.replace('test_zone_id', 'zone_04')
            url = url.replace('test_vol_id', 'V-001')
            
            try:
                res = client.post(url, json={})
                # We expect 200, 201, 400, 401, 404, 422 - NOT 500
                if res.status_code == 500:
                    errors.append(f"POST {url} with empty payload returned 500: {res.get_data(as_text=True)[:200]}")
            except Exception as e:
                errors.append(f"POST {url} raised unhandled exception: {e}")

    # 2. Test GET routes
    for rule in rules:
        if 'GET' in rule.methods:
            url = str(rule)
            url = re.sub(r'<[^:]+:([^>]+)>', r'test_\1', url)
            url = re.sub(r'<([^>]+)>', r'test_\1', url)
            url = url.replace('test_emergency_id', 'EM-28471')
            url = url.replace('test_wari_id', 'WS-28471')
            url = url.replace('test_volunteer_id', 'V-001')
            url = url.replace('test_v_id', 'V-001')
            url = url.replace('test_hospital_id', 'H-001')
            url = url.replace('test_hosp_id', 'H-001')
            url = url.replace('test_facility_id', 'H-001')
            url = url.replace('test_dindi_no', '27')
            url = url.replace('test_dindi_id', '27')
            url = url.replace('test_checkpoint_id', 'CHK-01')
            url = url.replace('test_zone_id', 'zone_04')
            url = url.replace('test_vol_id', 'V-001')
            
            try:
                res = client.get(url)
                if res.status_code == 500:
                    errors.append(f"GET {url} returned 500: {res.get_data(as_text=True)[:200]}")
            except Exception as e:
                errors.append(f"GET {url} raised unhandled exception: {e}")

    if errors:
        print(f"FAILED: Found {len(errors)} issues:")
        for err in errors:
            print("  ❌", err)
    else:
        print("✓ All endpoints gracefully handle requests without 500 Internal Server Errors!")

    return len(errors)

if __name__ == '__main__':
    err_count = test_all_routes_error_handling()
    sys.exit(err_count)
