#include "brainfrick.h"

struct bf_t bf = {NULL, 0};
char* outbuf = NULL;

void ptr_left(void){
    if(bf.pos > 0)
        --bf.pos;
    else
        bf.pos = BF_BUFFER_SIZE - 1;
}

void ptr_right(void){
    if(bf.pos < BF_BUFFER_SIZE - 1)
        ++bf.pos;
    else
        bf.pos = 0;

}

size_t parse_loop(const char* code, size_t start){
    size_t remaining_closing_brackets = 0;
    size_t i;
    for(i = start; i < strlen(code); i++){
        if(code[i] == '[')
            remaining_closing_brackets++;
        else if(code[i] == ']')
            remaining_closing_brackets--;
        if(remaining_closing_brackets == 0)
            break;
    }
    if(remaining_closing_brackets > 0)
        exit(EXIT_FAILURE);
    char* loop_contents = (char*) malloc(i - start + 1);
    strncpy(loop_contents, &code[start + 1], i - start);
    loop_contents[i - start] = '\0';

    while(bf.buf[bf.pos])
        interpret_code(loop_contents);
    
    free(loop_contents);
    return i;
}

void interpret_code(const char* code){
    for(size_t i = 0; i < strlen(code); i++){
        switch(code[i]){
            case '<':
                ptr_left();
                break;
            case '>':
                ptr_right();
                break;
            case '+':
                bf.buf[bf.pos]++;
                break;
            case '-':
                bf.buf[bf.pos]--;
                break;
            case '.':
                fprintf(stdout, "%c", bf.buf[bf.pos]);
                break;
            case ',':
                bf.buf[bf.pos] = (uint8_t) fgetc(stdin);
                break;
            case '[':
                size_t end_pos = parse_loop(code, i);
                i = end_pos;
                break;
        }
    }
}

void init_bf(){
    if(bf.buf)
        free(bf.buf);
    bf.buf = (uint8_t*) calloc(BF_BUFFER_SIZE, sizeof(uint8_t));
    bf.pos = 0;
}

void end_bf(){
    free(bf.buf);
    fclose(stdout);
    free(outbuf);
}

void set_outbuf(size_t s){
    if(outbuf)
        free(outbuf);
    outbuf = malloc(s);
    setvbuf(stdout, outbuf, _IOFBF, s);
}