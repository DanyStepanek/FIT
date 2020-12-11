#include "statistics.hpp"

Stat *TotalTimeStat = new Stat("Total Time");
Stat *LaserTimeStat = new Stat("Laser Time");
Stat *PressBrakeTimeStat = new Stat("PressBrake Time");

double total_start_time = .0;
double total_end_time = .0;
