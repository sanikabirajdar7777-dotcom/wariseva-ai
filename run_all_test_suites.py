import subprocess
import glob
import sys
import os
import time
import urllib.request
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

server_proc = None
try:
    urllib.request.urlopen("http://127.0.0.1:5000/api/health", timeout=1)
    print("Detected existing WariSeva AI server active on port 5000.\n")
except Exception:
    print("Starting background WariSeva AI test server on http://127.0.0.1:5000...")
    server_proc = subprocess.Popen(
        [sys.executable, os.path.join("backend", "app.py")],
        cwd=os.getcwd(),
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

test_files = sorted(glob.glob("test_*.py"))
results = {}

try:
    print(f"Running {len(test_files)} test suites in isolated processes...\n")
    for tf in test_files:
        cmd = [sys.executable, tf]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=os.getcwd())
        passed = res.returncode == 0
        results[tf] = (passed, res.stdout, res.stderr)
        status_str = "[PASS]" if passed else "[FAIL]"
        print(f"{status_str:<8} {tf}")

    print("\n----------------- SUMMARY -----------------")
    all_passed = all(p for p, _, _ in results.values())
    if all_passed:
        print(f"ALL {len(test_files)} TEST SUITES PASSED 100%!")
    else:
        failed = [tf for tf, (p, out, err) in results.items() if not p]
        print(f"{len(failed)} TEST SUITE(S) FAILED:")
        for f in failed:
            print(f"\n--- {f} ---")
            try:
                print(results[f][1])
                print(results[f][2])
            except Exception:
                print(results[f][1].encode('ascii', errors='replace').decode('ascii'))
                print(results[f][2].encode('ascii', errors='replace').decode('ascii'))
finally:
    if server_proc:
        try:
            server_proc.terminate()
            server_proc.wait(timeout=3)
        except Exception:
            pass
