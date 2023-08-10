TARGET 		:= wc

EXTERN_LIBS :=

CC 			:= clang
CFLAGS 		:= -std=c17 -Wall -Wextra -Werror -Wshadow -Wvla -Walloca -Wundef -Wfloat-equal \
			   -Wstrict-prototypes -Wconversion -Wswitch-enum -Wswitch-default -Wimplicit-fallthrough \
			   -Wunreachable-code -Wformat=2 -Wparentheses -Wmisleading-indentation -Wpedantic -pedantic -O2

CPPFLAGS 	:= -I .
LDFLAGS 	:= $(addprefix -l,$(EXTERN_LIBS))

OBJECTS     := $(patsubst %.c, %.o, $(shell find . -type f -name '*.c' 2>/dev/null))

RM 			:= rm -rf
MAKEFLAGS 	+= --no-print-directory


.PHONY: all
all: build

$(TARGET): $(OBJECTS)
	$(CC) $(OBJECTS) $(LDFLAGS) -o $@

.c.o:
	$(CC) -c $< -o $@ $(CFLAGS) $(CPPFLAGS)

.PHONY: build
build: $(TARGET)  ## Compile project

.PHONY: re
re:  ## Recompile project
	$(MAKE) fclean
	$(MAKE) all

.PHONY: clean
clean:  ## Remove all object files
	$(RM) $(OBJECTS)

.PHONY: fclean
fclean: clean  ## Remove all executable files + object files
	$(RM) $(TARGET)

.DEFAULT_GOAL := help
.PHONY: help
help:  ## Show this output, i.e. help to use the commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

info-%:
	@make --dry-run --always-make $* | grep -v "info"

print-%:
	@$(info '$*'='$($*)')

