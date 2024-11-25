from cffi import FFI

ffibuilder = FFI()

ffibuilder.cdef('void interpret_code(const char*, bool);')
ffibuilder.cdef('void init_bf(void);')
ffibuilder.cdef('void end_bf(void);')
ffibuilder.cdef('void set_frame_size(size_t s);')
ffibuilder.cdef('void init_display(void);')

ffibuilder.set_source("_brainfrick",
    """
        #include "brainfrick.h"
    """,
    sources=['brainfrick.c'], libraries=['ncurses'])

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)