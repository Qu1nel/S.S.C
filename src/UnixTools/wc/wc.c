#include "wc.h"


const char *argp_program_version = "Version: 0.1";
const char *argp_program_bug_address = "<covach.qn@gmail.com>";

static char doc[] =
    "wc - program for counting lines, bytes and words in a file.\n\n"
    "This is essentially a complete (but slightly reduced in functionality) of the original wc program."
    "\v\nThis program was written for fun for training purposes.";


static int32_t parse_options(int32_t key, char *argument, ArgumentParserState *state);


static ArgsOption options[] = {
    {"bytes", 'c', 0, 0, "print the byte counts", 0},
    {"lines", 'l', 0, 0, "print the newline counts", 0},
    {"max-line-length", 'L', 0, 0, "print the maximum display  width", 0},
    {"words", 'w', 0, 0, "print the word counts", 0},
    {0},
};

static Argp argp = {options, parse_options, 0, doc, 0, 0, 0};


int main(int argc, char *argv[])
{
    return argp_parse(&argp, argc, argv, 0, 0, 0);
}


static int32_t parse_options(int32_t key, char *argument, ArgumentParserState *state)
{
    switch (key) {
        case 'c':
            break;
        case 'l':
            break;
        case 'L':
            break;
        case 'w':
            break;
    }
    return 0;
}
