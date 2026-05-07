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


def is_valid_solution(sol, n):
    if len(sol) != n:
        return False
    if any(x == -1 for x in sol):
        return False
    for i in range(n):
        for j in range(i+1, n):
            if sol[i] == sol[j]:
                return False
            if abs(sol[i] - sol[j]) == abs(i - j):
                return False
    return True


def run_tests(student_file, tests_dir):
    mod, err = load_student(student_file)
    if err:
        return [{"name": "import", "passed": False, "error": err}]

    if not hasattr(mod, "nqueens"):
        return [{"name": "import", "passed": False,
                 "error": "No se encuentra la funcion nqueens(sol, n, found, row)."}]

    results = []
    test_files = sorted([f for f in os.listdir(tests_dir) if f.endswith(".in")])

    for test_file in test_files:
        test_name = test_file.replace(".in", "")
        in_path  = os.path.join(tests_dir, test_file)

        with open(in_path, "r", encoding="utf-8") as f:
            n = int(f.read().strip())

        sol = [-1] * n

        try:
            sol, found = mod.nqueens(sol, n, False, 0)
            passed = found and is_valid_solution(sol, n)
            got    = " ".join(map(str, sol)) if found else "sin solucion"
            results.append({
                "name":     test_name,
                "passed":   passed,
                "got":      got,
                "expected": "cualquier solucion valida de N-Queens",
                "error":    None if passed else "La solucion no es valida"
            })
        except Exception as e:
            results.append({
                "name":     test_name,
                "passed":   False,
                "got":      None,
                "expected": "solucion valida",
                "error":    str(e)
            })

    return results