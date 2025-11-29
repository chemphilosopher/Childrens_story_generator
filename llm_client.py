# llm_client.py
from typing import Optional

from config import (
    LLM_PROVIDER, LLM_MODEL,
    OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY
)


class LLMClient:
    def __init__(self, provider: Optional[str] = None, model: Optional[str] = None):
        self.provider = (provider or LLM_PROVIDER).lower()
        self.model = model or LLM_MODEL

        if self.provider == "openai":
            if not OPENAI_API_KEY:
                raise RuntimeError("OPENAI_API_KEY not set.")
            import openai
            openai.api_key = OPENAI_API_KEY
            self._openai = openai

        elif self.provider == "anthropic":
            if not ANTHROPIC_API_KEY:
                raise RuntimeError("ANTHROPIC_API_KEY not set.")
            import anthropic
            self._anthropic = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

        elif self.provider == "gemini":
            if not GEMINI_API_KEY:
                raise RuntimeError("GEMINI_API_KEY not set.")
            from google import genai
            self._gemini = genai.Client(api_key=GEMINI_API_KEY)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Simple one-shot text generation interface.
        """
        if self.provider == "openai":
            return self._generate_openai(prompt, system_prompt)
        elif self.provider == "anthropic":
            return self._generate_anthropic(prompt, system_prompt)
        elif self.provider == "gemini":
            return self._generate_gemini(prompt, system_prompt)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    # --- Provider-specific implementations ---

    def _generate_openai(self, prompt: str, system_prompt: Optional[str]) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        resp = self._openai.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return resp.choices[0].message.content

    def _generate_anthropic(self, prompt: str, system_prompt: Optional[str]) -> str:
        sys = system_prompt or "You are a helpful assistant."
        msg = self._anthropic.messages.create(
            model=self.model,
            system=sys,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )
        # anthropic content is a list of blocks
        return "".join(block.text for block in msg.content if hasattr(block, "text"))

    def _generate_gemini(self, prompt: str, system_prompt: Optional[str]) -> str:
        # Gemini doesn't strictly separate system/user in the same way; we just prepend.
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\nUser request:\n{prompt}"

        resp = self._gemini.models.generate_content(
            model=self.model,
            contents=[full_prompt],
        )
        return resp.candidates[0].content.parts[0].text
