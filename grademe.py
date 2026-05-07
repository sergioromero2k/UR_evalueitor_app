import customtkinter as ctk
import threading
import time
import os
import random
import shutil
import sys
from evaluator import run_problem, write_traces
from antitramp import AntiCheat

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROBLEMS_DIR = os.path.join(BASE_DIR, "problems")
ENTREGABLE_DIR = os.path.join(BASE_DIR, "entregable")
TRAZAS_DIR = os.path.join(BASE_DIR, "trazas")
EXAM_SECONDS = 90 * 60

GREEN = "#00ff41"
RED = "#ff2222"
ORANGE = "#ff8c00"
BLUE = "#00aaff"
GRAY = "#888888"
BG = "#0a0a0a"


class EVALUEITOR(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Confía en lo que sabes, ¡tú puedes!")
        self.iconbitmap("./assets/panda.ico")
        self.geometry("300x550")
        self.minsize(420, 550)
        self.configure(fg_color="#0d0d0d")

        self.mode = None
        self.selected_problems = []
        self.seconds_left = EXAM_SECONDS
        self.timer_running = False
        self.exam_active = False
        self.exam_start = None
        self.anticheat = AntiCheat()
        self.current_problem = 0

        self._build_home()

    # ─────────────────────────────────────────────
    #  HOME
    # ─────────────────────────────────────────────
    def _build_home(self):
        self._clear()
        self.unbind("<FocusOut>")

        ctk.CTkLabel(
            self,
            text="EVALUEITOR",
            font=ctk.CTkFont("Courier New", 34, "bold"),
            text_color=GREEN,
        ).pack(pady=(16, 0))
        ctk.CTkLabel(
            self,
            text="===== SIMULADOR DE PARCIAL =====",
            font=ctk.CTkFont("Courier New", 12),
            text_color=GRAY,
        ).pack(pady=(2, 10))

        # Reglas
        rules_frame = ctk.CTkFrame(
            self,
            fg_color="#111111",
            corner_radius=8,
            border_width=1,
            border_color="#003311",
        )
        rules_frame.pack(fill="x", padx=30, pady=(0, 10))

        ctk.CTkLabel(
            rules_frame,
            text="REGLAS",
            font=ctk.CTkFont("Courier New", 9, "bold"),
            text_color=BLUE,
        ).pack(anchor="w", padx=12, pady=(6, 2))

        for r in [
            "• Tiempo: 1h 30min  |  5 problemas aleatorios",
            "• Tus soluciones van en:  entregable/ex00/ex00.py",
            "• Sin main() ni input() → KO automatico",
            "• Salir de la ventana = infraccion registrada",
            "• Soluciones del profesor solo al terminar",
        ]:
            ctk.CTkLabel(
                rules_frame,
                text=r,
                font=ctk.CTkFont("Courier New", 8),
                text_color="#00add9",
            ).pack(anchor="w", padx=16, pady=1)
        ctk.CTkLabel(rules_frame, text="").pack(pady=2)

        # Modos
        ctk.CTkLabel(
            self,
            text="==== ELIGE MODO ====",
            font=ctk.CTkFont("Courier New", 15, "bold"),
            text_color=GREEN,
        ).pack(pady=(0, 8))

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(0, 10))

        for tag, name, desc, color, mode in [
            ("P1", "PARCIAL 1", "Grafos + Greedy", GREEN, "p1"),
            ("P2", "PARCIAL 2", "DyV + Backtracking", RED, "p2"),
            ("AZAR", "MODO LIBRE", "Todo aleatorio", BLUE, "libre"),
        ]:
            f = ctk.CTkFrame(
                btn_frame,
                fg_color="#111111",
                corner_radius=8,
                border_width=1,
                border_color="#333333",
            )
            f.pack(side="left", padx=6, ipadx=4, ipady=4)

            ctk.CTkLabel(
                f,
                text=f"[{tag}]",
                font=ctk.CTkFont("Courier New", 16, "bold"),
                text_color=color,
            ).pack(pady=(10, 2))
            ctk.CTkLabel(
                f,
                text=name,
                font=ctk.CTkFont("Courier New", 10, "bold"),
                text_color=color,
            ).pack()
            ctk.CTkLabel(
                f, text=desc, font=ctk.CTkFont("Courier New", 8), text_color=GRAY
            ).pack(pady=(2, 8))
            ctk.CTkButton(
                f,
                text="INICIAR",
                fg_color=color,
                text_color="#000000",
                font=ctk.CTkFont("Courier New", 8, "bold"),
                width=90,
                height=24,
                command=lambda m=mode: self._start_exam(m),
            ).pack(pady=(0, 10))

    # ─────────────────────────────────────────────
    #  INICIAR EXAMEN
    # ─────────────────────────────────────────────
    def _get_problems(self, mode):
        if not os.path.exists(PROBLEMS_DIR):
            return []
        all_p = sorted(
            [
                d
                for d in os.listdir(PROBLEMS_DIR)
                if os.path.isdir(os.path.join(PROBLEMS_DIR, d))
            ]
        )
        p1 = [
            "bfs",
            "dfs",
            "dijkstra",
            "prim",
            "kruskal",
            "topsort",
            "scheduling",
            "waiting",
            "coin",
            "knapsack_greedy",
            "art",
        ]
        p2 = [
            "merge",
            "quick",
            "binary",
            "max_vector",
            "knapsack_bt",
            "mochila",
            "nqueens",
            "coloreado",
            "laberinto",
            "bfs",
            "dfs",
            "dijkstra",
            "prim",
            "kruskal",
        ]
        if mode == "p1":
            pool = [p for p in all_p if any(t in p.lower() for t in p1)]
        elif mode == "p2":
            pool = [p for p in all_p if any(t in p.lower() for t in p2)]
        else:
            pool = all_p

        random.shuffle(pool)
        return pool[:5] if len(pool) >= 5 else pool

    def _start_exam(self, mode):
        # Agrandar ventana al iniciar examen
        self.geometry("1100x700")
        self.minsize(900, 600)
        self.mode = mode
        self.selected_problems = self._get_problems(mode)

        if not self.selected_problems:
            ctk.CTkToplevel(self).title("Sin problemas")
            return

        self._create_entregable()
        if os.path.exists(TRAZAS_DIR):
            for f in os.listdir(TRAZAS_DIR):
                try:
                    os.remove(os.path.join(TRAZAS_DIR, f))
                except Exception:
                    pass
        os.makedirs(TRAZAS_DIR, exist_ok=True)

        self.seconds_left = EXAM_SECONDS
        self.exam_active = True
        self.exam_start = time.time()
        self.current_problem = 0

        self._build_exam_screen()
        self._start_timer()
        self.bind("<FocusOut>", self._on_focus_out)

    def _create_entregable(self):
        if os.path.exists(ENTREGABLE_DIR):
            for root, dirs, files in os.walk(ENTREGABLE_DIR):
                for f in files:
                    try:
                        os.remove(os.path.join(root, f))
                    except Exception:
                        pass

        for i, prob in enumerate(self.selected_problems):
            folder = os.path.join(ENTREGABLE_DIR, f"ex{i:02d}")
            os.makedirs(folder, exist_ok=True)

            enunciado_file = os.path.join(PROBLEMS_DIR, prob, "enunciado.txt")
            enunciado = ""
            if os.path.exists(enunciado_file):
                with open(enunciado_file, "r", encoding="utf-8") as f:
                    enunciado = f.read()

            # Crear enunciado.txt en la carpeta del entregable
            enunciado_dest = os.path.join(folder, "enunciado.txt")
            with open(enunciado_dest, "w", encoding="utf-8") as f:
                f.write(enunciado)

            # Crear el .py vacío sin el nombre del algoritmo
            py_file = os.path.join(folder, f"ex{i:02d}.py")
            with open(py_file, "w", encoding="utf-8") as f:
                f.write("# Tu solución aquí:\n\n")

    # ─────────────────────────────────────────────
    #  EXAM SCREEN
    # ─────────────────────────────────────────────
    def _build_exam_screen(self):
        self._clear()

        # ── TOP BAR ──
        top = ctk.CTkFrame(self, fg_color="#111111", corner_radius=0, height=46)
        top.pack(fill="x")
        top.pack_propagate(False)

        ctk.CTkLabel(
            top,
            text=" EVALUEITOR",
            font=ctk.CTkFont("Courier New", 13, "bold"),
            text_color=BLUE,
        ).pack(side="left", padx=12)

        mode_colors = {"p1": BLUE, "p2": ORANGE, "libre": GREEN}
        mode_names = {"p1": "PARCIAL 1", "p2": "PARCIAL 2", "libre": "LIBRE"}
        ctk.CTkLabel(
            top,
            text=f"[ {mode_names[self.mode]} ]",
            font=ctk.CTkFont("Courier New", 9),
            text_color=mode_colors[self.mode],
        ).pack(side="left")

        self.violation_lbl = ctk.CTkLabel(
            top, text="", font=ctk.CTkFont("Courier New", 9), text_color=RED
        )
        self.violation_lbl.pack(side="left", padx=10)

        self.timer_lbl = ctk.CTkLabel(
            top,
            text="1:30:00",
            font=ctk.CTkFont("Courier New", 18, "bold"),
            text_color=GREEN,
        )
        self.timer_lbl.pack(side="right", padx=14)
        ctk.CTkLabel(
            top, text="TIEMPO:", font=ctk.CTkFont("Courier New", 9), text_color=GRAY
        ).pack(side="right")

        # ── MAIN BODY ──
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=10, pady=8)
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=2)
        body.rowconfigure(0, weight=1)

        # ── LEFT: lista de ejercicios + enunciado ──
        left = ctk.CTkFrame(
            body,
            fg_color="#111111",
            corner_radius=8,
            border_width=1,
            border_color="#222222",
        )
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        left.rowconfigure(1, weight=1)
        left.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            left,
            text="EJERCICIOS",
            font=ctk.CTkFont("Courier New", 9, "bold"),
            text_color=GRAY,
        ).grid(row=0, column=0, sticky="w", padx=10, pady=(8, 4))

        # Botones de ejercicios
        ex_frame = ctk.CTkFrame(left, fg_color="transparent")
        ex_frame.grid(row=0, column=0, sticky="ew", padx=6, pady=(28, 0))

        self.ex_btns = []
        for i, prob in enumerate(self.selected_problems):
            btn = ctk.CTkButton(
                ex_frame,
                text=f"ex{i:02d}",
                font=ctk.CTkFont("Courier New", 9, "bold"),
                fg_color="#1a1a1a",
                border_color=GRAY,
                border_width=1,
                text_color=GREEN,
                width=52,
                height=26,
                command=lambda x=i: self._show_enunciado(x),
            )
            btn.pack(side="left", padx=3)
            self.ex_btns.append(btn)

        # Enunciado
        self.enunciado_box = ctk.CTkTextbox(
            left,
            font=ctk.CTkFont("Courier New", 9),
            fg_color="#0a0a0a",
            text_color="#cccccc",
            wrap="word",
            state="disabled",
            corner_radius=6,
        )
        self.enunciado_box.grid(row=1, column=0, sticky="nsew", padx=6, pady=(6, 6))

        # ── RIGHT: log + botones evaluar ──
        right = ctk.CTkFrame(
            body,
            fg_color="#111111",
            corner_radius=8,
            border_width=1,
            border_color="#222222",
        )
        right.grid(row=0, column=1, sticky="nsew")
        right.rowconfigure(1, weight=1)
        right.columnconfigure(0, weight=1)

        # Botones evaluar
        eval_frame = ctk.CTkFrame(right, fg_color="transparent")
        eval_frame.grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 4))

        ctk.CTkLabel(
            eval_frame,
            text="EVALUAR:",
            font=ctk.CTkFont("Courier New", 9, "bold"),
            text_color=GRAY,
        ).pack(side="left", padx=(0, 8))

        self.eval_btns = []
        for i in range(len(self.selected_problems)):
            btn = ctk.CTkButton(
                eval_frame,
                text=f"ex{i:02d}",
                font=ctk.CTkFont("Courier New", 9, "bold"),
                fg_color="#1a1a1a",
                border_color=GREEN,
                border_width=1,
                text_color=GREEN,
                width=52,
                height=26,
                command=lambda x=i: self._eval_one(x),
            )
            btn.pack(side="left", padx=3)
            self.eval_btns.append(btn)

        ctk.CTkButton(
            eval_frame,
            text="TODOS",
            font=ctk.CTkFont("Courier New", 9, "bold"),
            fg_color="#1a1a1a",
            border_color=ORANGE,
            border_width=1,
            text_color=ORANGE,
            width=60,
            height=26,
            command=self._eval_all,
        ).pack(side="left", padx=(8, 0))

        # Log
        self.log_box = ctk.CTkTextbox(
            right,
            font=ctk.CTkFont("Courier New", 9),
            fg_color="#050505",
            text_color=GREEN,
            wrap="none",
            state="disabled",
            corner_radius=6,
        )
        self.log_box.grid(row=1, column=0, sticky="nsew", padx=6, pady=(0, 6))

        # ── BOTTOM ──
        bot = ctk.CTkFrame(self, fg_color="#111111", corner_radius=0, height=46)
        bot.pack(fill="x")
        bot.pack_propagate(False)

        ctk.CTkLabel(
            bot,
            text=f"  📁 entregable/  →  {ENTREGABLE_DIR}",
            font=ctk.CTkFont("Courier New", 8),
            text_color=GRAY,
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            bot,
            text="✖ RENDIRSE",
            fg_color="transparent",
            border_color=RED,
            border_width=1,
            text_color=RED,
            font=ctk.CTkFont("Courier New", 9, "bold"),
            width=100,
            height=28,
            command=self._confirm_giveup,
        ).pack(side="right", padx=6, pady=8)

        ctk.CTkButton(
            bot,
            text="⚑ ENTREGAR",
            fg_color=ORANGE,
            text_color="#000000",
            font=ctk.CTkFont("Courier New", 9, "bold"),
            width=100,
            height=28,
            command=self._confirm_submit,
        ).pack(side="right", padx=4, pady=8)

        # Mostrar enunciado del primero por defecto
        self._show_enunciado(0)
        self._log(
            f"Examen iniciado. {len(self.selected_problems)} problemas en entregable/"
        )
        self._log(f"Abre tu editor y edita los archivos en: {ENTREGABLE_DIR}")
        self._log("─" * 55)

    # ─────────────────────────────────────────────
    #  ENUNCIADO
    # ─────────────────────────────────────────────
    def _show_enunciado(self, idx):
        self.current_problem = idx
        prob = self.selected_problems[idx]
        enunciado_file = os.path.join(PROBLEMS_DIR, prob, "enunciado.txt")

        for i, btn in enumerate(self.ex_btns):
            btn.configure(border_color=GREEN if i == idx else GRAY)

        self.enunciado_box.configure(state="normal")
        self.enunciado_box.delete("1.0", "end")

        if os.path.exists(enunciado_file):
            with open(enunciado_file, "r", encoding="utf-8") as f:
                content = f.read()
            self.enunciado_box.insert("end", f"ex{idx:02d}\n{'─'*40}\n{content}")
        else:
            self.enunciado_box.insert("end", "Enunciado no encontrado.")

        self.enunciado_box.configure(state="disabled")

    # ─────────────────────────────────────────────
    #  LOG
    # ─────────────────────────────────────────────
    def _log(self, msg, color=None):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", msg + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    # ─────────────────────────────────────────────
    #  EVALUAR
    # ─────────────────────────────────────────────
    def _eval_one(self, idx):
        threading.Thread(target=self._run_eval, args=([idx],), daemon=True).start()

    def _eval_all(self):
        threading.Thread(
            target=self._run_eval,
            args=(list(range(len(self.selected_problems))),),
            daemon=True,
        ).start()

    def _run_eval(self, indices):
        self._log("─" * 55)
        self._log(f"[{time.strftime('%H:%M:%S')}] Evaluando...")

        for i in indices:
            prob = self.selected_problems[i]
            folder = f"ex{i:02d}"
            py_file = os.path.join(ENTREGABLE_DIR, folder, f"{folder}.py")
            prob_dir = os.path.join(PROBLEMS_DIR, prob)

            self._log(f"\n  {folder}")

            if not os.path.exists(py_file):
                self._log(f"    ✗ No encontrado: {folder}/{folder}.py")
                self.after(0, lambda b=self.eval_btns[i]: b.configure(border_color=RED))
                continue

            with open(py_file, "r", encoding="utf-8") as f:
                code = f.read()
            self.anticheat.check_code(code)

            if len(self.anticheat.violations) >= 3:
                self.after(0, self._exam_anulado)
                return

            runner_file = os.path.join(prob_dir, "test_runner.py")
            if os.path.exists(runner_file):
                result = self._run_with_runner(runner_file, py_file, prob_dir)
            else:
                result = run_problem(prob_dir, py_file, exam_active=self.exam_active)

            for t in result.get("tests", []):
                status = "OK" if t["passed"] else "KO"
                self._log(f"    {t['name']} ──── {status}")

            write_traces(TRAZAS_DIR, folder, result, exam_active=self.exam_active)

            ok = result.get("all_passed", False)
            color = GREEN if ok else RED
            self.after(
                0, lambda b=self.eval_btns[i], c=color: b.configure(border_color=c)
            )

            if ok:
                self._log(
                    f"    ✓ CORRECTO ({result.get('passed_count',0)}/{result.get('total_count',0)})"
                )
            else:
                self._log(
                    f"    ✗ FAIL ({result.get('passed_count',0)}/{result.get('total_count',0)}) → trazas/{folder}.txt"
                )

        if self.anticheat.violations:
            self.after(
                0,
                lambda: self.violation_lbl.configure(
                    text=f"⚠ {len(self.anticheat.violations)} infracción(es)"
                ),
            )

        self._log("─" * 55)

    def _exam_anulado(self):
        self.timer_running = False
        self.exam_active = False
        self.unbind("<FocusOut>")
        self.geometry("720x480")
        self._clear()

        ctk.CTkLabel(
            self,
            text="EXAMEN ANULADO",
            font=ctk.CTkFont("Courier New", 36, "bold"),
            text_color=RED,
        ).pack(pady=(60, 10))
        ctk.CTkLabel(
            self,
            text="Se han detectado infracciones graves.",
            font=ctk.CTkFont("Courier New", 11),
            text_color=GRAY,
        ).pack()
        ctk.CTkLabel(
            self,
            text="SUSPENSO — Trampa detectada",
            font=ctk.CTkFont("Courier New", 13, "bold"),
            text_color=RED,
        ).pack(pady=(16, 0))

        vf = ctk.CTkFrame(
            self, fg_color="#220000", corner_radius=8, border_width=1, border_color=RED
        )
        vf.pack(padx=40, pady=16, fill="x")
        ctk.CTkLabel(
            vf,
            text="INFRACCIONES:",
            font=ctk.CTkFont("Courier New", 9, "bold"),
            text_color=RED,
        ).pack(anchor="w", padx=12, pady=(8, 4))
        for v in self.anticheat.violations:
            ctk.CTkLabel(
                vf,
                text=f"  • {v}",
                font=ctk.CTkFont("Courier New", 9),
                text_color="#cc4444",
            ).pack(anchor="w", padx=16)
        ctk.CTkLabel(vf, text="").pack(pady=4)

        ctk.CTkButton(
            self,
            text="↩  NUEVO EXAMEN",
            fg_color=RED,
            text_color="#fff",
            font=ctk.CTkFont("Courier New", 10, "bold"),
            width=160,
            height=34,
            command=lambda: [
                self.geometry("720x480"),
                self.minsize(680, 440),
                self._build_home(),
            ],
        ).pack(pady=16)

    def _run_with_runner(self, runner_file, student_file, prob_dir):
        import importlib.util
        import sys

        # Limpiar caché de módulos anteriores
        for key in list(sys.modules.keys()):
            if key.startswith("student") or key.startswith("runner"):
                del sys.modules[key]

        spec = importlib.util.spec_from_file_location(
            f"runner_{os.path.basename(prob_dir)}", runner_file
        )
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
            tests = mod.run_tests(student_file, prob_dir)
        except Exception as e:

            return {
                "tests": [],
                "all_passed": False,
                "passed_count": 0,
                "total_count": 0,
                "error": str(e),
            }

        passed = sum(1 for t in tests if t.get("passed"))
        total = len(tests)
        return {
            "tests": tests,
            "all_passed": passed == total,
            "passed_count": passed,
            "total_count": total,
        }

    # ─────────────────────────────────────────────
    #  TIMER
    # ─────────────────────────────────────────────
    def _start_timer(self):
        self.timer_running = True
        threading.Thread(target=self._tick, daemon=True).start()

    def _tick(self):
        while self.timer_running and self.seconds_left > 0:
            time.sleep(1)
            self.seconds_left -= 1
            self.after(0, self._update_timer)
        if self.seconds_left <= 0:
            self.after(0, self._time_up)

    def _update_timer(self):
        try:
            h = self.seconds_left // 3600
            m = (self.seconds_left % 3600) // 60
            s = self.seconds_left % 60
            self.timer_lbl.configure(text=f"{h}:{m:02d}:{s:02d}")
            if self.seconds_left <= 300:
                self.timer_lbl.configure(text_color=RED)
            elif self.seconds_left <= 900:
                self.timer_lbl.configure(text_color=ORANGE)
        except Exception:
            pass

    def _time_up(self):
        self.timer_running = False
        self._finish_exam()

    # ─────────────────────────────────────────────
    #  ANTICHEAT
    # ─────────────────────────────────────────────
    def _on_focus_out(self, event):
        if self.exam_active and str(event.widget) == str(self):
            self.anticheat.register_focus_loss()
            self.violation_lbl.configure(
                text=f"⚠ {len(self.anticheat.violations)} infracción(es)"
            )

    # ─────────────────────────────────────────────
    #  ENTREGAR / RENDIRSE
    # ─────────────────────────────────────────────
    def _confirm_submit(self):
        win = ctk.CTkToplevel(self)
        win.title("Entregar")
        win.after(200, lambda: win.iconbitmap("./assets/panda.ico"))
        win.geometry("320x200")
        win.minsize(300, 180)
        win.grab_set()
        ctk.CTkLabel(
            win,
            text="¿Entregar el examen?",
            font=ctk.CTkFont("Courier New", 18, "bold"),
            text_color=ORANGE,
        ).pack(pady=(24, 8))
        ctk.CTkLabel(
            win,
            text="Se mostrarán las soluciones del profesor.",
            font=ctk.CTkFont("Courier New", 9),
            text_color=GRAY,
        ).pack()
        f = ctk.CTkFrame(win, fg_color="transparent")
        f.pack(pady=16)
        ctk.CTkButton(
            f,
            text="SÍ, ENTREGAR",
            fg_color=ORANGE,
            text_color="#000",
            width=120,
            command=lambda: [win.destroy(), self._finish_exam()],
        ).pack(side="left", padx=8)
        ctk.CTkButton(
            f,
            text="CANCELAR",
            fg_color="transparent",
            border_width=1,
            border_color=GRAY,
            text_color=GRAY,
            width=100,
            command=win.destroy,
        ).pack(side="left")

    def _confirm_giveup(self):
        win = ctk.CTkToplevel(self)
        win.title("Rendirse")
        win.after(200, lambda: win.iconbitmap("./assets/panda.ico"))
        win.geometry("320x200")
        win.minsize(300, 180)
        win.grab_set()
        ctk.CTkLabel(
            win,
            text="¿Rendirse?",
            font=ctk.CTkFont("Courier New", 18, "bold"),
            text_color=RED,
        ).pack(pady=(24, 8))
        ctk.CTkLabel(
            win,
            text="Se mostrarán las soluciones del profesor.",
            font=ctk.CTkFont("Courier New", 9),
            text_color=GRAY,
        ).pack()
        f = ctk.CTkFrame(win, fg_color="transparent")
        f.pack(pady=16)
        ctk.CTkButton(
            f,
            text="SÍ, RENDIRSE",
            fg_color=RED,
            text_color="#fff",
            width=120,
            command=lambda: [win.destroy(), self._finish_exam()],
        ).pack(side="left", padx=8)
        ctk.CTkButton(
            f,
            text="CANCELAR",
            fg_color="transparent",
            border_width=1,
            border_color=GRAY,
            text_color=GRAY,
            width=100,
            command=win.destroy,
        ).pack(side="left")

    # ─────────────────────────────────────────────
    #  FINISH
    # ─────────────────────────────────────────────
    def _finish_exam(self):
        self.timer_running = False
        self.exam_active = False
        self.unbind("<FocusOut>")
        self._build_result_screen()

    def _build_result_screen(self):
        self.geometry("950x620")
        self.minsize(850, 550)
        try:
            self.iconbitmap("./assets/panda.ico")
        except Exception:
            pass
        self._clear()
        elapsed = int(time.time() - self.exam_start)
        h = elapsed // 3600
        m = (elapsed % 3600) // 60
        s = elapsed % 60
        ctk.CTkLabel(
            self,
            text="RESULTADO FINAL",
            font=ctk.CTkFont("Courier New", 22, "bold"),
            text_color=GREEN,
        ).pack(pady=(24, 4))
        ctk.CTkLabel(
            self,
            text=f"Tiempo: {h}h {m:02d}m {s:02d}s  |  Infracciones: {len(self.anticheat.violations)}",
            font=ctk.CTkFont("Courier New", 9),
            text_color=GRAY,
        ).pack()

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=16, pady=10)

        correct = 0
        for i, prob in enumerate(self.selected_problems):
            folder = f"ex{i:02d}"
            py_file = os.path.join(ENTREGABLE_DIR, folder, f"{folder}.py")
            prob_dir = os.path.join(PROBLEMS_DIR, prob)

            runner_file = os.path.join(prob_dir, "test_runner.py")
            if os.path.exists(runner_file):
                result = self._run_with_runner(runner_file, py_file, prob_dir)
            else:
                result = run_problem(prob_dir, py_file, exam_active=False)

            write_traces(TRAZAS_DIR, folder, result, exam_active=False)

            ok = result.get("all_passed", False)
            passed = result.get("passed_count", 0)
            total = result.get("total_count", 0)
            score = int((passed / total * 20)) if total > 0 else 0
            if ok:
                correct += 1

            color = GREEN if ok else RED
            card = ctk.CTkFrame(
                scroll,
                fg_color="#111111",
                corner_radius=8,
                border_width=1,
                border_color=color,
            )
            card.pack(fill="x", pady=4)

            ctk.CTkLabel(
                card,
                text=f"  {'✓' if ok else '✗'}  {folder}  —  {passed}/{total} tests  —  {score}/20 pts",
                font=ctk.CTkFont("Courier New", 10, "bold"),
                text_color=color,
            ).pack(anchor="w", padx=10, pady=(8, 2))

            diff = result.get("prof_diff", "")
            if diff:
                ctk.CTkLabel(
                    card,
                    text=f"  Diferencia con el profesor:\n{diff[:300]}",
                    font=ctk.CTkFont("Courier New", 8),
                    text_color=BLUE,
                    justify="left",
                ).pack(anchor="w", padx=14, pady=(0, 8))

        total_score = sum(
            int(
                run_problem(
                    os.path.join(PROBLEMS_DIR, self.selected_problems[i]),
                    os.path.join(ENTREGABLE_DIR, f"ex{i:02d}", f"ex{i:02d}.py"),
                    exam_active=False,
                ).get("passed_count", 0)
                / max(
                    run_problem(
                        os.path.join(PROBLEMS_DIR, self.selected_problems[i]),
                        os.path.join(ENTREGABLE_DIR, f"ex{i:02d}", f"ex{i:02d}.py"),
                        exam_active=False,
                    ).get("total_count", 1),
                    1,
                )
                * 20
            )
            for i in range(len(self.selected_problems))
        )

        passed_text = "APROBADO 🎉" if correct >= 3 else "SUSPENSO 💀"
        color = GREEN if correct >= 3 else RED

        ctk.CTkLabel(
            self,
            text=f"{correct}/5 correctos  —  {total_score}/100  —  {passed_text}",
            font=ctk.CTkFont("Courier New", 14, "bold"),
            text_color=color,
        ).pack(pady=8)

        ctk.CTkButton(
            self,
            text="↩  NUEVO EXAMEN",
            fg_color=GREEN,
            text_color="#000",
            font=ctk.CTkFont("Courier New", 11, "bold"),
            width=180,
            height=36,
            command=lambda: [
                self.geometry("720x480"),
                self.minsize(680, 440),
                self._build_home(),
            ],
        ).pack(pady=(0, 16))

    # ─────────────────────────────────────────────
    #  UTILS
    # ─────────────────────────────────────────────
    def _clear(self):
        for w in self.winfo_children():
            w.destroy()


# ─────────────────────────────────────────────────
#  CLI --check
# ─────────────────────────────────────────────────
def run_check_cli():
    from evaluator import run_problem, write_traces
    import importlib.util

    if not os.path.exists(ENTREGABLE_DIR):
        print("No existe carpeta entregable/. Inicia el examen primero.")
        return

    all_p = sorted(os.listdir(PROBLEMS_DIR)) if os.path.exists(PROBLEMS_DIR) else []
    prob_map = {f"ex{i:02d}": p for i, p in enumerate(all_p)}

    ex_folders = sorted(
        [
            d
            for d in os.listdir(ENTREGABLE_DIR)
            if os.path.isdir(os.path.join(ENTREGABLE_DIR, d))
        ]
    )

    os.makedirs(TRAZAS_DIR, exist_ok=True)
    print("\n" + "=" * 50)
    print("  EVALUEITOR — CORRECCION")
    print("=" * 50)

    for folder in ex_folders:
        py_file = os.path.join(ENTREGABLE_DIR, folder, f"{folder}.py")
        prob_name = prob_map.get(folder, folder)
        prob_dir = os.path.join(PROBLEMS_DIR, prob_name)

        print(f"\n  {folder} [{prob_name}]")

        if not os.path.exists(py_file):
            print(f"    x No encontrado: {folder}/{folder}.py")
            continue

        runner_file = os.path.join(prob_dir, "test_runner.py")
        if os.path.exists(runner_file):
            spec = importlib.util.spec_from_file_location("runner", runner_file)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            tests = mod.run_tests(py_file, prob_dir)
            passed = sum(1 for t in tests if t.get("passed"))
            result = {
                "tests": tests,
                "all_passed": passed == len(tests),
                "passed_count": passed,
                "total_count": len(tests),
            }
        else:
            result = run_problem(prob_dir, py_file, exam_active=True)

        for t in result.get("tests", []):
            status = "OK" if t["passed"] else "KO"
            print(f"    {t['name']} ---- {status}")

        write_traces(TRAZAS_DIR, folder, result, exam_active=True)

        if result["all_passed"]:
            print(f"    OK CORRECTO")
        else:
            print(
                f"    FAIL ({result.get('passed_count',0)}/{result.get('total_count',0)}) -> trazas/{folder}.txt"
            )

    print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    if "--check" in sys.argv:
        run_check_cli()
    else:
        app = EVALUEITOR()
        app.mainloop()
