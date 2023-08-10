#include "wc.h"

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int32_t parse_options(int32_t key, char *argument, ArgumentParserState *state);
static void init_arguments(Arguments *args);

ArgsOption options[] = {
    {0, 0, 0, 0, "Program output control options:", 1},
    {"bytes", 'c', 0, 0, "Print the byte counts", 0},
    {"lines", 'l', 0, 0, "Print the newline counts", 0},
    {"max-line-length", 'L', 0, 0, "Print the maximum display  width", 0},
    {"words", 'w', 0, 0, "Print the word counts", 0},
    {0, 0, 0, 0, "Informational Options:", -1},
    {0},
};


static Argp argp = {options, parse_options, args_doc, doc, 0, 0, 0};


int main(int argc, char *argv[])
{
    Arguments arguments;
    init_arguments(&arguments);

    return argp_parse(&argp, argc, argv, 0, 0, &arguments);
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

static void init_arguments(Arguments *arguments)
{
    arguments->bytes = true;
    arguments->lines = true;
    arguments->words = true;
    arguments->maxLineLength = false;
}
