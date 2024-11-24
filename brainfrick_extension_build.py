from cffi import FFI

ffibuilder = FFI()

ffibuilder.cdef('void interpret_code(const char*, bool, bool);')

ffibuilder.set_source("_brainfrick",
    """
        #include "brainfrick.h"
    """,
    sources=['brainfrick.c'])

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)