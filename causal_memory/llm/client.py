# causal_memory/llm/client.py

import requests
from typing import Optional


class OllamaClient:

    def __init__(
        self,
        base_url: str = "http://132.156.103.65:11434/api/generate",
        model: str = "llama3.1:8b",
        timeout_s: int = 90,
    ):
        self.base_url = base_url
        self.model = model
        self.timeout_s = timeout_s

    def query(
        self,
        prompt: str,
        system: Optional[str] = None,
    ) -> str:

        full_prompt = prompt

        if system is not None:
            full_prompt = f"{system}\n\n{prompt}"

        r = requests.post(
            self.base_url,
            json={
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
            },
            timeout=self.timeout_s,
        )

        r.raise_for_status()

        data = r.json()

        return data["response"]