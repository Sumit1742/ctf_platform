all:
	gcc -o vuln vuln.c -fno-stack-protector -z execstack -no-pie -m32 -w 2>/dev/null || \
	gcc -o vuln vuln.c -fno-stack-protector -no-pie -w

clean:
	rm -f vuln
