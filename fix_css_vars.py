with open('static/style.css', 'r', encoding='utf-8') as f:
    style_code = f.read()

target = """:root {
    /* Brand Colors (Saffron Wari Inspired) */"""

replacement = """:root {
    --font-display: 'Outfit', 'Plus Jakarta Sans', sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
    --accent-red: #FF0055;
    --accent-cyan: #00E5FF;
    --accent-orange: #FF6B00;
    --shadow-card: 0 8px 32px rgba(0, 0, 0, 0.45);
    --trans-fast: 0.15s ease;

    /* Brand Colors (Saffron Wari Inspired) */"""

assert target in style_code, "Could not find target in style.css"
style_code = style_code.replace(target, replacement)

with open('static/style.css', 'w', encoding='utf-8') as f:
    f.write(style_code)

print("Updated root variables in style.css!")
