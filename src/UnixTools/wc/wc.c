#include "wc.h"

#include <ctype.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int32_t parse_options(int32_t key, char *argument, ArgumentParserState *state);
static void check_mode(Arguments **args, const Mode setmode);

static Counting *count_statistics_from(FILE *input, Counting *total);
static void print_statistics(const Counting result, const uint16_t settings, const char *file);


ArgsOption options[] = {
    {.name = NULL, .key = 0, .arg = NULL, .flags = 0, .doc = "Program output control options:", .group = 1},

    {.name = "bytes", .key = 'c', .arg = NULL, .flags = 0, .doc = "Print the byte counts", .group = 0},
    {.name = "words", .key = 'w', .arg = NULL, .flags = 0, .doc = "Print the word counts", .group = 0},
    {.name = "lines", .key = 'l', .arg = NULL, .flags = 0, .doc = "Print the newline counts", .group = 0},

    {.name = "max-line-length",
     .key = 'L',
     .arg = NULL,
     .flags = 0,
     .doc = "Print the maximum display  width",
     .group = 0},

    {.name = NULL, .key = 0, .arg = NULL, .flags = 0, .doc = "Informational Options:", .group = -1},
    {.name = NULL},
};


int main(int argc, char *argv[])
{
    Arguments arguments = {.mode = 0, .files = {.name = NULL, .count = 0}};
    Argp argp = {options, parse_options, args_doc, doc, 0, 0, 0};

    if (argp_parse(&argp, argc, argv, 0, 0, &arguments) == 0) {
        Counting total_result = {.total_newlines = 0, .total_words = 0, .total_bytes = 0, .max_line_length = 0};

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
                    Counting *file_stat = count_statistics_from(from, &total_result);
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
            Counting *stdout_stat = count_statistics_from(stdin, &total_result);
            print_statistics(total_result, arguments.mode, "stdin");
            free(stdout_stat);
        }
    }

    return EXIT_SUCCESS;
}


static Counting *count_statistics_from(FILE *input, Counting *total)
{
    Counting *file_count = (Counting *)malloc(sizeof(Counting));

    file_count->total_bytes = 0;
    file_count->total_words = 0;
    file_count->total_newlines = 0;
    file_count->max_line_length = 0;

    size_t line_width = 0;

    bool in_space = true;

    int ch;
    while ((ch = fgetc(input)) != EOF) {
        file_count->total_bytes++;
        line_width++;
        if (isspace(ch)) {
            in_space = true;
            if (ch == '\n') {
                line_width--;
                if (file_count->max_line_length < line_width) {
                    file_count->max_line_length = line_width;
                }
                line_width = 0;
                file_count->total_newlines++;
            }
        } else {
            file_count->total_words += in_space;
            in_space = false;
        }
    }

    if (total->max_line_length < file_count->max_line_length) {
        total->max_line_length = file_count->max_line_length;
    }

    total->total_bytes += file_count->total_bytes;
    total->total_words += file_count->total_words;
    total->total_newlines += file_count->total_newlines;

    return file_count;
}

static int32_t parse_options(int32_t key, char *argument, ArgumentParserState *state)
{
    Arguments *arguments = (Arguments *)state->input;
    switch (key) {
        case 'l':
            check_mode(&arguments, PRI_NEWLINES);
            break;
        case 'w':
            check_mode(&arguments, PRI_WORDS);
            break;
        case 'c':
            check_mode(&arguments, PRI_BYTES);
            break;
        case 'L':
            check_mode(&arguments, PRI_MAX_LINE_LENGTH);
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

static void check_mode(Arguments **args, const Mode setmode)
{
    if ((*args)->mode == NO_INIT) {
        (*args)->mode = (uint16_t)setmode;
    } else {
        (*args)->mode |= (uint16_t)setmode;
    }
}


static void print_statistics(const Counting result, const uint16_t settings, const char *file)
{
    if (settings & PRI_NEWLINES) {
        fprintf(stdout, "%10zu\t", result.total_newlines);
    }
    if (settings & PRI_WORDS) {
        fprintf(stdout, "%10zu\t", result.total_words);
    }
    if (settings & PRI_BYTES) {
        fprintf(stdout, "%10zu\t", result.total_bytes);
    }
    if (settings & PRI_MAX_LINE_LENGTH) {
        fprintf(stdout, "%10zu\t", result.max_line_length);
    }
    fprintf(stdout, "%s\n", file);
}
