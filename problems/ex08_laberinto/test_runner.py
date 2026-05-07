import sys
import os
import importlib.util
import copy
import io

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


def parse_input(raw_lines):
    n, m = int(raw_lines[0].split()[0]), int(raw_lines[0].split()[1])
    lab  = []
    for i in range(1, n+1):
        row = list(map(int, raw_lines[i].split()))
        lab.append(row)
    return lab, n, m


def is_valid_path(best, n, m):
    if best[n-1][m-1] == 0x3f3f3f3f or best[n-1][m-1] == 0:
        return False
    return True


def path_length(best, n, m):
    return best[n-1][m-1]


def run_tests(student_file, tests_dir):
    mod, err = load_student(student_file)
    if err:
        return [{"name": "import", "passed": False, "error": err}]

    if not hasattr(mod, "labyrinth"):
        return [{"name": "import", "passed": False,
                 "error": "No se encuentra la funcion labyrinth(lab, best, r, c, k)."}]

    results = []
    test_files = sorted([f for f in os.listdir(tests_dir) if f.endswith(".in")])

    for test_file in test_files:
        test_name = test_file.replace(".in", "")
        in_path  = os.path.join(tests_dir, test_file)
        out_path = os.path.join(tests_dir, test_file.replace(".in", ".out"))

        with open(in_path,  "r", encoding="utf-8") as f: raw_lines = f.read().splitlines()
        with open(out_path, "r", encoding="utf-8") as f: expected  = f.read().strip()

        lab, n, m = parse_input(raw_lines)

        k         = 1
        lab[0][0]  = k
        best       = copy.deepcopy(lab)
        for i in range(n):
            for j in range(m):
                if best[i][j] == 0:
                    best[i][j] = 0x3f3f3f3f

        # Restaurar la celda de inicio en best para que no interfiera
        best[0][0] = k

        try:
            best = mod.labyrinth(lab, best, 0, 0, k+1)

            if best[n-1][m-1] == 0x3f3f3f3f:
                got = "SIN SALIDA"
            else:
                rows = []
                for row in best:
                    rows.append(" ".join(str(x) if x != 0x3f3f3f3f else "0" for x in row))
                got = "\n".join(rows)

            passed = got.strip() == expected.strip()
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