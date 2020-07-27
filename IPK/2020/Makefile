CXX=g++
PRJ=ipk-sniffer
#
PROGS=$(PRJ)
CXXFLAGS=	-std=c++11 -pedantic	-Wall

FILES= $(PRJ).cpp

all: $(PROGS)

$(PRJ): $(FILES)
	$(CXX)	$(CXXFLAGS)	-o	$@	$(FILES)	-lpcap

clean:
	rm -f	*.o	*.out	$(PROGS)
