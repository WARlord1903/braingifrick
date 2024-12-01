from cffi import FFI
import platform
import os

lib = None

ffibuilder = FFI()

ffibuilder.cdef('void interpret_code(const char*, bool);')
ffibuilder.cdef('void init_bf(void);')
ffibuilder.cdef('void end_bf(void);')
ffibuilder.cdef('void set_frame_size(size_t s);')
ffibuilder.cdef('void init_display(void);')

if platform.system() == 'Windows':
    if not os.path.exists('brainfrick.dll'):
        print(os.system('gcc -shared -o .\\brainfrick.dll .\\brainfrick.c -lncursesw'))
    lib = ffibuilder.dlopen('brainfrick.dll')
else:
    ffibuilder.set_source("_brainfrick",
        """
            #include "brainfrick.h"
        """,
        sources=['brainfrick.c'], libraries=['ncurses'])

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)