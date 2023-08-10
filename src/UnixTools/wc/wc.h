#ifndef WC_H

#include <argp.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct argp_option ArgsOption;
typedef struct argp Argp;
typedef struct argp_state ArgumentParserState;

typedef struct arguments {
    bool bytes;
    bool lines;
    bool maxLineLength;
    bool words;
} Arguments;

#endif  // !WC_H
