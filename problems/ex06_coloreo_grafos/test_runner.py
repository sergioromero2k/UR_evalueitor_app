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


def is_valid_coloring(sol, g, m):
    for node in range(len(sol)):
        if sol[node] == 0:
            return False
        if sol[node] > m:
            return False
        for adj in g['g'][node]:
            if adj < node and sol[adj] == sol[node]:
                return False
    return True


def parse_input(raw_lines):
    n, m = int(raw_lines[0].split()[0]), int(raw_lines[0].split()[1])
    g    = {'n': n, 'g': []}
    for i in range(1, n+1):
        if i < len(raw_lines) and raw_lines[i].strip():
            neighbors = list(map(int, raw_lines[i].split()))
        else:
            neighbors = []
        g['g'].append(neighbors)
    return g, m


def run_tests(student_file, tests_dir):
    mod, err = load_student(student_file)
    if err:
        return [{"name": "import", "passed": False, "error": err}]

    if not hasattr(mod, "coloring_va"):
        return [{"name": "import", "passed": False,
                 "error": "No se encuentra la funcion coloring_va(g, m, sol, node)."}]

    results = []
    test_files = sorted([f for f in os.listdir(tests_dir) if f.endswith(".in")])

    for test_file in test_files:
        test_name = test_file.replace(".in", "")
        in_path  = os.path.join(tests_dir, test_file)
        out_path = os.path.join(tests_dir, test_file.replace(".in", ".out"))

        with open(in_path,  "r", encoding="utf-8") as f: raw_lines = f.read().splitlines()
        with open(out_path, "r", encoding="utf-8") as f: expected  = f.read().strip()

        g, m = parse_input(raw_lines)
        sol  = [0] * g['n']

        try:
            sol, found = mod.coloring_va(g, m, sol, 0)

            if not found:
                got    = "NO HAY SOLUCION"
                passed = got == expected
            else:
                valid  = is_valid_coloring(sol, g, m)
                got    = " ".join(map(str, sol))
                if expected == "NO HAY SOLUCION":
                    passed = False
                else:
                    passed = valid

            results.append({
                "name":     test_name,
                "passed":   passed,
                "got":      got,
                "expected": expected,
                "error":    None if passed else "Solucion no valida o incorrecta"
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