import sys
import os
import importlib.util
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
    g = [[] for _ in range(n)]
    for i in range(1, m+1):
        u, v = int(raw_lines[i].split()[0]), int(raw_lines[i].split()[1])
        g[u].append(v)
        g[v].append(u)
    return g, n


def is_valid_hamiltonian(cycle, g, n):
    if len(cycle) != n + 1:
        return False
    if cycle[0] != 0 or cycle[-1] != 0:
        return False
    visited = set()
    for i in range(n):
        node = cycle[i]
        next_node = cycle[i+1]
        if node in visited:
            return False
        visited.add(node)
        if next_node not in g[node]:
            return False
    return len(visited) == n


def run_tests(student_file, tests_dir):
    mod, err = load_student(student_file)
    if err:
        return [{"name": "import", "passed": False, "error": err}]

    if not hasattr(mod, "hamiltonian_cycle_bt"):
        return [{"name": "import", "passed": False,
                 "error": "No se encuentra la funcion hamiltonian_cycle_bt(g, v, sol)."}]

    results = []
    test_files = sorted([f for f in os.listdir(tests_dir) if f.endswith(".in")])

    for test_file in test_files:
        test_name = test_file.replace(".in", "")
        in_path  = os.path.join(tests_dir, test_file)
        out_path = os.path.join(tests_dir, test_file.replace(".in", ".out"))

        with open(in_path,  "r", encoding="utf-8") as f: raw_lines = f.read().splitlines()
        with open(out_path, "r", encoding="utf-8") as f: expected  = f.read().strip()

        g, n = parse_input(raw_lines)

        captured   = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured

        try:
            sol = [0]
            mod.hamiltonian_cycle_bt(g, 0, sol)
            sys.stdout = old_stdout
            got = captured.getvalue().strip()

            if expected == "SIN CICLO":
                passed = got == "" or got == "SIN CICLO"
            else:
                # Verificar que todos los ciclos impresos son validos
                lines_got = got.strip().splitlines()
                lines_exp = expected.strip().splitlines()
                all_valid = all(
                    is_valid_hamiltonian(list(map(int, l.split())), g, n)
                    for l in lines_got if l.strip()
                )
                passed = all_valid and len(lines_got) == len(lines_exp)

            results.append({
                "name":     test_name,
                "passed":   passed,
                "got":      got,
                "expected": expected,
                "error":    None if passed else "Ciclos invalidos o numero incorrecto"
            })
        except Exception as e:
            sys.stdout = old_stdout
            results.append({
                "name":     test_name,
                "passed":   False,
                "got":      None,
                "expected": expected,
                "error":    str(e)
            })

    return results