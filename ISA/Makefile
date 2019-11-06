CXX=g++
PRJ=isa-tazatel
#
PROGS=$(PRJ)
CXXFLAGS= -std=c++11 -pedantic -Wall

FILES= isa-tazatel.cpp

all: $(PROGS)

$(PRJ): $(FILES)
	$(CXX)	$(CXXFLAGS)	-o	$@	$(FILES)	-lpcap	-lresolv

clean:
	rm -f	*.o	*.out	$(PROGS)
