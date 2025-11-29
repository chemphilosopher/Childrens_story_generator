#!/usr/bin/env python3
"""
Interactive GUI for Children's Story Generator.

Allows users to upload documents or paste text, which will be transformed
into engaging, memorable children's stories with illustrations.
"""

import os
import sys
import tempfile
from pathlib import Path
from typing import Optional

import streamlit as st
from PIL import Image

from llm_client import LLMClient
from prompt_builder import build_image_prompt
from story_and_image import (
    generate_illustration_for_story,
    get_gemini_image_client,
    sanitize_user_input,
)


def extract_text_from_file(uploaded_file) -> str:
    """
    Extract text from uploaded file.

    Supports: TXT, PDF, DOCX files.
    """
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
    """
    Generate a story that incorporates learning from source material.

    Args:
        source_text: Educational content to incorporate.
        theme: Story theme/lesson to emphasize.
        character: Main character name.
        age_group: Target age range.
        length_words: Target story length.

    Returns:
        Generated educational story.
    """
    # Truncate source text if too long (keep first 2000 chars)
    if len(source_text) > 2000:
        source_snippet = source_text[:2000] + "..."
    else:
        source_snippet = source_text

    system_prompt = f"""You are a children's author who writes gentle, vivid bedtime stories
for ages {age_group}, with simple language but rich imagery. You excel at transforming
complex topics into memorable, engaging stories that help children learn."""

    user_prompt = f"""
Write a {length_words}-word children's story featuring "{character}".

SOURCE MATERIAL (use this as inspiration for the story's educational content):
\"\"\"
{source_snippet}
\"\"\"

STORY THEME: {theme}

INSTRUCTIONS:
- Transform the key concepts from the source material into a fun, memorable adventure
- Make complex ideas simple and relatable for young children
- Weave educational content naturally into the narrative
- The story should be warm, hopeful, and curious
- Easy to read aloud with a clear beginning, middle, and end
- Use simple language but vivid imagery
- No explicit religious terminology; keep it symbolic and philosophical

The child reading this should learn something valuable from the source material while being
entertained by {character}'s adventure.
"""

    llm = LLMClient()
    story = llm.generate(user_prompt.strip(), system_prompt=system_prompt)

    # Validate story was generated
    if not story or len(story.strip()) < 50:
        raise RuntimeError(
            "Generated story is too short or empty. Please try again with different inputs."
        )

    return story


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Children's Story Generator",
        page_icon="📚",
        layout="wide",
    )

    st.title("📚 Educational Story Generator for Kids")
    st.markdown("""
    Transform complex texts and documents into fun, memorable children's stories!
    Upload educational content, and watch it come to life as an engaging adventure.
    """)

    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")

        # LLM Provider selection
        provider = st.selectbox(
            "Text Generation Provider",
            ["openai", "anthropic", "gemini"],
            help="Choose which LLM to use for story generation"
        )

        # Model selection based on provider
        model_defaults = {
            "openai": "gpt-4o",
            "anthropic": "claude-3-5-sonnet-20241022",
            "gemini": "gemini-1.5-pro-latest"
        }

        model = st.text_input(
            "Model Name",
            value=model_defaults.get(provider, "gpt-4o"),
            help="Model to use for text generation"
        )

        # Set environment variables
        os.environ["LLM_PROVIDER"] = provider
        os.environ["LLM_MODEL"] = model

        st.divider()

        # Character selection
        character_preset = st.selectbox(
            "Character",
            ["Timmy the Beetle", "Tiny Philosopher Kai", "Custom"],
            help="Choose a pre-made character or create your own"
        )

        if character_preset == "Custom":
            character = st.text_input(
                "Custom Character Name",
                value="Ruby the Robot",
                max_chars=100
            )
            persona = st.selectbox("Visual Style", ["timmy", "philosopher"])
        else:
            character = character_preset
            persona = "timmy" if "Timmy" in character else "philosopher"

        # Age group
        age_group = st.selectbox(
            "Target Age Group",
            ["4-6", "4-8", "6-10"],
            index=1,
            help="Age range for story complexity"
        )

        # Story length
        length_words = st.slider(
            "Story Length (words)",
            min_value=300,
            max_value=1000,
            value=600,
            step=100,
            help="Approximate word count"
        )

    # Main content area
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📝 Input Your Educational Content")

        # Input method selection
        input_method = st.radio(
            "How would you like to provide content?",
            ["Upload Document", "Paste Text"],
            horizontal=True
        )

        source_text = ""

        if input_method == "Upload Document":
            uploaded_file = st.file_uploader(
                "Upload a document (TXT, PDF, DOCX)",
                type=['txt', 'pdf', 'docx'],
                help="Upload educational content to transform into a story"
            )

            if uploaded_file:
                with st.spinner("Reading document..."):
                    source_text = extract_text_from_file(uploaded_file)

                if source_text:
                    st.success(f"✓ Extracted {len(source_text)} characters from {uploaded_file.name}")
                    with st.expander("Preview extracted text"):
                        st.text_area(
                            "Content",
                            value=source_text[:500] + ("..." if len(source_text) > 500 else ""),
                            height=150,
                            disabled=True
                        )

        else:  # Paste Text
            source_text = st.text_area(
                "Paste your educational content here",
                height=200,
                placeholder="Example: The water cycle is how water moves around Earth. "
                           "Water evaporates from oceans, forms clouds, falls as rain, "
                           "and returns to oceans. This process repeats endlessly...",
                help="Paste any text you want to transform into a story"
            )

        # Theme/lesson input
        theme = st.text_input(
            "Story Theme/Lesson",
            value="curiosity and discovery",
            max_chars=200,
            help="What should children learn or feel from this story?"
        )

        # Generate button
        generate_button = st.button(
            "✨ Generate Story & Illustration",
            type="primary",
            use_container_width=True
        )

    with col2:
        st.header("📖 Your Generated Story")

        # Placeholder for results
        story_placeholder = st.empty()
        image_placeholder = st.empty()

    # Generate story when button is clicked
    if generate_button:
        if not source_text or not source_text.strip():
            st.error("⚠️ Please provide some educational content first!")
            return

        if not theme or not theme.strip():
            st.error("⚠️ Please specify a story theme!")
            return

        # Check API keys
        required_key = f"{provider.upper()}_API_KEY"
        if not os.environ.get(required_key):
            st.error(f"⚠️ {required_key} not set! Please set it in your environment.")
            st.code(f"export {required_key}='your-key-here'")
            return

        if not os.environ.get("GEMINI_API_KEY"):
            st.error("⚠️ GEMINI_API_KEY not set! Required for image generation.")
            st.code("export GEMINI_API_KEY='your-key-here'")
            return

        try:
            # Sanitize inputs
            safe_theme = sanitize_user_input(theme, max_length=200)
            safe_character = sanitize_user_input(character, max_length=100)

            # Generate story
            with st.spinner(f"🎨 Crafting your story with {provider.upper()}..."):
                story = generate_educational_story(
                    source_text=source_text,
                    theme=safe_theme,
                    character=safe_character,
                    age_group=age_group,
                    length_words=length_words,
                )

            # Display story
            with col2:
                st.success("✓ Story generated!")
                story_placeholder.markdown(f"### {safe_character} and {safe_theme.title()}")
                story_placeholder.markdown(story)

                # Download button for story
                st.download_button(
                    "📥 Download Story (TXT)",
                    data=story,
                    file_name=f"story_{safe_character.replace(' ', '_')}.txt",
                    mime="text/plain"
                )

            # Generate illustration
            with st.spinner("🎨 Creating illustration with NanoBanana..."):
                # Save to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                    tmp_path = tmp_file.name

                img_path = generate_illustration_for_story(
                    story_title=f"{safe_character} and {safe_theme}",
                    story_text=story,
                    character=persona,
                    out_file=tmp_path,
                )

            # Display image
            with col2:
                st.success("✓ Illustration generated!")
                img = Image.open(img_path)
                image_placeholder.image(img, use_container_width=True)

                # Download button for image
                with open(img_path, "rb") as f:
                    st.download_button(
                        "📥 Download Image (PNG)",
                        data=f,
                        file_name=f"illustration_{safe_character.replace(' ', '_')}.png",
                        mime="image/png"
                    )

                # Clean up temp file
                try:
                    os.unlink(tmp_path)
                except:
                    pass

            st.balloons()

        except ValueError as e:
            st.error(f"❌ Input error: {str(e)}")
        except RuntimeError as e:
            st.error(f"❌ Generation error: {str(e)}")
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
            st.exception(e)


if __name__ == "__main__":
    main()
