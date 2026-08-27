import os
import sys
import io
import time
import subprocess
import urllib.request

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

project_dir = os.path.dirname(os.path.abspath(__file__))
test_files = [f for f in sorted(os.listdir(project_dir)) if f.startswith('test_') and f.endswith('.py')]

server_proc = None
try:
    urllib.request.urlopen("http://127.0.0.1:5000/api/health", timeout=1)
    print("Detected existing WariSeva AI server active on port 5000.\n")
except Exception:
    print("Starting background WariSeva AI test server on http://127.0.0.1:5000...")
    server_proc = subprocess.Popen(
        [sys.executable, os.path.join(project_dir, "backend", "app.py")],
        cwd=project_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    for i in range(40):
        time.sleep(0.3)
        try:
            urllib.request.urlopen("http://127.0.0.1:5000/api/health", timeout=1)
            print("Background test server ready.\n")
            break
        except Exception:
            pass

print(f"Found {len(test_files)} test files to execute.\n")

failed = []
passed = []

try:
    for tf in test_files:
        print(f"Running {tf} ...", end=" ", flush=True)
        res = subprocess.run([sys.executable, tf], cwd=project_dir, capture_output=True, text=True, encoding='utf-8', errors='replace')
        if res.returncode == 0:
            print("✓ PASS")
            passed.append(tf)
        else:
            print("✗ FAIL")
            print(res.stdout)
            print(res.stderr)
            failed.append((tf, res.stderr or res.stdout))

    print("\n======================================================================")
    print(f"TEST EXECUTION SUMMARY: {len(passed)} PASSED, {len(failed)} FAILED")
    print("======================================================================")
    if failed:
        for tf, err in failed:
            print(f"FAILED: {tf}")
            print(err[:300])
            print("---")
    else:
        print("ALL TEST SUITES IN THE ENTIRE REPOSITORY PASSED WITH 100% SUCCESS!")
finally:
    if server_proc:
        try:
            server_proc.terminate()
            server_proc.wait(timeout=3)
        except Exception:
            pass
