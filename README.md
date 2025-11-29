# Children's Story Generator with Decoupled LLM Architecture

A flexible children's story generator that lets you choose any LLM provider (OpenAI, Anthropic, Google Gemini) for story generation while using NanoBanana (Gemini's flash image model) for beautiful illustrations.

## Features

- **Decoupled LLM Architecture**: Switch between OpenAI GPT, Anthropic Claude, or Google Gemini for story generation
- **Consistent Image Generation**: Uses Google's NanoBanana (gemini-2.0-flash-exp) for high-quality illustrations
- **Character Profiles**: Pre-configured characters (Timmy the Beetle, Tiny Philosopher Kid)
- **Configurable**: Control story themes, character selection, and output paths
- **Age-Appropriate**: Designed for ages 4-8 with gentle, vivid bedtime stories

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

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Childrens_story_generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables (see Configuration section below)

## Configuration

Create a `.env` file or set environment variables:

```bash
# Choose your LLM provider for story generation
export LLM_PROVIDER="openai"          # or "anthropic" or "gemini"
export LLM_MODEL="gpt-4o"             # or "claude-3-5-sonnet-20241022" or "gemini-1.5-pro-latest"

# API Keys (set the ones you'll use)
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GEMINI_API_KEY="..."

# Image model (NanoBanana) - usually keep this as default
export GEMINI_IMAGE_MODEL="gemini-2.0-flash-exp"
```

See `.env.example` for a template.

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

**Import errors?**
- Make sure you've installed the provider SDK you're using: `pip install openai` or `pip install anthropic`

**API key errors?**
- Check that your environment variables are set correctly
- Verify your API keys are valid and have sufficient credits

**No image generated?**
- Ensure `GEMINI_API_KEY` is set (required for NanoBanana)
- Check that the Gemini API is enabled in your Google Cloud project

## License

MIT

## Contributing

Contributions welcome! Feel free to open issues or submit pull requests.
