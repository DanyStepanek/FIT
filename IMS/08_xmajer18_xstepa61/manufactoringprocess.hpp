/********************************************************************
 *	IMS project: Téma č. 8: Diskrétní model výrobního procesu (SHO) *
 *	@author Daniel Stepanek (xstepa61)                              *
 *	@author Tomas Majerech (xmajer18)                               *
 *	Date: 07.12.2020                                                *
 *	VUT FIT Brno                                                    *
 *                                                                 *
 *******************************************************************/

#ifndef MANUFACTORINGPROCESS_H
#define MANUFACTORINGPROCESS_H


#include <simlib.h>
#include <iostream>

#include "laserprocess.hpp"
#include "entities.hpp"
#include "statistics.hpp"

class ManufacturingProcess: public Process{
private:
  double start_time;
  double end_time;

  unsigned employee_count;
  unsigned pressbrake_count;
  unsigned sheet_count;

public:
  /**  Creates ManufacturingProcess
  *  First process of simulation
  *  @param employee_count Count uf employees in system
  *  @param pressbrake_count Count of PressBrake in system (max 2)
  *  @param sheet_count Count of sheets (Default 7)
  */
  ManufacturingProcess(unsigned employee_count, unsigned pressbrake_count, unsigned sheet_count);

  void Behavior();
};


#endif
