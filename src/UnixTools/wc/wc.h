#ifndef WC_H
#define WC_H

#include <argp.h>
#include <argz.h>
#include <inttypes.h>

typedef struct argp_option ArgsOption_t;
typedef struct argp Argp_t;
typedef struct argp_state ArgumentParserState_t;

typedef struct Arguments {
    uint16_t mode;

    struct {
        char *name;
        size_t count;
    } files;
} Arguments_t;

typedef enum MODE {
    PRI_MAX_LINE_LENGTH = 010,
    PRI_NEWLINES = 04,
    PRI_WORDS = 02,
    PRI_BYTES = 01,
    PRI_ALL = 017,
    PRI_LWB = 07,
    NO_INIT = 0
} Mode_t;

typedef struct Counting {
    size_t total_newlines;
    size_t total_words;
    size_t total_bytes;
    size_t max_line_length;
} Counting_t;

extern const char *argp_program_version;
extern const char *argp_program_bug_address;
extern char args_doc[];
extern char doc[];

#endif  // !WC_H
