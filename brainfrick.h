#ifndef BRAINFRICK_H
#define BRAINFRICK_H

#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <stdio.h>

#define BF_BUFFER_SIZE 30000

struct bf_t {
    uint8_t* buf;
    size_t pos;
};

void interpret_code(const char*, bool, bool);

#endif