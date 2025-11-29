# Multi-Provider LLM Guide

Your Children's Story Generator supports **three LLM providers** for story text generation while always using NanoBanana (Gemini) for illustrations.

## 🎯 Quick Reference

| Provider | Best For | Story Model | Setup Time |
|----------|----------|-------------|------------|
| **OpenAI** | Creative, whimsical stories | `gpt-4o` | 5 min |
| **Anthropic** | Thoughtful, educational narratives | `claude-3-5-sonnet-20241022` | 5 min |
| **Gemini** | Balanced creativity & coherence | `gemini-1.5-pro-latest` | 5 min |

**Image Generation:** All three use **NanoBanana** (`gemini-2.0-flash-exp`) for consistent, high-quality illustrations.

---

## ✅ Your Project Already Supports All Three!

The architecture is **already configured** to work with any provider:

```
Story Text: OpenAI GPT / Anthropic Claude / Google Gemini (your choice)
            ↓
Image: NanoBanana (gemini-2.0-flash-exp) - always the same
```

---

## 📋 Setup Each Provider

### 1️⃣ OpenAI (GPT Models)

**Get API Key:**
- Visit: https://platform.openai.com/api-keys
- Create account and add billing
- Generate new API key

**Set Environment Variables:**
```bash
export OPENAI_API_KEY="sk-your-key-here"
export LLM_PROVIDER="openai"
export LLM_MODEL="gpt-4o"  # or gpt-4o-mini, gpt-4-turbo
```

**Recommended Models:**
- `gpt-4o` - Latest, most creative (recommended)
- `gpt-4o-mini` - Faster, cheaper, still good quality
- `gpt-4-turbo` - Previous flagship model

**Test:**
```bash
python story_and_image.py \
  --theme "a magical garden adventure" \
  --character "Timmy the Beetle" \
  --persona timmy
```

---

### 2️⃣ Anthropic (Claude Models)

**Get API Key:**
- Visit: https://console.anthropic.com/
- Create account and add billing
- Generate API key

**Set Environment Variables:**
```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
export LLM_PROVIDER="anthropic"
export LLM_MODEL="claude-3-5-sonnet-20241022"
```

**Recommended Models:**
- `claude-3-5-sonnet-20241022` - Most capable, thoughtful (recommended)
- `claude-3-5-haiku-20241022` - Faster, cheaper alternative
- `claude-3-opus-20240229` - Previous flagship (more expensive)

**Test:**
```bash
python story_and_image.py \
  --theme "the courage to ask questions" \
  --character "Tiny Philosopher Kai" \
  --persona philosopher
```

---

### 3️⃣ Google Gemini (Gemini Models)

**Get API Key:**
- Visit: https://makersuite.google.com/app/apikey
- Create/login to Google account
- Generate API key (free tier available!)

**Set Environment Variables:**
```bash
export GEMINI_API_KEY="your-gemini-key-here"
export LLM_PROVIDER="gemini"
export LLM_MODEL="gemini-1.5-pro-latest"
```

**Recommended Models:**
- `gemini-1.5-pro-latest` - Most capable (recommended)
- `gemini-1.5-flash` - Faster, cheaper alternative
- `gemini-1.5-flash-8b` - Smallest, fastest

**Test:**
```bash
python story_and_image.py \
  --theme "finding beauty in small moments" \
  --character "Timmy the Beetle" \
  --persona timmy
```

---

## 🖥️ Using Providers in the GUI

### Launch GUI:
```bash
streamlit run app.py
```

### Change Provider:
1. Start the wizard and progress to **Step 5: Review**
2. Expand **"⚙️ Advanced Settings (LLM Provider)"**
3. Select from dropdown:
   - `openai`
   - `anthropic`
   - `gemini`
4. Model auto-fills with sensible default (or customize)
5. Click "🎨 Create My Story!"

**Note:** Make sure the corresponding API key is set in your environment before launching Streamlit!

---

## 🔧 Command Line Examples

### Using OpenAI:
```bash
export OPENAI_API_KEY="sk-..."
export LLM_PROVIDER="openai"
export LLM_MODEL="gpt-4o"

python story_and_image.py \
  --theme "discovering wonder" \
  --character "Timmy the Beetle"
```

### Using Anthropic:
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export LLM_PROVIDER="anthropic"
export LLM_MODEL="claude-3-5-sonnet-20241022"

python story_and_image.py \
  --theme "the joy of learning" \
  --character "Tiny Philosopher Kai" \
  --persona philosopher
```

### Using Gemini:
```bash
export GEMINI_API_KEY="..."
export LLM_PROVIDER="gemini"
export LLM_MODEL="gemini-1.5-pro-latest"

python story_and_image.py \
  --theme "patience and growth" \
  --character "Timmy the Beetle"
```

---

## 🔄 Switching Between Providers

You can switch providers anytime by changing environment variables:

```bash
# Switch from OpenAI to Claude
export LLM_PROVIDER="anthropic"
export LLM_MODEL="claude-3-5-sonnet-20241022"

# Generate a story (will use Claude now)
python story_and_image.py --theme "curiosity"
```

---

## 💰 Cost Comparison

**Story Generation (600 words):**
- OpenAI `gpt-4o`: ~$0.01-0.03 per story
- OpenAI `gpt-4o-mini`: ~$0.001-0.003 per story ⭐ Cheapest
- Anthropic `claude-3-5-sonnet`: ~$0.02-0.04 per story
- Anthropic `claude-3-5-haiku`: ~$0.005-0.01 per story
- Gemini `gemini-1.5-pro`: ~$0.01-0.02 per story
- Gemini `gemini-1.5-flash`: FREE tier available! ⭐ Best for testing

**Image Generation (NanoBanana):**
- `gemini-2.0-flash-exp`: FREE tier (60 requests/min, 1500/day) ⭐

**Budget-Friendly Combo:**
```bash
export LLM_PROVIDER="gemini"
export LLM_MODEL="gemini-1.5-flash"
export GEMINI_API_KEY="..."  # Same key for text + images!
```

---

## 🎨 Provider Personality Differences

### OpenAI (GPT-4o)
**Style:** Creative, whimsical, playful
**Best for:**
- Imaginative adventures
- Magical realism
- Playful characters
- Unexpected plot twists

**Example Output:**
> "Timmy's shell sparkled like emeralds in the morning dew. Today felt different—the kind of different that makes your antennae tingle with excitement..."

---

### Anthropic (Claude)
**Style:** Thoughtful, educational, philosophical
**Best for:**
- Life lessons
- Moral stories
- Educational content
- Deeper meanings
- Gentle wisdom

**Example Output:**
> "Timmy paused at the edge of the leaf, contemplating the vast garden below. Sometimes, he realized, the biggest adventures begin with the smallest steps..."

---

### Gemini
**Style:** Balanced, coherent, consistent
**Best for:**
- Clear narratives
- Educational content
- Reliable quality
- Consistent tone
- Good general-purpose choice

**Example Output:**
> "Timmy the Beetle set out on his morning walk through the garden. The sun was warm, and the flowers were in bloom. He had a feeling today would be special..."

---

## 🔑 Managing Multiple API Keys

### Option 1: Environment Variables (Current Method)
```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GEMINI_API_KEY="..."
```

### Option 2: .env File
Create `.env` in project root:
```bash
# Copy from template
cp .env.example .env

# Edit with your keys
nano .env
```

Then load before running:
```bash
source .env  # Load all keys at once
python story_and_image.py --theme "adventure"
```

---

## 🐛 Troubleshooting

### ❌ "Provider API key not set"
**Solution:** Set the required API key:
```bash
# Check which provider you're using
echo $LLM_PROVIDER

# Set the corresponding key
export OPENAI_API_KEY="sk-..."      # if using openai
export ANTHROPIC_API_KEY="sk-ant-..." # if using anthropic
export GEMINI_API_KEY="..."         # if using gemini
```

### ❌ "Invalid model for provider"
**Problem:** Model doesn't match provider

**Solution:** Check model matches provider:
```bash
# OpenAI models
export LLM_MODEL="gpt-4o"  # NOT claude-3-5-sonnet

# Anthropic models
export LLM_MODEL="claude-3-5-sonnet-20241022"  # NOT gpt-4o

# Gemini models
export LLM_MODEL="gemini-1.5-pro-latest"  # NOT gpt-4o
```

### ❌ "Package not installed"
**Solution:** Install the provider SDK:
```bash
pip install openai      # For OpenAI
pip install anthropic   # For Anthropic
pip install google-genai  # For Gemini (also needed for NanoBanana)
```

### ❌ GUI shows wrong provider
**Solution:** Set environment variables BEFORE launching Streamlit:
```bash
export LLM_PROVIDER="anthropic"
export ANTHROPIC_API_KEY="sk-ant-..."
streamlit run app.py
```

---

## 📊 Quick Comparison Table

| Feature | OpenAI | Anthropic | Gemini |
|---------|--------|-----------|--------|
| **Creativity** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Educational** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Consistency** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Cost (Budget)** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Free Tier** | ❌ | ❌ | ✅ |
| **Setup Speed** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## ✨ Recommendations

### For Beginners:
**Use Gemini** with free tier
```bash
export GEMINI_API_KEY="..."
export LLM_PROVIDER="gemini"
export LLM_MODEL="gemini-1.5-flash"
```

### For Best Quality:
**Use OpenAI GPT-4o** or **Anthropic Claude 3.5 Sonnet**
```bash
# OpenAI
export LLM_PROVIDER="openai"
export LLM_MODEL="gpt-4o"

# OR Anthropic
export LLM_PROVIDER="anthropic"
export LLM_MODEL="claude-3-5-sonnet-20241022"
```

### For Educational Content:
**Use Anthropic Claude**
```bash
export LLM_PROVIDER="anthropic"
export LLM_MODEL="claude-3-5-sonnet-20241022"
```

### For Creative Adventures:
**Use OpenAI GPT-4o**
```bash
export LLM_PROVIDER="openai"
export LLM_MODEL="gpt-4o"
```

---

## 🚀 Next Steps

1. **Choose your provider** based on the comparison above
2. **Get API key** from the provider's website
3. **Set environment variables** for your chosen provider
4. **Test with CLI** or launch the GUI
5. **Generate your first story!**

Remember: All three providers use the same **NanoBanana** image generation, so illustrations will be consistently high-quality regardless of which LLM you choose for text!

---

**Need Help?**
- See [README.md](README.md) for installation
- See [NANOBANANA_VERIFICATION.md](NANOBANANA_VERIFICATION.md) for image testing
- See [GUI_GUIDE.md](GUI_GUIDE.md) for GUI instructions
