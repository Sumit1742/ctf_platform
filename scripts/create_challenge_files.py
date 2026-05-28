#!/usr/bin/env python3
"""
Generate the OSINT challenge image (suspicious.jpg) with embedded GPS EXIF data.

Run this ONCE to create the challenge file, then upload it via Django admin.

Requirements: pip install Pillow piexif
"""
import struct
import os
from PIL import Image, ImageDraw, ImageFont
import piexif


def deg_to_dms_rational(deg_float):
    """Convert decimal degrees to (degrees, minutes, seconds) as EXIF rationals."""
    deg_float = abs(deg_float)
    d = int(deg_float)
    m_float = (deg_float - d) * 60
    m = int(m_float)
    s = round((m_float - m) * 60 * 10000)
    return [(d, 1), (m, 1), (s, 10000)]


def create_challenge_image(output_path: str, lat: float, lon: float):
    """
    Create a realistic-looking photo with GPS coordinates hidden in EXIF.

    Default coordinates: India Gate, New Delhi (a famous landmark)
    lat=28.6129, lon=77.2295
    """
    # Create a plausible "outdoor photo" — just a coloured rectangle for the challenge
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color=(135, 160, 180))
    draw = ImageDraw.Draw(img)

    # Sky gradient simulation
    for y in range(height // 2):
        c = int(100 + y * 0.3)
        draw.line([(0, y), (width, y)], fill=(c, c + 20, c + 50))

    # Ground
    for y in range(height // 2, height):
        c = int(60 + (y - height // 2) * 0.1)
        draw.line([(0, y), (width, y)], fill=(c + 20, c + 30, c))

    # Simple "monument" silhouette
    draw.rectangle([350, 200, 450, 450], fill=(80, 70, 60))
    draw.polygon([(350, 200), (400, 120), (450, 200)], fill=(80, 70, 60))

    # Add some noise/texture so it looks like a real photo
    import random
    random.seed(42)
    pixels = img.load()
    for _ in range(5000):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        r, g, b = pixels[x, y]
        noise = random.randint(-10, 10)
        pixels[x, y] = (
            max(0, min(255, r + noise)),
            max(0, min(255, g + noise)),
            max(0, min(255, b + noise)),
        )

    # Save without EXIF first
    img.save(output_path, 'JPEG', quality=85)

    # Now inject GPS EXIF
    exif_dict = {
        "0th": {
            piexif.ImageIFD.Make: b"Canon",
            piexif.ImageIFD.Model: b"Canon EOS 5D Mark IV",
            piexif.ImageIFD.Software: b"Adobe Lightroom",
            piexif.ImageIFD.DateTime: b"2024:03:15 14:32:07",
        },
        "Exif": {
            piexif.ExifIFD.DateTimeOriginal: b"2024:03:15 14:32:07",
            piexif.ExifIFD.ExifVersion: b"0230",
        },
        "GPS": {
            piexif.GPSIFD.GPSVersionID: (2, 3, 0, 0),
            piexif.GPSIFD.GPSLatitudeRef:  b'N' if lat >= 0 else b'S',
            piexif.GPSIFD.GPSLatitude:     deg_to_dms_rational(lat),
            piexif.GPSIFD.GPSLongitudeRef: b'E' if lon >= 0 else b'W',
            piexif.GPSIFD.GPSLongitude:    deg_to_dms_rational(lon),
            piexif.GPSIFD.GPSAltitudeRef:  0,
            piexif.GPSIFD.GPSAltitude:     (214, 1),  # 214m above sea level
        },
    }

    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, output_path)

    print(f"[+] Challenge image created: {output_path}")
    print(f"[+] Embedded GPS: {lat}°N, {lon}°E")
    print(f"[+] Players should run: exiftool {output_path}")
    print(f"[+] The flag is: CTF{{gps_exif_metadata_leak}}")


def create_stego_image(output_path: str, secret_message: str):
    """
    Create a PNG with the flag hidden via LSB steganography.
    Players need to write or find a decoder.
    """
    width, height = 640, 480
    img = Image.new('RGB', (width, height))
    pixels = img.load()

    # Create a visually interesting image
    import math
    for y in range(height):
        for x in range(width):
            r = int(128 + 100 * math.sin(x * 0.05))
            g = int(128 + 100 * math.sin(y * 0.05))
            b = int(128 + 100 * math.sin((x + y) * 0.03))
            pixels[x, y] = (r % 256, g % 256, b % 256)

    # LSB encode the secret
    secret_bytes = (secret_message + '\x00').encode('utf-8')
    bits = ''.join(f'{byte:08b}' for byte in secret_bytes)

    pixel_list = list(img.getdata())
    new_pixels = []
    bit_idx = 0

    for pixel in pixel_list:
        r, g, b = pixel
        if bit_idx < len(bits):
            r = (r & ~1) | int(bits[bit_idx]); bit_idx += 1
        if bit_idx < len(bits):
            g = (g & ~1) | int(bits[bit_idx]); bit_idx += 1
        if bit_idx < len(bits):
            b = (b & ~1) | int(bits[bit_idx]); bit_idx += 1
        new_pixels.append((r, g, b))

    result = Image.new('RGB', img.size)
    result.putdata(new_pixels)
    result.save(output_path, 'PNG')

    print(f"[+] Stego image created: {output_path}")
    print(f"[+] Hidden message: {secret_message}")
    print(f"[+] Players can decode with: python decode_lsb.py {output_path}")


if __name__ == '__main__':
    os.makedirs('challenge_files', exist_ok=True)

    # OSINT challenge image — India Gate coordinates
    create_challenge_image('challenge_files/suspicious.jpg', lat=28.6129, lon=77.2295)

    # Forensics stego image
    create_stego_image('challenge_files/suspicious.png', 'CTF{st3g0_1s_not_s3cur1ty}')

    print("\n[+] Upload these files via Django admin:")
    print("    challenge_files/suspicious.jpg -> OSINT challenge")
    print("    challenge_files/suspicious.png -> Forensics challenge")
