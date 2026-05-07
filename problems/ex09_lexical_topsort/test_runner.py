import sys
import os
import importlib.util
import io

def load_student(student_file):
    with open(student_file, "r") as f:
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
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as e:
        return None, f"ERROR al importar tu archivo: {e}"
    return mod, None


def parse_input(raw_lines):
    n, m = int(raw_lines[0].split()[0]), int(raw_lines[0].split()[1])
    g    = [[] for _ in range(n)]
    for i in range(1, m + 1):
        u, v = int(raw_lines[i].split()[0]), int(raw_lines[i].split()[1])
        g[u].append(v)
    return g, n


def run_tests(student_file, tests_dir):
    mod, err = load_student(student_file)
    if err:
        return [{"name": "import", "passed": False, "error": err}]

    if not hasattr(mod, "lexic_top_sort"):
        return [{"name": "import", "passed": False,
                 "error": "No se encuentra la función lexic_top_sort(g, n)."}]

    results = []
    test_files = sorted([f for f in os.listdir(tests_dir) if f.endswith(".in")])

    for test_file in test_files:
        test_name = test_file.replace(".in", "")
        in_path  = os.path.join(tests_dir, test_file)
        out_path = os.path.join(tests_dir, test_file.replace(".in", ".out"))

        with open(in_path)  as f: raw_lines = f.read().splitlines()
        with open(out_path) as f: expected  = f.read().strip()

        g, n = parse_input(raw_lines)

        captured   = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured

        try:
            mod.lexic_top_sort(g, n)
            sys.stdout = old_stdout
            got    = captured.getvalue().strip()
            passed = got == expected
            results.append({
                "name": test_name,
                "passed": passed,
                "got": got,
                "expected": expected,
                "error": None
            })
        except Exception as e:
            sys.stdout = old_stdout
            results.append({
                "name": test_name,
                "passed": False,
                "got": None,
                "expected": expected,
                "error": str(e)
            })

    return results