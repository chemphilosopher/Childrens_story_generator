# Children's Story Generator with Decoupled LLM Architecture

A flexible children's story generator that lets you choose any LLM provider (OpenAI, Anthropic, Google Gemini) for story generation while using NanoBanana (Gemini's flash image model) for beautiful illustrations.

**✨ NEW: Interactive GUI!** Transform educational documents and complex texts into fun, memorable children's stories with our easy-to-use web interface!

## Features

- **🎨 Interactive Web GUI**: Upload documents (PDF, DOCX, TXT) or paste text to generate educational stories
- **📚 Educational Mode**: Transform complex content into child-friendly learning adventures
- **Decoupled LLM Architecture**: Switch between OpenAI GPT, Anthropic Claude, or Google Gemini for story generation
- **Consistent Image Generation**: Uses Google's NanoBanana (gemini-2.0-flash-exp) for high-quality illustrations
- **Character Profiles**: Pre-configured characters (Timmy the Beetle, Tiny Philosopher Kid) or create your own
- **Configurable**: Control story themes, character selection, output paths, and age groups
- **Age-Appropriate**: Designed for ages 4-10 with gentle, vivid bedtime stories
- **Dual Interface**: Use the GUI or command-line interface

## Two Ways to Use

### Option 1: Interactive GUI (Recommended for Beginners) 🆕

Perfect for uploading educational materials and creating stories interactively!

```bash
# Install dependencies with GUI support
pip install -r requirements.txt

# Set your API keys
export OPENAI_API_KEY="sk-..."
export GEMINI_API_KEY="..."

# Launch the web interface
streamlit run app.py
```

Then upload documents, paste text, and watch complex content transform into engaging stories!

👉 **See the [GUI Guide](GUI_GUIDE.md) for detailed instructions and examples.**

### Option 2: Command Line (For Automation & Scripts)

Perfect for batch processing and integration into other tools!

```bash
python story_and_image.py \
  --theme "a tiny adventure in the garden" \
  --character "Timmy the Beetle" \
  --persona timmy
```

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  story_and_image.py                 │
│                   (Orchestrator)                    │
└───────────────┬─────────────────┬───────────────────┘
                │                 │
        ┌───────▼────────┐  ┌────▼──────────────────┐
        │  llm_client.py │  │  prompt_builder.py    │
        │  (Story Gen)   │  │  (Character Profiles) │
        └───────┬────────┘  └────┬──────────────────┘
                │                │
    ┌───────────▼────────────────▼──────────────┐
    │         NanoBanana (Gemini Image)         │
    │         gemini-2.0-flash-exp              │
    └───────────────────────────────────────────┘
```

## Prerequisites

Before you begin, ensure you have:

- **Python 3.8 or higher** (Check with `python --version`)
- **pip** (Python package manager)
- **API keys** from at least one LLM provider:
  - [OpenAI API Key](https://platform.openai.com/api-keys) (requires billing setup)
  - [Anthropic API Key](https://console.anthropic.com/) (requires billing setup)
  - [Google AI Studio API Key](https://makersuite.google.com/app/apikey)
- **Gemini API key** (required for image generation, even if you use OpenAI/Anthropic for stories)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/Childrens_story_generator.git
cd Childrens_story_generator
```

2. Create and activate a virtual environment (recommended):
```bash
# On Linux/Mac:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
# Option 1: Install only what you need (recommended)
pip install google-genai pillow  # Core dependencies

# Then install your chosen LLM provider:
pip install openai      # For OpenAI
# OR
pip install anthropic   # For Anthropic
# OR both are already included in google-genai for Gemini

# Option 2: Install everything (all providers)
pip install -r requirements.txt
```

4. Verify installation:
```bash
python -c "import PIL, google.genai; print('✓ Core dependencies installed')"
```

5. Set up your environment variables (see Configuration section below)

## Configuration

Set up your environment variables:

```bash
# Choose your LLM provider for story generation
export LLM_PROVIDER="openai"          # or "anthropic" or "gemini"
export LLM_MODEL="gpt-4o"             # or "claude-3-5-sonnet-20241022" or "gemini-1.5-pro-latest"

# API Keys (set the ones you'll use)
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GEMINI_API_KEY="..."           # REQUIRED for image generation

# Image model (NanoBanana) - usually keep this as default
export GEMINI_IMAGE_MODEL="gemini-2.0-flash-exp"
```

**Note:** If using Anthropic or Gemini, you MUST also set the appropriate `LLM_MODEL`:
- Anthropic: `claude-3-5-sonnet-20241022`, `claude-3-5-haiku-20241022`
- Gemini: `gemini-1.5-pro-latest`, `gemini-1.5-flash`

See `.env.example` for a template.

## Quick Start

Test your setup with a simple story:

```bash
python story_and_image.py \
  --theme "a tiny adventure in the garden" \
  --character "Timmy the Beetle" \
  --persona timmy
```

You should see:
```
Validating inputs...
Generating story with theme: 'a tiny adventure in the garden'...
Saving story...
✓ Story saved to: output/story.txt
Generating illustration...
✓ Image saved to: output/story_image.png

✓ Story generation complete!
```

Check the `output/` directory for your generated story and illustration!

## Usage

### Basic Usage

Generate a story with default settings (OpenAI):

```bash
python story_and_image.py \
  --theme "discovering wonder in a tiny forest stream" \
  --character "Timmy the Beetle" \
  --persona timmy
```

### Using Different LLM Providers

**With Anthropic Claude:**
```bash
export LLM_PROVIDER="anthropic"
export LLM_MODEL="claude-3-5-sonnet-20241022"
python story_and_image.py \
  --theme "the courage to ask questions" \
  --character "Tiny Philosopher Kai" \
  --persona philosopher
```

**With Google Gemini:**
```bash
export LLM_PROVIDER="gemini"
export LLM_MODEL="gemini-1.5-pro-latest"
python story_and_image.py \
  --theme "finding beauty in small moments" \
  --character "Timmy the Beetle" \
  --persona timmy
```

### Command-Line Arguments

```
--theme         (required) Theme of the story (e.g., 'courage in small things')
--character     Character name (default: "Timmy the Beetle")
--persona       Visual character style: 'timmy' or 'philosopher' (default: timmy)
--out-image     Output image path (default: output/story_image.png)
--out-story     Output story text file (default: output/story.txt)
```

### Example Commands

1. **Timmy the Beetle explores friendship:**
```bash
python story_and_image.py \
  --theme "the joy of making new friends" \
  --character "Timmy the Beetle" \
  --persona timmy \
  --out-image output/timmy_friendship.png \
  --out-story output/timmy_friendship.txt
```

2. **Philosopher kid ponders big questions:**
```bash
python story_and_image.py \
  --theme "why the sky changes colors" \
  --character "Young Kai" \
  --persona philosopher \
  --out-image output/kai_sky.png \
  --out-story output/kai_sky.txt
```

## Project Structure

```
Childrens_story_generator/
├── config.py              # Configuration and API key management
├── llm_client.py          # Provider-agnostic LLM wrapper
├── prompt_builder.py      # Character profiles and image prompt builder
├── story_and_image.py     # Main orchestration script
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variable template
├── .gitignore            # Git ignore patterns
└── output/               # Generated stories and images
    ├── *.txt             # Story text files
    └── *.png             # Generated illustrations
```

## How It Works

1. **Story Generation**: The `llm_client.py` module provides a unified interface for OpenAI, Anthropic, or Gemini. You choose your provider via environment variables.

2. **Image Prompt Building**: `prompt_builder.py` takes the generated story and creates a detailed visual prompt based on the selected character persona (Timmy or Philosopher).

3. **Image Generation**: The visual prompt is sent to NanoBanana (Gemini's flash image model) which generates a high-quality 3D figurine-style illustration.

4. **Output**: Both the story text and image are saved to the `output/` directory.

## Character Profiles

### Timmy the Beetle
- Shiny deep green shell with tiny gold speckles
- Large, curious, expressive eyes
- Blue backpack with a yellow star
- Kind, thoughtful, curious personality
- Shy but brave when it matters

### Tiny Philosopher Kid
- About 6 years old
- Dark brown, slightly messy hair
- Simple shirt, shorts, small satchel
- Thoughtful, kind, slightly amused expression
- Perfect for stories about big questions

## Tips

1. **Provider Selection**:
   - OpenAI GPT-4o: Great for creative, whimsical stories
   - Anthropic Claude: Excellent for thoughtful, philosophical narratives
   - Google Gemini: Good balance of creativity and coherence

2. **Theme Ideas**:
   - "overcoming fear of the dark"
   - "the beauty of being different"
   - "learning to share"
   - "curiosity and exploration"
   - "patience and growth"

3. **API Costs**: Consider using the flash models for cost efficiency during testing:
   - `gpt-4o-mini` for OpenAI
   - `claude-3-5-haiku-20241022` for Anthropic
   - `gemini-1.5-flash` for Google

## Troubleshooting

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'openai'` (or `anthropic`, `google.genai`)

**Solution:**
- Install the missing provider SDK:
  ```bash
  pip install openai      # For OpenAI
  pip install anthropic   # For Anthropic
  pip install google-genai  # For Gemini
  ```
- Verify installation: `pip list | grep openai`

### API Key Errors

**Problem:** `RuntimeError: OPENAI_API_KEY not set` (or similar for other providers)

**Solution:**
1. Verify your environment variable is set: `echo $OPENAI_API_KEY`
2. If empty, export it: `export OPENAI_API_KEY="sk-your-key-here"`
3. Check that your API key is valid in the provider's dashboard
4. Ensure your API key has billing enabled and sufficient credits

**Problem:** `RuntimeError: OpenAI API key is invalid`

**Solution:**
- Verify the API key hasn't been revoked
- Check for extra spaces or quotes in your key
- Generate a new API key from the provider dashboard

### Model Errors

**Problem:** `RuntimeError: Invalid OpenAI model: claude-3-5-sonnet-20241022`

**Solution:**
- You're using a model from the wrong provider! Check that `LLM_MODEL` matches `LLM_PROVIDER`:
  - OpenAI: `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo`
  - Anthropic: `claude-3-5-sonnet-20241022`, `claude-3-5-haiku-20241022`
  - Gemini: `gemini-1.5-pro-latest`, `gemini-1.5-flash`

### No Image Generated

**Problem:** Story generates but no image appears

**Solution:**
- Ensure `GEMINI_API_KEY` is set (required for ALL image generation)
- Check Gemini API quota in [Google Cloud Console](https://console.cloud.google.com/)
- Verify the output directory is writable
- Try a different theme - some themes may violate content policies

### Rate Limiting

**Problem:** `RuntimeError: OpenAI rate limit exceeded`

**Solution:**
- Wait 30-60 seconds and try again
- Upgrade your API plan for higher rate limits
- Switch to a different provider temporarily

### Permission Errors

**Problem:** `Permission denied` when saving files

**Solution:**
- Check write permissions: `ls -ld output/`
- Create output directory manually: `mkdir -p output`
- Run with appropriate permissions or change output directory

### Input Validation Errors

**Problem:** `ValueError: Input exceeds maximum length`

**Solution:**
- Keep themes under 200 characters
- Keep character names under 100 characters
- Simplify your input text

**Problem:** `ValueError: Input contains potentially malicious content`

**Solution:**
- Avoid phrases like "ignore previous instructions" in your theme
- Use simple, straightforward language
- If you think this is a false positive, rephrase your theme slightly

### Path Security Errors

**Problem:** `ValueError: Security error: Path '../../../etc/passwd' attempts to escape base directory`

**Solution:**
- Don't use `..` in output paths
- Output files must be within the `output/` directory
- Use simple filenames like `my_story.txt`

### General Tips

- **Check your internet connection** - All features require API access
- **Verify Python version**: `python --version` (should be 3.8+)
- **Check API status pages**:
  - [OpenAI Status](https://status.openai.com/)
  - [Anthropic Status](https://status.anthropic.com/)
  - [Google Cloud Status](https://status.cloud.google.com/)

### Still Having Issues?

1. Enable verbose error messages by running with `python -u story_and_image.py ...`
2. Check that all environment variables are set: `env | grep -E "(LLM|API_KEY)"`
3. Try the Quick Start example first to verify basic functionality
4. Open an issue on GitHub with the full error message and your setup details (but DO NOT include API keys!)

## License

MIT

## Contributing

Contributions welcome! Feel free to open issues or submit pull requests.
