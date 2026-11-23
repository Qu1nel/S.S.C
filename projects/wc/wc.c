#include "wc.h"

#include <ctype.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>


extern Counting_t *count_statistics_from(FILE *restrict input, Counting_t *restrict total);
extern void print_statistics(const Counting_t result, const uint16_t settings, const char *restrict file);


static int32_t parse_options(int32_t key, char *restrict argument, ArgumentParserState_t *restrict state);

static int count_data_from_files(Arguments_t *args);
static int _count_files(const Arguments_t *restrict args, Counting_t *restrict total_result);
static int _count_stdin(const Arguments_t *restrict args, Counting_t *restrict total_result);

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
        int status = count_data_from_files(&arguments);
        if (status != 0) {
            return EXIT_FAILURE;
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


static int count_data_from_files(Arguments_t *args)
{
    Counting_t total_result = {.total_newlines = 0, .total_words = 0, .total_bytes = 0, .max_line_length = 0};

    if (args->mode == 0) {
        args->mode = PRI_LWB;
    }

    int (*__count)(const Arguments_t *restrict, Counting_t *restrict);
    __count = (args->files.name != NULL) ? &_count_files : &_count_stdin;

    int status = __count(args, &total_result);

    free(args->files.name);

    return status;
}


static int _count_files(const Arguments_t *restrict args, Counting_t *restrict total_result)
{
    const char *prev = NULL;
    char *file_name;

    size_t count_files = 0;

    while ((file_name = argz_next(args->files.name, args->files.count, prev))) {
        FILE *from = NULL;

        if ((from = fopen(file_name, "r")) == NULL) {
            perror(file_name);
        } else {
            count_files++;

            Counting_t *file_stat;
            if ((file_stat = count_statistics_from(from, total_result)) == NULL) {
                perror("memory error");
                return 1;
            }

            print_statistics(*file_stat, args->mode, file_name);
            free(file_stat);
            fclose(from);
        }

        prev = file_name;
    }

    if (count_files > 0) {
        print_statistics(*total_result, args->mode, "total");
    }


    return 0;
}


static int _count_stdin(const Arguments_t *restrict args, Counting_t *restrict total_result)
{
    Counting_t *stdout_stat = NULL;
    if ((stdout_stat = count_statistics_from(stdin, total_result)) == NULL) {
        perror("memory error");
        return 1;
    }

    print_statistics(*total_result, args->mode, "stdin");
    free(stdout_stat);
    return 0;
}
