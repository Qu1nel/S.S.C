#include "wc.h"

#include <ctype.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>


extern Counting_t *count_statistics_from(FILE *restrict input, Counting_t *restrict total);
extern void print_statistics(const Counting_t result, const uint16_t settings, const char *restrict file);

static int32_t parse_options(int32_t key, char *restrict argument, ArgumentParserState_t *restrict state);


// clang-format off
static ArgsOption_t options[] = {
    {.name = NULL, .key = 0, .arg = NULL, .flags = 0, .doc = "Program output control options:", .group = 1},

    {.name = "bytes", .key = 'c', .arg = NULL, .flags = 0, .doc = "Print the byte counts", .group = 0},
    {.name = "words", .key = 'w', .arg = NULL, .flags = 0, .doc = "Print the word counts", .group = 0},
    {.name = "lines", .key = 'l', .arg = NULL, .flags = 0, .doc = "Print the newline counts", .group = 0},
    {.name = "max-line-length", .key = 'L', .arg = NULL, .flags = 0, .doc = "Print the maximum display  width", .group = 0},

    {.name = NULL, .key = 0, .arg = NULL, .flags = 0, .doc = "Informational Options:", .group = -1},
    {.name = NULL},
};
// clang-format on


int main(int argc, char *argv[])
{
    Arguments_t arguments = {.mode = 0, .files = {.name = NULL, .count = 0}};
    Argp_t argp = {options, parse_options, args_doc, doc, 0, 0, 0};

    if (argp_parse(&argp, argc, argv, 0, 0, &arguments) == 0) {
        Counting_t total_result = {.total_newlines = 0, .total_words = 0, .total_bytes = 0, .max_line_length = 0};

        if (arguments.mode == 0) {
            arguments.mode = PRI_LWB;
        }

        if (arguments.files.name != NULL) {
            const char *prev = NULL;
            char *file_name;

            size_t count_files = 0;

            while ((file_name = argz_next(arguments.files.name, arguments.files.count, prev))) {
                FILE *from = NULL;

                if ((from = fopen(file_name, "r")) == NULL) {
                    perror(file_name);
                } else {
                    count_files++;

                    Counting_t *file_stat;
                    if ((file_stat = count_statistics_from(from, &total_result)) == NULL) {
                        perror("memory error");
                        return EXIT_FAILURE;
                    }

                    print_statistics(*file_stat, arguments.mode, file_name);
                    free(file_stat);
                    fclose(from);
                }

                prev = file_name;
            }

            if (count_files > 0) {
                print_statistics(total_result, arguments.mode, "total");
            }

            free(arguments.files.name);
        } else {
            Counting_t *stdout_stat = NULL;
            if ((stdout_stat = count_statistics_from(stdin, &total_result)) == NULL) {
                perror("memory error");
                return EXIT_FAILURE;
            }

            print_statistics(total_result, arguments.mode, "stdin");
            free(stdout_stat);
        }
    }

    return EXIT_SUCCESS;
}


static int32_t parse_options(int32_t key, char *restrict argument, ArgumentParserState_t *restrict state)
{
    Arguments_t *arguments = (Arguments_t *)state->input;
    switch (key) {
        case 'l':
            arguments->mode |= PRI_NEWLINES;
            break;
        case 'w':
            arguments->mode |= PRI_WORDS;
            break;
        case 'c':
            arguments->mode |= PRI_BYTES;
            break;
        case 'L':
            arguments->mode |= PRI_MAX_LINE_LENGTH;
            break;
        case ARGP_KEY_INIT:
            arguments->files.name = NULL;
            arguments->files.count = 0;
            break;
        case ARGP_KEY_ARG:
            argz_add(&arguments->files.name, &arguments->files.count, argument);
            break;
        default:
            return ARGP_ERR_UNKNOWN;
    }
    return 0;
}
