 /********************************************************************
  *	IMS project: Téma č. 8: Diskrétní model výrobního procesu (SHO) *
  *	@author Daniel Stepanek (xstepa61)                              *
 	*	@author Tomas Majerech (xmajer18)                               *
  *	Date: 07.12.2020                                                *
  *	VUT FIT Brno                                                    *
  *                                                                 *
  *******************************************************************/


#include <iostream>
#include <getopt.h>
#include <cstdlib>
#include <simlib.h>

#include "manufactoringprocess.hpp"
#include "statistics.hpp"

#define DEFAULT_ITERATION_COUNT 1
#define DEFAULT_SHEET_COUNT 7
#define DEFAULT_EMPLOYEE_COUNT 1
#define DEFAULT_PRESSBRAKE_COUNT 1
#define DEFAULT_TIME 16 * 60 // two shifts (8h each)


using namespace std;

void printHelp(){

	cerr << "Possible arguments:" << endl
		   << "\t-p or --pbrake to specify the press brake count." << endl
       << "\t-e or --employee to specify the employee count." << endl
       << "\t-t or --time to specify the end time." << endl
			 << "\t-i or --iter to specify number of simulations with the same values" << endl
			 << "\t-f or --file for output" << endl;

  cerr << "Possible values:" << endl
       << "\tPress Brake: [1, 2]" << endl
       << "\tEmployees: [1, 2, 3]" << endl
       << "\tTime: < 0 ; INF >" << endl
			 << "\tIter: <0 ; INF>" << endl;
}

int main(int argc, char* argv[]){

	unsigned iterations = DEFAULT_ITERATION_COUNT;
  unsigned sheet_count = DEFAULT_SHEET_COUNT;
  unsigned employee_count = DEFAULT_EMPLOYEE_COUNT;
  unsigned pressbrake_count = DEFAULT_PRESSBRAKE_COUNT;
  unsigned end_time = DEFAULT_TIME;

  int opt;
	char *err;
	static const char *shortOptions = "p:e:t:i:f:h";
	static const struct option longOptions[] = {
    {"help", no_argument, nullptr, 'h'},
		{"pbrake", no_argument, nullptr, 'p'},
    {"employee", no_argument, nullptr, 'e'},
    {"time", no_argument, nullptr, 't'},
		{"iter", no_argument, nullptr, 'i'},
		{"file", no_argument, nullptr, 'f'},
		{nullptr, 0, nullptr, 0},
	};

	while ((opt = getopt_long(argc, argv, shortOptions, longOptions, nullptr)) != -1)
	{
		switch (opt)
		{
			case 0:
				break;
			case 'f':
				SetOutput(optarg);
				break;

			case 'i':
				iterations = strtoul(optarg, &err, 10);

				if (*err != '\0')
				{
					cerr << "Press brake count must be a positive number.\n";
					return EXIT_FAILURE;
				}

				break;


			case 'p':
        pressbrake_count = strtoul(optarg, &err, 10);

        if (pressbrake_count > DEFAULT_PRESSBRAKE_CAPACITY || pressbrake_count == 0){
          cerr << "Press brake count must be in range <1 ; "
               << DEFAULT_PRESSBRAKE_CAPACITY << ">" << endl;
          return EXIT_FAILURE;
        }

        if (*err != '\0')
				{
					cerr << "Press brake count must be a positive number.\n";
					return EXIT_FAILURE;
				}

				break;

      case 'e':
        employee_count = strtoul(optarg, &err, 10);

        if (employee_count > DEFAULT_EMPLOYEE_CAPACITY || employee_count == 0){
          cerr << "Employee count must be in range <1 ; "
               << DEFAULT_EMPLOYEE_CAPACITY << ">" << endl;
          return EXIT_FAILURE;
        }

        if (*err != '\0')
				{
					cerr << "Employee count must be a positive integer.\n";
					return EXIT_FAILURE;
				}

        break;

      case 't':
        end_time = strtoul(optarg, &err, 10);

        if (*err != '\0')
				{
					cerr << "Time must be a positive integer.\n";
					return EXIT_FAILURE;
				}

        break;
      case 'h':
        printHelp();
        return EXIT_SUCCESS;

			case '?':
			default:
				printHelp();
				return EXIT_FAILURE;
		}
	}

	if (optind < argc)
	{
		printHelp();
		return EXIT_FAILURE;
	}


	for(unsigned i=0; i < iterations; i++){
		Init(0, end_time);

	  (new ManufacturingProcess(employee_count, pressbrake_count, sheet_count))->Activate();
	  Run();

		if (total_end_time == 0.0){
			total_end_time = end_time;
		}

		double total_time = total_end_time - total_start_time;
		(*TotalTimeStat)(total_time);

		CutoutPieceStore.Output();
		PressBrakeOutStore.Output();
	}

	(*LaserTimeStat).Output();
	(*PressBrakeTimeStat).Output();
	(*TotalTimeStat).Output();




  return EXIT_SUCCESS;
}
