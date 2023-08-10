#ifndef WC_H
#define WC_H

#include <argp.h>
#include <argz.h>
#include <inttypes.h>

typedef struct argp_option ArgsOption;
typedef struct argp Argp;
typedef struct argp_state ArgumentParserState;

typedef struct position_arguments {
    char *name;
    size_t count;
} PosArgs;

typedef struct arguments {
    uint16_t mode;
    PosArgs files;
} Arguments;

typedef enum MODE {
    PRI_MAX_LINE_LENGTH = 010,
    PRI_NEWLINES = 04,
    PRI_WORDS = 02,
    PRI_BYTES = 01,
    PRI_ALL = 017,
    PRI_LWB = 07
} Mode;

extern const char *argp_program_version;
extern const char *argp_program_bug_address;
extern char args_doc[];
extern char doc[];

#endif  // !WC_H
