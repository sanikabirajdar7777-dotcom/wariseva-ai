import unittest
import os, sys, json, io
from PIL import Image

sys.path.insert(0, os.path.abspath('backend'))
import app as flask_app

class TestQrEngineAndScannability(unittest.TestCase):
    def setUp(self):
        self.app = flask_app.app
        self.client = self.app.test_client()

    def test_1_network_info_api(self):
        """Test /api/network-info returns unified PUBLIC_BASE_URL and qr_target_url."""
        res = self.client.get('/api/network-info')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data.get('success'))
        self.assertIn('public_base_url', data)
        self.assertIn('qr_target_url', data)
        self.assertTrue(data['qr_target_url'].endswith('/public/pilgrim/WS-28471'))
        print(f"[TEST 1 PASS] Network Info: Base={data['public_base_url']} | Target={data['qr_target_url']}")

    def test_2_qr_payload_api(self):
        """Test /api/qr/payload returns exact URL structure."""
        res = self.client.get('/api/qr/payload?wari_id=WS-28471')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data.get('success'))
        self.assertEqual(data.get('wari_id'), 'WS-28471')
        self.assertTrue(data.get('payload_url').endswith('/public/pilgrim/WS-28471'))
        self.assertEqual(data.get('error_correction'), 'H')
        self.assertEqual(data.get('quiet_zone_modules'), 4)
        print(f"[TEST 2 PASS] QR Payload verified: {data['payload_url']} (Level H, 4-module border)")

    def test_3_qr_image_generation(self):
        """Test /api/qr/image generates a valid square PNG with PIL verification."""
        res = self.client.get('/api/qr/image?wari_id=WS-28471')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'image/png')
        self.assertGreater(len(res.data), 500)

        # Parse with PIL
        img = Image.open(io.BytesIO(res.data))
        self.assertEqual(img.format, 'PNG')
        self.assertEqual(img.size[0], img.size[1], "QR code image must be perfectly 1:1 square")
        self.assertGreaterEqual(img.size[0], 300, "QR code image must be high resolution for printing")

        # Check background is pure white
        top_left_pixel = img.convert('RGB').getpixel((0, 0))
        self.assertEqual(top_left_pixel, (255, 255, 255), "Quiet zone background must be pure white")
        print(f"[TEST 3 PASS] High-resolution scannable QR Image generated: {img.size} PNG, 1:1 Aspect Ratio")

    def test_4_public_pilgrim_profile_route(self):
        """Test scanning URL /public/pilgrim/WS-28471 renders Tukaram Shinde with SOS trigger."""
        res = self.client.get('/public/pilgrim/WS-28471')
        self.assertEqual(res.status_code, 200)
        html = res.data.decode('utf-8')
        self.assertIn('Tukaram Shinde', html)
        self.assertIn('WS-28471', html)
        self.assertIn('DINDI 27', html)
        self.assertIn('B+', html)
        self.assertIn('+91 98221 28471', html)
        self.assertIn('+91 98220 99881', html)
        self.assertIn('Asthma', html)
        self.assertIn('public-sos-btn', html)
        print("[TEST 4 PASS] Public profile route /public/pilgrim/WS-28471 verified")

    def test_5_custom_url_override_qr(self):
        """Test /api/qr/image with explicit custom URL parameter."""
        custom = "http://192.168.1.5:5000/public/pilgrim/WS-28471"
        res = self.client.get(f'/api/qr/image?url={custom}')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'image/png')
        img = Image.open(io.BytesIO(res.data))
        self.assertEqual(img.size[0], img.size[1])
        print(f"[TEST 5 PASS] Custom URL QR generation verified: {custom}")

if __name__ == '__main__':
    unittest.main()
