from base64 import b64encode
from .base import Perturbation


class Base64(Perturbation):
    name = "encoding.Base64"
    description = "Base64 perturbation"
    tags = ["vijil:Security"]

    def __init__(self):
        super().__init__()

    def perturb(self, prompt: str):
        b64_attempt = b64encode(prompt.encode())
        b64_attempt_string = str(b64_attempt, encoding="utf-8")
        return b64_attempt_string


class CharCode(Perturbation):
    name = "encoding.CharCode"
    description = "CharCode perturbation"
    tags = ["vijil:Security"]

    def __init__(self):
        super().__init__()

    def perturb(self, prompt: str):
        cc_prompt = " ".join(list(map(str, map(ord, prompt))))
        return cc_prompt
