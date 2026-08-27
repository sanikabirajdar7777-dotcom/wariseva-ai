import re

with open('backend/app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add socket import if needed
if 'import socket' not in code:
    code = "import socket\n" + code

# 2. Add get_lan_ip and /api/network-info route
network_info_code = """
def get_lan_ip():
    \"\"\"Detect computer's real LAN IPv4 address (192.168.x.x, 10.x.x.x, 172.16.x.x-172.31.x.x).\"\"\"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        # Connect to public DNS to determine default network interface IP (no packets sent)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        if ip and not ip.startswith('127.'):
            return ip
    except Exception:
        pass

    try:
        hostname = socket.gethostname()
        for ip in socket.gethostbyname_ex(hostname)[2]:
            if ip.startswith(('192.168.', '10.', '172.')):
                return ip
    except Exception:
        pass

    return '127.0.0.1'

@app.route('/api/network-info', methods=['GET'])
def get_network_info():
    \"\"\"Return real local machine LAN IP and base URL for physical phone QR scanning.\"\"\"
    lan_ip = get_lan_ip()
    port = 5000
    public_base_url = f"http://{lan_ip}:{port}"
    qr_target_url = f"{public_base_url}/public/pilgrim/WS-28471"
    
    return jsonify({
        'success': True,
        'lan_ip': lan_ip,
        'port': port,
        'public_base_url': public_base_url,
        'qr_target_url': qr_target_url,
        'hostname': socket.gethostname(),
        'is_lan_available': (lan_ip != '127.0.0.1'),
        'instructions': 'Connect your phone and laptop to the SAME Wi-Fi network and scan the QR with your phone camera.'
    }), 200
"""

marker = "if __name__ == '__main__':"
assert marker in code, "Could not find main marker in app.py"

parts = code.split(marker)
new_main_block = """if __name__ == '__main__':
    lan_ip = get_lan_ip()
    print(f"Starting WariSeva AI server on http://127.0.0.1:5000")
    print(f"Physical Phone Access URL: http://{lan_ip}:5000/public/pilgrim/WS-28471")
    app.run(host='0.0.0.0', port=5000, debug=True)
"""

new_code = parts[0] + network_info_code + "\n" + new_main_block

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(new_code)

print("Updated backend/app.py with get_lan_ip() and GET /api/network-info endpoint!")
