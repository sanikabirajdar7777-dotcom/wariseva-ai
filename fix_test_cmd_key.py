with open('test_qr_identity_workflow.py', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace("cmd_res['active_count']", "cmd_res['count']")

with open('test_qr_identity_workflow.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated test_qr_identity_workflow.py command center assertion!")
