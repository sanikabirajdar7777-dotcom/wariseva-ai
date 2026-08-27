with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = """                        <div class="rsh-id-tag">
                            <span>Incident:</span>
                            <strong id="em-id-display">EM-28471</strong>
                        </div>"""

replacement = """                        <div class="rsh-right-col" style="display: flex; align-items: center; gap: 12px;">
                            <div class="stopwatch-display-box" id="em-stopwatch-box">
                                <span class="stopwatch-label">⏱️ RESPONSE TIME</span>
                                <span class="stopwatch-time" id="em-stopwatch-timer">00:00</span>
                            </div>
                            <div class="rsh-id-tag">
                                <span>Incident:</span>
                                <strong id="em-id-display">EM-28471</strong>
                            </div>
                        </div>"""

assert target in html, "Could not find target in index.html"
html = html.replace(target, replacement)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html with em-stopwatch-timer!")
