/********************************************************************
 *	IMS project: Téma č. 8: Diskrétní model výrobního procesu (SHO) *
 *	@author Daniel Stepanek (xstepa61)                              *
 *	@author Tomas Majerech (xmajer18)                               *
 *	Date: 07.12.2020                                                *
 *	VUT FIT Brno                                                    *
 *                                                                 *
 *******************************************************************/

#ifndef STAT_H
#define STAT_H

#include <simlib.h>
#include <iostream>

/**
* Total time of simulation.
*/
extern Stat *TotalTimeStat;

/**
* Time spend by cutting.
*/
extern Stat *LaserTimeStat;

/**
* Time spend by bending.
*/
extern Stat *PressBrakeTimeStat;

/**
* Begin and end of simulation.
*/
extern double total_start_time;
extern double total_end_time;

#endif
