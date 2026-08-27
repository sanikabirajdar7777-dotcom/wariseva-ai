with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = """                <button type="button" id="btn-test-qr-scan" class="demo-action-btn" style="background: rgba(255, 214, 0, 0.15); border: 1px solid #FFD600; color:#FFD600; font-weight:800;" title="Test Public QR Profile URL directly in browser">
                    ⚡ TEST QR SCAN
                </button>
                <button type="button" id="run-simulation-demo-btn" class="demo-action-btn pulse-orange" title="Auto-advance complete emergency response lifecycle">
                    ▶ SIMULATE RESPONSE
                </button>"""

replacement = """                <button type="button" id="btn-test-qr-scan" class="demo-action-btn" style="background: rgba(255, 214, 0, 0.15); border: 1px solid #FFD600; color:#FFD600; font-weight:800;" title="Test Public QR Profile URL directly in browser">
                    ⚡ TEST QR SCAN
                </button>
                <button type="button" id="create-demo-em-btn" class="demo-action-btn primary" title="Create standard demo emergency">
                    ⚡ CREATE DEMO EMERGENCY
                </button>
                <button type="button" id="run-simulation-demo-btn" class="demo-action-btn pulse-orange" title="Auto-advance complete emergency response lifecycle">
                    ▶ SIMULATE RESPONSE
                </button>"""

assert target in html, "Could not find target in index.html"
html = html.replace(target, replacement)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Restored create-demo-em-btn to toolbar in index.html!")
