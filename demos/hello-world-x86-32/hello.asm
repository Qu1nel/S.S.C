global _start

section .text

_start:  ; main() {
    call WRITE_HELLO    ; WRITE_HELLO()
    call SUCCEED_EXIT   ; SUCCEED_EXIT()
;}

; syscall(4, 1, msg, 14) == write(1, "Hello, World!\n\0", 14);
WRITE_HELLO:  ; void WRITE_HELLO() {
    mov eax, 0x04       ; write(
    mov ebx, 0x1        ;   1,
    mov ecx, msg        ;   "Hello, World\n\0",
    mov edx, 14         ;   14,
    int 0x80            ; );
    ; printf("Hello, World!\n");
;}

; syscall(1, 0) == _exit(0);
SUCCEED_EXIT:  ; void EXIT() {
    mov eax, 0x01       ; _exit(
    mov ebx, 0          ;   0  # <return code>
    int 0x80            ; );
    ; return 0

;}

;The .rodata stores only constants (read only memory)
;The order of the sections is irrelevant.
section .rodata
    ; 0xA (10) = '\n' - CR
    ; 0x0 (0) = '\0' - NULL terminator
    msg: db "Hello, World!", 0xA, 0x0   ; char msg[] = 'Hello, World\n\0'

