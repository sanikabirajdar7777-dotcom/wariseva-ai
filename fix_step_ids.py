with open('static/script.js', 'r', encoding='utf-8') as f:
    code = f.read()

target = """        const step5Dist = document.getElementById('step-5-dist-tag');
        const step5Eta = document.getElementById('step-5-eta-tag');

        if (ripDist) ripDist.textContent = `${distM}m`;
        if (ripEta) ripEta.textContent = `${etaMin} min`;
        if (ripStatus) ripStatus.textContent = statusText;
        if (ripPill) {
            ripPill.textContent = statusState;
            ripPill.className = `rip-status-pill ${statusState === '🟢 WITH PATIENT' ? 'with-patient' : ''}`;
        }
        if (volDist) volDist.textContent = `${distM}m`;
        if (step5Dist) step5Dist.textContent = `${distM}m`;
        if (step5Eta) step5Eta.textContent = `${etaMin} min`;"""

replacement = """        const step8Dist = document.getElementById('step-8-dist-tag');
        const step8Eta = document.getElementById('step-8-eta-tag');

        if (ripDist) ripDist.textContent = `${distM}m`;
        if (ripEta) ripEta.textContent = `${etaMin} min`;
        if (ripStatus) ripStatus.textContent = statusText;
        if (ripPill) {
            ripPill.textContent = statusState;
            ripPill.className = `rip-status-pill ${statusState === '🟢 WITH PATIENT' ? 'with-patient' : ''}`;
        }
        if (volDist) volDist.textContent = `${distM}m`;
        if (step8Dist) step8Dist.textContent = `${distM}m`;
        if (step8Eta) step8Eta.textContent = `${etaMin} min`;"""

assert target in code, "Could not find target in script.js"
code = code.replace(target, replacement)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated script.js step tag IDs to step-8!")
