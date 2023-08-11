const char *argp_program_version = "Version: 1.0";
const char *argp_program_bug_address = "<covach.qn@gmail.com>";
char args_doc[] = "[FILE]...";
char doc[] =
    ""
    "wc - program for counting lines, bytes and words in a file.\n\n"

    "Prints the number of newline characters, words, and bytes for each FILE and the and a summary line if multiple "
    "FILES have been specified. A word is defined as a sequence of printed characters of non-zero length separated by "
    "a space character.\n\n"

    "If FILE is not specified or is specified as -, reads standard input.\n\n"

    "This is essentially a complete (but slightly reduced in functionality) of the original wc program."
    "The following parameters are used to select the counters to be output (counters are always output in this order: "
    "newline characters, words, characters, bytes, maximum string length):\n"

    "\v\nThis program was written for fun for training purposes.";
