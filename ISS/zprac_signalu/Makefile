PRJ=filtr
(CC)= gcc
CFLAGS= -Wall -std=c99 -pedantic -lm

all: $(PRJ)

$(PRJ): $(PRJ).c
	$(CC) $(CFLAGS) -o $@ $(PRJ).c

clean:
	rm -f *.o $(PRJ)
