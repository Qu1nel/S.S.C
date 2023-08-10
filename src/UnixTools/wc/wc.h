#ifndef WC_H

#include <argp.h>
#include <argz.h>
#include <inttypes.h>

typedef struct argp_option ArgsOption;
typedef struct argp Argp;
typedef struct argp_state ArgumentParserState;

typedef struct arguments {
    bool bytes;
    bool lines;
    bool maxLineLength;
    bool words;
} Arguments;

extern const char *argp_program_version;
extern const char *argp_program_bug_address;
extern char args_doc[];
extern char doc[];

#endif  // !WC_H
