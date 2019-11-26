section .data
    msg db 'Hello, assembler...', 0xa, 0xd
    len equ $ - msg

section .text
    global _start

_start:
;.global _start
    ; вывод строки на экран
    ; mov dst, src

    mov eax, 4  ; номер системного вызова sys_write
    mov ebx, 1  ; фойловый дескриптор stdout
    mov ecx, msg ; строка
    mov edx, len ; длина строки
    syscall  ; прерывание для вызова (аналогично можно int 0x80)

    ; теперь выходим из программы
    mov eax, 1  ; системный вызов sys_exit
    mov ebx, 0 ; это будет статус нашего выхода

    int 0x80
