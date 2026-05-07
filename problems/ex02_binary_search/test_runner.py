import sys
import os
import importlib.util

def load_student(student_file):
    with open(student_file, "r", encoding="utf-8") as f:
        code = f.read()
    lines = code.splitlines()
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped in ("main()", "main()  "):
            context = "\n".join(lines[max(0, i-3):i])
            if "__name__" not in context:
                return None, "ERROR: Has llamado a main() directamente."
        if "input(" in stripped and not stripped.startswith("#"):
            return None, "ERROR: Has usado input(). Solo escribe las funciones."

    spec = importlib.util.spec_from_file_location("student", student_file)
    mod  = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as e:
        return None, f"ERROR al importar tu archivo: {e}"
    return mod, None


def run_tests(student_file, tests_dir):
    mod, err = load_student(student_file)
    if err:
        return [{"name": "import", "passed": False, "error": err}]

    if not hasattr(mod, "binary_search"):
        return [{"name": "import", "passed": False,
                 "error": "No se encuentra la funcion binary_search(v, number, low, high)."}]

    results = []
    test_files = sorted([f for f in os.listdir(tests_dir) if f.endswith(".in")])

    for test_file in test_files:
        test_name = test_file.replace(".in", "")
        in_path  = os.path.join(tests_dir, test_file)
        out_path = os.path.join(tests_dir, test_file.replace(".in", ".out"))

        with open(in_path,  "r", encoding="utf-8") as f: raw_lines = f.read().splitlines()
        with open(out_path, "r", encoding="utf-8") as f: expected  = f.read().strip()

        v      = list(map(int, raw_lines[1].split()))
        number = int(raw_lines[2])

        try:
            result = mod.binary_search(v, number, 0, len(v)-1)
            got    = str(result)
            passed = got == expected
            results.append({
                "name":     test_name,
                "passed":   passed,
                "got":      got,
                "expected": expected,
                "error":    None
            })
        except Exception as e:
            results.append({
                "name":     test_name,
                "passed":   False,
                "got":      None,
                "expected": expected,
                "error":    str(e)
            })

    return results