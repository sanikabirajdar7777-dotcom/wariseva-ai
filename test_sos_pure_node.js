const fs = require('fs');
const path = require('path');
const vm = require('vm');

const html = fs.readFileSync(path.join(__dirname, 'templates', 'index.html'), 'utf-8');
const scriptContent = fs.readFileSync(path.join(__dirname, 'static', 'script.js'), 'utf-8');

console.log("=================================================");
console.log("WARISEVA AI — PURE JS SOS BUTTON HANDLER TEST");
console.log("=================================================\n");

// Build a mock DOM tree from the HTML elements of interest
class ClassList {
    constructor() { this.classes = new Set(); }
    add(...cls) { cls.forEach(c => this.classes.add(c)); }
    remove(...cls) { cls.forEach(c => this.classes.delete(c)); }
    contains(c) { return this.classes.has(c); }
    toggle(c) { if (this.contains(c)) this.remove(c); else this.add(c); }
}

class MockElement {
    constructor(id, tag = 'div') {
        this.id = id;
        this.tagName = tag.toUpperCase();
        this.classList = new ClassList();
        this.listeners = {};
        this.style = {};
        this.children = [];
        this.textContent = '';
        this.innerHTML = '';
        this.value = '';
    }
    addEventListener(type, fn) {
        if (!this.listeners[type]) this.listeners[type] = [];
        this.listeners[type].push(fn);
    }
    click() {
        const evt = { type: 'click', target: this, preventDefault: () => {}, stopPropagation: () => {} };
        if (this.listeners['click']) {
            this.listeners['click'].forEach(fn => fn(evt));
        }
    }
    setAttribute() {}
    getAttribute() { return null; }
    querySelector() { return null; }
    querySelectorAll() { return []; }
    appendChild(c) { this.children.push(c); return c; }
    removeChild() {}
    remove() {}
}

const elements = {};
// Extract all IDs from HTML
const idRegex = /id=["']([^"']+)["']/g;
let match;
while ((match = idRegex.exec(html)) !== null) {
    const id = match[1];
    if (!elements[id]) {
        elements[id] = new MockElement(id);
    }
}

// Set initial classes based on HTML
if (elements['home-view']) elements['home-view'].classList.add('active');
if (elements['sos-modal']) elements['sos-modal'].classList.add('modal-overlay', 'hidden');
if (elements['wristband-auth-modal']) elements['wristband-auth-modal'].classList.add('modal-overlay', 'hidden');

const mockDocument = {
    getElementById: (id) => elements[id] || null,
    querySelector: (sel) => {
        if (sel.startsWith('#')) return elements[sel.slice(1)] || null;
        return null;
    },
    querySelectorAll: () => [],
    createElement: (tag) => new MockElement('', tag),
    body: new MockElement('body', 'body'),
    listeners: {},
    addEventListener: (type, fn) => {
        if (!mockDocument.listeners[type]) mockDocument.listeners[type] = [];
        mockDocument.listeners[type].push(fn);
    }
};

const mockWindow = {
    document: mockDocument,
    localStorage: {
        store: {},
        getItem(k) { return this.store[k] || null; },
        setItem(k, v) { this.store[k] = String(v); },
        removeItem(k) { delete this.store[k]; },
        clear() { this.store = {}; }
    },
    sessionStorage: {
        store: {},
        getItem(k) { return this.store[k] || null; },
        setItem(k, v) { this.store[k] = String(v); },
        removeItem(k) { delete this.store[k]; },
        clear() { this.store = {}; }
    },
    location: { origin: 'http://127.0.0.1:5000', href: 'http://127.0.0.1:5000/' },
    speechSynthesis: { speak: () => {}, cancel: () => {}, getVoices: () => [] },
    SpeechSynthesisUtterance: function(t) { this.text = t; },
    BroadcastChannel: function() { return { postMessage: () => {}, close: () => {} }; },
    L: {
        map: function() {
            const m = {
                setView: () => m,
                flyTo: () => m,
                fitBounds: () => m,
                invalidateSize: () => m,
                on: () => m,
                removeLayer: () => m,
                hasLayer: () => false
            };
            return m;
        },
        tileLayer: () => ({ addTo: () => ({}) }),
        marker: function() {
            const m = {
                addTo: () => m,
                setLatLng: () => m,
                on: () => m,
                bindPopup: () => m,
                openPopup: () => m
            };
            return m;
        },
        polyline: () => ({ addTo: () => ({}), setLatLngs: () => ({}) }),
        divIcon: () => ({})
    },
    setTimeout: (fn) => fn(),
    setInterval: () => 1,
    clearInterval: () => {},
    clearTimeout: () => {},
    addEventListener: () => {},
    removeEventListener: () => {},
    fetch: () => Promise.resolve({ ok: true, json: () => Promise.resolve({}) })
};

mockWindow.window = mockWindow;
global.window = mockWindow;
global.document = mockDocument;
global.localStorage = mockWindow.localStorage;
global.sessionStorage = mockWindow.sessionStorage;
global.location = mockWindow.location;
global.L = mockWindow.L;

// Run script
vm.runInNewContext(scriptContent, mockWindow);

// Fire DOMContentLoaded
if (mockDocument.listeners['DOMContentLoaded']) {
    mockDocument.listeners['DOMContentLoaded'].forEach(fn => fn());
}

console.log("1. Checking Initial States:");
const mainSosBtn = elements['main-sos-button'];
const sosModal = elements['sos-modal'];
const cancelSosBtn = elements['cancel-sos-btn'];
const confirmSosBtn = elements['confirm-sos-btn'];
const emergencyView = elements['emergency-view'];

console.log("  Main SOS Button found:", !!mainSosBtn);
console.log("  SOS Modal found:", !!sosModal);
console.log("  SOS Modal initially hidden:", sosModal.classList.contains('hidden'));

console.log("\n2. Test A: Click Main SOS Button:");
mainSosBtn.click();
console.log("  Modal visible after click 1:", !sosModal.classList.contains('hidden'));
if (sosModal.classList.contains('hidden')) {
    console.error("FAIL: Modal not shown!");
    process.exit(1);
}
console.log("  [PASS] Confirmation modal appeared!");

console.log("\n3. Test B: Click CANCEL button:");
cancelSosBtn.click();
console.log("  Modal hidden after Cancel:", sosModal.classList.contains('hidden'));
if (!sosModal.classList.contains('hidden')) {
    console.error("FAIL: Modal not hidden after cancel!");
    process.exit(1);
}
console.log("  [PASS] Confirmation modal closed!");

console.log("\n4. Test C: Click Main SOS Button Again:");
mainSosBtn.click();
console.log("  Modal visible after click 2:", !sosModal.classList.contains('hidden'));
if (sosModal.classList.contains('hidden')) {
    console.error("FAIL: Modal did not reopen!");
    process.exit(1);
}
console.log("  [PASS] Confirmation modal reopened!");

console.log("\n5. Test D: Click DISPATCH SOS button:");
confirmSosBtn.click();

console.log("  Modal closed after Dispatch:", sosModal.classList.contains('hidden'));
console.log("  Emergency View active:", emergencyView.classList.contains('active'));
console.log("  Active Emergency in State:", mockWindow.WariState.activeEmergency.id);

if (mockWindow.WariState.activeEmergency.id === 'EM-28471' && emergencyView.classList.contains('active')) {
    console.log("\n=================================================");
    console.log("ALL ACCEPTANCE CRITERIA VERIFIED AND PASSED 100%!");
    console.log("=================================================");
} else {
    console.error("FAIL: State or View not properly updated!");
    process.exit(1);
}
