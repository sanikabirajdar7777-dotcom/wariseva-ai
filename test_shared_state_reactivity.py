import unittest
import json
from backend.app import app, get_db_connection

class TestSharedStateReactivity(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with open('static/script.js', 'r', encoding='utf-8') as f:
            self.script_js = f.read()
        with open('templates/volunteer_dashboard.html', 'r', encoding='utf-8') as f:
            self.vol_html = f.read()
        with open('templates/hospital_dashboard.html', 'r', encoding='utf-8') as f:
            self.hosp_html = f.read()

    def test_01_script_js_contains_reactive_sync_engine(self):
        """Verify script.js has BroadcastChannel, localStorage listener, and polling sync"""
        self.assertIn('wariseva_emergency_channel', self.script_js)
        self.assertIn('wariseva_shared_emergency_state', self.script_js)
        self.assertIn('applySharedEmergencyState', self.script_js)
        self.assertIn('initSharedEmergencySync', self.script_js)
        self.assertIn("window.addEventListener('storage'", self.script_js)

    def test_02_volunteer_and_hospital_dashboards_broadcast_state(self):
        """Verify volunteer and hospital dashboards broadcast updates to channel and storage"""
        self.assertIn('wariseva_shared_emergency_state', self.vol_html)
        self.assertIn('wariseva_emergency_channel', self.vol_html)
        self.assertIn('broadcastEmergencyUpdate', self.vol_html)

        self.assertIn('wariseva_shared_emergency_state', self.hosp_html)
        self.assertIn('wariseva_emergency_channel', self.hosp_html)
        self.assertIn('broadcastHospitalAcceptance', self.hosp_html)

    def test_03_backend_reactive_state_progression(self):
        """Verify API endpoints update single source of truth and compute accurate stages"""
        # 1. Create Emergency
        res_create = self.app.post('/api/demo/create-emergency')
        self.assertIn(res_create.status_code, [200, 201])
        em_id = 'EM-28471'

        # Check public status endpoint initial stage
        res_st1 = self.app.get(f'/api/public/emergency-status/{em_id}')
        self.assertEqual(res_st1.status_code, 200)
        data_st1 = json.loads(res_st1.data)
        self.assertIn(data_st1['stage'], [4, 6])

        # 2. Volunteer Accepts Case -> Stage becomes 7
        res_vacpt = self.app.post(f'/api/volunteer/cases/{em_id}/accept', json={'volunteer_id': 'V-001'})
        self.assertEqual(res_vacpt.status_code, 200)
        res_st2 = self.app.get(f'/api/public/emergency-status/{em_id}')
        data_st2 = json.loads(res_st2.data)
        self.assertEqual(data_st2['stage'], 7)
        self.assertEqual(data_st2['status'], 'ACCEPTED')

        # 3. Volunteer En Route -> Stage becomes 8
        res_vstart = self.app.post(f'/api/volunteer/cases/{em_id}/start', json={'volunteer_id': 'V-001'})
        self.assertEqual(res_vstart.status_code, 200)
        res_st3 = self.app.get(f'/api/public/emergency-status/{em_id}')
        data_st3 = json.loads(res_st3.data)
        self.assertEqual(data_st3['stage'], 8)
        self.assertEqual(data_st3['status'], 'EN_ROUTE')

        # 4. Volunteer Arrives -> Stage becomes 9
        res_varr = self.app.post(f'/api/volunteer/cases/{em_id}/arrived', json={'volunteer_id': 'V-001'})
        self.assertEqual(res_varr.status_code, 200)
        res_st4 = self.app.get(f'/api/public/emergency-status/{em_id}')
        data_st4 = json.loads(res_st4.data)
        self.assertEqual(data_st4['stage'], 9)
        self.assertEqual(data_st4['status'], 'ARRIVED')

        # 5. Hospital Accepts Case -> Stage becomes 11
        res_hacpt = self.app.post(f'/api/hospital/cases/{em_id}/accept', json={'hospital_id': 'H-001'})
        self.assertEqual(res_hacpt.status_code, 200)
        res_st5 = self.app.get(f'/api/public/emergency-status/{em_id}')
        data_st5 = json.loads(res_st5.data)
        self.assertEqual(data_st5['stage'], 11)
        self.assertEqual(data_st5['hospital_status'], 'ACCEPTED')

        # 6. Case Resolved -> Stage becomes 12
        res_res = self.app.post(f'/api/volunteer/cases/{em_id}/resolve', json={'volunteer_id': 'V-001'})
        self.assertEqual(res_res.status_code, 200)
        res_st6 = self.app.get(f'/api/public/emergency-status/{em_id}')
        data_st6 = json.loads(res_st6.data)
        self.assertEqual(data_st6['stage'], 12)
        self.assertEqual(data_st6['status'], 'RESOLVED')

if __name__ == '__main__':
    unittest.main()
