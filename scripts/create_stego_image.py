#!/usr/bin/env python3
"""
create_stego_image.py
Creates the Forensics challenge image with a secret hidden via LSB steganography.

Usage:
    pip install Pillow
    python scripts/create_stego_image.py

Output: media/challenge_files/suspicious.png
        (Upload this via Django admin to the Forensics challenge)

Players solve it with:
    python -c "
    from PIL import Image
    img = Image.open('suspicious.png').convert('RGB')
    pixels = list(img.getdata())
    bits = ''.join(str(c & 1) for p in pixels for c in p)
    msg = ''
    for i in range(0, len(bits), 8):
        ch = chr(int(bits[i:i+8], 2))
        if ch == chr(0): break
        msg += ch
    print(msg)
    "

Or with zsteg:
    zsteg -a suspicious.png
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import random

SECRET = "CTF{st3g0_1s_not_s3cur1ty}"

OUT_DIR = Path(__file__).parent.parent / "media" / "challenge_files"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUT_DIR / "suspicious.png"


def lsb_encode(image: Image.Image, secret_text: str) -> Image.Image:
    """Encode secret_text into the LSB of each colour channel."""
    img = image.convert("RGB")
    pixels = list(img.getdata())

    payload = (secret_text + "\x00").encode("utf-8")
    bits = "".join(f"{byte:08b}" for byte in payload)

    if len(bits) > len(pixels) * 3:
        raise ValueError("Secret too long for this image size.")

    new_pixels = []
    bit_idx = 0
    for r, g, b in pixels:
        if bit_idx < len(bits):
            r = (r & ~1) | int(bits[bit_idx]); bit_idx += 1
        if bit_idx < len(bits):
            g = (g & ~1) | int(bits[bit_idx]); bit_idx += 1
        if bit_idx < len(bits):
            b = (b & ~1) | int(bits[bit_idx]); bit_idx += 1
        new_pixels.append((r, g, b))

    result = Image.new("RGB", img.size)
    result.putdata(new_pixels)
    return result


def create_cover_image(size=(640, 480)) -> Image.Image:
    """Create a natural-looking cover image (a simple landscape)."""
    rng = random.Random(42)  # deterministic
    img = Image.new("RGB", size)
    draw = ImageDraw.Draw(img)

    # Sky — gradient blues
    for y in range(280):
        r = int(90 + y * 0.2)
        g = int(130 + y * 0.25)
        b = int(200 + y * 0.08)
        draw.line([(0, y), (size[0], y)], fill=(min(r,255), min(g,255), min(b,255)))

    # Hills
    for layer, (base_y, height, colour) in enumerate([
        (280, 120, (60, 100, 60)),
        (320, 80,  (70, 115, 55)),
        (350, 60,  (85, 130, 65)),
    ]):
        points = [(0, size[1])]
        x = 0
        y = base_y
        while x <= size[0]:
            y += rng.randint(-12, 12)
            y = max(base_y - height, min(base_y + 20, y))
            points.append((x, y))
            x += rng.randint(15, 35)
        points.append((size[0], size[1]))
        draw.polygon(points, fill=colour)

    # Water reflection at bottom
    draw.rectangle([0, 400, size[0], size[1]], fill=(55, 90, 130))
    for y in range(400, size[1], 4):
        alpha = int(180 + rng.randint(-30, 30))
        for x in range(0, size[0], rng.randint(20, 60)):
            w = rng.randint(10, 50)
            draw.line([(x, y), (x + w, y)],
                      fill=(80 + rng.randint(-10, 10),
                             120 + rng.randint(-10, 10),
                             160 + rng.randint(-10, 10)))

    # A few birds
    for _ in range(5):
        bx = rng.randint(50, size[0] - 50)
        by = rng.randint(40, 160)
        draw.arc([bx, by, bx + 14, by + 7], 0, 180, fill=(20, 20, 20), width=2)
        draw.arc([bx + 14, by, bx + 28, by + 7], 0, 180, fill=(20, 20, 20), width=2)

    # Slight blur to look photographic
    img = img.filter(ImageFilter.GaussianBlur(radius=0.6))
    return img


def verify_decode(path: Path, expected: str):
    """Verify the hidden message can be decoded correctly."""
    img = Image.open(str(path)).convert("RGB")
    pixels = list(img.getdata())
    bits = "".join(str(c & 1) for p in pixels for c in p)
    msg = ""
    for i in range(0, len(bits), 8):
        ch = chr(int(bits[i:i+8], 2))
        if ch == "\x00":
            break
        msg += ch
    assert msg == expected, f"Decode mismatch! Got: {msg!r}"
    return msg


def main():
    print("Creating Forensics (steganography) challenge image...")

    print("  Generating cover image...")
    cover = create_cover_image()

    print(f"  Encoding secret: {SECRET!r}")
    stego = lsb_encode(cover, SECRET)

    stego.save(str(OUT_PATH), "PNG")
    print(f"  Saved to: {OUT_PATH}")

    print("  Verifying decode...")
    decoded = verify_decode(OUT_PATH, SECRET)
    print(f"  ✓ Verified: {decoded!r}")

    print()
    print("Next steps:")
    print("  1. Go to /admin/challenges/challengefile/add/")
    print("  2. Upload suspicious.png and attach it to 'Hidden in Plain Sight'")
    print()
    print("Players can solve it with:")
    print("  $ zsteg -a suspicious.png")
    print("  or with a custom Python LSB decoder (see script docstring)")


if __name__ == "__main__":
    main()
