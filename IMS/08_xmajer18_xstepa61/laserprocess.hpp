/********************************************************************
 *	IMS project: Téma č. 8: Diskrétní model výrobního procesu (SHO) *
 *	@author Daniel Stepanek (xstepa61)                              *
 *	@author Tomas Majerech (xmajer18)                               *
 *	Date: 07.12.2020                                                *
 *	VUT FIT Brno                                                    *
 *                                                                 *
 *******************************************************************/

#ifndef LASERPROCESS_H
#define LASERPROCESS_H

#include <simlib.h>
#include <iostream>

#include "pressbrakeprocess.hpp"
#include "clearworkstationprocess.hpp"
#include "entities.hpp"
#include "statistics.hpp"

class LaserProcess: public Process {
private:

  double start_time;
  double end_time;

  unsigned employee_count;
  unsigned pressbrake_count;

public:
  /**  Creates LaserProcess
  *
  *  @param employee_count Count uf employees in system
  *  @param pressbrake_count Count of press brakes in system (max 2)
  */
  LaserProcess(unsigned employee_count, unsigned pressbrake_count);

  void Behavior();
};

#endif
