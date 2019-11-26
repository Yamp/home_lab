global _start
_start:
    mov ebx, 123
    mov eax, ebx  ; это будет статус нашего выхода

    add ebx, ecx  ; это будет статус нашего выхода
    sub ebx, ecx  ; это будет статус нашего выхода

    mul ebx  ; always to eax
    div edx

    mov eax, 1
    mov ebx, 42  ; это будет статус нашего выхода

    int 0x80  ; это значит выполнит интеррапт 0x80 который значит syscall, который находится в eax. 1 это значит выйти.
