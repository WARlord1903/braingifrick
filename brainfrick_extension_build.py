from cffi import FFI

ffibuilder = FFI()

ffibuilder.cdef('void interpret_code(const char*);')
ffibuilder.cdef('void init_bf();')
ffibuilder.cdef('void end_bf();')
ffibuilder.cdef('void set_outbuf(size_t);')

ffibuilder.set_source("_brainfrick",
    """
        #include "brainfrick.h"
    """,
    sources=['brainfrick.c'])

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)