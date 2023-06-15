CC := nasm
CFLAGS := -f elf32
LDFLAGS := -m elf_i386

TARGET := hello

BLD_DIR := build32
EXECUTABLE = $(BLD_DIR)/$(TARGET)

SRCS := $(shell find . -type f -name '*.asm' 2>/dev/null)
OBJS = $(SRCS:.asm=.o)

default: makedirs all

.PHONY: all
all: $(EXECUTABLE)

$(EXECUTABLE): $(OBJS)
	ld $(LDFLAGS) $^ -o $@

$(OBJS): $(SRCS)
	$(CC) $(CFLAGS) $< -o $@

.PHONY: makedirs
makedirs: 
	@mkdir -p $(BLD_DIR)

.PHONY: build
build: makedirs $(EXECUTABLE)

.PHONY: run
run: $(EXECUTABLE)
	./$(EXECUTABLE)

.PHONY: clean
clean:
	rm -rf $(EXECUTABLE) $(OBJS)

