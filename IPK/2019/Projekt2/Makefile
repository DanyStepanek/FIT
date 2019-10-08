CXX=g++
PRJ=ipk-scan
#
PROGS=$(PRJ)
CXXFLAGS= -pedantic

FILES= ipk-scan.cpp

all: $(PROGS)

$(PRJ): $(FILES)
	$(CXX)	$(CXXFLAGS)	-o	$@	$(FILES)	-lpcap

clean:
	rm -f	*.o	*.out	$(PROGS)
