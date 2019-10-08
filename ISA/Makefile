CXX=g++
PRJ=isa-tazatel
#
PROGS=$(PRJ)
CXXFLAGS= -pedantic -Wall

FILES= isa-tazatel.cpp

all: $(PROGS)

$(PRJ): $(FILES)
	$(CXX)	$(CXXFLAGS)	-o	$@	$(FILES)	-lpcap

clean:
	rm -f	*.o	*.out	$(PROGS)
