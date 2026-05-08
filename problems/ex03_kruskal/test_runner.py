import sys
import os
import importlib.util

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


def build_graph(raw):
    idx = 0
    n, m = int(raw[idx]), int(raw[idx+1]); idx += 2
    g = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v, w = int(raw[idx]), int(raw[idx+1]), int(raw[idx+2])
        idx += 3
        g[u].append((u, v, w))
        g[v].append((v, u, w))
    return g, n


def run_tests(student_file, tests_dir):
    mod, err = load_student(student_file)
    if err:
        return [{"name": "import", "passed": False, "error": err}]

    if not hasattr(mod, "kruskal"):
        return [{"name": "import", "passed": False,
                 "error": "No se encuentra la función kruskal(g)."}]

    results = []
    test_files = sorted([f for f in os.listdir(tests_dir) if f.endswith(".in")])

    for test_file in test_files:
        test_name = test_file.replace(".in", "")
        in_path  = os.path.join(tests_dir, test_file)
        out_path = os.path.join(tests_dir, test_file.replace(".in", ".out"))

        with open(in_path, encoding="utf-8") as f:
            raw = f.read().split()
        with open(out_path, encoding="utf-8") as f:
            expected = f.read().strip()

        g, n = build_graph(raw)

        try:
            result = mod.kruskal(g)
            got    = str(result).strip()
            passed = got == expected
            results.append({
                "name": test_name,
                "passed": passed,
                "got": got,
                "expected": expected,
                "error": None
            })
        except Exception as e:
            results.append({
                "name": test_name,
                "passed": False,
                "got": None,
                "expected": expected,
                "error": str(e)
            })

    return results