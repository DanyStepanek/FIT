/********************************************************************
 *	IMS project: Téma č. 8: Diskrétní model výrobního procesu (SHO) *
 *	@author Daniel Stepanek (xstepa61)                              *
 *	@author Tomas Majerech (xmajer18)                               *
 *	Date: 07.12.2020                                                *
 *	VUT FIT Brno                                                    *
 *                                                                 *
 *******************************************************************/

#ifndef CLEARWORKSTATIONPROCESS_H
#define CLEARWORKSTATIONPROCESS_H

#include <simlib.h>
#include <iostream>
#include "entities.hpp"
#include "statistics.hpp"

class ClearWorkstationProcess: public Process {
private:
  double start_time;
  double end_time;
public:
  void Behavior();
};


#endif
