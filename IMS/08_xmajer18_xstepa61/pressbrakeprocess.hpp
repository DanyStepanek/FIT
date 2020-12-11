/********************************************************************
 *	IMS project: Téma č. 8: Diskrétní model výrobního procesu (SHO) *
 *	@author Daniel Stepanek (xstepa61)                              *
 *	@author Tomas Majerech (xmajer18)                               *
 *	Date: 07.12.2020                                                *
 *	VUT FIT Brno                                                    *
 *                                                                 *
 *******************************************************************/

#ifndef PRESSBRAKEPROCESS_H
#define PRESSBRAKEPROCESS_H

#include <simlib.h>
#include <iostream>

#include "storage.hpp"
#include "entities.hpp"
#include "statistics.hpp"

#define TOOL_MUST_BE_CHANGED_4 4

class PressBrakeProcess: public Process {
private:
  double start_time;
  double end_time;

  /**
  * Each piece must be bent with 5 different tools.
  * Tool is changed four times in process.
  */
  unsigned tool_changed;
public:
  /**  Creates PressBrakeProcess
  * init tool_changed to 0
  */
  PressBrakeProcess();
  void Behavior();
};

#endif
