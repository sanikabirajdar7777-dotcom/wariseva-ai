with open('test_qr_identity_workflow.py', 'r', encoding='utf-8') as f:
    code = f.read()

target = "if __name__ == '__main__':"
replacement = """if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')"""

code = code.replace(target, replacement)

with open('test_qr_identity_workflow.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated sys.stdout encoding in test_qr_identity_workflow.py!")
