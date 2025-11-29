# prompt_builder.py
"""
Character profile definitions and image prompt builder.

This module contains pre-defined character profiles for children's story
illustrations and builds detailed visual prompts for the NanoBanana image
generation model based on story content and selected character persona.

Character Profiles:
    - Timmy the Beetle: Friendly beetle character for nature-themed stories
    - Tiny Philosopher Kid: Young thoughtful child for contemplative stories
"""
from textwrap import shorten

TIMMY_PROFILE = """
Timmy the Beetle is a small, friendly beetle for a children's book.
- Shell: shiny deep green with tiny gold speckles
- Eyes: large, curious, expressive
- Accessories: small blue backpack with a yellow star
- Personality: kind, thoughtful, curious, shy but brave when it matters
Style: soft 3D figurine / toy style, warm children's book illustration.
"""

TINY_PHILOSOPHER_PROFILE = """
The tiny philosopher kid is about 6 years old.
- Hair: dark brown, slightly messy
- Clothes: simple shirt, shorts, small satchel
- Expression: thoughtful, kind, slightly amused
Style: soft 3D figurine / toy style, gentle lighting, children's book vibe.
"""


def build_image_prompt(
    story_title: str,
    story_text: str,
    character: str = "timmy",
) -> str:
    """
    Build a detailed image generation prompt from story content.

    Creates a comprehensive prompt for NanoBanana (Gemini image model) that
    includes character visual details, scene context, and artistic direction
    based on the selected character persona.

    Args:
        story_title: Title/description of the story.
        story_text: Full text of the generated story.
        character: Character persona - "timmy" for beetle, "philosopher" for kid.

    Returns:
        Formatted image generation prompt string.

    Note:
        Story text is shortened to 400 characters to fit within prompt limits
        while providing enough context for visual generation.
    """
    scene_snippet = shorten(story_text.replace("\n", " "), width=400, placeholder="…")

    if character.lower() == "timmy":
        base_profile = TIMMY_PROFILE
        char_label = "Timmy the Beetle"
    else:
        base_profile = TINY_PHILOSOPHER_PROFILE
        char_label = "the tiny philosopher kid"

    prompt = f"""
Create a single high-quality 3D figurine-style children's book illustration.

Character:
{base_profile}

Scene:
This image should illustrate a key moment from the story "{story_title}".
Focus on {char_label} in an emotionally important scene.

Story moment to visualize (for inspiration, not for text rendering):
\"\"\"{scene_snippet}\"\"\"

Requirements:
- Show {char_label} clearly in the center of the frame.
- Warm, inviting lighting, suitable for a bedtime story.
- Hint of wonder, curiosity, and adventure.
- No text in the image.
- Composition should work well as a full-page illustration.
"""
    return prompt.strip()
