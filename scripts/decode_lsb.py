#!/usr/bin/env python3
"""
LSB Steganography Decoder — Forensics challenge solution script.

This is the SOLUTION (for CTF organisers / writeup reference).

Usage: python decode_lsb.py suspicious.png
"""
import sys
from PIL import Image


def lsb_decode(image_path: str) -> str:
    img = Image.open(image_path).convert('RGB')
    pixels = list(img.getdata())

    bits = ''
    for pixel in pixels:
        for channel in pixel:
            bits += str(channel & 1)

    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        if len(byte) < 8:
            break
        char = chr(int(byte, 2))
        if char == '\x00':
            break
        chars.append(char)

    return ''.join(chars)


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'suspicious.png'
    result = lsb_decode(path)
    print(f'[+] Hidden message: {result}')
