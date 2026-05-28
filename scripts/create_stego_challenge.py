"""
scripts/create_stego_challenge.py

Generates the forensics challenge image using LSB steganography.
The flag is hidden in the least significant bits of the RGB channels.

Usage:
    pip install Pillow
    python scripts/create_stego_challenge.py

Upload challenge_assets/suspicious.png to the Forensics challenge.
"""

from PIL import Image, ImageDraw
import os, random


FLAG = "CTF{st3g0_1s_not_s3cur1ty}"


# ── LSB Encoder ────────────────────────────────────────────────────────

def lsb_encode(image: Image.Image, secret: str) -> Image.Image:
    """Hide secret string in the LSBs of the image's RGB values."""
    pixels = list(image.getdata())
    width, height = image.size

    payload = secret.encode("utf-8") + b"\x00"  # null terminator
    bits = "".join(f"{byte:08b}" for byte in payload)

    if len(bits) > len(pixels) * 3:
        raise ValueError(f"Image too small: need {len(bits)} bits, have {len(pixels) * 3}")

    new_pixels = []
    bit_idx = 0
    for r, g, b in pixels:
        if bit_idx < len(bits):
            r = (r & 0xFE) | int(bits[bit_idx]); bit_idx += 1
        if bit_idx < len(bits):
            g = (g & 0xFE) | int(bits[bit_idx]); bit_idx += 1
        if bit_idx < len(bits):
            b = (b & 0xFE) | int(bits[bit_idx]); bit_idx += 1
        new_pixels.append((r, g, b))

    result = Image.new("RGB", image.size)
    result.putdata(new_pixels)
    return result


def lsb_decode(image: Image.Image) -> str:
    """Extract hidden string from LSBs — for verification."""
    pixels = list(image.getdata())
    bits = ""
    for r, g, b in pixels:
        bits += str(r & 1)
        bits += str(g & 1)
        bits += str(b & 1)

    chars = []
    for i in range(0, len(bits), 8):
        byte = int(bits[i:i + 8], 2)
        if byte == 0:
            break
        chars.append(chr(byte))
    return "".join(chars)


# ── Generate a plausible-looking base image ────────────────────────────

def generate_base_image(width=640, height=480) -> Image.Image:
    """Create a 'normal' looking photo — abstract cityscape."""
    random.seed(42)
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)

    # Sky
    for y in range(int(height * 0.55)):
        t = y / (height * 0.55)
        r = int(30 + t * 80)
        g = int(50 + t * 100)
        b = int(120 + t * 80)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Ground / road
    for y in range(int(height * 0.55), height):
        t = (y - height * 0.55) / (height * 0.45)
        shade = int(40 + t * 30)
        draw.line([(0, y), (width, y)], fill=(shade, shade, shade + 5))

    # Buildings
    buildings = [
        (20,  300, 90,  height, (60, 65, 70)),
        (100, 250, 170, height, (55, 60, 65)),
        (180, 200, 260, height, (70, 70, 75)),
        (270, 280, 340, height, (50, 55, 60)),
        (350, 180, 430, height, (65, 65, 70)),
        (440, 240, 510, height, (60, 62, 68)),
        (520, 210, 600, height, (58, 60, 66)),
        (610, 260, 640, height, (52, 55, 62)),
    ]
    for x1, y1, x2, y2, color in buildings:
        draw.rectangle([x1, y1, x2, y2], fill=color)
        # Windows
        for wx in range(x1 + 8, x2 - 8, 18):
            for wy in range(y1 + 10, y2 - 10, 22):
                lit = random.random() > 0.4
                wc = (220, 200, 100) if lit else (30, 35, 40)
                draw.rectangle([wx, wy, wx + 8, wy + 12], fill=wc)

    # Moon
    draw.ellipse([560, 30, 600, 70], fill=(240, 240, 200))

    return img


# ── Main ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    os.makedirs("challenge_assets", exist_ok=True)

    print("[*] Generating base image...")
    base = generate_base_image()

    print(f"[*] Encoding flag: {FLAG}")
    stego = lsb_encode(base, FLAG)

    out_path = "challenge_assets/suspicious.png"
    stego.save(out_path, format="PNG")
    print(f"[+] Saved: {out_path}")

    # Verify
    recovered = lsb_decode(stego)
    assert recovered == FLAG, f"Verification failed: got '{recovered}'"
    print(f"[+] Verified: decoded flag = '{recovered}'")

    print()
    print("Next steps:")
    print("  1. Upload 'suspicious.png' to the Forensics challenge via Django admin")
    print("  2. Players can solve with: zsteg suspicious.png")
    print("     or write their own LSB decoder")
    print()
    print("Solver hint (don't share with players):")
    print("  python -c \"")
    print("  from PIL import Image")
    print("  img = Image.open('suspicious.png')")
    print("  bits = ''.join(str(c & 1) for px in img.getdata() for c in px[:3])")
    print("  print(''.join(chr(int(bits[i:i+8],2)) for i in range(0,len(bits),8) if int(bits[i:i+8],2)))")
    print("  \"")
