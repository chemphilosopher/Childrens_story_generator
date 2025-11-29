# GUI Guide - Educational Story Generator

Transform complex documents and texts into fun, memorable children's stories with an easy-to-use web interface!

## Features

✨ **Document Upload**: Upload PDF, DOCX, or TXT files
📝 **Text Paste**: Paste any text directly
🎨 **Auto-Illustration**: Generates beautiful images with NanoBanana
👶 **Age-Appropriate**: Adjust complexity for different age groups
🎭 **Character Choice**: Pre-made characters or create your own
🔄 **Multi-Provider**: Switch between OpenAI, Anthropic, or Gemini
📥 **Download**: Save stories and images instantly

## Quick Start

### 1. Install Dependencies

```bash
# Install all dependencies including GUI
pip install -r requirements.txt

# Or install just what you need:
pip install streamlit google-genai pillow
pip install openai  # Your chosen LLM provider

# Optional: For document upload support
pip install PyPDF2 python-docx
```

### 2. Set Your API Keys

```bash
# For story generation (choose one):
export OPENAI_API_KEY="sk-..."
# OR
export ANTHROPIC_API_KEY="sk-ant-..."

# For image generation (required):
export GEMINI_API_KEY="..."
```

### 3. Launch the GUI

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

## How to Use

### Step 1: Configure (Sidebar)

- **Provider**: Choose OpenAI, Anthropic, or Gemini
- **Model**: Select the specific model (auto-filled with sensible defaults)
- **Character**: Pick Timmy the Beetle, Tiny Philosopher, or create custom
- **Age Group**: 4-6, 4-8, or 6-10 years
- **Story Length**: 300-1000 words

### Step 2: Input Educational Content

**Option A: Upload Document**
- Click "Upload Document"
- Select TXT, PDF, or DOCX file
- App automatically extracts text

**Option B: Paste Text**
- Click "Paste Text"
- Copy/paste your content into the text box

Examples of content:
- Science concepts (water cycle, photosynthesis)
- Historical events (moon landing, ancient civilizations)
- Math concepts (fractions, geometry)
- Life lessons (friendship, honesty, perseverance)
- Any educational material you want to make fun!

### Step 3: Set Theme/Lesson

Tell the app what the story should teach:
- "curiosity and discovery"
- "the importance of teamwork"
- "understanding the water cycle"
- "learning to be patient"

### Step 4: Generate!

Click **"✨ Generate Story & Illustration"**

Watch as your educational content transforms into:
1. An engaging story (appears on the right)
2. A beautiful illustration (below the story)

### Step 5: Download

Use the download buttons to save:
- **Story** as `.txt` file
- **Illustration** as `.png` file

## Example Use Cases

### 1. Science Lesson → Story

**Input (uploaded PDF):**
```
The water cycle describes how water moves on Earth.
Water evaporates from oceans into the atmosphere,
condenses into clouds, falls as precipitation,
and flows back to the oceans.
```

**Theme:** "the endless journey of water"

**Result:** A story about Timmy the Beetle discovering how his friend the water droplet travels around the world!

### 2. History Lesson → Story

**Input (pasted text):**
```
In 1969, Neil Armstrong became the first person to walk
on the moon as part of the Apollo 11 mission.
"That's one small step for man, one giant leap for mankind."
```

**Theme:** "dreams and determination"

**Result:** A story about a young philosopher dreaming of touching the stars and learning about courage.

### 3. Life Skills → Story

**Input:**
```
Friendship means being kind, listening to others,
sharing, and helping when someone needs you.
Good friends make us laugh and support us when we're sad.
```

**Theme:** "what it means to be a true friend"

**Result:** Timmy the Beetle learns what friendship really means through a garden adventure.

## Tips for Best Results

### 1. Keep Source Material Focused
- Upload excerpts rather than entire textbooks
- 500-2000 words is ideal
- Focus on one main concept per story

### 2. Clear Themes Work Best
- Be specific: "learning to share toys" vs. "sharing"
- One lesson per story
- Positive framing

### 3. Choose the Right Character
- **Timmy the Beetle**: Nature, science, exploration themes
- **Tiny Philosopher**: Big questions, emotions, abstract concepts
- **Custom**: Create a character that fits your topic!

### 4. Adjust Age Group
- **4-6**: Very simple language, basic concepts
- **4-8**: Balanced complexity (default)
- **6-10**: More sophisticated vocabulary and ideas

### 5. Provider Selection
- **OpenAI (GPT-4o)**: Creative, whimsical stories
- **Anthropic (Claude)**: Thoughtful, educational narratives
- **Gemini**: Good balance, built-in text+image synergy

## Troubleshooting

### "API key not set" Error

**Problem:** Missing API key for selected provider

**Solution:**
```bash
# Check which provider you selected in the sidebar
# Then set the corresponding key:
export OPENAI_API_KEY="sk-..."
export GEMINI_API_KEY="..."  # Always needed for images
```

Restart Streamlit after setting keys.

### "No module named 'streamlit'" Error

**Solution:**
```bash
pip install streamlit
```

### PDF/DOCX Upload Not Working

**Solution:**
```bash
pip install PyPDF2 python-docx
```

### Image Generation Fails

**Problem:** GEMINI_API_KEY not set or quota exceeded

**Solution:**
1. Verify: `echo $GEMINI_API_KEY`
2. Set it: `export GEMINI_API_KEY="your-key"`
3. Check quota at [Google AI Studio](https://makersuite.google.com/)

### App Doesn't Open in Browser

**Solution:**
```bash
# Manually open the URL shown in terminal:
# Network URL: http://192.168.x.x:8501
# Local URL: http://localhost:8501
```

### Story Quality Issues

**Tips:**
- Provide more context in source material
- Make theme more specific
- Try a different LLM provider
- Adjust age group
- Regenerate with slightly different theme wording

## Advanced: Running on Different Port

```bash
streamlit run app.py --server.port 8080
```

## Advanced: Deploy to Cloud

Deploy your story generator to Streamlit Cloud for free!

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo
4. Add API keys in Streamlit Cloud settings (Secrets)
5. Share with teachers, parents, kids!

Format for secrets:
```toml
OPENAI_API_KEY = "sk-..."
GEMINI_API_KEY = "..."
```

## Command Line Still Available!

The GUI doesn't replace the CLI - both work:

```bash
# Use GUI:
streamlit run app.py

# Use CLI:
python story_and_image.py --theme "courage" --character "Timmy"
```

## Need Help?

- 📖 Check the main [README.md](README.md)
- 🐛 Report issues on GitHub
- 💡 Suggest features via pull requests

---

**Happy Story Creating!** Transform learning into adventure! 🚀📚✨
