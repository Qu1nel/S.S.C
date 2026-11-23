global _start

section .text

_start:
    call WRITE_HELLO
    call EXIT

WRITE_HELLO:
    mov eax, 0x04
    mov ebx, 0x1
    mov ecx, msg
    mov edx, 14
    int 0x80

EXIT:
    mov eax, 0x01
    mov ebx, 0
    int 0x80

section .rodata
    msg: db "Hello, World!", 0xA, 0x0
