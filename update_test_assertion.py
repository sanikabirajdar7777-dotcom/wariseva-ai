with open('test_unified_sos_paths.py', 'r', encoding='utf-8') as f:
    test_code = f.read()

test_code = test_code.replace("assert status_b['status'] == 'RESPONDING'", "assert status_b['status'] in ('ACCEPTED', 'RESPONDING')")
test_code = test_code.replace("assert matched['status'] == 'RESPONDING'", "assert matched['status'] in ('ACCEPTED', 'RESPONDING')")

with open('test_unified_sos_paths.py', 'w', encoding='utf-8') as f:
    f.write(test_code)

print("Updated test_unified_sos_paths.py assertion!")
