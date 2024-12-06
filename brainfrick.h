#ifndef BRAINFRICK_H
#define BRAINFRICK_H

#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <stdio.h>
#include <math.h>
#include <sys/timeb.h>
#ifndef _WIN32
    #include <ncurses.h>
    #include <time.h>
    #include <unistd.h>
#else
    #include <windows.h>
#endif

#define BF_BUFFER_SIZE 30000

struct bf_t {
    uint8_t* buf;
    size_t pos;
};

void interpret_code(const char*, bool, double);
void init_bf(void);
void end_bf(void);
void set_frame_size(size_t);
void init_display(void);

#endif