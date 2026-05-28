#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

/* ============================================================
   Stack Smash 101 — CTF Challenge
   Intentionally vulnerable binary for educational purposes.
   Compile: gcc -o vuln vuln.c -fno-stack-protector -z execstack -no-pie -m32 -w
   ============================================================ */

void win() {
    char *flag = getenv("FLAG");
    printf("\n[+] You smashed the stack!\n");
    if (flag) {
        printf("[+] Flag: %s\n", flag);
    } else {
        printf("[+] Flag: CTF{buff3r_0v3rfl0w_pwn3d}\n");
    }
    fflush(stdout);
    exit(0);
}

void banner() {
    printf("================================\n");
    printf("  Welcome to the Name Server!  \n");
    printf("================================\n");
    printf("[*] win()  is at: %p\n", (void*)win);
    printf("[*] Enter your name: ");
    fflush(stdout);
}

void vulnerable() {
    char buffer[64];
    /* INTENTIONALLY VULNERABLE: gets() has no bounds checking */
    gets(buffer);
    printf("[*] Hello, %s!\n", buffer);
    fflush(stdout);
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin,  NULL, _IONBF, 0);
    banner();
    vulnerable();
    printf("[*] Goodbye!\n");
    return 0;
}
