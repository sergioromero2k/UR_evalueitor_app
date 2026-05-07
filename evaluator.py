import subprocess
import sys
import os
import difflib


def evaluate_solution(question, user_code):
    if not user_code or len(user_code.strip()) < 15:
        return {
            "correct": False,
            "similar": False,
            "feedback": "No has escrito codigo o es demasiado corto para evaluarse.",
            "trace": "",
            "prof_diff": _generate_diff("", question.get("prof_code", ""))
        }

    test_results = _run_tests(question, user_code)
    prof_diff = _generate_diff(user_code, question.get("prof_code", ""))

    passed = sum(1 for t in test_results if t["passed"])
    total = len(test_results)

    if total == 0:
        similar = _is_similar(user_code, question.get("prof_code", ""))
        return {
            "correct": similar,
            "similar": similar,
            "feedback": "Sin tests automaticos. Comparado con el codigo del profesor.",
            "trace": "",
            "prof_diff": prof_diff
        }

    correct = passed == total
    similar = passed >= total // 2 or _is_similar(user_code, question.get("prof_code", ""))

    feedback_lines = []
    if correct:
        feedback_lines.append(f"Todos los tests pasados ({passed}/{total}).")
        feedback_lines.append("Tu solucion funciona correctamente.")
    else:
        feedback_lines.append(f"{passed}/{total} tests pasados.")
        feedback_lines.append("Algunos casos de prueba han fallado.")

    trace_lines = []
    for t in test_results:
        status = "OK" if t["passed"] else "KO"
        trace_lines.append(f"{t['name']} ---- {status}")
        if not t["passed"] and t.get("error"):
            trace_lines.append(f"   ERROR: {t['error'][:200]}")

    return {
        "correct": correct,
        "similar": similar,
        "feedback": "\n".join(feedback_lines),
        "trace": "\n".join(trace_lines),
        "prof_diff": prof_diff
    }


def _run_tests(question, user_code):
    test_cases = question.get("test_cases", [])
    return [_run_single_test(user_code, tc) for tc in test_cases]


def _run_single_test(user_code, test_case):
    setup       = test_case.get("setup", "")
    call        = test_case.get("call", "")
    restore     = test_case.get("restore", "")
    check       = test_case.get("check", "True")
    description = test_case.get("description", "Test")

    full_code = f"""
import sys, io
{user_code}
{setup}
{call}
{restore}
try:
    _result = bool({check})
    print("EVALUEITOR_OK" if _result else "EVALUEITOR_FAIL")
except Exception as e:
    print(f"EVALUEITOR_ERROR:{{e}}")
"""
    try:
        result = subprocess.run(
            [sys.executable, "-c", full_code],
            capture_output=True,
            text=True,
            timeout=10,
            encoding="utf-8",
            errors="replace"
        )
        output = result.stdout.strip()
        stderr = result.stderr.strip()

        if "EVALUEITOR_OK" in output:
            return {"passed": True, "description": description, "error": None}
        elif "EVALUEITOR_FAIL" in output:
            return {"passed": False, "description": description,
                    "error": "La condicion de check no se cumplio"}
        elif "EVALUEITOR_ERROR" in output:
            err = output.split("EVALUEITOR_ERROR:")[-1].strip()
            return {"passed": False, "description": description, "error": err}
        else:
            err_msg = stderr[:300] if stderr else output[:300]
            return {"passed": False, "description": description, "error": err_msg}

    except subprocess.TimeoutExpired:
        return {"passed": False, "description": description,
                "error": "TIMEOUT: hay un bucle infinito?"}
    except Exception as e:
        return {"passed": False, "description": description, "error": str(e)}


def _generate_diff(user_code, prof_code):
    if not prof_code:
        return ""
    user_lines = _clean_code(user_code).splitlines(keepends=True)
    prof_lines = _clean_code(prof_code).splitlines(keepends=True)
    diff = list(difflib.unified_diff(
        user_lines, prof_lines,
        fromfile="TU CODIGO", tofile="CODIGO DEL PROFESOR", lineterm=""
    ))
    if not diff:
        return "Tu codigo es muy similar al del profesor."
    diff_text = "".join(diff[:40])
    if len(diff) > 40:
        diff_text += f"\n... (+{len(diff)-40} lineas mas)"
    return diff_text


def _clean_code(code):
    lines = []
    for line in code.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            lines.append(line.rstrip())
    return "\n".join(lines)


def _is_similar(user_code, prof_code):
    if not user_code or not prof_code:
        return False
    ratio = difflib.SequenceMatcher(
        None,
        _clean_code(user_code).lower(),
        _clean_code(prof_code).lower()
    ).ratio()
    return ratio > 0.4


def run_problem(problem_dir, student_file, exam_active=True):
    results = {
        "problem": os.path.basename(problem_dir),
        "student_file": student_file,
        "tests": [],
        "correct": False,
        "similar_to_prof": False,
        "all_passed": False,
    }

    if not os.path.exists(student_file):
        results["error"] = f"Archivo no encontrado: {student_file}"
        return results

    tests = _find_tests(problem_dir)
    if not tests:
        results["error"] = "No hay tests en este problema"
        return results

    passed = 0
    for i, (inp_file, out_file) in enumerate(tests):
        test_result = _run_single_file_test(student_file, inp_file, out_file, i)
        results["tests"].append(test_result)
        if test_result["passed"]:
            passed += 1

    results["all_passed"]   = passed == len(tests)
    results["passed_count"] = passed
    results["total_count"]  = len(tests)

    if not exam_active:
        solution_file = os.path.join(problem_dir, "solutions", "solution_prof.py")
        if os.path.exists(solution_file):
            results["prof_diff"]       = _diff_files(student_file, solution_file)
            results["similar_to_prof"] = _is_similar_files(student_file, solution_file)

    results["correct"] = results["all_passed"]
    return results


def _find_tests(problem_dir):
    tests = []
    if not os.path.exists(problem_dir):
        return tests
    files    = sorted(os.listdir(problem_dir))
    in_files = [f for f in files if f.endswith(".in")]
    for in_f in in_files:
        out_f = in_f.replace(".in", ".out")
        if out_f in files:
            tests.append((
                os.path.join(problem_dir, in_f),
                os.path.join(problem_dir, out_f)
            ))
    return tests


def _run_single_file_test(student_file, input_file, expected_file, test_num):
    with open(input_file,    "r", encoding="utf-8") as f: stdin_data = f.read()
    with open(expected_file, "r", encoding="utf-8") as f: expected   = f.read().strip()

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

        return {
            "test_num": test_num,
            "name":     f"test{test_num:02d}",
            "passed":   passed,
            "got":      got      if not passed else None,
            "expected": expected if not passed else None,
            "stderr":   stderr[:300] if stderr else None,
            "timeout":  False,
        }

    except subprocess.TimeoutExpired:
        return {
            "test_num": test_num,
            "name":     f"test{test_num:02d}",
            "passed":   False,
            "got":      None,
            "expected": expected,
            "stderr":   None,
            "timeout":  True,
        }
    except Exception as e:
        return {
            "test_num": test_num,
            "name":     f"test{test_num:02d}",
            "passed":   False,
            "got":      None,
            "expected": expected,
            "stderr":   str(e),
            "timeout":  False,
        }


def _diff_files(student_file, solution_file):
    try:
        with open(student_file,  "r", encoding="utf-8") as f: s = f.readlines()
        with open(solution_file, "r", encoding="utf-8") as f: p = f.readlines()
        diff = list(difflib.unified_diff(
            s, p,
            fromfile="TU CODIGO",
            tofile="CODIGO DEL PROFESOR",
            lineterm=""
        ))
        if not diff:
            return "Tu codigo es identico al del profesor."
        return "".join(diff[:50])
    except Exception:
        return ""


def _is_similar_files(student_file, solution_file):
    try:
        with open(student_file,  "r", encoding="utf-8") as f: s = f.read().lower()
        with open(solution_file, "r", encoding="utf-8") as f: p = f.read().lower()
        return difflib.SequenceMatcher(None, s, p).ratio() > 0.4
    except Exception:
        return False


def write_traces(traces_dir, problem_name, results, exam_active=True):
    os.makedirs(traces_dir, exist_ok=True)
    trace_file = os.path.join(traces_dir, f"{problem_name}.txt")

    lines = []
    lines.append("=" * 50)
    lines.append(f"TRAZAS: {problem_name}")
    lines.append("=" * 50)
    lines.append("")

    for t in results.get("tests", []):
        status = "OK" if t["passed"] else "KO"
        lines.append(f"{t['name']} ---- {status}")

        if not t["passed"]:
            if t.get("timeout"):
                lines.append("  ERROR: TIMEOUT - posible bucle infinito")
            elif t.get("stderr"):
                lines.append(f"  ERROR: {t['stderr']}")
            else:
                lines.append(f"  OBTENIDO: {str(t.get('got', ''))[:200]}")
                lines.append(f"  ESPERADO: {str(t.get('expected', ''))[:200]}")
        lines.append("")

    if not exam_active and results.get("prof_diff"):
        lines.append("=" * 50)
        lines.append("DIFERENCIA CON EL PROFESOR:")
        lines.append("=" * 50)
        lines.append(results["prof_diff"])

    with open(trace_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return trace_file