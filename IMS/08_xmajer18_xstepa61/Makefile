CXX=g++
PRJ=ims_project
OUT_DIR=./results
ZIP_NAME=08_xmajer18_xstepa61
#
PROGS=$(PRJ)
CXXFLAGS=	-std=c++17 -pedantic	-Wall	-g	-O2

FILES= main.cpp	statistics.cpp	clearworkstationprocess.cpp	entities.cpp	laserprocess.cpp	manufactoringprocess.cpp	pressbrakeprocess.cpp	storage.cpp

all:	$(PROGS)
	make dir

.PHONY: run
run:
	./$(PRJ) -f $(OUT_DIR)/simulation_00.out
	./$(PRJ) -e 2 -p 2 -f $(OUT_DIR)/simulation_01.out
	./$(PRJ) -e 3 -p 3 -f $(OUT_DIR)/simulation_02.out
	./$(PRJ) -e 1 -p 2 -f $(OUT_DIR)/simulation_03.out
	./$(PRJ) -e 2 -p 3 -f $(OUT_DIR)/simulation_04.out
	./$(PRJ) -e 2 -p 1 -f $(OUT_DIR)/simulation_05.out
	./$(PRJ) -e 3 -p 2 -f $(OUT_DIR)/simulation_06.out


.PHONY: dir
dir:
	mkdir -p $(OUT_DIR)

$(PRJ): $(FILES)
	$(CXX)	$(CXXFLAGS)	-o	$@	$(FILES)	-lsimlib	-lm

zip:
	make clean
	find . -name "*" -print | zip $(ZIP_NAME) -@


clean:
	rm	-f	*.o	*.out	$(PROGS)
	rm	-rf	$(OUT_DIR)
