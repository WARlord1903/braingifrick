#include "brainfrick.h"

struct bf_t bf = {NULL, 0};
char* frame = NULL;
size_t frame_size;

#ifdef _WIN32
HANDLE* hconsole;

void cls(void){
    CONSOLE_SCREEN_BUFFER_INFO csbi;
    CHAR_INFO fill;

    GetConsoleScreenBufferInfo(hconsole, &csbi);

    SMALL_RECT scrollRect = {0, 0, csbi.dwSize.X, csbi.dwSize.Y};
    COORD scrollTarget = {0, (SHORT)(0 - csbi.dwSize.Y)};

    fill.Char.UnicodeChar = TEXT(' ');
    fill.Attributes = csbi.wAttributes;

    ScrollConsoleScreenBuffer(hconsole, &scrollRect, NULL, scrollTarget, &fill);

    csbi.dwCursorPosition.X = 0;
    csbi.dwCursorPosition.Y = 0;

    SetConsoleCursorPosition(hconsole, csbi.dwCursorPosition);
}
#endif

size_t parse_loop(const char* code, size_t start, bool buffering, double framerate){
    size_t remaining_closing_brackets = 0;
    size_t i;
    for(i = start; code[i]; i++){
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

void interpret_code(const char* code, bool buffering, double framerate){
    static size_t char_count = 0;
    #ifndef _WIN32
        const double frame_time = 1. / framerate * 1000000000;
    #else
        const double frame_time = 1. / framerate * 1000;
    #endif
    static size_t curr_frame;
    #ifdef _WIN32
        static DWORD epoch = 0;
        if(epoch == 0)
            epoch = timeGetTime();
    #else
        static struct timespec epoch = {0};
        if(epoch.tv_sec == 0)
            clock_gettime(CLOCK_MONOTONIC_RAW, &epoch);
    #endif

    for(size_t i = 0; code[i]; i++){
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
                        frame[frame_size] = '\0';
                        #ifndef _WIN32
                            mvprintw(0, 0, "%s", frame);
                            refresh();
                            struct timespec end;
                            clock_gettime(CLOCK_MONOTONIC_RAW, &end);
                            while(epoch.tv_sec * 1000000000 + epoch.tv_nsec + frame_time * curr_frame > end.tv_sec * 1000000000 + end.tv_nsec)
                                clock_gettime(CLOCK_MONOTONIC_RAW, &end);
                        #else
                            timeBeginPeriod(1);
                            const COORD start_pos = {0, 0};
                            SetConsoleCursorPosition(hconsole, start_pos);
                            fputs(frame, stdout);
                            while(timeGetTime() < epoch + (DWORD) (frame_time * curr_frame));
                            timeEndPeriod(1);
                        #endif

                        char_count = 0;
                        curr_frame++;
                    }
                }
                else
                    fputc((char) bf.buf[bf.pos], stdout);
                break;
            case ',':
                bf.buf[bf.pos] = (uint8_t) fgetc(stdin);
                break;
            case '[':
                i = parse_loop(code, i, buffering, framerate);
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
    free(bf.buf);
    if(frame)
        free(frame);
    #ifndef _WIN32
        fflush(stdout);
        endwin();
    #else
        // cls();
    #endif
}

void set_frame_size(size_t s){
    if(frame)
        free(frame);
    frame = malloc(s + 1);
    frame_size = s;
}

void init_display(void){
    #ifndef _WIN32
        initscr();
    #else
        hconsole = GetStdHandle(STD_OUTPUT_HANDLE);
        cls();
    #endif
}