with open('static/style.css', 'r', encoding='utf-8') as f:
    css_code = f.read()

target = """.wb-qr-pure-box {
    background: #FFFFFF;
    padding: 6px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
}
.wb-qr-pure-box canvas, .wb-qr-pure-box img, .wb-qr-pure-box svg {
    display: block !important;
    width: 96px !important;
    height: 96px !important;
}"""

replacement = """.wristband-band {
    width: 100%;
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    border: 2px solid #38BDF8;
    border-radius: 18px;
    display: flex;
    align-items: stretch;
    position: relative;
    overflow: hidden;
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.7), inset 0 1px 0 rgba(255, 255, 255, 0.15);
    min-height: 330px;
    color: #FFFFFF;
}

.wb-band-main {
    flex: 1;
    display: grid;
    grid-template-columns: 1fr 1.3fr 1.3fr;
    align-items: center;
    padding: 18px 20px;
    gap: 16px;
}

.wb-qr-pure-box {
    background: #FFFFFF !important;
    padding: 12px !important;
    border-radius: 12px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5) !important;
    border: 2px solid #E2E8F0 !important;
    width: 300px !important;
    height: 300px !important;
    max-width: 100% !important;
}

.wb-qr-pure-box canvas, .wb-qr-pure-box img, .wb-qr-pure-box svg {
    display: block !important;
    width: 276px !important;
    height: 276px !important;
    image-rendering: pixelated !important;
    background: #FFFFFF !important;
}"""

assert target in css_code, "Could not find target in style.css"
css_code = css_code.replace(target, replacement)

with open('static/style.css', 'w', encoding='utf-8') as f:
    f.write(css_code)

print("Updated static/style.css to give the QR code a full 300x300px unconstrained box!")
