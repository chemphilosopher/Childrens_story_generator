# NanoBanana API Verification Guide

This guide helps you verify that NanoBanana (Google's Gemini 2.0 Flash image model) is properly configured and working in your Children's Story Generator.

## What is NanoBanana?

**NanoBanana** is Google's code name for `gemini-2.0-flash-exp`, a fast and high-quality image generation model in the Gemini family. Your story generator uses:

- **Any LLM** (OpenAI GPT, Anthropic Claude, or Google Gemini) for story text generation
- **NanoBanana exclusively** for all illustrations (consistent, high-quality images)

## Current Configuration

### ✅ NanoBanana is Already Set Up

Your project is **already configured** to use NanoBanana:

1. **config.py** (line 34):
   ```python
   GEMINI_IMAGE_MODEL = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-2.0-flash-exp")
   ```

2. **story_and_image.py** (line 229-232):
   ```python
   response = client.models.generate_content(
       model=GEMINI_IMAGE_MODEL,  # Uses gemini-2.0-flash-exp
       contents=[prompt],
   )
   ```

3. **.env.example** (line 19):
   ```bash
   GEMINI_IMAGE_MODEL=gemini-2.0-flash-exp
   ```

## How to Verify NanoBanana Works

### Option 1: Quick Test Script (Recommended)

Run the included test script:

```bash
# Make sure GEMINI_API_KEY is set
export GEMINI_API_KEY="your-key-here"

# Run the verification test
python test_nanobanana.py
```

**Expected output if working:**
```
============================================================
NanoBanana API Test
============================================================

1. Checking GEMINI_API_KEY...
   ✓ API key found (starts with: AIzaSyBm1...)

2. Checking image model configuration...
   Model: gemini-2.0-flash-exp
   ✓ Using NanoBanana (gemini-2.0-flash-exp)

3. Testing API connection...
   ✓ Gemini client initialized

4. Testing image generation (this may take 10-30 seconds)...
   ✓ Response received from API
   ✓ Image generated successfully!
   ✓ Test image saved to: output/nanobanana_test.png
   Image size: 1024x1024 pixels

============================================================
✅ NanoBanana API is working correctly!

You can now use the story generator:
  • GUI: streamlit run app.py
  • CLI: python story_and_image.py --theme 'adventure' --character 'Timmy'
============================================================
```

### Option 2: Generate a Test Story

Generate a complete story with illustration:

```bash
# Set API keys
export GEMINI_API_KEY="your-gemini-key"
export OPENAI_API_KEY="your-openai-key"  # Or ANTHROPIC_API_KEY

# Generate story
python story_and_image.py \
  --theme "a tiny adventure in the garden" \
  --character "Timmy the Beetle" \
  --persona timmy
```

Check `output/story_image.png` - if it exists, NanoBanana is working!

### Option 3: Use the GUI

```bash
streamlit run app.py
```

1. Configure your provider (OpenAI/Anthropic/Gemini)
2. Walk through the wizard to create a story
3. If an image appears at the end, NanoBanana is working!

## Troubleshooting

### ❌ "GEMINI_API_KEY not set"

**Solution:**
```bash
export GEMINI_API_KEY="your-key-here"
```

Get your key at: https://makersuite.google.com/app/apikey

### ❌ "No image returned from NanoBanana"

**Possible causes:**

1. **Content policy restriction** - Try a different theme
   ```bash
   # Avoid: violent, adult, or controversial themes
   # Good: "friendship", "curiosity", "adventure in nature"
   ```

2. **API quota exceeded** - Check usage at: https://console.cloud.google.com/
   - Gemini has free tier limits (60 requests/minute, 1500/day for flash models)
   - Wait a few minutes or upgrade quota

3. **Invalid API key** - Verify at: https://makersuite.google.com/app/apikey

4. **Model not available** - Ensure you're using `gemini-2.0-flash-exp`
   ```bash
   echo $GEMINI_IMAGE_MODEL  # Should be: gemini-2.0-flash-exp
   ```

### ❌ "google-genai package not installed"

**Solution:**
```bash
pip install google-genai pillow
```

### ⚠️ Using a Different Image Model

**Warning:** NanoBanana (`gemini-2.0-flash-exp`) is specifically optimized for the 3D figurine style used in this project.

If you want to experiment with other models:
```bash
export GEMINI_IMAGE_MODEL="gemini-exp-1206"  # Experimental model
# or
export GEMINI_IMAGE_MODEL="gemini-2.0-flash-exp"  # Back to NanoBanana (recommended)
```

**Available Gemini image models:**
- `gemini-2.0-flash-exp` - **NanoBanana (recommended)** - Fast, high-quality, consistent style
- `gemini-exp-1206` - Experimental newer model
- `gemini-pro-vision` - Older vision model (not optimized for generation)

## Verification Checklist

Run through this checklist to ensure everything is working:

- [ ] `GEMINI_API_KEY` is set in environment
- [ ] `config.py` has `GEMINI_IMAGE_MODEL = "gemini-2.0-flash-exp"`
- [ ] `python test_nanobanana.py` passes all tests
- [ ] Test image appears in `output/nanobanana_test.png`
- [ ] Full story generation creates both text and image
- [ ] GUI wizard generates images successfully

## Advanced: Checking API Calls

To see exactly what's being sent to NanoBanana, add debug output:

```python
# In story_and_image.py, before line 229, add:
print(f"DEBUG: Using model: {GEMINI_IMAGE_MODEL}")
print(f"DEBUG: Prompt length: {len(prompt)} chars")
```

This will show you:
```
DEBUG: Using model: gemini-2.0-flash-exp
DEBUG: Prompt length: 843 chars
```

## Architecture Summary

```
┌──────────────────────────────────────────┐
│         Story Text Generation            │
│  (OpenAI GPT / Anthropic Claude /        │
│         Google Gemini)                   │
│              ↓                           │
│      User chooses via                    │
│      LLM_PROVIDER env var                │
└──────────────────────────────────────────┘
                 ↓
┌──────────────────────────────────────────┐
│   Image Prompt Builder (prompt_builder)  │
│   - Extracts scene from story            │
│   - Adds character profile               │
│   - Formats for image generation         │
└──────────────────────────────────────────┘
                 ↓
┌──────────────────────────────────────────┐
│       NanoBanana Image Generation        │
│      (gemini-2.0-flash-exp ONLY)         │
│   - Generates 3D figurine-style art      │
│   - 1024x1024 PNG images                 │
│   - Consistent with character profiles   │
└──────────────────────────────────────────┘
```

## Need Help?

1. Run `python test_nanobanana.py` to diagnose issues
2. Check [README.md](README.md) troubleshooting section
3. Verify API key at https://makersuite.google.com/app/apikey
4. Check quota at https://console.cloud.google.com/

---

**Status:** ✅ NanoBanana is pre-configured and ready to use in your project!
