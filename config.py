# config.py
import os

# Text LLM provider config
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "openai")  # "openai", "anthropic", "gemini"
LLM_MODEL = os.environ.get("LLM_MODEL", "gpt-4o")       # override in env if you like

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Image model (NanoBanana / Gemini image)
GEMINI_IMAGE_MODEL = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-2.0-flash-exp")  # NanoBanana
