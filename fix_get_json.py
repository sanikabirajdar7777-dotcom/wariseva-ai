with open('backend/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace request.get_json() with request.get_json(silent=True)
updated_content = content.replace("request.get_json()", "request.get_json(silent=True)")

if content != updated_content:
    with open('backend/app.py', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    print("Safely replaced request.get_json() with silent=True in app.py")
else:
    print("No changes needed for get_json")
