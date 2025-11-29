#!/usr/bin/env python3
"""
Test script to verify NanoBanana (Gemini image generation) API functionality.

This script performs a minimal test to ensure your GEMINI_API_KEY is set correctly
and that NanoBanana (gemini-2.0-flash-exp) can generate images.
"""

import sys
from io import BytesIO
from pathlib import Path

from PIL import Image
from google import genai

from config import GEMINI_API_KEY, GEMINI_IMAGE_MODEL


def test_nanobanana_connection():
    """Test basic connection to Gemini API."""
    print("=" * 60)
    print("NanoBanana API Test")
    print("=" * 60)

    # Check API key
    print("\n1. Checking GEMINI_API_KEY...")
    if not GEMINI_API_KEY:
        print("   ❌ GEMINI_API_KEY not set!")
        print("   Set it with: export GEMINI_API_KEY='your-key-here'")
        return False

    print(f"   ✓ API key found (starts with: {GEMINI_API_KEY[:10]}...)")

    # Check model configuration
    print(f"\n2. Checking image model configuration...")
    print(f"   Model: {GEMINI_IMAGE_MODEL}")
    if GEMINI_IMAGE_MODEL != "gemini-2.0-flash-exp":
        print(f"   ⚠️  Warning: Expected 'gemini-2.0-flash-exp' (NanoBanana)")
    else:
        print(f"   ✓ Using NanoBanana (gemini-2.0-flash-exp)")

    # Test API connection
    print("\n3. Testing API connection...")
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        print("   ✓ Gemini client initialized")
    except Exception as e:
        print(f"   ❌ Failed to initialize client: {e}")
        return False

    # Test image generation with simple prompt
    print("\n4. Testing image generation (this may take 10-30 seconds)...")
    test_prompt = """
Create a cute 3D figurine-style illustration of a friendly green beetle
with large curious eyes, wearing a small blue backpack, standing in a
sunny garden with colorful flowers. Warm lighting, cheerful atmosphere.
No text in the image.
"""

    try:
        response = client.models.generate_content(
            model=GEMINI_IMAGE_MODEL,
            contents=[test_prompt.strip()],
        )

        if not response or not response.candidates:
            print("   ❌ No image candidates returned")
            return False

        print("   ✓ Response received from API")

        # Try to extract image
        image_found = False
        for candidate in response.candidates:
            if not hasattr(candidate, 'content') or not candidate.content.parts:
                continue

            for part in candidate.content.parts:
                if (hasattr(part, "inline_data") and
                    part.inline_data and
                    hasattr(part.inline_data, "mime_type") and
                    part.inline_data.mime_type.startswith("image/")):

                    # Save test image
                    data = part.inline_data.data
                    image = Image.open(BytesIO(data))

                    test_output = Path("output/nanobanana_test.png")
                    test_output.parent.mkdir(parents=True, exist_ok=True)
                    image.save(test_output)

                    print(f"   ✓ Image generated successfully!")
                    print(f"   ✓ Test image saved to: {test_output}")
                    print(f"   Image size: {image.size[0]}x{image.size[1]} pixels")
                    image_found = True
                    break

            if image_found:
                break

        if not image_found:
            print("   ❌ No image data found in response")
            print("   This may be due to content policy restrictions")
            return False

        return True

    except Exception as e:
        print(f"   ❌ Image generation failed: {e}")
        return False


def main():
    """Run the test."""
    success = test_nanobanana_connection()

    print("\n" + "=" * 60)
    if success:
        print("✅ NanoBanana API is working correctly!")
        print("\nYou can now use the story generator:")
        print("  • GUI: streamlit run app.py")
        print("  • CLI: python story_and_image.py --theme 'adventure' --character 'Timmy'")
    else:
        print("❌ NanoBanana API test failed")
        print("\nTroubleshooting:")
        print("  1. Verify GEMINI_API_KEY is set correctly")
        print("  2. Check API key at: https://makersuite.google.com/app/apikey")
        print("  3. Ensure billing is enabled for Gemini API")
        print("  4. Check quota at: https://console.cloud.google.com/")
    print("=" * 60)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
