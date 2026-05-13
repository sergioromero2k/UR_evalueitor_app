import sys
import os
import subprocess

def run_tests(student_file, tests_dir):
    results = []
    test_files = sorted([f for f in os.listdir(tests_dir) if f.endswith(".in")])

    for test_file in test_files:
        test_name = test_file.replace(".in", "")
        in_path  = os.path.join(tests_dir, test_file)
        out_path = os.path.join(tests_dir, test_file.replace(".in", ".out"))

        with open(in_path,  "r", encoding="utf-8") as f: stdin_data = f.read()
        with open(out_path, "r", encoding="utf-8") as f: expected  = f.read().strip()

        try:
            result = subprocess.run(
                [sys.executable, student_file],
                input=stdin_data,
                capture_output=True,
                text=True,
                timeout=10,
                encoding="utf-8",
                errors="replace"
            )
            got    = result.stdout.strip()
            stderr = result.stderr.strip()
            passed = got == expected

            results.append({
                "name":     test_name,
                "passed":   passed,
                "got":      got      if not passed else None,
                "expected": expected if not passed else None,
                "error":    stderr[:200] if stderr and not passed else None,
                "timeout":  False
            })
        except subprocess.TimeoutExpired:
            results.append({
                "name":    test_name,
                "passed":  False,
                "got":     None,
                "expected": expected,
                "error":   "TIMEOUT",
                "timeout": True
            })
        except Exception as e:
            results.append({
                "name":    test_name,
                "passed":  False,
                "got":     None,
                "expected": expected,
                "error":   str(e),
                "timeout": False
            })

    return results