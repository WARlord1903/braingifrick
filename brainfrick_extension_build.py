from cffi import FFI
import platform

if platform.system() == 'Windows':
    with open('setup.cfg', 'w') as f:
        f.write('[build]\ncompiler=mingw32\n[build_ext]\ncompiler=mingw32')
        f.close()
        
ffibuilder = FFI()

ffibuilder.cdef('void interpret_code(const char*, bool, double);')
ffibuilder.cdef('void init_bf(void);')
ffibuilder.cdef('void end_bf(void);')
ffibuilder.cdef('void set_frame_size(size_t s);')
ffibuilder.cdef('void init_display(void);')

ffibuilder.set_source("_brainfrick",
    """
        #include "brainfrick.h"
    """,
        sources=['brainfrick.c'], extra_compile_args=['-O2'], libraries=['ncursesw'] if platform.system() != 'Windows' else ['winmm'])


if __name__ == "__main__":
    ffibuilder.compile(verbose=True)