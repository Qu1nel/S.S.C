#include <argp.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    return argp_parse(0, argc, argv, 0, 0, 0);
}
