#include <stdbool.h>
#include <stdlib.h>

#include "wc.h"


const char *argp_program_version = "Version: 1.0";
const char *argp_program_bug_address = "<covach.qn@gmail.com>";
char args_doc[] = "[FILE]...";
char doc[] =
    "wc - program for counting lines, bytes and words in a file.\n\n"

    "Prints the number of newline characters, words, and bytes for each FILE and the and a summary line if multiple "
    "FILES have been specified. A word is defined as a sequence of printed characters of non-zero length separated by "
    "a space character.\n\n"

    "If FILE is not specified or is specified as -, reads standard input.\n\n"

    "This is essentially a complete (but slightly reduced in functionality) of the original wc program."
    "The following parameters are used to select the counters to be output (counters are always output in this order: "
    "newline characters, words, characters, bytes, maximum string length):\n"

    "\v\nThis program was written for fun for training purposes.";


extern Counting_t *count_statistics_from(FILE *restrict input, Counting_t *restrict total)
{
    Counting_t *file_count = (Counting_t *)malloc(sizeof(Counting_t));

    if (file_count == NULL) return NULL;

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


extern void print_statistics(const Counting_t result, const uint16_t settings, const char *restrict file)
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
