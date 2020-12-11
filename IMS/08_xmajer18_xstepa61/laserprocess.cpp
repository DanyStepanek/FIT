#include "laserprocess.hpp"

LaserProcess::LaserProcess(unsigned employee_count, unsigned pressbrake_count){
  this->pressbrake_count = pressbrake_count;
  this->employee_count = employee_count;
}

void LaserProcess::Behavior() {
    
    Seize(Laser);
    Enter(EmployeeStore, 1);

    this->start_time = Time;

    while(!(SheetStore.Empty())){
      Leave(SheetStore, 1);
      Wait(Normal(22, 0.5));
      Enter(CutoutPieceStore, 32);
    }
    Leave(CutoutPieceStore, 200);
    Enter(PressBrakeStore, 200);

    Leave(EmployeeStore, 1);
    Release(Laser);

    (new ClearWorkstationProcess())->Activate();

    for(unsigned i = 0; i < this->pressbrake_count; i++){
      if(EmployeeStore.Free() != 0){
        Enter(EmployeeStore, 1);
        Enter(PressBrake, 1);
        (new PressBrakeProcess())->Activate();
      }
    }

    this->end_time = Time;
    double laser_duration = this->end_time - this->start_time;
    (*LaserTimeStat)(laser_duration);

}
