#!/usr/bin/env python3
"""
Interactive GUI for Children's Story Generator.

Guided wizard that walks users through creating engaging, memorable
children's stories with illustrations.
"""

import os
import sys
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any

import streamlit as st
from PIL import Image

from llm_client import LLMClient
from prompt_builder import build_image_prompt
from story_and_image import (
    generate_illustration_for_story,
    get_gemini_image_client,
    sanitize_user_input,
)


# Story type templates with pre-configured settings
STORY_TYPES = {
    "Educational Story": {
        "description": "Transform educational content into fun learning adventures",
        "icon": "📚",
        "needs_source": True,
        "default_themes": [
            "discovering how things work",
            "learning through curiosity",
            "understanding the world around us",
            "the joy of asking questions"
        ]
    },
    "Bedtime Story": {
        "description": "Gentle, calming stories perfect for winding down",
        "icon": "🌙",
        "needs_source": False,
        "default_themes": [
            "peaceful dreams and wonder",
            "finding comfort in the night",
            "gentle adventure before sleep",
            "the magic of nighttime"
        ]
    },
    "Life Lesson": {
        "description": "Stories that teach values and social skills",
        "icon": "❤️",
        "needs_source": False,
        "default_themes": [
            "being a good friend",
            "showing kindness to others",
            "learning to share",
            "being brave when scared",
            "patience and perseverance"
        ]
    },
    "Adventure Story": {
        "description": "Exciting journeys that spark imagination",
        "icon": "🗺️",
        "needs_source": False,
        "default_themes": [
            "exploring new places",
            "solving mysteries",
            "helping others on a quest",
            "discovering hidden treasures"
        ]
    },
    "Nature & Science": {
        "description": "Explore the wonders of the natural world",
        "icon": "🌱",
        "needs_source": True,
        "default_themes": [
            "how plants grow",
            "the water cycle adventure",
            "seasons and changes",
            "animal homes and habitats"
        ]
    }
}


def extract_text_from_file(uploaded_file) -> str:
    """Extract text from uploaded file (TXT, PDF, DOCX)."""
    file_extension = uploaded_file.name.split('.')[-1].lower()

    try:
        if file_extension == 'txt':
            return uploaded_file.read().decode('utf-8')

        elif file_extension == 'pdf':
            try:
                import PyPDF2
                from io import BytesIO
                pdf_reader = PyPDF2.PdfReader(BytesIO(uploaded_file.read()))
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
            except ImportError:
                st.error("PDF support requires PyPDF2. Install with: pip install PyPDF2")
                return ""

        elif file_extension in ['docx', 'doc']:
            try:
                import docx
                from io import BytesIO
                doc = docx.Document(BytesIO(uploaded_file.read()))
                text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                return text
            except ImportError:
                st.error("DOCX support requires python-docx. Install with: pip install python-docx")
                return ""
        else:
            st.error(f"Unsupported file type: {file_extension}")
            return ""

    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return ""


def generate_educational_story(
    source_text: str,
    theme: str,
    character: str,
    age_group: str = "4-8",
    length_words: int = 600,
) -> str:
    """Generate a story that incorporates learning from source material."""
    if len(source_text) > 2000:
        source_snippet = source_text[:2000] + "..."
    else:
        source_snippet = source_text

    system_prompt = f"""You are a children's author who writes gentle, vivid bedtime stories
for ages {age_group}, with simple language but rich imagery. You excel at transforming
complex topics into memorable, engaging stories that help children learn."""

    # Build source material section if provided
    source_section = ""
    if source_text:
        source_section = f"SOURCE MATERIAL (use this as inspiration for the story educational content):\n{source_snippet}\n"

    user_prompt = f"""
Write a {length_words}-word children's story featuring "{character}".

{source_section}
STORY THEME: {theme}

INSTRUCTIONS:
- {'Transform the key concepts from the source material into a fun, memorable adventure' if source_text else 'Create an engaging adventure about this theme'}
- Make complex ideas simple and relatable for young children
- The story should be warm, hopeful, and curious
- Easy to read aloud with a clear beginning, middle, and end
- Use simple language but vivid imagery
- No explicit religious terminology; keep it symbolic and philosophical
"""

    llm = LLMClient()
    story = llm.generate(user_prompt.strip(), system_prompt=system_prompt)

    if not story or len(story.strip()) < 50:
        raise RuntimeError("Generated story is too short or empty. Please try again.")

    return story


def initialize_session_state():
    """Initialize session state variables."""
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'story_config' not in st.session_state:
        st.session_state.story_config = {}
    if 'generated_story' not in st.session_state:
        st.session_state.generated_story = None
    if 'generated_image_path' not in st.session_state:
        st.session_state.generated_image_path = None


def step_1_story_type():
    """Step 1: Choose story type."""
    st.header("Step 1: What kind of story do you want? 📖")
    st.markdown("Choose the type of story you'd like to create:")

    # Display story type cards
    cols = st.columns(2)
    for idx, (story_type, info) in enumerate(STORY_TYPES.items()):
        col = cols[idx % 2]
        with col:
            if st.button(
                f"{info['icon']} {story_type}\n\n{info['description']}",
                key=f"type_{story_type}",
                use_container_width=True,
                type="primary" if st.session_state.story_config.get('type') == story_type else "secondary"
            ):
                st.session_state.story_config['type'] = story_type
                st.session_state.story_config['type_info'] = info
                st.session_state.step = 2
                st.rerun()

    if st.session_state.story_config.get('type'):
        st.success(f"✓ Selected: {st.session_state.story_config['type']}")
        if st.button("Next: Choose Theme →", type="primary"):
            st.session_state.step = 2
            st.rerun()


def step_2_theme():
    """Step 2: Choose or enter theme."""
    story_type = st.session_state.story_config['type']
    type_info = st.session_state.story_config['type_info']

    st.header(f"Step 2: What should your {story_type.lower()} be about? 💡")

    st.markdown(f"**Story Type:** {type_info['icon']} {story_type}")

    # Show suggested themes
    st.subheader("Suggested Themes:")
    suggested = type_info['default_themes']

    theme_cols = st.columns(2)
    for idx, theme in enumerate(suggested):
        col = theme_cols[idx % 2]
        with col:
            if st.button(
                f"✨ {theme}",
                key=f"theme_{idx}",
                use_container_width=True
            ):
                st.session_state.story_config['theme'] = theme
                st.session_state.step = 3
                st.rerun()

    st.markdown("---")
    st.subheader("Or create your own theme:")
    custom_theme = st.text_input(
        "What lesson or adventure should the story focus on?",
        placeholder="e.g., 'learning to be patient' or 'the water cycle'",
        max_chars=200,
        help="What do you want children to learn or feel from this story?"
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Back"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if custom_theme and st.button("Next: Choose Content →", type="primary", use_container_width=True):
            st.session_state.story_config['theme'] = custom_theme
            st.session_state.step = 3
            st.rerun()


def step_3_content():
    """Step 3: Provide content (if needed) or skip."""
    story_type = st.session_state.story_config['type']
    type_info = st.session_state.story_config['type_info']
    theme = st.session_state.story_config['theme']

    st.header(f"Step 3: Add Educational Content 📝")
    st.markdown(f"**Theme:** {theme}")

    if type_info['needs_source']:
        st.info(f"💡 For {story_type}, you can optionally provide educational content to transform into a story.")
    else:
        st.info("💡 This story type doesn't require source material, but you can add it if you want!")

    # Input method
    input_method = st.radio(
        "How would you like to provide content?",
        ["Skip (Generate from theme only)", "Upload Document", "Paste Text"],
        help="Choose 'Skip' for pure imagination, or provide content for educational stories"
    )

    source_text = ""

    if input_method == "Upload Document":
        uploaded_file = st.file_uploader(
            "Upload educational content (TXT, PDF, DOCX)",
            type=['txt', 'pdf', 'docx']
        )

        if uploaded_file:
            with st.spinner("Reading document..."):
                source_text = extract_text_from_file(uploaded_file)

            if source_text:
                st.success(f"✓ Extracted {len(source_text)} characters")
                with st.expander("Preview content"):
                    st.text_area(
                        "Content",
                        value=source_text[:500] + ("..." if len(source_text) > 500 else ""),
                        height=150,
                        disabled=True
                    )

    elif input_method == "Paste Text":
        source_text = st.text_area(
            "Paste your educational content here",
            height=200,
            placeholder="Example: The water cycle is how water moves around Earth...",
            help="Paste any text you want to transform into a story"
        )

    st.session_state.story_config['source_text'] = source_text

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Back"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("Next: Choose Character →", type="primary", use_container_width=True):
            st.session_state.step = 4
            st.rerun()


def step_4_character():
    """Step 4: Choose or create character."""
    theme = st.session_state.story_config['theme']

    st.header("Step 4: Who's the star of your story? ⭐")
    st.markdown(f"**Theme:** {theme}")

    char_option = st.radio(
        "Choose a character:",
        ["Timmy the Beetle 🐞", "Tiny Philosopher Kai 🧒", "Create My Own"],
        help="Pick a pre-made character or create your own!"
    )

    if char_option == "Timmy the Beetle 🐞":
        st.session_state.story_config['character'] = "Timmy the Beetle"
        st.session_state.story_config['persona'] = "timmy"

        with st.expander("About Timmy"):
            st.markdown("""
            **Timmy the Beetle** is perfect for:
            - Nature and science stories
            - Garden adventures
            - Learning about the environment
            - Curious exploration

            Timmy has a shiny green shell, large curious eyes, and a little blue backpack!
            """)

    elif char_option == "Tiny Philosopher Kai 🧒":
        st.session_state.story_config['character'] = "Tiny Philosopher Kai"
        st.session_state.story_config['persona'] = "philosopher"

        with st.expander("About Kai"):
            st.markdown("""
            **Tiny Philosopher Kai** is perfect for:
            - Life lessons and values
            - Big questions about the world
            - Emotional learning
            - Thoughtful adventures

            Kai is about 6 years old, thoughtful, kind, and loves to ponder!
            """)

    else:  # Create My Own
        custom_name = st.text_input(
            "What's your character's name?",
            placeholder="e.g., Ruby the Robot, Max the Dragon",
            max_chars=100
        )

        if custom_name:
            st.session_state.story_config['character'] = custom_name

            visual_style = st.selectbox(
                "Visual style for illustration:",
                ["Nature/Animal (like Timmy)", "Child/Person (like Kai)"],
                help="This affects how the illustration looks"
            )
            st.session_state.story_config['persona'] = "timmy" if "Nature" in visual_style else "philosopher"

    # Age group and length
    st.markdown("---")
    st.subheader("Story Details:")

    age_group = st.select_slider(
        "Age Group",
        options=["4-6 (Very Simple)", "4-8 (Balanced)", "6-10 (More Complex)"],
        value="4-8 (Balanced)",
        help="Adjust language complexity"
    )
    st.session_state.story_config['age_group'] = age_group.split()[0]  # Extract "4-8"

    length = st.slider(
        "Story Length (words)",
        min_value=300,
        max_value=1000,
        value=600,
        step=100
    )
    st.session_state.story_config['length_words'] = length

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Back"):
            st.session_state.step = 3
            st.rerun()
    with col2:
        if st.session_state.story_config.get('character') and st.button("Review & Generate →", type="primary", use_container_width=True):
            st.session_state.step = 5
            st.rerun()


def step_5_review():
    """Step 5: Review and generate."""
    st.header("Step 5: Review & Generate ✨")

    config = st.session_state.story_config

    # Show summary
    st.subheader("Your Story Configuration:")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        **Story Type:** {config.get('type', 'Not set')}
        **Theme:** {config.get('theme', 'Not set')}
        **Character:** {config.get('character', 'Not set')}
        """)

    with col2:
        st.markdown(f"""
        **Age Group:** {config.get('age_group', '4-8')} years
        **Length:** ~{config.get('length_words', 600)} words
        **Source Content:** {'Yes (' + str(len(config.get('source_text', ''))) + ' chars)' if config.get('source_text') else 'No'}
        """)

    if config.get('source_text'):
        with st.expander("View source content"):
            st.text_area("Content", value=config['source_text'][:500] + "...", height=100, disabled=True)

    st.markdown("---")

    # Provider settings (collapsible)
    with st.expander("⚙️ Advanced Settings (LLM Provider)"):
        provider = st.selectbox(
            "Text Generation Provider",
            ["openai", "anthropic", "gemini"],
            help="Choose which LLM to use"
        )
        os.environ["LLM_PROVIDER"] = provider

        model_defaults = {
            "openai": "gpt-4o",
            "anthropic": "claude-3-5-sonnet-20241022",
            "gemini": "gemini-1.5-pro-latest"
        }
        model = st.text_input("Model", value=model_defaults[provider])
        os.environ["LLM_MODEL"] = model

    # Generate button
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Back"):
            st.session_state.step = 4
            st.rerun()

    with col2:
        if st.button("🎨 Create My Story!", type="primary", use_container_width=True):
            # Validate API keys
            provider = os.environ.get("LLM_PROVIDER", "openai")
            required_key = f"{provider.upper()}_API_KEY"

            if not os.environ.get(required_key):
                st.error(f"⚠️ {required_key} not set! Please set it in your environment.")
                st.code(f"export {required_key}='your-key-here'")
                return

            if not os.environ.get("GEMINI_API_KEY"):
                st.error("⚠️ GEMINI_API_KEY not set! Required for image generation.")
                return

            # Generate story
            with st.spinner("🎨 Crafting your story..."):
                try:
                    safe_theme = sanitize_user_input(config['theme'], max_length=200)
                    safe_character = sanitize_user_input(config['character'], max_length=100)

                    story = generate_educational_story(
                        source_text=config.get('source_text', ''),
                        theme=safe_theme,
                        character=safe_character,
                        age_group=config.get('age_group', '4-8'),
                        length_words=config.get('length_words', 600),
                    )

                    st.session_state.generated_story = story

                except Exception as e:
                    st.error(f"❌ Story generation failed: {str(e)}")
                    return

            # Generate illustration
            with st.spinner("🎨 Creating illustration..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                        tmp_path = tmp_file.name

                    img_path = generate_illustration_for_story(
                        story_title=f"{safe_character} and {safe_theme}",
                        story_text=story,
                        character=config.get('persona', 'timmy'),
                        out_file=tmp_path,
                    )

                    st.session_state.generated_image_path = img_path

                except Exception as e:
                    st.error(f"❌ Image generation failed: {str(e)}")
                    st.session_state.generated_image_path = None

            st.session_state.step = 6
            st.rerun()


def step_6_result():
    """Step 6: Show results."""
    st.header("Your Story is Ready! 📖✨")

    config = st.session_state.story_config
    story = st.session_state.generated_story
    img_path = st.session_state.generated_image_path

    # Display story
    st.subheader(f"{config['character']} and {config['theme'].title()}")
    st.markdown(story)

    # Download story
    st.download_button(
        "📥 Download Story (TXT)",
        data=story,
        file_name=f"story_{config['character'].replace(' ', '_')}.txt",
        mime="text/plain"
    )

    # Display image
    if img_path:
        st.subheader("Illustration:")
        img = Image.open(img_path)
        st.image(img, use_container_width=True)

        # Download image
        with open(img_path, "rb") as f:
            st.download_button(
                "📥 Download Image (PNG)",
                data=f,
                file_name=f"illustration_{config['character'].replace(' ', '_')}.png",
                mime="image/png"
            )

    st.markdown("---")

    # Create another story
    if st.button("✨ Create Another Story", type="primary", use_container_width=True):
        # Reset state
        st.session_state.step = 1
        st.session_state.story_config = {}
        st.session_state.generated_story = None
        st.session_state.generated_image_path = None
        st.rerun()


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Story Wizard",
        page_icon="📚",
        layout="wide",
    )

    # Initialize session state
    initialize_session_state()

    # Header
    st.title("📚 Educational Story Wizard")
    st.markdown("*Create magical, memorable stories for children - step by step!*")

    # Progress bar
    if st.session_state.step < 6:
        progress = (st.session_state.step - 1) / 5
        st.progress(progress, text=f"Step {st.session_state.step} of 5")

    st.markdown("---")

    # Route to appropriate step
    if st.session_state.step == 1:
        step_1_story_type()
    elif st.session_state.step == 2:
        step_2_theme()
    elif st.session_state.step == 3:
        step_3_content()
    elif st.session_state.step == 4:
        step_4_character()
    elif st.session_state.step == 5:
        step_5_review()
    elif st.session_state.step == 6:
        step_6_result()

    # Footer
    st.markdown("---")
    st.markdown("*Powered by your choice of OpenAI, Anthropic, or Gemini for stories • NanoBanana for illustrations*")


if __name__ == "__main__":
    main()
