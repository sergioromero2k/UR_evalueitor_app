import sys
import os
import importlib.util
import inspect

def load_student(student_file):
    """Carga el archivo del estudiante y detecta si tiene main() suelto."""
    with open(student_file, "r") as f:
        code = f.read()

    # Detectar main() suelto (fuera de if __name__)
    lines = code.splitlines()
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped in ("main()", "main()  ", "main() "):
            # Comprobar que no está dentro de if __name__
            context = "\n".join(lines[max(0, i-3):i])
            if "__name__" not in context:
                return None, "ERROR: Has llamado a main() directamente. El evaluador importa tu archivo. Elimina la llamada a main() o ponla dentro de 'if __name__ == \"__main__\"'"

    spec = importlib.util.spec_from_file_location("student", student_file)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as e:
        return None, f"ERROR al importar tu archivo: {e}"

    return mod, None


def build_graph(lines, directed=False):
    """Construye lista de adyacencia desde líneas de texto."""
    idx = 0
    n, m = int(lines[idx]), int(lines[idx+1])
    idx += 2
    g = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v = int(lines[idx]), int(lines[idx+1])
        idx += 2
        g[u].append(v)
        if not directed:
            g[v].append(u)
    return g, n


def run_tests(student_file, tests_dir):
    """Ejecuta todos los tests contra el archivo del estudiante."""
    mod, err = load_student(student_file)
    if err:
        return [{"name": "import", "passed": False, "error": err}]

    # Comprobar que tiene la función bfs
    if not hasattr(mod, "bfs"):
        return [{"name": "import", "passed": False,
                 "error": "No se encuentra la función bfs(g) en tu archivo."}]

    results = []
    test_files = sorted([
        f for f in os.listdir(tests_dir)
        if f.endswith(".in")
    ])

    for test_file in test_files:
        test_name = test_file.replace(".in", "")
        in_path  = os.path.join(tests_dir, test_file)
        out_path = os.path.join(tests_dir, test_file.replace(".in", ".out"))

        with open(in_path)  as f: raw = f.read().split()
        with open(out_path) as f: expected = f.read().strip()

        g, n = build_graph(raw)

        # Capturar stdout
        import io
        captured = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured

        try:
            mod.bfs(g)
            sys.stdout = old_stdout
            got = captured.getvalue().strip()
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