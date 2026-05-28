"""
scripts/create_osint_challenge.py

Run this once to generate the OSINT challenge image with
embedded GPS coordinates. Upload the resulting file to the
challenge via Django admin.

Usage:
    pip install Pillow piexif
    python scripts/create_osint_challenge.py
"""

from PIL import Image, ImageDraw, ImageFont
import piexif
import os


# ── GPS coordinates to embed (India Gate, New Delhi) ──────────────────
LAT  = 28.6129   # degrees North
LON  = 77.2295   # degrees East
# The flag is revealed when players decode these coordinates
# and see CTF{gps_exif_metadata_leak} is stored in the UserComment field


def to_dms_rational(deg):
    """Convert decimal degrees to (degrees, minutes, seconds) as EXIF rationals."""
    d = int(deg)
    m_float = (deg - d) * 60
    m = int(m_float)
    s = round((m_float - m) * 60 * 10000)
    return [(d, 1), (m, 1), (s, 10000)]


def build_image(path="suspicious.jpg"):
    """Create a plausible-looking photo."""
    width, height = 800, 600
    img = Image.new("RGB", (width, height), color=(50, 55, 60))
    draw = ImageDraw.Draw(img)

    # Sky gradient simulation
    for y in range(300):
        r = int(80 + y * 0.3)
        g = int(120 + y * 0.2)
        b = int(180 - y * 0.1)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Ground
    for y in range(300, height):
        shade = int(60 + (y - 300) * 0.1)
        draw.line([(0, y), (width, y)], fill=(shade, shade + 5, shade))

    # Simple monument silhouette
    draw.rectangle([375, 160, 425, 300], fill=(40, 40, 40))
    draw.polygon([(340, 160), (460, 160), (400, 80)], fill=(50, 50, 50))

    # Watermark-like text
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None
    draw.text((10, height - 25), "IMG_20241103_142857.jpg", fill=(180, 180, 180), font=font)

    img.save(path, quality=88)
    return path


def embed_exif(image_path, output_path):
    """Embed GPS + flag in EXIF UserComment."""
    img = Image.open(image_path)

    gps_ifd = {
        piexif.GPSIFD.GPSVersionID:     (2, 3, 0, 0),
        piexif.GPSIFD.GPSLatitudeRef:   b"N",
        piexif.GPSIFD.GPSLatitude:      to_dms_rational(abs(LAT)),
        piexif.GPSIFD.GPSLongitudeRef:  b"E",
        piexif.GPSIFD.GPSLongitude:     to_dms_rational(abs(LON)),
        piexif.GPSIFD.GPSAltitudeRef:   0,
        piexif.GPSIFD.GPSAltitude:      (216, 1),
    }

    # Store flag in UserComment field (players who read all EXIF fields will find it)
    flag_bytes = b"ASCII\x00\x00\x00CTF{gps_exif_metadata_leak}"

    exif_dict = {
        "0th": {
            piexif.ImageIFD.Make:             b"CTFCamera",
            piexif.ImageIFD.Model:            b"HackArena v1",
            piexif.ImageIFD.DateTime:         b"2024:11:03 14:28:57",
            piexif.ImageIFD.Software:         b"HackArena CTF",
        },
        "Exif": {
            piexif.ExifIFD.DateTimeOriginal:  b"2024:11:03 14:28:57",
            piexif.ExifIFD.UserComment:       flag_bytes,
        },
        "GPS": gps_ifd,
    }

    exif_bytes = piexif.dump(exif_dict)
    img.save(output_path, exif=exif_bytes, quality=88)
    print(f"[+] Challenge image saved: {output_path}")
    print(f"    Embedded GPS: {LAT}°N, {LON}°E")
    print(f"    Embedded flag in UserComment: CTF{{gps_exif_metadata_leak}}")
    print()
    print("Next steps:")
    print("  1. Upload 'suspicious.jpg' to the OSINT challenge via Django admin")
    print("  2. Players run: exiftool suspicious.jpg")
    print("  3. They find GPS coords AND the flag in UserComment")


if __name__ == "__main__":
    os.makedirs("challenge_assets", exist_ok=True)
    raw = build_image("challenge_assets/raw_photo.jpg")
    embed_exif(raw, "challenge_assets/suspicious.jpg")
