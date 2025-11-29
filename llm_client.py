# llm_client.py
"""
Provider-agnostic LLM client wrapper.

This module provides a unified interface for generating text with multiple
LLM providers (OpenAI, Anthropic, Google Gemini). Provider SDKs are lazily
imported only when needed to minimize dependencies.
"""
from typing import Optional

from config import (
    LLM_PROVIDER, LLM_MODEL,
    OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY
)


class LLMClient:
    """
    Unified client for multiple LLM providers.

    Supports OpenAI, Anthropic, and Google Gemini APIs with a consistent
    interface for text generation.

    Args:
        provider: LLM provider name ("openai", "anthropic", or "gemini").
                 Defaults to LLM_PROVIDER from config.
        model: Model identifier (provider-specific). Defaults to LLM_MODEL from config.

    Raises:
        RuntimeError: If required API key is not set or SDK is not installed.
        ValueError: If provider is not supported.
    """

    def __init__(self, provider: Optional[str] = None, model: Optional[str] = None):
        self.provider = (provider or LLM_PROVIDER).lower()
        self.model = model or LLM_MODEL

        if self.provider == "openai":
            if not OPENAI_API_KEY:
                raise RuntimeError(
                    "OPENAI_API_KEY environment variable is not set.\n"
                    "Set it with: export OPENAI_API_KEY='your-key-here'"
                )
            try:
                from openai import OpenAI
                self._openai = OpenAI(api_key=OPENAI_API_KEY)
            except ImportError:
                raise RuntimeError(
                    "OpenAI package not installed. Install with: pip install openai"
                )

        elif self.provider == "anthropic":
            if not ANTHROPIC_API_KEY:
                raise RuntimeError(
                    "ANTHROPIC_API_KEY environment variable is not set.\n"
                    "Set it with: export ANTHROPIC_API_KEY='your-key-here'"
                )
            try:
                import anthropic
                self._anthropic = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
            except ImportError:
                raise RuntimeError(
                    "Anthropic package not installed. Install with: pip install anthropic"
                )

        elif self.provider == "gemini":
            if not GEMINI_API_KEY:
                raise RuntimeError(
                    "GEMINI_API_KEY environment variable is not set.\n"
                    "Set it with: export GEMINI_API_KEY='your-key-here'"
                )
            try:
                from google import genai
                self._gemini = genai.Client(api_key=GEMINI_API_KEY)
            except ImportError:
                raise RuntimeError(
                    "Google GenAI package not installed. Install with: pip install google-genai"
                )
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate text from the configured LLM provider.

        Args:
            prompt: User message/prompt to send to the LLM.
            system_prompt: Optional system message (provider-dependent handling).

        Returns:
            Generated text response from the LLM.

        Raises:
            ValueError: If prompt is empty or provider is not supported.
            RuntimeError: If API call fails.
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")

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
        """Generate text using OpenAI API with error handling."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            resp = self._openai.chat.completions.create(
                model=self.model,
                messages=messages,
                timeout=30.0,
            )

            if not resp.choices or len(resp.choices) == 0:
                raise RuntimeError("OpenAI returned empty response")

            content = resp.choices[0].message.content
            if not content:
                raise RuntimeError("OpenAI returned empty content")

            return content

        except Exception as e:
            error_msg = str(e)
            if "rate" in error_msg.lower() and "limit" in error_msg.lower():
                raise RuntimeError("OpenAI rate limit exceeded. Please wait and try again.")
            elif "api_key" in error_msg.lower() or "auth" in error_msg.lower():
                raise RuntimeError("OpenAI API key is invalid. Please check your API key.")
            elif "model" in error_msg.lower():
                raise RuntimeError(f"Invalid OpenAI model: {self.model}")
            else:
                raise RuntimeError(f"OpenAI API error: {error_msg}")

    def _generate_anthropic(self, prompt: str, system_prompt: Optional[str]) -> str:
        """Generate text using Anthropic API with error handling."""
        sys = system_prompt or "You are a helpful assistant."

        try:
            msg = self._anthropic.messages.create(
                model=self.model,
                system=sys,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}],
                timeout=30.0,
            )

            if not msg.content:
                raise RuntimeError("Anthropic returned empty response")

            # Anthropic content is a list of text blocks
            text = "".join(block.text for block in msg.content if hasattr(block, "text"))

            if not text:
                raise RuntimeError("Anthropic returned no text content")

            return text

        except Exception as e:
            error_msg = str(e)
            if "rate" in error_msg.lower() and "limit" in error_msg.lower():
                raise RuntimeError("Anthropic rate limit exceeded. Please wait and try again.")
            elif "api_key" in error_msg.lower() or "auth" in error_msg.lower():
                raise RuntimeError("Anthropic API key is invalid. Please check your API key.")
            elif "model" in error_msg.lower():
                raise RuntimeError(f"Invalid Anthropic model: {self.model}")
            else:
                raise RuntimeError(f"Anthropic API error: {error_msg}")

    def _generate_gemini(self, prompt: str, system_prompt: Optional[str]) -> str:
        """Generate text using Gemini API with error handling."""
        # Gemini doesn't strictly separate system/user prompts; prepend system prompt
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\nUser request:\n{prompt}"

        try:
            resp = self._gemini.models.generate_content(
                model=self.model,
                contents=[full_prompt],
            )

            if not resp.candidates or len(resp.candidates) == 0:
                raise RuntimeError("Gemini returned no candidates")

            candidate = resp.candidates[0]
            if not hasattr(candidate, 'content') or not candidate.content.parts:
                raise RuntimeError("Gemini response has no content parts")

            text = candidate.content.parts[0].text
            if not text:
                raise RuntimeError("Gemini returned empty text")

            return text

        except AttributeError as e:
            raise RuntimeError(f"Unexpected Gemini response structure: {str(e)}")
        except Exception as e:
            error_msg = str(e)
            if "quota" in error_msg.lower() or "rate" in error_msg.lower():
                raise RuntimeError("Gemini quota/rate limit exceeded. Please wait and try again.")
            elif "api_key" in error_msg.lower() or "auth" in error_msg.lower():
                raise RuntimeError("Gemini API key is invalid. Please check your API key.")
            elif "model" in error_msg.lower():
                raise RuntimeError(f"Invalid Gemini model: {self.model}")
            else:
                raise RuntimeError(f"Gemini API error: {error_msg}")
