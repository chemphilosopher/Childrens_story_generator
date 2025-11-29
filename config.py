# config.py
"""
Configuration module for Children's Story Generator.

Loads configuration from environment variables with sensible defaults.
Supports multiple LLM providers (OpenAI, Anthropic, Gemini) for story generation
and uses Google Gemini (NanoBanana) for image generation.

Environment Variables:
    LLM_PROVIDER: Choice of "openai", "anthropic", or "gemini" (default: "openai")
    LLM_MODEL: Model name appropriate for the selected provider (default: "gpt-4o")
    OPENAI_API_KEY: API key for OpenAI (required if using OpenAI)
    ANTHROPIC_API_KEY: API key for Anthropic (required if using Anthropic)
    GEMINI_API_KEY: API key for Google Gemini (always required for image generation)
    GEMINI_IMAGE_MODEL: Gemini model for images (default: "gemini-2.0-flash-exp")

Note:
    The default LLM_MODEL is "gpt-4o" which only works with OpenAI provider.
    When using other providers, you MUST set LLM_MODEL appropriately:
    - Anthropic: "claude-3-5-sonnet-20241022" or similar
    - Gemini: "gemini-1.5-pro-latest" or similar
"""
import os

# Text LLM provider config
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "openai")  # "openai", "anthropic", "gemini"
LLM_MODEL = os.environ.get("LLM_MODEL", "gpt-4o")       # override in env if you like

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Image model (NanoBanana / Gemini image)
GEMINI_IMAGE_MODEL = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-2.0-flash-exp")  # NanoBanana
