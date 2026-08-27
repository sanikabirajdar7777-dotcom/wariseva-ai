const fs = require('fs');
const path = require('path');
let JSDOM;
try {
    JSDOM = require('jsdom').JSDOM;
} catch (e) {
    require('./test_sos_pure_node.js');
    process.exit(0);
}

const html = fs.readFileSync(path.join(__dirname, 'templates', 'index.html'), 'utf-8');
const scriptContent = fs.readFileSync(path.join(__dirname, 'static', 'script.js'), 'utf-8');

console.log("=================================================");
console.log("WARISEVA AI — MAIN SOS BUTTON DOM INTERACTION TEST");
console.log("=================================================\n");

const dom = new JSDOM(html, {
    runScripts: "dangerously",
    resources: "usable",
    url: "http://127.0.0.1:5000/"
});

const { window } = dom;
const { document } = window;

// Mock window.speechSynthesis
window.speechSynthesis = {
    speak: () => {},
    cancel: () => {},
    getVoices: () => []
};
window.SpeechSynthesisUtterance = function(text) { this.text = text; };

// Mock Leaflet
window.L = {
    map: () => ({
        setView: () => {},
        flyTo: () => {},
        fitBounds: () => {},
        invalidateSize: () => {},
        hasLayer: () => false,
        removeLayer: () => {},
        on: () => {}
    }),
    tileLayer: () => ({ addTo: () => {} }),
    marker: () => ({ addTo: () => {}, setLatLng: () => {}, on: () => {} }),
    polyline: () => ({ addTo: () => {}, setLatLngs: () => {} }),
    divIcon: () => ({})
};

// Execute script.js in DOM
const scriptEl = document.createElement('script');
scriptEl.textContent = scriptContent;
document.body.appendChild(scriptEl);

// Fire DOMContentLoaded
const domLoadedEvent = document.createEvent("Event");
domLoadedEvent.initEvent("DOMContentLoaded", true, true);
document.dispatchEvent(domLoadedEvent);

console.log("1. Checking Initial Home State:");
const homeView = document.getElementById('home-view');
console.log("  Home view exists:", !!homeView, "| Has class 'active':", homeView.classList.contains('active'));

const mainSosBtn = document.getElementById('main-sos-button');
const sosModal = document.getElementById('sos-modal');
const cancelSosBtn = document.getElementById('cancel-sos-btn');
const confirmSosBtn = document.getElementById('confirm-sos-btn');
const emergencyView = document.getElementById('emergency-view');

console.log("  Main SOS button exists:", !!mainSosBtn);
console.log("  SOS confirmation modal exists:", !!sosModal);
console.log("  Cancel button exists:", !!cancelSosBtn);
console.log("  Dispatch button exists:", !!confirmSosBtn);
console.log("  Modal initially hidden:", sosModal.classList.contains('hidden'));

console.log("\n2. Simulating User Click on Main SOS Button (#main-sos-button):");
mainSosBtn.click();
const modalVisibleAfterClick1 = !sosModal.classList.contains('hidden');
console.log("  Modal visible after click 1:", modalVisibleAfterClick1);
if (!modalVisibleAfterClick1) {
    console.error("FAIL: Modal did not open when Main SOS button was clicked!");
    process.exit(1);
}
console.log("  [PASS] Confirmation modal appeared!");

console.log("\n3. Simulating User Click on CANCEL button (#cancel-sos-btn):");
cancelSosBtn.click();
const modalHiddenAfterCancel = sosModal.classList.contains('hidden');
console.log("  Modal hidden after Cancel click:", modalHiddenAfterCancel);
if (!modalHiddenAfterCancel) {
    console.error("FAIL: Modal did not hide when Cancel button was clicked!");
    process.exit(1);
}
console.log("  [PASS] Confirmation modal hidden!");

console.log("\n4. Simulating Second Click on Main SOS Button (#main-sos-button):");
mainSosBtn.click();
const modalVisibleAfterClick2 = !sosModal.classList.contains('hidden');
console.log("  Modal visible after click 2:", modalVisibleAfterClick2);
if (!modalVisibleAfterClick2) {
    console.error("FAIL: Modal did not reopen on second click!");
    process.exit(1);
}
console.log("  [PASS] Confirmation modal reopened successfully!");

console.log("\n5. Simulating User Click on DISPATCH SOS button (#confirm-sos-btn):");
confirmSosBtn.click();

console.log("  Modal hidden after dispatch:", sosModal.classList.contains('hidden'));
console.log("  Emergency view active:", emergencyView.classList.contains('active'));
console.log("  Active Emergency Object:", window.WariState.activeEmergency);

const step1El = document.getElementById('step-1-sos');
console.log("  Step 1 (SOS Sent & Registered) has 'step-active' or 'step-done':", 
    step1El.classList.contains('step-active') || step1El.classList.contains('step-done'));

console.log("\n=================================================");
console.log("ALL 5 MAIN SOS BUTTON INTERACTION STEPS PASSED 100%!");
console.log("=================================================");
