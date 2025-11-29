# prompt_builder.py
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
