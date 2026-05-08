import time

BANNED = [
    "pip install",
    "import requests",
    "import openai",
    "import anthropic",
    "import urllib.request",
    "import httpx",
    "import aiohttp",
    "subprocess.run",
    "subprocess.call",
    "os.system",
]


class AntiCheat:
    def __init__(self):
        self.violations = []
        self._last_focus = 0
        self.penalty_seconds = 0
        self._prev_code = {}  # guarda el codigo anterior por archivo

    def check_code(self, code, file_key="default"):
        # Detectar imports prohibidos
        code_lower = code.lower()
        for b in BANNED:
            if b in code_lower:
                msg = f"[{time.strftime('%H:%M:%S')}] Import prohibido: '{b}'"
                if msg not in self.violations:
                    self.violations.append(msg)
                    if len(self.violations) % 6 == 0:
                        penalty = self._calc_penalty()
                        self.penalty_seconds += penalty
                        return penalty
                return 0

        # Detectar pegado masivo (mas de 10 lineas nuevas de golpe)
        prev = self._prev_code.get(file_key, "")
        prev_lines = len(prev.splitlines())
        curr_lines = len(code.splitlines())
        diff_lines = curr_lines - prev_lines

        if diff_lines >= 10:
            msg = f"[{time.strftime('%H:%M:%S')}] Pegado masivo detectado: +{diff_lines} lineas de golpe"
            if msg not in self.violations:
                self.violations.append(msg)
                if len(self.violations) % 6 == 0:
                    penalty = self._calc_penalty()
                    self.penalty_seconds += penalty
                    self._prev_code[file_key] = code
                    return penalty

        self._prev_code[file_key] = code
        return 0

    def register_focus_loss(self):
        now = time.time()
        if now - self._last_focus > 2:
            self._last_focus = now
            msg = f"[{time.strftime('%H:%M:%S')}] Cambio de ventana detectado"
            self.violations.append(msg)
            # Solo penalizar cada 6 infracciones
            if len(self.violations) % 6 == 0:
                penalty = self._calc_penalty()
                self.penalty_seconds += penalty
                return penalty
        return 0

    def _calc_penalty(self):
        return 1 * 60  # siempre 2 minutos
