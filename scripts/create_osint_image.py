#!/usr/bin/env python3
"""
create_osint_image.py
Creates the OSINT challenge image with embedded GPS EXIF metadata.

Usage:
    pip install Pillow piexif
    python scripts/create_osint_image.py

Output: media/challenge_files/suspicious.jpg
        (Upload this via Django admin to the OSINT challenge)
"""

import os
import struct
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
    import piexif
except ImportError:
    print("Install deps: pip install Pillow piexif")
    raise


# === CONFIGURE THIS ===
# GPS coords to embed (players will extract these and identify the location)
# Default: India Gate, New Delhi (28.6129°N, 77.2295°E)
GPS_LAT  = 28.6129
GPS_LON  = 77.2295
GPS_DESC = "India Gate, New Delhi"
# ======================

OUT_DIR = Path(__file__).parent.parent / "media" / "challenge_files"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUT_DIR / "suspicious.jpg"


def to_dms_rational(decimal_deg):
    """Convert decimal degrees to (degrees, minutes, seconds) as EXIF rationals."""
    d = int(abs(decimal_deg))
    m_float = (abs(decimal_deg) - d) * 60
    m = int(m_float)
    s = round((m_float - m) * 60 * 10000)
    return [(d, 1), (m, 1), (s, 10000)]


def create_image():
    """Create a realistic-looking photo with hidden GPS metadata."""
    # Create a 640x480 "photo" — looks like a city street photo
    img = Image.new("RGB", (640, 480), color=(100, 120, 140))
    draw = ImageDraw.Draw(img)

    # Sky gradient (simple)
    for y in range(200):
        shade = int(100 + (y / 200) * 60)
        draw.line([(0, y), (640, y)], fill=(shade - 20, shade, shade + 40))

    # Ground
    draw.rectangle([0, 200, 640, 480], fill=(80, 80, 75))

    # Buildings silhouette
    buildings = [(50, 80), (120, 60), (200, 100), (300, 50), (400, 90), (500, 70), (580, 110)]
    for bx, bh in buildings:
        draw.rectangle([bx, 200 - bh, bx + 60, 200], fill=(40, 45, 55))
        # Windows
        for wx in range(bx + 8, bx + 55, 14):
            for wy in range(200 - bh + 10, 200, 18):
                draw.rectangle([wx, wy, wx + 8, wy + 10],
                                fill=(255, 240, 180) if (wx + wy) % 3 != 0 else (40, 45, 55))

    # Road
    draw.rectangle([0, 360, 640, 420], fill=(50, 50, 50))
    for x in range(0, 640, 60):
        draw.rectangle([x, 387, x + 35, 393], fill=(220, 220, 180))

    # Add subtle text (part of the story)
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None

    draw.text((20, 450), "IMG_20241103_144522.jpg", fill=(200, 200, 200), font=font)
    draw.text((460, 450), "f/2.8  1/200s  ISO400", fill=(180, 180, 180), font=font)

    # Save without EXIF first
    img.save(str(OUT_PATH), "JPEG", quality=88)
    print(f"  Base image created: {OUT_PATH}")
    return img


def embed_gps(out_path, lat, lon):
    """Embed GPS coordinates into EXIF."""
    img = Image.open(str(out_path))

    gps_ifd = {
        piexif.GPSIFD.GPSVersionID:     (2, 3, 0, 0),
        piexif.GPSIFD.GPSLatitudeRef:   b'N' if lat >= 0 else b'S',
        piexif.GPSIFD.GPSLatitude:      to_dms_rational(lat),
        piexif.GPSIFD.GPSLongitudeRef:  b'E' if lon >= 0 else b'W',
        piexif.GPSIFD.GPSLongitude:     to_dms_rational(lon),
        piexif.GPSIFD.GPSAltitude:      (216, 1),  # 216 metres
        piexif.GPSIFD.GPSAltitudeRef:   0,
    }

    zeroth_ifd = {
        piexif.ImageIFD.Make:           b"FujiFilm",
        piexif.ImageIFD.Model:          b"X-T5",
        piexif.ImageIFD.Software:       b"Adobe Lightroom 7.0",
        piexif.ImageIFD.DateTime:       b"2024:11:03 14:45:22",
        piexif.ImageIFD.Artist:         b"anonymous_researcher",
        piexif.ImageIFD.ImageDescription: b"Last photo before going dark.",
    }

    exif_dict = {
        "0th": zeroth_ifd,
        "GPS": gps_ifd,
    }

    exif_bytes = piexif.dump(exif_dict)
    img.save(str(out_path), "JPEG", quality=88, exif=exif_bytes)
    print(f"  GPS metadata embedded: {lat}°N, {lon}°E  ({GPS_DESC})")


def main():
    print("Creating OSINT challenge image...")
    create_image()
    embed_gps(OUT_PATH, GPS_LAT, GPS_LON)
    print(f"\n✓ Done! File saved to: {OUT_PATH}")
    print(f"  Location hidden: {GPS_DESC}")
    print()
    print("Next steps:")
    print("  1. Run the Django dev server: python manage.py runserver")
    print("  2. Go to /admin/challenges/challengefile/add/")
    print("  3. Upload this file and attach it to the 'Find the Whistleblower' challenge")
    print()
    print("Players solve it with:")
    print("  $ exiftool suspicious.jpg | grep -i gps")


if __name__ == "__main__":
    main()
