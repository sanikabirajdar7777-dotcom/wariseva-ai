import os

js_path = os.path.join(os.path.dirname(__file__), 'static', 'script.js')
with open(js_path, 'r', encoding='utf-8') as f:
    js_text = f.read()

# Clean up see-all-services-btn
old_services = """        document.getElementById('see-all-services-btn')?.addEventListener('click', () => {
            switchView('services-view');
            loadServicesCards('WATER');
        });"""

js_text = js_text.replace(old_services, "")

# Clean up legacy safety-id-form block
old_safety_form = """        // 9. Safety ID Form Submission
        const safetyForm = document.getElementById('safety-id-form');
        if (safetyForm) {
            safetyForm.addEventListener('submit', (e) => {
                e.preventDefault();
                const name = document.getElementById('user-name')?.value?.trim() || 'Warkari Pilgrim';
                const phone = document.getElementById('user-phone')?.value?.trim() || '+91 98221 28471';

                fetch('/safety-id/create', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, phone })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        window.WariState.currentWariId = data.wari_id;
                        window.WariState.currentUserName = data.name;
                        const dUser = document.getElementById('display-user-name');
                        if (dUser) dUser.textContent = data.name;
                        const dWari = document.getElementById('display-wari-id');
                        if (dWari) dWari.textContent = data.wari_id;
                        const dCap = document.getElementById('qr-id-caption');
                        if (dCap) dCap.textContent = data.wari_id;
                        const dHead = document.getElementById('header-wari-id');
                        if (dHead) dHead.textContent = data.wari_id;
                        const dModal = document.getElementById('modal-active-wari-id');
                        if (dModal) dModal.textContent = data.wari_id;

                        safetyForm.classList.add('hidden');
                        document.getElementById('safety-id-result')?.classList.remove('hidden');
                        showToast(`Safety ID ${data.wari_id} Active!`, 'success');
                    } else {
                        const err = document.getElementById('form-error');
                        if (err) {
                            err.textContent = data.error || 'Failed to create Safety ID.';
                            err.classList.remove('hidden');
                        }
                    }
                })
                .catch(() => {
                    showToast('Safety ID registered in offline demo mode.', 'info');
                });
            });
        }

        document.getElementById('create-another-btn')?.addEventListener('click', () => {
            document.getElementById('safety-id-result')?.classList.add('hidden');
            safetyForm?.classList.remove('hidden');
        });"""

js_text = js_text.replace(old_safety_form, "")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_text)

print("Cleaned up legacy stubs in script.js.")
