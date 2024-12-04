#include "brainfrick.h"

struct bf_t bf = {NULL, 0};
char* frame = NULL;
size_t frame_size;

size_t parse_loop(const char* code, size_t start, bool buffering, size_t framerate){
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
        interpret_code(loop_contents, buffering, framerate);
    
    free(loop_contents);
    return i;
}

void interpret_code(const char* code, bool buffering, size_t framerate){
    static size_t char_count = 0;
    static struct timeb start = {0};
    struct timeb end;
    if(start.time == 0)
        ftime(&start);

    for(size_t i = 0; i < strlen(code); i++){
        switch(code[i]){
            case '<':
                if(bf.pos > 0)
                    --bf.pos;
                else
                    bf.pos = BF_BUFFER_SIZE - 1;
                break;
            case '>':
                if(bf.pos < BF_BUFFER_SIZE - 1)
                    ++bf.pos;
                else
                    bf.pos = 0;
                break;
            case '+':
                bf.buf[bf.pos]++;
                break;
            case '-':
                bf.buf[bf.pos]--;
                break;
            case '.':
                if(buffering){
                    frame[char_count++] = (char) bf.buf[bf.pos];
                    if(char_count == frame_size){
                        mvprintw(0, 0, "%s", frame);
                        ftime(&end);
                        while((int) 1000. * (end.time - start.time) + (end.millitm - start.millitm) < 1000. * (1. / framerate))
                            ftime(&end);
                        refresh();
                        char_count = 0;
                        ftime(&start);
                    }
                }
                else
                    fputc((char) bf.buf[bf.pos], stdout);
                break;
            case ',':
                bf.buf[bf.pos] = (uint8_t) fgetc(stdin);
                break;
            case '[':
                size_t end_pos = parse_loop(code, i, buffering, framerate);
                i = end_pos;
                break;
        }
    }
}

void init_bf(void){
    if(bf.buf)
        free(bf.buf);
    bf.buf = (uint8_t*) calloc(BF_BUFFER_SIZE, sizeof(uint8_t));
    bf.pos = 0;
}

void end_bf(void){
    if(bf.buf)
        free(bf.buf);
    if(frame)
        free(frame);
    fflush(stdout);
    endwin();
}

void set_frame_size(size_t s){
    if(frame)
        free(frame);
    frame = malloc(s + 1);
    frame_size = s;
}

void init_display(void){
    initscr();
}