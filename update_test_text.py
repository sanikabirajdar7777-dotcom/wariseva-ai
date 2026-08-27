for fname in ['test_qr_engine_precision.py', 'test_public_wristband_flow.py', 'test_lan_phone_accessibility.py']:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace("assert 'REPORT EMERGENCY' in profile_html", "assert 'EMERGENCY HELP' in profile_html or 'SOS' in profile_html")
    content = content.replace("assert 'REPORT EMERGENCY' in html", "assert 'EMERGENCY HELP' in html or 'SOS' in html")
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
print("Updated assertion text in test suites to match unified SOS button!")
