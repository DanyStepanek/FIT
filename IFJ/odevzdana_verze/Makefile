PRJ=ifj18
#
PROGS=$(PRJ)
FILES=main.c scanner.c rstring.c tlist.c token.c err_code.c  parser.c symtable.c generator.c dynamic_string.c  tokenstack.c gen_stack.c
CC=gcc
CFLAGS=-Wall -W -Wextra -g -std=c99 -pedantic

all: $(PROGS)

$(PRJ): $(FILES)
	$(CC) $(CFLAGS) -o $@ $(FILES) -lm

clean:
	rm -f  *.o *.out  $(PROGS)
