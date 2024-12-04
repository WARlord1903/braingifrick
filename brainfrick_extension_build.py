from cffi import FFI
import platform

ffibuilder = FFI()

ffibuilder.cdef('void interpret_code(const char*, bool, size_t);')
ffibuilder.cdef('void init_bf(void);')
ffibuilder.cdef('void end_bf(void);')
ffibuilder.cdef('void set_frame_size(size_t s);')
ffibuilder.cdef('void init_display(void);')

ffibuilder.set_source("_brainfrick",
    """
        #include "brainfrick.h"
    """,
        sources=['brainfrick.c'], include_dirs=[] if platform.system() != 'Windows' else ['C:\\msys64\\mingw64\\include'], library_dirs=[] if platform.system() != 'Windows' else ['C:\\msys64\\mingw64\\lib'], libraries=['ncursesw'])


if __name__ == "__main__":
    ffibuilder.compile(verbose=True, target='_brainfrick.pyd')