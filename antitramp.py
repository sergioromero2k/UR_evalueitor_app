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
        self.penalty_seconds = 0  # segundos totales a descontar

    def check_code(self, code):
        code_lower = code.lower()
        for b in BANNED:
            if b in code_lower:
                msg = f"[{time.strftime('%H:%M:%S')}] Import prohibido: '{b}'"
                if msg not in self.violations:
                    self.violations.append(msg)
                    # Solo penalizar cada 6 infracciones
                    if len(self.violations) % 6 == 0:
                        penalty = self._calc_penalty()
                        self.penalty_seconds += penalty
                        return penalty
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
        # Primera infraccion: 5 min, luego aumenta 2 min cada vez
        n = len(self.violations)
        return (5 + (n - 1) * 2) * 60  # en segundos
