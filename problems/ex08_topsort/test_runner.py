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
    parts = raw_lines[0].split()
    n, m  = int(parts[0]), int(parts[1])
    names = [raw_lines[i + 1].strip() for i in range(n)]
    g     = {name: [] for name in names}
    for i in range(n + 1, n + 1 + m):
        u, v = int(raw_lines[i].split()[0]), int(raw_lines[i].split()[1])
        g[names[u]].append(names[v])
    return g, names, n


def is_valid_topsort(result_names, g):
    """Comprueba que el orden es topológicamente válido."""
    pos = {name: i for i, name in enumerate(result_names)}
    for u, neighbors in g.items():
        for v in neighbors:
            if pos.get(u, -1) > pos.get(v, len(result_names)):
                return False
    return True


def run_tests(student_file, tests_dir):
    mod, err = load_student(student_file)
    if err:
        return [{"name": "import", "passed": False, "error": err}]

    if not hasattr(mod, "topsort"):
        return [{"name": "import", "passed": False,
                 "error": "No se encuentra la función topsort(g)."}]

    results = []
    test_files = sorted([f for f in os.listdir(tests_dir) if f.endswith(".in")])

    for test_file in test_files:
        test_name = test_file.replace(".in", "")
        in_path  = os.path.join(tests_dir, test_file)

        with open(in_path) as f: raw_lines = f.read().splitlines()

        g, names, n = parse_input(raw_lines)

        captured   = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured

        try:
            mod.topsort(g)
            sys.stdout = old_stdout
            got  = captured.getvalue().strip()
            # Aceptamos cualquier orden topológico válido
            result_names = got.split()
            passed = (
                len(result_names) == n and
                set(result_names) == set(names) and
                is_valid_topsort(result_names, g)
            )
            results.append({
                "name": test_name,
                "passed": passed,
                "got": got,
                "expected": "cualquier orden topológico válido",
                "error": None if passed else "El orden no es topológicamente válido"
            })
        except Exception as e:
            sys.stdout = old_stdout
            results.append({
                "name": test_name,
                "passed": False,
                "got": None,
                "expected": "orden topológico válido",
                "error": str(e)
            })

    return results