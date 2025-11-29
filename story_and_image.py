# story_and_image.py

import argparse
from io import BytesIO
from pathlib import Path

from PIL import Image
from google import genai

from config import GEMINI_API_KEY, GEMINI_IMAGE_MODEL
from llm_client import LLMClient
from prompt_builder import build_image_prompt


def get_gemini_image_client() -> genai.Client:
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY not set.")
    return genai.Client(api_key=GEMINI_API_KEY)


def decode_and_save_image(part, output_path: Path) -> Path:
    data = part.inline_data.data
    image = Image.open(BytesIO(data))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)
    return output_path


def generate_story_with_llm(
    theme: str,
    character: str,
    length_words: int = 600,
) -> str:
    system_prompt = (
        "You are a children's author who writes gentle, vivid bedtime stories "
        "for ages 4–8, with simple language but rich imagery."
    )
    user_prompt = f"""
Write a {length_words}-word children's story featuring "{character}".
Theme: {theme}

The story should be:
- Warm, hopeful, and curious.
- Easy to read aloud.
- With a clear beginning, middle, and end.
- No explicit religious terminology; keep it symbolic and philosophical.
"""

    llm = LLMClient()
    return llm.generate(user_prompt.strip(), system_prompt=system_prompt)


def generate_illustration_for_story(
    story_title: str,
    story_text: str,
    character: str,
    out_file: str,
) -> str:
    client = get_gemini_image_client()
    prompt = build_image_prompt(story_title, story_text, character)

    response = client.models.generate_content(
        model=GEMINI_IMAGE_MODEL,
        contents=[prompt],
    )

    output_path = Path(out_file)

    for candidate in response.candidates:
        for part in candidate.content.parts:
            if getattr(part, "inline_data", None) and part.inline_data.mime_type.startswith("image/"):
                decode_and_save_image(part, output_path)
                return str(output_path)

    raise RuntimeError("No image returned from NanoBanana / Gemini image model.")


def main():
    parser = argparse.ArgumentParser(description="Generate story + NanoBanana illustration.")
    parser.add_argument("--theme", required=True, help="Theme of the story (e.g. 'courage in small things').")
    parser.add_argument("--character", default="Timmy the Beetle", help="Main character name.")
    parser.add_argument("--persona", default="timmy", choices=["timmy", "philosopher"],
                        help="Visual persona: 'timmy' or 'philosopher'.")
    parser.add_argument("--out-image", default="output/story_image.png", help="Output image path.")
    parser.add_argument("--out-story", default="output/story.txt", help="Output story text file.")
    args = parser.parse_args()

    # 1) Generate story with chosen LLM (OpenAI / Anthropic / Gemini)
    story = generate_story_with_llm(
        theme=args.theme,
        character=args.character,
        length_words=600,
    )

    out_story_path = Path(args.out_story)
    out_story_path.parent.mkdir(parents=True, exist_ok=True)
    out_story_path.write_text(story, encoding="utf-8")
    print(f"Story saved to: {out_story_path}")

    # 2) Generate NanoBanana illustration based on that story
    img_path = generate_illustration_for_story(
        story_title=f"{args.character} and {args.theme}",
        story_text=story,
        character=args.persona,
        out_file=args.out_image,
    )
    print(f"Image saved to: {img_path}")


if __name__ == "__main__":
    main()
