import time

BANNED = [
    "pip install",
    "import requests",
    "import openai",
    "import anthropic",
    "import urllib",
    "subprocess",
    "import httpx",
    "import aiohttp",
    "__import__",
]


class AntiCheat:
    def __init__(self):
        self.violations = []
        self._last = 0

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

    def check_code(self, code):
        code_lower = code.lower()
        for b in BANNED:
            if b in code_lower:
                msg = f"[{time.strftime('%H:%M:%S')}] Import prohibido: '{b}'"
                if msg not in self.violations:
                    self.violations.append(msg)

    def register_focus_loss(self):
        now = time.time()
        if now - self._last > 2:
            self._last = now
            msg = f"[{time.strftime('%H:%M:%S')}] Cambio de ventana detectado"
            self.violations.append(msg)
