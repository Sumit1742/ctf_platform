FROM ubuntu:22.04
RUN dpkg --add-architecture i386 && \
    apt-get update && \
    apt-get install -y gcc gcc-multilib make socat libc6-dev-i386 && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /challenge
COPY vuln.c Makefile ./
RUN make
ENV FLAG="CTF{buff3r_0v3rfl0w_pwn3d}"
EXPOSE 4444
CMD ["socat", "TCP-LISTEN:4444,reuseaddr,fork,crnl", "EXEC:./vuln,pty,stderr"]
