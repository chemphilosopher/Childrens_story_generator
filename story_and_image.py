# story_and_image.py
"""
Main orchestration script for children's story generation.

This script coordinates the full workflow:
1. Validate and sanitize user inputs
2. Generate story text using chosen LLM provider (OpenAI/Anthropic/Gemini)
3. Build visual prompt from story content
4. Generate illustration using NanoBanana (Gemini flash image model)
5. Save both story text and image to output directory
"""

import argparse
import re
import sys
from io import BytesIO
from pathlib import Path

from PIL import Image
from google import genai

from config import GEMINI_API_KEY, GEMINI_IMAGE_MODEL
from llm_client import LLMClient
from prompt_builder import build_image_prompt


def validate_output_path(filepath: str, base_dir: str = "output") -> Path:
    """
    Validate output path to prevent directory traversal attacks.

    Args:
        filepath: User-provided file path.
        base_dir: Allowed base directory for outputs (default: "output").

    Returns:
        Validated absolute Path object within base directory.

    Raises:
        ValueError: If path attempts to escape base directory or has invalid extension.
    """
    # Resolve to absolute paths
    base = Path(base_dir).resolve()
    target = (base / filepath).resolve()

    # Ensure target is within base directory
    try:
        target.relative_to(base)
    except ValueError:
        raise ValueError(
            f"Security error: Path '{filepath}' attempts to escape base directory '{base_dir}'"
        )

    # Validate file extension (defense in depth)
    allowed_extensions = {'.png', '.jpg', '.jpeg', '.txt'}
    if target.suffix.lower() not in allowed_extensions:
        raise ValueError(
            f"Invalid file extension '{target.suffix}'. "
            f"Allowed: {', '.join(allowed_extensions)}"
        )

    return target


def sanitize_user_input(text: str, max_length: int = 200) -> str:
    """
    Sanitize user input to prevent prompt injection attacks.

    Args:
        text: User-provided text.
        max_length: Maximum allowed length (default: 200 chars).

    Returns:
        Sanitized text safe for use in LLM prompts.

    Raises:
        ValueError: If input is empty, too long, or contains malicious patterns.
    """
    if not text or not text.strip():
        raise ValueError("Input cannot be empty")

    # Enforce length limit
    if len(text) > max_length:
        raise ValueError(
            f"Input exceeds maximum length of {max_length} characters (got {len(text)})"
        )

    # Remove control characters and normalize whitespace
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()

    # Block common injection patterns
    dangerous_patterns = [
        (r'ignore\s+(previous|all|above)', "instruction bypass"),
        (r'disregard\s+(previous|all|above)', "instruction bypass"),
        (r'system\s*:', "system prompt injection"),
        (r'\[INST\]', "instruction injection"),
    ]

    for pattern, description in dangerous_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            raise ValueError(f"Input contains potentially malicious content: {description}")

    return text


def get_gemini_image_client() -> genai.Client:
    """
    Initialize Gemini client for image generation.

    Returns:
        Configured Gemini client.

    Raises:
        RuntimeError: If GEMINI_API_KEY is not set.
    """
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY environment variable is not set.\n"
            "Image generation requires Gemini API. Set it with:\n"
            "export GEMINI_API_KEY='your-key-here'"
        )
    return genai.Client(api_key=GEMINI_API_KEY)


def decode_and_save_image(part, output_path: Path) -> Path:
    """
    Decode image data from API response and save to file.

    Args:
        part: Content part from Gemini response containing inline image data.
        output_path: Path object where image should be saved.

    Returns:
        Path object of saved image.

    Raises:
        RuntimeError: If image decoding or saving fails.
    """
    try:
        data = part.inline_data.data
        image = Image.open(BytesIO(data))
        output_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path)
        return output_path
    except AttributeError:
        raise RuntimeError("Invalid image data structure from API")
    except OSError as e:
        raise RuntimeError(f"Failed to save image: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Image processing error: {str(e)}")


def generate_story_with_llm(
    theme: str,
    character: str,
    length_words: int = 600,
) -> str:
    """
    Generate a children's story using the configured LLM provider.

    Args:
        theme: Story theme (e.g., "courage in small things").
        character: Main character name (e.g., "Timmy the Beetle").
        length_words: Target story length in words (default: 600).

    Returns:
        Generated story text suitable for ages 4-8.

    Raises:
        ValueError: If inputs are invalid.
        RuntimeError: If story generation fails.
    """
    # Inputs are already sanitized by main(), but validate length
    if length_words < 100 or length_words > 2000:
        raise ValueError("Story length must be between 100 and 2000 words")

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
    story = llm.generate(user_prompt.strip(), system_prompt=system_prompt)

    # Validate story was generated
    if not story or len(story.strip()) < 50:
        raise RuntimeError(
            "Generated story is too short or empty. Please try again with a different theme."
        )

    return story


def generate_illustration_for_story(
    story_title: str,
    story_text: str,
    character: str,
    out_file: str,
) -> str:
    """
    Generate an illustration using NanoBanana (Gemini image model).

    Args:
        story_title: Title for the visual prompt.
        story_text: Full story text for scene extraction.
        character: Character persona ("timmy" or "philosopher").
        out_file: Output path for generated image (PNG).

    Returns:
        Path to saved image file.

    Raises:
        RuntimeError: If image generation or saving fails.
    """
    try:
        client = get_gemini_image_client()
        prompt = build_image_prompt(story_title, story_text, character)

        response = client.models.generate_content(
            model=GEMINI_IMAGE_MODEL,
            contents=[prompt],
        )

        # Validate response
        if not response or not response.candidates:
            raise RuntimeError("Gemini returned no image candidates")

        output_path = Path(out_file)

        for candidate in response.candidates:
            if not hasattr(candidate, 'content') or not candidate.content.parts:
                continue

            for part in candidate.content.parts:
                # Safely check for inline image data
                if (hasattr(part, "inline_data") and
                    part.inline_data and
                    hasattr(part.inline_data, "mime_type") and
                    part.inline_data.mime_type.startswith("image/")):
                    decode_and_save_image(part, output_path)
                    return str(output_path)

        raise RuntimeError(
            "No image returned from NanoBanana / Gemini image model.\n"
            "This may be due to content policy restrictions or API issues.\n"
            "Try a different theme or character description."
        )

    except RuntimeError:
        raise  # Re-raise our custom errors
    except Exception as e:
        raise RuntimeError(f"Failed to generate illustration: {str(e)}")


def main():
    """Main entry point for story and image generation."""
    parser = argparse.ArgumentParser(
        description="Generate children's story + NanoBanana illustration.",
        epilog="Example: python story_and_image.py --theme 'courage' --character 'Timmy the Beetle'"
    )
    parser.add_argument(
        "--theme",
        required=True,
        help="Theme of the story (e.g. 'courage in small things'). Max 200 chars."
    )
    parser.add_argument(
        "--character",
        default="Timmy the Beetle",
        help="Main character name. Max 100 chars."
    )
    parser.add_argument(
        "--persona",
        default="timmy",
        choices=["timmy", "philosopher"],
        help="Visual persona: 'timmy' for beetle, 'philosopher' for kid."
    )
    parser.add_argument(
        "--out-image",
        default="output/story_image.png",
        help="Output image path (relative to 'output/' directory)."
    )
    parser.add_argument(
        "--out-story",
        default="output/story.txt",
        help="Output story text file (relative to 'output/' directory)."
    )
    args = parser.parse_args()

    try:
        # Validate and sanitize inputs
        print("Validating inputs...")
        safe_theme = sanitize_user_input(args.theme, max_length=200)
        safe_character = sanitize_user_input(args.character, max_length=100)

        # Validate output paths to prevent directory traversal
        out_story_path = validate_output_path(args.out_story)
        out_image_path = validate_output_path(args.out_image)

        # 1) Generate story with chosen LLM (OpenAI / Anthropic / Gemini)
        print(f"Generating story with theme: '{safe_theme}'...")
        story = generate_story_with_llm(
            theme=safe_theme,
            character=safe_character,
            length_words=600,
        )

        # Save story
        print("Saving story...")
        out_story_path.parent.mkdir(parents=True, exist_ok=True)
        out_story_path.write_text(story, encoding="utf-8")
        print(f"✓ Story saved to: {out_story_path}")

        # 2) Generate NanoBanana illustration based on that story
        print("Generating illustration...")
        img_path = generate_illustration_for_story(
            story_title=f"{safe_character} and {safe_theme}",
            story_text=story,
            character=args.persona,
            out_file=str(out_image_path),
        )
        print(f"✓ Image saved to: {img_path}")

        print("\n✓ Story generation complete!")
        return 0

    except ValueError as e:
        print(f"\n✗ Input error: {str(e)}", file=sys.stderr)
        return 1
    except RuntimeError as e:
        print(f"\n✗ Error: {str(e)}", file=sys.stderr)
        return 1
    except PermissionError as e:
        print(f"\n✗ Permission denied: {str(e)}", file=sys.stderr)
        print("Check that you have write permissions to the output directory.", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"\n✗ File system error: {str(e)}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n\n✗ Interrupted by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}", file=sys.stderr)
        print("\nIf this persists, please check:", file=sys.stderr)
        print("1. API keys are set correctly", file=sys.stderr)
        print("2. Required packages are installed", file=sys.stderr)
        print("3. Internet connection is working", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
