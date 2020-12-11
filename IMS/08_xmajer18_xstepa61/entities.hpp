/********************************************************************
 *	IMS project: Téma č. 8: Diskrétní model výrobního procesu (SHO) *
 *	@author Daniel Stepanek (xstepa61)                              *
 *	@author Tomas Majerech (xmajer18)                               *
 *	Date: 07.12.2020                                                *
 *	VUT FIT Brno                                                    *
 *                                                                 *
 *******************************************************************/

#ifndef ENTITITES_H
#define ENTITITES_H

#include <simlib.h>
#include <iostream>


#define DEFAULT_EMPLOYEE_CAPACITY 4
#define DEFAULT_PRESSBRAKE_CAPACITY 3


extern Facility Forklift;

extern Facility Laser;

/**
* Store with press brakes (capacity 2)
*/
extern Store PressBrake;

/**
* Store with sheets (capacity 7)
*/
extern Store SheetStore;

/**
* Store with laser cutouts (capacity 300)
*/
extern Store CutoutPieceStore;

/**
* Store with pieces to bend on press brake (capacity 200)
*/
extern Store PressBrakeStore;

/**
* Store with bent pieces from a press brake (capacity 200)
*/
extern Store PressBrakeOutStore;

/**
* Store of all employees in the system (capacity 3)
*/
extern Store EmployeeStore;



#endif
